import logging
import base64
import json

from monolithe.specifications import Specification, SpecificationAttribute, SpecificationAPI, RepositoryManager

from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent

class SDRepositoryExporter():
    """

    """

    def __init__(self, repository, storage_controller, push_controller, job, sdk):
        """
        """
        self._sdk = sdk
        self._repository = repository
        self._job = job
        self._storage_controller = storage_controller
        self._push_controller = push_controller

    def export_specifications(self):
        """
        """
        self._export_specifications()
        self._export_abstracts()

        self._set_job_complete()

    ## UTILITIES

    def _set_job_complete(self):
        """
        """
        self._job.progress = 1.0
        self._job.status = 'SUCCESS'
        self._storage_controller.update(self._job)
        event = GAPushEvent(action=GARequest.ACTION_UPDATE, entity=self._job)
        self._push_controller.push_events(events=[event])

    def _export_abstracts(self):
        """
        """
        abstracts, count = self._storage_controller.get_all(parent=self._repository, resource_name=self._sdk.SDAbstract.rest_name)
        apiinfo = self._export_apiinfo()

        for abstract in abstracts:

            mono_spec = Specification(monolithe_config=None, filename=abstract.name)

            mono_spec.description   = abstract.description
            mono_spec.entity_name   = abstract.entity_name
            mono_spec.package       = abstract.package
            mono_spec.rest_name   = abstract.object_rest_name
            mono_spec.resource_name = abstract.object_resource_name
            mono_spec.allows_get    = abstract.allows_get
            mono_spec.allows_update = abstract.allows_update
            mono_spec.allows_create = abstract.allows_create
            mono_spec.allows_delete = abstract.allows_delete

            mono_spec.child_apis  = self._export_child_apis(specification=abstract, apiinfo=apiinfo)
            mono_spec.attributes  = self._export_attributes(specification=abstract)

            with open('/Users/Tonio/Desktop/vomit/%s' % abstract.name, 'w') as f:
                f.write(json.dumps(mono_spec.to_dict(), indent=4, sort_keys=True))

    def _export_specifications(self):
        """
        """
        specifications, count = self._storage_controller.get_all(parent=self._repository, resource_name=self._sdk.SDSpecification.rest_name)
        apiinfo = self._export_apiinfo()

        for specification in specifications:

            abstracts, count = self._storage_controller.get_all(parent=specification, resource_name=self._sdk.SDAbstract.rest_name)

            mono_spec = Specification(monolithe_config=None, filename=specification.name)

            mono_spec.description   = specification.description
            mono_spec.entity_name   = specification.entity_name
            mono_spec.package       = specification.package
            mono_spec.rest_name   = specification.object_rest_name
            mono_spec.resource_name = specification.object_resource_name
            mono_spec.is_root       = specification.root
            mono_spec.allows_get    = specification.allows_get
            mono_spec.allows_update = specification.allows_update
            mono_spec.allows_create = specification.allows_create
            mono_spec.allows_delete = specification.allows_delete
            mono_spec.extends       = [abstract.name.replace(".spec", "") for abstract in abstracts]

            mono_spec.child_apis  = self._export_child_apis(specification=specification, apiinfo=apiinfo)
            mono_spec.attributes  = self._export_attributes(specification=specification)

            with open('/Users/Tonio/Desktop/vomit/%s' % specification.name, 'w') as f:
                f.write(json.dumps(mono_spec.to_dict(), indent=4, sort_keys=True))

    def _export_apiinfo(self):
        """
        """
        objects, count = self._storage_controller.get_all(parent=self._repository, resource_name=self._sdk.SDAPIInfo.rest_name, filter='parentID == %s' % self._repository.id)
        apiinfo = objects[0]

        with open('/Users/Tonio/Desktop/vomit/api.info', 'w') as f:
            info = {'version': apiinfo.version, 'prefix': apiinfo.prefix, 'root': apiinfo.root}
            f.write(json.dumps(info, indent=4, sort_keys=True))

        return apiinfo

    def _export_child_apis(self, specification, apiinfo):
        """
        """
        ret = []
        child_apis, count = self._storage_controller.get_all(parent=specification, resource_name=self._sdk.SDChildAPI.rest_name)

        for child_api in child_apis:

            mono_child_api = SpecificationAPI(specification=specification)
            remote_specification = self._storage_controller.get(resource_name=self._sdk.SDSpecification.rest_name, identifier=child_api.associated_specification_id)

            mono_child_api.specification = remote_specification.object_rest_name
            mono_child_api.deprecated    = child_api.deprecated
            mono_child_api.relationship  = child_api.relationship
            mono_child_api.allows_get    = child_api.allows_get
            mono_child_api.allows_create = child_api.allows_create
            mono_child_api.allows_update = child_api.allows_update
            mono_child_api.allows_delete = child_api.allows_delete

            ret.append(mono_child_api)

        return ret

    def _export_attributes(self, specification):
        """
        """
        ret = []
        attributes, count = self._storage_controller.get_all(parent=specification, resource_name=self._sdk.SDAttribute.rest_name)

        for attribute in attributes:
            mono_attr = SpecificationAttribute(rest_name=attribute.name)

            mono_attr.description     = attribute.description
            mono_attr.rest_name     = attribute.name
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