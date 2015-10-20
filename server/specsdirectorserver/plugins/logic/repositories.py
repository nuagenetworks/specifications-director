import logging
import base64
import json

from github import Github
from monolithe.specifications import Specification, RepositoryManager
from monolithe.specifications.repositorymanager import MODE_NORMAL, MODE_RAW_SPECS, MODE_RAW_ABSTRACTS

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary


logger = logging.getLogger('specsdirector.plugins.logic.repository')

class SDRepositoryLogicPlugin(GALogicPlugin):
    """

    """

    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='repositories logic',
                                version=1.0,
                                identifier="specsdirector.plugins.logic.repositories",
                                subscriptions={
                                    "repository": [GARequest.ACTION_CREATE]
                                })

    def did_perform_write(self, context):
        """
        """
        logger.debug("populating")

        sdk = SDKLibrary().get_sdk('default')

        repository = context.object

        # try:
        manager = RepositoryManager(monolithe_config=None, api_url=repository.url, login_or_token=repository.password,
                                    password=None, organization=repository.organization, repository=repository.repository, repository_path=repository.path)

        # api info
        apiinfo = sdk.SDAPIInfo(data=manager.get_api_info(branch=repository.branch))
        self.core_controller.storage_controller.create(apiinfo, repository)

        # astract specs
        abstracts_info = self._populate_specs(manager=manager, repository=repository, mode=MODE_RAW_ABSTRACTS, root_rest_name=apiinfo.root, sdk=sdk) # abstracts first!
        self._populate_api(repository=repository, specification_info=abstracts_info, root_rest_name=apiinfo.root, sdk=sdk)

        # solid specs
        specs_info = self._populate_specs(manager=manager, repository=repository, mode=MODE_RAW_SPECS, root_rest_name=apiinfo.root, sdk=sdk)
        self._populate_api(repository=repository, specification_info=specs_info, root_rest_name=apiinfo.root, sdk=sdk)

        return context


    def _populate_api(self, repository, specification_info, root_rest_name, sdk):
        """
        """
        for rest_name, spec_info in specification_info.iteritems():

            mono_specification = spec_info['mono_specification']
            specification = spec_info['specification']

            for mono_api in mono_specification.parent_apis:

                if not mono_api.remote_name in specification_info:
                    continue

                parent_api = sdk.SDParentAPI()
                parent_api.deprecated = mono_api.deprecated
                parent_api.relationship = mono_api.relationship
                parent_api.allows_create = False
                parent_api.allows_get = False
                parent_api.allows_update = False
                parent_api.allows_delete = False

                if parent_api.relationship == 'root':
                    remote_specification = specification_info[root_rest_name]['specification']
                else:
                    remote_specification = specification_info[mono_api.remote_name]['specification']

                parent_api.associated_specification_id = remote_specification.id

                for operation in mono_api.operations:
                    if operation.method == 'POST':
                        parent_api.allows_create = True
                    elif operation.method == 'GET':
                        parent_api.allows_get = True
                    elif operation.method == 'PUT':
                        parent_api.allows_update = True
                    elif operation.method == 'DELETE':
                        parent_api.allows_delete = True

                out = self.core_controller.storage_controller.create(parent_api, specification)

                child_api = sdk.SDChildAPI(data=parent_api.to_dict())
                child_api.associated_parent_apiid = parent_api.id
                child_api.associated_specification_id = specification.id
                self.core_controller.storage_controller.create(child_api, remote_specification)


    def _populate_extends(self, repository, mono_specification, specification, sdk):
        """
        """
        extensions = []

        for extension_name in mono_specification.extends:

            objects, count = self.core_controller.storage_controller.get_all(parent=repository, resource_name=sdk.SDAbstract.rest_name, filter='name == %s.spec' % extension_name)

            if count:
                extensions = extensions + objects

        if len(extensions):
            self.core_controller.storage_controller.assign(sdk.SDAbstract.rest_name, extensions, specification)

        return extensions

    def _populate_attributes(self, mono_specification, specification, sdk):
        """
        """
        ret = []
        specification.issues = []

        for mono_attribute in mono_specification.attributes:
            attr = sdk.SDAttribute()
            attr.name = mono_attribute.remote_name
            attr.allowed_chars = mono_attribute.allowed_chars
            attr.allowed_choices = mono_attribute.allowed_choices
            attr.autogenerated = mono_attribute.autogenerated
            attr.channel = mono_attribute.channel
            attr.creation_only = mono_attribute.creation_only
            attr.default_order = mono_attribute.default_order
            attr.deprectated = mono_attribute.deprectated
            attr.description = mono_attribute.description
            attr.exposed = mono_attribute.exposed
            attr.filterable = mono_attribute.filterable
            attr.format = mono_attribute.format
            attr.max_length = mono_attribute.max_length
            attr.max_value = mono_attribute.max_value
            attr.min_length = mono_attribute.min_length
            attr.min_value = mono_attribute.min_value
            attr.orderable = mono_attribute.orderable
            attr.read_only = mono_attribute.read_only
            attr.required = mono_attribute.required
            attr.transient = mono_attribute.transient
            attr.type = mono_attribute.type
            attr.unique = mono_attribute.unique
            attr.unique_scope = "no"
            attr.issues = []

            if not attr.validate():

                specification.issues.append('Some attributes were not declared correctly. Please review attributes')
                self.core_controller.storage_controller.update(specification)

                for property_name, error in attr.errors.iteritems():
                    attr.issues.append('Some error has been found in attribute %s declaration: Type has been reverted to "string". please review' % attr.name)
                    attr.type = 'string'

            self.core_controller.storage_controller.create(attr, specification)

            ret.append(attr)

        return ret

    def _populate_specs(self, manager, repository, mode, root_rest_name, sdk):
        """
        """
        mono_specifications = manager.get_all_specifications(branch=repository.branch, mode=mode)

        ret = {}

        for mono_specification in mono_specifications:

            specification = sdk.SDSpecification() if mode == MODE_RAW_SPECS else sdk.SDAbstract()
            specification.name = mono_specification.filename
            specification.description = mono_specification.description
            specification.package = mono_specification.package
            specification.object_rest_name = mono_specification.remote_name
            specification.object_resource_name = mono_specification.resource_name
            specification.entity_name = mono_specification.instance_name
            specification.root_rest_name = root_rest_name

            if len(mono_specification.self_apis) and len(mono_specification.self_apis[0].operations):
                for operation in mono_specification.self_apis[0].operations:
                    if operation.method == 'POST':
                        specification.allows_create = True
                    elif operation.method == 'GET':
                        specification.allows_get = True
                    elif operation.method == 'PUT':
                        specification.allows_update = True
                    elif operation.method == 'DELETE':
                        specification.allows_delete = True

            self.core_controller.storage_controller.create(specification, repository)

            extensions = self._populate_extends(mono_specification=mono_specification, repository=repository, specification=specification,  sdk=sdk)
            attributes = self._populate_attributes(mono_specification=mono_specification, specification=specification, sdk=sdk)

            ret[mono_specification.remote_name] = {'mono_specification': mono_specification , 'specification': specification}

        return ret





