import logging
import base64
import json

from github import Github
from monolithe.specifications import Specification, RepositoryManager
from monolithe.specifications.repositorymanager import MODE_NORMAL, MODE_RAW_SPECS, MODE_RAW_ABSTRACTS
from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent

class SDSpecificationImporter():
    """

    """
    def __init__(self, storage_controller, push_controller, sdk):
        """
        """
        self._sdk                = sdk
        self._storage_controller = storage_controller
        self._push_controller    = push_controller

    def import_apiinfo(self, repository, manager):
        """
        """
        apiinfo = self._sdk.SDAPIInfo(data=manager.get_api_info(branch=repository.branch))
        self._storage_controller.create(apiinfo, repository)

    def import_specifications(self, repository, manager):
        """
        """
        self._import_specs(repository=repository, manager=manager, mode=MODE_RAW_SPECS)

    def import_abstracts(self, repository, manager):
        """
        """
        self._import_specs(repository=repository, manager=manager, mode=MODE_RAW_ABSTRACTS)


    ## PRIVATE

    def clean_repository(self, repository):
        """
        """
        specifications, count = self._storage_controller.get_all(resource_name=self._sdk.SDSpecification.rest_name, parent=repository)
        if count:
            self._storage_controller.delete_multiple(resources=specifications, cascade=True)
            events = []
            for specification in specifications:
                events.append(GAPushEvent(action=GARequest.ACTION_DELETE, entity=specification))
            self._push_controller.push_events(events=events)

        abstracts, count = self._storage_controller.get_all(resource_name=self._sdk.SDAbstract.rest_name, parent=repository)
        if count:
            self._storage_controller.delete_multiple(resources=abstracts, cascade=True)
            events = []
            for  abstract in abstracts:
                events.append(GAPushEvent(action=GARequest.ACTION_DELETE, entity=abstract))
            self._push_controller.push_events(events=events)

        apiinfos, count = self._storage_controller.get_all(resource_name=self._sdk.SDAPIInfo.rest_name, parent=repository)
        if count: self._storage_controller.delete_multiple(resources=apiinfos, cascade=True)

    def _import_specs(self, repository, manager, mode):
        """
        """
        mono_specifications = manager.get_all_specifications(branch=repository.branch, mode=mode)

        specs_info = {}

        for rest_name, mono_specification in mono_specifications.iteritems():

            specification = self._sdk.SDSpecification() if mode == MODE_RAW_SPECS else self._sdk.SDAbstract()

            specification.name                 = mono_specification.filename
            specification.description          = mono_specification.description
            specification.package              = mono_specification.package
            specification.object_rest_name     = mono_specification.rest_name
            specification.object_resource_name = mono_specification.resource_name
            specification.entity_name          = mono_specification.entity_name
            specification.root                 = mono_specification.is_root
            specification.allows_create        = mono_specification.allows_create
            specification.allows_get           = mono_specification.allows_get
            specification.allows_update        = mono_specification.allows_update
            specification.allows_delete        = mono_specification.allows_delete

            self._storage_controller.create(specification, repository)

            event = GAPushEvent(action=GARequest.ACTION_CREATE, entity=specification)
            self._push_controller.push_events(events=[event])

            extensions = self._import_extends(repository=repository, mono_specification=mono_specification, specification=specification)
            attributes = self._import_attributes(mono_specification=mono_specification, specification=specification)

            specs_info[mono_specification.rest_name] = {'mono_specification': mono_specification , 'specification': specification}

        self._import_apis(specification_info=specs_info, mode=mode)

    def _import_apis(self, specification_info, mode):
        """
        """
        for rest_name, spec_info in specification_info.iteritems():

            mono_specification = spec_info['mono_specification']
            specification      = spec_info['specification']

            for mono_api in mono_specification.child_apis:

                api = self._sdk.SDChildAPI()

                api.remote_specification_name = mono_api.remote_specification_name
                api.deprecated                = mono_api.deprecated
                api.relationship              = mono_api.relationship
                api.allows_create             = mono_api.allows_create
                api.allows_get                = mono_api.allows_get
                api.allows_update             = mono_api.allows_update
                api.allows_delete             = mono_api.allows_delete

                if mode == MODE_RAW_SPECS:
                    remote_specification = specification_info[mono_api.remote_specification_name]['specification']
                    api.associated_specification_id = remote_specification.id

                self._storage_controller.create(api, specification)

    def _import_extends(self, repository, mono_specification, specification):
        """
        """
        extensions = []

        for extension_name in mono_specification.extends:

            objects, count = self._storage_controller.get_all(parent=repository, resource_name=self._sdk.SDAbstract.rest_name, filter='name == %s.spec' % extension_name)

            if count:
                extensions = extensions + objects

        if len(extensions):
            self._storage_controller.assign(self._sdk.SDAbstract.rest_name, extensions, specification)

        return extensions

    def _import_attributes(self, mono_specification, specification):
        """
        """
        ret = []
        specification.issues = []

        for mono_attribute in mono_specification.attributes:

            attr = self._sdk.SDAttribute()

            attr.name            = mono_attribute.rest_name
            attr.allowed_chars   = mono_attribute.allowed_chars
            attr.allowed_choices = mono_attribute.allowed_choices
            attr.autogenerated   = mono_attribute.autogenerated
            attr.channel         = mono_attribute.channel
            attr.creation_only   = mono_attribute.creation_only
            attr.default_order   = mono_attribute.default_order
            attr.deprecated      = mono_attribute.deprecated
            attr.description     = mono_attribute.description
            attr.exposed         = mono_attribute.exposed
            attr.filterable      = mono_attribute.filterable
            attr.format          = mono_attribute.format
            attr.max_length      = mono_attribute.max_length
            attr.max_value       = mono_attribute.max_value
            attr.min_length      = mono_attribute.min_length
            attr.min_value       = mono_attribute.min_value
            attr.orderable       = mono_attribute.orderable
            attr.read_only       = mono_attribute.read_only
            attr.required        = mono_attribute.required
            attr.transient       = mono_attribute.transient
            attr.type            = mono_attribute.type
            attr.unique          = mono_attribute.unique
            attr.unique_scope    = mono_attribute.unique_scope
            attr.issues          = []

            if not attr.validate():

                specification.issues.append('Some attributes were not declared correctly. Please review attributes')
                self._storage_controller.update(specification)

                print attr.errors

                for property_name, error in attr.errors.iteritems():
                    attr.issues.append('Some error has been found in attribute %s declaration: Type has been reverted to "string". please review' % attr.name)
                    attr.type = 'string'

            self._storage_controller.create(attr, specification)

            ret.append(attr)

        return ret
