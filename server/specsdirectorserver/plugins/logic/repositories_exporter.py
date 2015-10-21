import logging
import base64
import json

from github import Github
from monolithe.specifications import Specification, SpecificationAttribute, SpecificationAPI, RepositoryManager
from monolithe.specifications.repositorymanager import MODE_NORMAL, MODE_RAW_SPECS, MODE_RAW_ABSTRACTS

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary


logger = logging.getLogger('specsdirector.plugins.logic.repositories.exporter')

class SDRepositoryExporterLogicPlugin(GALogicPlugin):
    """

    """

    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='repositories exporter logic', version=1.0, identifier="specsdirector.plugins.logic.repositories.exporter",
                                subscriptions={
                                    "repository": [GARequest.ACTION_UPDATE]
                                })

    def did_perform_write(self, context):
        """
        """
        sdk = SDKLibrary().get_sdk('default')
        repository = context.object

        self._export_specifications(repository=repository, sdk=sdk)
        self._export_abstracts(repository=repository, sdk=sdk)

        return context

    ## UTILITIES

    def _export_abstracts(self, repository, sdk):
        """
        """
        abstracts, count = self.core_controller.storage_controller.get_all(parent=repository, resource_name=sdk.SDAbstract.rest_name)
        apiinfo = self._export_apiinfo(repository=repository, sdk=sdk)

        for abstract in abstracts:

            mono_spec = Specification(monolithe_config=None, filename=abstract.name)

            mono_spec.description   = abstract.description
            mono_spec.name          = abstract.entity_name
            mono_spec.package       = abstract.package
            mono_spec.remote_name   = abstract.object_rest_name
            mono_spec.resource_name = abstract.object_resource_name
            mono_spec.allows_get    = abstract.allows_get
            mono_spec.allows_update = abstract.allows_update
            mono_spec.allows_create = abstract.allows_create
            mono_spec.allows_delete = abstract.allows_delete

            mono_spec.child_apis  = self._export_child_apis(specification=abstract, apiinfo=apiinfo, sdk=sdk)
            mono_spec.attributes  = self._export_attributes(specification=abstract, sdk=sdk)

            with open('/Users/Tonio/Desktop/vomit/%s' % abstract.name, 'w') as f:
                f.write(json.dumps(mono_spec.to_dict(), indent=4))

    def _export_specifications(self, repository, sdk):
        """
        """
        specifications, count = self.core_controller.storage_controller.get_all(parent=repository, resource_name=sdk.SDSpecification.rest_name)
        apiinfo = self._export_apiinfo(repository=repository, sdk=sdk)

        for specification in specifications:

            abstracts, count = self.core_controller.storage_controller.get_all(parent=repository, resource_name=sdk.SDAbstract.rest_name)

            mono_spec = Specification(monolithe_config=None, filename=specification.name)

            mono_spec.description   = specification.description
            mono_spec.name          = specification.entity_name
            mono_spec.package       = specification.package
            mono_spec.remote_name   = specification.object_rest_name
            mono_spec.resource_name = specification.object_resource_name
            mono_spec.is_root       = specification.root
            mono_spec.allows_get    = specification.allows_get
            mono_spec.allows_update = specification.allows_update
            mono_spec.allows_create = specification.allows_create
            mono_spec.allows_delete = specification.allows_delete
            mono_spec.extends       = [abstract.name.replace(".spec", "") for abstract in abstracts]

            mono_spec.child_apis  = self._export_child_apis(specification=specification, apiinfo=apiinfo, sdk=sdk)
            mono_spec.attributes  = self._export_attributes(specification=specification, sdk=sdk)

            with open('/Users/Tonio/Desktop/vomit/%s' % specification.name, 'w') as f:
                f.write(json.dumps(mono_spec.to_dict(), indent=4))

    def _export_apiinfo(self, repository, sdk):
        """
        """
        objects, count = self.core_controller.storage_controller.get_all(parent=repository, resource_name=sdk.SDAPIInfo.rest_name, filter='parentID == %s' % repository.id)
        apiinfo = objects[0]

        with open('/Users/Tonio/Desktop/vomit/api.info', 'w') as f:
            info = {'version': apiinfo.version, 'prefix': apiinfo.prefix, 'root': apiinfo.root}
            f.write(json.dumps(info, indent=4))

        return apiinfo

    def _export_child_apis(self, specification, apiinfo, sdk):
        """
        """
        ret = []
        child_apis, count = self.core_controller.storage_controller.get_all(parent=specification, resource_name=sdk.SDChildAPI.rest_name)

        for child_api in child_apis:

            mono_child_api = SpecificationAPI(specification=specification)
            remote_specification = self.core_controller.storage_controller.get(resource_name=sdk.SDSpecification.rest_name, identifier=child_api.associated_specification_id)

            mono_child_api.specification = remote_specification.object_rest_name
            mono_child_api.deprecated    = child_api.deprecated
            mono_child_api.relationship  = child_api.relationship
            mono_child_api.allows_get    = child_api.allows_get
            mono_child_api.allows_create = child_api.allows_create
            mono_child_api.allows_update = child_api.allows_update
            mono_child_api.allows_delete = child_api.allows_delete

            ret.append(mono_child_api)

        return ret

    def _export_attributes(self, specification, sdk):
        """
        """
        ret = []
        attributes, count = self.core_controller.storage_controller.get_all(parent=specification, resource_name=sdk.SDAttribute.rest_name)

        for attribute in attributes:
            mono_attr = SpecificationAttribute(specification=None)

            mono_attr.description     = attribute.description
            mono_attr.remote_name     = attribute.name
            mono_attr.type            = attribute.type
            mono_attr.allowed_chars   = attribute.allowed_chars
            mono_attr.allowed_choices = attribute.allowed_choices
            mono_attr.autogenerated   = attribute.autogenerated
            mono_attr.availability    = attribute.availability
            mono_attr.creation_only   = attribute.creation_only
            mono_attr.default_order   = attribute.default_order
            mono_attr.default_value   = attribute.default_value
            mono_attr.deprecated      = attribute.deprecated
            mono_attr.filterable      = attribute.filterable
            mono_attr.format          = attribute.format
            mono_attr.max_length      = attribute.max_length
            mono_attr.max_value       = attribute.max_value
            mono_attr.min_length      = attribute.min_length
            mono_attr.min_value       = attribute.min_value
            mono_attr.orderable       = attribute.orderable
            mono_attr.readonly        = attribute.read_only
            mono_attr.required        = attribute.required
            mono_attr.unique          = attribute.unique
            mono_attr.unique_scope    = attribute.unique_scope

            ret.append(mono_attr)

        return ret