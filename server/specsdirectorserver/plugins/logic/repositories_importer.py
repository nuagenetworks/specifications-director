import logging
import base64
import json

from github import Github
from monolithe.specifications import Specification, RepositoryManager
from monolithe.specifications.repositorymanager import MODE_NORMAL, MODE_RAW_SPECS, MODE_RAW_ABSTRACTS

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.repositories.importer')

class SDRepositoryImporterLogicPlugin(GALogicPlugin):
    """

    """

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='repositories importer logic', version=1.0, identifier="specsdirector.plugins.logic.repositories.importer",
                                subscriptions={
                                    "repository": [GARequest.ACTION_CREATE]
                                })

    def did_perform_write(self, context):
        """
        """

        if context.request.action == GARequest.ACTION_UPDATE:
            self._export_spec(context)
            return context

        logger.debug("populating")

        sdk = SDKLibrary().get_sdk('default')
        repository = context.object

        manager = RepositoryManager(monolithe_config=None,
                                    api_url=repository.url,
                                    login_or_token=repository.password,
                                    password=None,
                                    organization=repository.organization,
                                    repository=repository.repository,
                                    repository_path=repository.path)

        # api info
        apiinfo = sdk.SDAPIInfo(data=manager.get_api_info(branch=repository.branch))
        self.core_controller.storage_controller.create(apiinfo, repository)

        # astract specs (first!)
        self._import_specs(manager=manager, repository=repository, mode=MODE_RAW_ABSTRACTS, sdk=sdk)

        # solid specs
        self._import_specs(manager=manager, repository=repository, mode=MODE_RAW_SPECS, sdk=sdk)

        return context

    ## UTILITIES

    def _import_specs(self, manager, repository, mode, sdk):
        """
        """
        mono_specifications = manager.get_all_specifications(branch=repository.branch, mode=mode)

        specs_info = {}

        for rest_name, mono_specification in mono_specifications.iteritems():

            specification = sdk.SDSpecification() if mode == MODE_RAW_SPECS else sdk.SDAbstract()
            specification.name = mono_specification.filename
            specification.description = mono_specification.description
            specification.package = mono_specification.package
            specification.object_rest_name = mono_specification.remote_name
            specification.object_resource_name = mono_specification.resource_name
            specification.entity_name = mono_specification.instance_name
            specification.root = mono_specification.is_root
            specification.allows_create = mono_specification.allows_create
            specification.allows_get = mono_specification.allows_get

            self.core_controller.storage_controller.create(specification, repository)

            extensions = self._import_extends(mono_specification=mono_specification, repository=repository, specification=specification,  sdk=sdk)
            attributes = self._import_attributes(mono_specification=mono_specification, specification=specification, sdk=sdk)

            specs_info[mono_specification.remote_name] = {'mono_specification': mono_specification , 'specification': specification}

        self._import_apis(repository=repository, specification_info=specs_info, mode=mode, sdk=sdk)

    def _import_apis(self, repository, specification_info, mode, sdk):
        """
        """
        for rest_name, spec_info in specification_info.iteritems():

            mono_specification = spec_info['mono_specification']
            specification      = spec_info['specification']

            for mono_api in mono_specification.child_apis:

                api               = sdk.SDChildAPI()
                api.deprecated    = mono_api.deprecated
                api.relationship  = mono_api.relationship
                api.specification = mono_api.specification
                api.allows_create = mono_api.allows_create
                api.allows_get    = mono_api.allows_get
                api.allows_update = mono_api.allows_update
                api.allows_delete = mono_api.allows_delete

                if mode == MODE_RAW_SPECS:
                    remote_specification = specification_info[mono_api.specification]['specification']
                    api.associated_specification_id = remote_specification.id

                self.core_controller.storage_controller.create(api, specification)

    def _import_extends(self, repository, mono_specification, specification, sdk):
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

    def _import_attributes(self, mono_specification, specification, sdk):
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
            attr.deprecated = mono_attribute.deprecated
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
