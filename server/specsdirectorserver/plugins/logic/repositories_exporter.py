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
        return GAPluginManifest(name='repositories exporter logic',
                                version=1.0,
                                identifier="specsdirector.plugins.logic.repositories.exporter",
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

            mono_spec.self_apis   = self._export_self_api(specification=abstract)
            mono_spec.parent_apis = self._export_parent_apis(specification=abstract, apiinfo=apiinfo, sdk=sdk)
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
            mono_spec.extends       = [abstract.name.replace(".spec", "") for abstract in abstracts]

            mono_spec.self_apis   = self._export_self_api(specification=specification)
            mono_spec.parent_apis = self._export_parent_apis(specification=specification, apiinfo=apiinfo, sdk=sdk)
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

    def _export_self_api(self, specification):
        """
        """
        mono_self_api = SpecificationAPI(specification=specification)

        if specification.object_resource_name and specification.object_resource_name and specification.entity_name:
            mono_self_api.path          = '/%s/{id}' % (specification.object_resource_name)
            mono_self_api.resource_name = specification.object_resource_name
            mono_self_api.remote_name   = specification.object_rest_name
            mono_self_api.entity_name   = specification.entity_name
            mono_self_api.operations    = self._export_operations(specification)
            return [mono_self_api]
        else:
            return []


    def _export_parent_apis(self, specification, apiinfo, sdk):
        """
        """
        ret = []
        parent_apis, count = self.core_controller.storage_controller.get_all(parent=specification, resource_name=sdk.SDParentAPI.rest_name)

        for parent_api in parent_apis:

            remote_specification = self.core_controller.storage_controller.get(resource_name=sdk.SDSpecification.rest_name, identifier=parent_api.associated_specification_id)
            mono_parent_api = SpecificationAPI(specification=specification)

            mono_parent_api.deprecated   = parent_api.deprecated
            mono_parent_api.relationship = parent_api.relationship
            mono_parent_api.operations   = self._export_operations(parent_api)

            if remote_specification.object_resource_name == apiinfo.root:
                mono_parent_api.path  = '/%s' % (specification.object_resource_name)
                related_specification = specification

            else:
                mono_parent_api.path  = '/%s/{id}/%s' % (remote_specification.object_resource_name, specification.object_resource_name)
                related_specification = remote_specification

            mono_parent_api.resource_name = related_specification.object_resource_name
            mono_parent_api.remote_name   = related_specification.object_rest_name
            mono_parent_api.entity_name   = related_specification.entity_name

            ret.append(mono_parent_api)

        return ret

    def _export_child_apis(self, specification, apiinfo, sdk):
        """
        """
        ret = []
        child_apis, count = self.core_controller.storage_controller.get_all(parent=specification, resource_name=sdk.SDChildAPI.rest_name)

        for child_api in child_apis:

            mono_child_api = SpecificationAPI(specification=specification)
            remote_specification = self.core_controller.storage_controller.get(resource_name=sdk.SDSpecification.rest_name, identifier=child_api.associated_specification_id)

            mono_child_api.deprecated = child_api.deprecated
            mono_child_api.relationship = child_api.relationship
            mono_child_api.operations = self._export_operations(child_api)

            if specification.object_rest_name == apiinfo.root:
                mono_child_api.path = '/%s' % (remote_specification.object_resource_name)

            else:
                mono_child_api.path = '/%s/{id}/%s' % (specification.object_resource_name, remote_specification.object_resource_name)

            mono_child_api.resource_name = remote_specification.object_resource_name
            mono_child_api.remote_name   = remote_specification.object_rest_name
            mono_child_api.entity_name   = remote_specification.entity_name

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

    def _export_operations(self, obj):
        """
        """
        ret = []

        if hasattr(obj, 'allows_get') and obj.allows_get:
            mono_operation = SpecificationAPIOperation()
            mono_operation.method = 'GET'
            ret.append(mono_operation)

        if hasattr(obj, 'allows_create') and obj.allows_create:
            mono_operation = SpecificationAPIOperation()
            mono_operation.method = 'POST'
            ret.append(mono_operation)

        if hasattr(obj, 'allows_update') and obj.allows_update:
            mono_operation = SpecificationAPIOperation()
            mono_operation.method = 'UPDATE'
            ret.append(mono_operation)

        if hasattr(obj, 'allows_delete') and obj.allows_delete:
            mono_operation = SpecificationAPIOperation()
            mono_operation.method = 'DELETE'
            ret.append(mono_operation)

        return ret