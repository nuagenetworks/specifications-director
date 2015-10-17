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
        return GAPluginManifest(name='repository logic',
                                version=1.0,
                                identifier="specsdirector.plugins.logic.repository",
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
        abstracts_info = self._populate_specs(manager=manager, repository=repository, mode=MODE_RAW_ABSTRACTS, sdk=sdk) # abstracts first!
        self._populate_api(repository=repository, specification_info=abstracts_info, api_type='children_apis', api_class=sdk.SDChildAPI, sdk=sdk)
        self._populate_api(repository=repository, specification_info=abstracts_info, api_type='parent_apis', api_class=sdk.SDParentAPI, sdk=sdk)

        # solid specs
        specs_info = self._populate_specs(manager=manager, repository=repository, mode=MODE_RAW_SPECS, sdk=sdk)
        self._populate_api(repository=repository, specification_info=specs_info, api_type='children_apis', api_class=sdk.SDChildAPI, sdk=sdk)
        self._populate_api(repository=repository, specification_info=specs_info, api_type='parent_apis', api_class=sdk.SDParentAPI, sdk=sdk)

        return context


    def _populate_api(self, repository, specification_info, api_type, api_class, sdk):
        """
        """
        for rest_name, spec_info in specification_info.iteritems():

            mono_specification = spec_info['mono_specification']
            specification = spec_info['specification']

            for mono_api in getattr(mono_specification, api_type):

                if not mono_api.remote_name in specification_info:
                    continue

                remote_specification = specification_info[mono_api.remote_name]['specification']
                remote_mono_specification = specification_info[mono_api.remote_name]['mono_specification']

                api = api_class()
                api.deprecated = mono_api.deprecated
                api.relationship = mono_api.relationship
                api.allows_create = False
                api.allows_get = False
                api.allows_update = False
                api.allows_delete = False

                if api_type == 'children_apis':
                    api.path = '/%s/id/%s' % (mono_specification.resource_name, remote_mono_specification.resource_name)
                elif api_type == 'parent_apis':
                    api.path = '/%s/id/%s' % (remote_mono_specification.resource_name, mono_specification.resource_name)
                else:
                    api.path = '/%s/id' % mono_specification.resource_name

                api.associated_specification_id = remote_specification.id

                for operation in mono_api.operations:
                    if operation.method == 'POST':
                        api.allows_create = True
                    elif operation.method == 'GET':
                        api.allows_get = True
                    elif operation.method == 'PUT':
                        api.allows_update = True
                    elif operation.method == 'DELETE':
                        api.allows_delete = True

                self.core_controller.storage_controller.create(api, specification)

    def _populate_model(self, mono_specification, specification, sdk):
        """
        """
        model = sdk.SDModel()
        model.description = mono_specification.description
        model.package = mono_specification.package
        model.object_rest_name = mono_specification.remote_name
        model.object_resource_name = mono_specification.resource_name
        model.entity_name = mono_specification.instance_name

        if len(mono_specification.self_apis) and len(mono_specification.self_apis[0].operations):
            for operation in mono_specification.self_apis[0].operations:
                if operation.method == 'POST':
                    model.allows_create = True
                elif operation.method == 'GET':
                    model.allows_get = True
                elif operation.method == 'PUT':
                    model.allows_update = True
                elif operation.method == 'DELETE':
                    model.allows_delete = True

        self.core_controller.storage_controller.create(model, specification)

        return model

    def _populate_extends(self, repository, mono_specification, model, sdk):
        """
        """
        extensions = []

        for extension_name in mono_specification.extends:

            objects, count = self.core_controller.storage_controller.get_all(parent=repository, resource_name=sdk.SDAbstract.rest_name, filter='name == %s.spec' % extension_name)

            if count:
                extensions = extensions + objects

        if len(extensions):
            self.core_controller.storage_controller.assign(sdk.SDAbstract.rest_name, extensions, model)

        return extensions

    def _populate_attributes(self, mono_specification, specification, sdk):
        """
        """
        ret = []
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

            validation = self.core_controller.storage_controller.create(attr, specification)
            if validation:
                pass#print "%s: %s: %s" % (attr.name, validation[0].title, validation[0].description)

            ret.append(attr)

        return ret

    def _populate_specs(self, manager, repository, mode, sdk):
        """
        """
        mono_specifications = manager.get_all_specifications(branch=repository.branch, mode=mode)

        ret = {}

        for mono_specification in mono_specifications:

            specification = sdk.SDSpecification() if mode == MODE_RAW_SPECS else sdk.SDAbstract()
            specification.name = mono_specification.filename

            self.core_controller.storage_controller.create(specification, repository)

            model      = self._populate_model(mono_specification=mono_specification, specification=specification, sdk=sdk)
            extensions = self._populate_extends(mono_specification=mono_specification, repository=repository, model=model, sdk=sdk)
            attributes = self._populate_attributes(mono_specification=mono_specification, specification=specification, sdk=sdk)

            ret[mono_specification.remote_name] = {'mono_specification': mono_specification , 'specification': specification}

        return ret





