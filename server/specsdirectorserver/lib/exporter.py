import logging
import json
import ConfigParser

from garuda.core.models import GARequest, GAPushEvent

from monolithe.specifications import Specification, SpecificationAttribute, SpecificationAPI, RepositoryManager


class SDSpecificationExporter():
    """

    """

    def __init__(self, storage_controller, push_controller, sdk):
        """
        """
        self._sdk = sdk
        self._storage_controller = storage_controller
        self._push_controller = push_controller

    def export_specification(self, specification, session_username):
        """
        """
        mono_spec = Specification(monolithe_config=None, filename=specification.name)

        mono_spec.description   = specification.description
        mono_spec.package       = specification.package
        mono_spec.allows_get    = specification.allows_get
        mono_spec.allows_update = specification.allows_update
        mono_spec.allows_create = specification.allows_create
        mono_spec.allows_delete = specification.allows_delete

        if specification.rest_name == self._sdk.SDSpecification.rest_name:
            response = self._storage_controller.get_all(user_identifier=session_username, parent=specification, resource_name=self._sdk.SDAbstract.rest_name)

            if response.count:
                mono_spec.extends = [abstract.name.replace(".spec", "") for abstract in response.data]

            mono_spec.is_root       = specification.root
            mono_spec.entity_name   = specification.entity_name
            mono_spec.rest_name     = specification.object_rest_name
            mono_spec.resource_name = specification.object_resource_name

        mono_spec.child_apis  = self._export_child_apis(specification=specification, session_username=session_username)
        mono_spec.attributes  = self._export_attributes(specification=specification, session_username=session_username)

        return mono_spec

    def export_monolithe_config(self, monolitheconfig):
        """
        """
        parser = ConfigParser.ConfigParser()
        parser.add_section('monolithe')
        parser.set('monolithe', 'product_name', monolitheconfig.product_name if monolitheconfig.product_name else "")
        parser.set('monolithe', 'product_accronym', monolitheconfig.product_accronym if monolitheconfig.product_accronym else "")
        parser.set('monolithe', 'copyright', monolitheconfig.copyright if monolitheconfig.copyright else "")

        parser.add_section('sdk')
        parser.set('sdk', 'sdk_output', monolitheconfig.sdk_output if monolitheconfig.sdk_output else "")
        parser.set('sdk', 'sdk_user_vanilla', monolitheconfig.sdkuser_vanilla if monolitheconfig.sdkuser_vanilla else "")
        parser.set('sdk', 'sdk_name', monolitheconfig.sdk_name if monolitheconfig.sdk_name else "")
        parser.set('sdk', 'sdk_class_prefix', monolitheconfig.sdk_class_prefix if monolitheconfig.sdk_class_prefix else "")
        parser.set('sdk', 'sdk_bambou_version', monolitheconfig.sdk_bambou_version if monolitheconfig.sdk_bambou_version else "")
        parser.set('sdk', 'sdk_version', monolitheconfig.sdk_version if monolitheconfig.sdk_version else "")
        parser.set('sdk', 'sdk_revision_number', monolitheconfig.sdk_revision_number if monolitheconfig.sdk_revision_number else "")
        parser.set('sdk', 'sdk_url', monolitheconfig.sdkurl if monolitheconfig.sdkurl else "")
        parser.set('sdk', 'sdk_author', monolitheconfig.sdk_author if monolitheconfig.sdk_author else "")
        parser.set('sdk', 'sdk_email', monolitheconfig.sdk_email if monolitheconfig.sdk_email else "")
        parser.set('sdk', 'sdk_description', monolitheconfig.sdk_description if monolitheconfig.sdk_description else "")
        parser.set('sdk', 'sdk_license_name', monolitheconfig.sdk_license_name if monolitheconfig.sdk_license_name else "")
        parser.set('sdk', 'sdk_cli_name', monolitheconfig.sdkcli_name if monolitheconfig.sdkcli_name else "")

        parser.add_section('apidoc')
        parser.set('apidoc', 'apidoc_output', monolitheconfig.api_doc_output if monolitheconfig.api_doc_output else "")
        parser.set('apidoc', 'apidoc_user_vanilla', monolitheconfig.api_doc_user_vanilla if monolitheconfig.api_doc_user_vanilla else "")

        parser.add_section('sdkdoc')
        parser.set('sdkdoc', 'sdkdoc_output', monolitheconfig.sdk_doc_output if monolitheconfig.sdk_doc_output else "")
        parser.set('sdkdoc', 'sdkdoc_user_vanilla', monolitheconfig.sdk_doc_user_vanilla if monolitheconfig.sdk_doc_user_vanilla else "")
        parser.set('sdkdoc', 'sdkdoc_tmp_path', monolitheconfig.sdk_doc_tmp_path if monolitheconfig.sdk_doc_tmp_path else "")

        return parser

    ## PRIVATE
    def _export_child_apis(self, specification, session_username):
        """
        """
        ret = []
        response = self._storage_controller.get_all(user_identifier=session_username, parent=specification, resource_name=self._sdk.SDChildAPI.rest_name)

        for child_api in response.data:

            mono_child_api = SpecificationAPI(remote_specification_name=specification.name)
            response = self._storage_controller.get(user_identifier=session_username, resource_name=self._sdk.SDSpecification.rest_name, identifier=child_api.associated_specification_id)

            mono_child_api.remote_specification_name = response.data.object_rest_name
            mono_child_api.deprecated                = child_api.deprecated
            mono_child_api.relationship              = child_api.relationship
            mono_child_api.allows_get                = child_api.allows_get
            mono_child_api.allows_create             = child_api.allows_create
            mono_child_api.allows_update             = child_api.allows_update
            mono_child_api.allows_delete             = child_api.allows_delete
            mono_child_api.allows_bulk_create        = child_api.allows_bulk_create
            mono_child_api.allows_bulk_update        = child_api.allows_bulk_update
            mono_child_api.allows_bulk_delete        = child_api.allows_bulk_delete

            ret.append(mono_child_api)

        return ret

    def _export_attributes(self, specification, session_username):
        """
        """
        ret = []
        response = self._storage_controller.get_all(user_identifier=session_username, parent=specification, resource_name=self._sdk.SDAttribute.rest_name)

        for attribute in response.data:
            mono_attr = SpecificationAttribute(rest_name=attribute.name)

            mono_attr.description     = attribute.description
            mono_attr.rest_name       = attribute.name
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
            mono_attr.subtype         = attribute.subtype

            ret.append(mono_attr)

        return ret