import logging
import base64
import json

from github import Github
from monolithe.specifications import Specification, RepositoryManager
from monolithe.specifications.repositorymanager import MODE_NORMAL, MODE_RAW_SPECS, MODE_RAW_ABSTRACTS
from garuda.core.models import GAError, GAPluginManifest, GARequest

class SDSpecificationImporter():
    """

    """
    def __init__(self, storage_controller, push_controller, sdk):
        """
        """
        self._sdk                = sdk
        self._storage_controller = storage_controller
        self._push_controller    = push_controller

    def import_repository_info(self, repository, manager, session_username):
        """
        """
        repository.push_permission = manager.get_repository_push_permission()
        self._storage_controller.update(user_identifier=session_username, resource=repository)

    def import_apiinfo(self, repository, manager, session_username):
        """
        """
        apiinfo = self._sdk.SDAPIInfo()

        try:
            apiinfo.from_dict(manager.get_api_info(branch=repository.branch))
        except:
            apiinfo.version = '1.0'
            apiinfo.prefix = 'api'

        self._storage_controller.create(user_identifier=session_username, resource=apiinfo, parent=repository)

    def import_monolitheconfig(self, repository, manager, session_username):
        """
        """
        monolithe_config = self._sdk.SDMonolitheConfig()

        try:
            parser = manager.get_monolithe_config(branch=repository.branch)

            monolithe_config.product_name         = parser.get('monolithe', 'product_name')
            monolithe_config.product_accronym     = parser.get('monolithe', 'product_accronym')
            monolithe_config.copyright            = parser.get('monolithe', 'copyright')

            monolithe_config.sdk_output           = parser.get('sdk', 'sdk_output')
            monolithe_config.sdkuser_vanilla      = parser.get('sdk', 'sdk_user_vanilla')
            monolithe_config.sdk_name             = parser.get('sdk', 'sdk_name')
            monolithe_config.sdk_class_prefix     = parser.get('sdk', 'sdk_class_prefix')
            monolithe_config.sdk_bambou_version   = parser.get('sdk', 'sdk_bambou_version')
            monolithe_config.sdk_version          = parser.get('sdk', 'sdk_version')
            monolithe_config.sdk_revision_number  = parser.get('sdk', 'sdk_revision_number')
            monolithe_config.sdkurl               = parser.get('sdk', 'sdk_url')
            monolithe_config.sdk_author           = parser.get('sdk', 'sdk_author')
            monolithe_config.sdk_email            = parser.get('sdk', 'sdk_email')
            monolithe_config.sdk_description      = parser.get('sdk', 'sdk_description')
            monolithe_config.sdk_license_name     = parser.get('sdk', 'sdk_license_name')
            monolithe_config.sdkcli_name          = parser.get('sdk', 'sdk_cli_name')

            monolithe_config.api_doc_output       = parser.get('apidoc', 'apidoc_output')
            monolithe_config.api_doc_user_vanilla = parser.get('apidoc', 'apidoc_user_vanilla')

            monolithe_config.sdk_doc_output       = parser.get('sdkdoc', 'sdkdoc_output')
            monolithe_config.sdk_doc_user_vanilla = parser.get('sdkdoc', 'sdkdoc_user_vanilla')
            monolithe_config.sdk_doc_tmp_path     = parser.get('sdkdoc', 'sdkdoc_tmp_path')

        except:
            monolithe_config.sdk_output = './codegen'
            monolithe_config.sdk_class_prefix = 'GA'
            monolithe_config.sdk_bambou_version = '2.0.0'
            monolithe_config.sdk_version = '1.0'
            monolithe_config.sdk_revision_number = '1'
            monolithe_config.api_doc_output = './apidocgen'
            monolithe_config.sdk_doc_output = './sdkdocgen'

        self._storage_controller.create(user_identifier=session_username, resource=monolithe_config, parent=repository)

    def import_specifications(self, repository, manager, session_username):
        """
        """
        self._import_specs(repository=repository, manager=manager, mode=MODE_RAW_SPECS, session_username=session_username)

    def import_abstracts(self, repository, manager, session_username):
        """
        """
        self._import_specs(repository=repository, manager=manager, mode=MODE_RAW_ABSTRACTS, session_username=session_username)


    ## PRIVATE

    def clean_repository(self, repository, session_username):
        """
        """
        response = self._storage_controller.get_all(user_identifier=session_username, resource_name=self._sdk.SDSpecification.rest_name, parent=repository)
        if response.count:
            self._storage_controller.delete_multiple(user_identifier=session_username, resources=response.data)

        response = self._storage_controller.get_all(user_identifier=session_username, resource_name=self._sdk.SDAbstract.rest_name, parent=repository)

        if response.count:
            self._storage_controller.delete_multiple(user_identifier=session_username, resources=response.data)

        response = self._storage_controller.get_all(user_identifier=session_username, resource_name=self._sdk.SDAPIInfo.rest_name, parent=repository)

        if response.count:
            self._storage_controller.delete_multiple(user_identifier=session_username, resources=response.data)

        response = self._storage_controller.get_all(user_identifier=session_username, resource_name=self._sdk.SDMonolitheConfig.rest_name, parent=repository)

        if response.count:
            self._storage_controller.delete_multiple(user_identifier=session_username, resources=response.data)

    def _import_specs(self, repository, manager, mode, session_username):
        """
        """
        mono_specifications = manager.get_all_specifications(branch=repository.branch, mode=mode)

        specs_info = {}

        for rest_name, mono_specification in mono_specifications.iteritems():

            specification = self._sdk.SDSpecification() if mode == MODE_RAW_SPECS else self._sdk.SDAbstract()

            specification.name                 = mono_specification.filename
            specification.description          = mono_specification.description
            specification.package              = mono_specification.package
            specification.allows_create        = mono_specification.allows_create
            specification.allows_get           = mono_specification.allows_get
            specification.allows_update        = mono_specification.allows_update
            specification.allows_delete        = mono_specification.allows_delete

            if specification.rest_name == self._sdk.SDSpecification.rest_name:
                specification.object_rest_name     = mono_specification.rest_name
                specification.object_resource_name = mono_specification.resource_name
                specification.entity_name          = mono_specification.entity_name
                specification.root                 = mono_specification.is_root

            self._storage_controller.create(user_identifier=session_username, resource=specification, parent=repository)

            extensions = self._import_extends(repository=repository, mono_specification=mono_specification, specification=specification, session_username=session_username)
            attributes = self._import_attributes(mono_specification=mono_specification, specification=specification, session_username=session_username)

            specs_info[mono_specification.rest_name] = {'mono_specification': mono_specification , 'specification': specification}

        self._import_apis(specification_info=specs_info, mode=mode, session_username=session_username)

    def _import_apis(self, specification_info, mode, session_username):
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
                api.allows_bulk_create        = mono_api.allows_bulk_create
                api.allows_bulk_update        = mono_api.allows_bulk_update
                api.allows_bulk_delete        = mono_api.allows_bulk_delete

                if mode == MODE_RAW_SPECS:
                    remote_specification = specification_info[mono_api.remote_specification_name]['specification']
                    api.associated_specification_id = remote_specification.id

                    if api.relationship == 'root':
                        api.path = '/%s' % remote_specification.object_resource_name
                    else:
                        api.path = '/%s/id/%s' % (specification.object_resource_name, remote_specification.object_resource_name)

                self._storage_controller.create(user_identifier=session_username, resource=api, parent=specification)

    def _import_extends(self, repository, mono_specification, specification, session_username):
        """
        """
        extensions = []

        for extension_name in mono_specification.extends:

            response = self._storage_controller.get_all(user_identifier=session_username, parent=repository, resource_name=self._sdk.SDAbstract.rest_name, filter='name == "%s.spec"' % extension_name)

            if response.count:
                extensions = extensions + response.data

        if len(extensions):
            self._storage_controller.assign(user_identifier=session_username, resource_name=self._sdk.SDAbstract.rest_name, resources=extensions, parent=specification)

        return sorted(extensions)

    def _import_attributes(self, mono_specification, specification, session_username):
        """
        """
        ret = []
        specification.issues = []

        for mono_attribute in mono_specification.attributes:

            attr = self._sdk.SDAttribute()

            attr.name            = mono_attribute.rest_name
            attr.allowed_chars   = mono_attribute.allowed_chars
            attr.allowed_choices = sorted(mono_attribute.allowed_choices) if mono_attribute.allowed_choices else None
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
            attr.subtype         = mono_attribute.subtype
            attr.unique          = mono_attribute.unique
            attr.unique_scope    = mono_attribute.unique_scope
            attr.issues          = []

            if not attr.validate():

                specification.issues.append('Some attributes were not declared correctly. Please review attributes')
                self._storage_controller.update(user_identifier=session_username, resource=specification)

                for property_name, error in attr.errors.iteritems():
                    attr.issues.append('Some error has been found in attribute %s declaration: Type has been reverted to "string". please review' % attr.name)
                    attr.type = 'string'

            self._storage_controller.create(user_identifier=session_username, resource=attr, parent=specification)

            ret.append(attr)

        return ret
