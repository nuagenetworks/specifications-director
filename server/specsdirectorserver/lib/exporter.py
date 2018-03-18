# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Alcatel-Lucent Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import ConfigParser
import re

from monolithe.specifications import Specification, SpecificationAttribute, SpecificationAPI


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

        mono_spec.description = specification.description
        mono_spec.package = specification.package
        mono_spec.allows_get = specification.allows_get
        mono_spec.allows_update = specification.allows_update
        mono_spec.allows_create = specification.allows_create
        mono_spec.allows_delete = specification.allows_delete

        if specification.rest_name == self._sdk.SDSpecification.rest_name:
            response = self._storage_controller.get_all(user_identifier=session_username, parent=specification, resource_name=self._sdk.SDAbstract.rest_name)

            if response.count:
                mono_spec.extends = sorted([abstract.name.replace(".spec", "") for abstract in response.data])

            mono_spec.is_root = specification.root
            mono_spec.entity_name = specification.entity_name
            mono_spec.rest_name = specification.object_rest_name
            mono_spec.resource_name = specification.object_resource_name
            mono_spec.userlabel = specification.userlabel
            mono_spec.template = specification.template
            mono_spec.allowed_job_commands = sorted(specification.allowed_job_commands) if specification.allowed_job_commands else None

        mono_spec.child_apis = self._export_child_apis(specification=specification, session_username=session_username)
        mono_spec.attributes = self._export_attributes(specification=specification, session_username=session_username)

        return mono_spec

    def export_monolithe_config(self, monolitheconfig):
        """
        """
        parser = ConfigParser.ConfigParser()
        parser.add_section(u'monolithe')
        parser.set('monolithe', 'product_name', monolitheconfig.product_name if monolitheconfig.product_name else "")
        parser.set('monolithe', 'product_accronym', monolitheconfig.product_accronym if monolitheconfig.product_accronym else "")
        parser.set('monolithe', 'copyright', monolitheconfig.copyright if monolitheconfig.copyright else "")

        parser.add_section(u'transformer')
        parser.set('transformer', 'output', monolitheconfig.output if monolitheconfig.output else "")
        parser.set('transformer', 'user_vanilla', monolitheconfig.user_vanilla if monolitheconfig.user_vanilla else "")
        parser.set('transformer', 'name', monolitheconfig.name if monolitheconfig.name else "")
        parser.set('transformer', 'class_prefix', monolitheconfig.class_prefix if monolitheconfig.class_prefix else "")
        parser.set('transformer', 'bambou_version', monolitheconfig.bambou_version if monolitheconfig.bambou_version else "")
        parser.set('transformer', 'version', monolitheconfig.version if monolitheconfig.version else "")
        parser.set('transformer', 'revision_number', monolitheconfig.revision_number if monolitheconfig.revision_number else "")
        parser.set('transformer', 'url', monolitheconfig.url if monolitheconfig.url else "")
        parser.set('transformer', 'author', monolitheconfig.author if monolitheconfig.author else "")
        parser.set('transformer', 'email', monolitheconfig.email if monolitheconfig.email else "")
        parser.set('transformer', 'description', monolitheconfig.description if monolitheconfig.description else "")
        parser.set('transformer', 'license_name', monolitheconfig.license_name if monolitheconfig.license_name else "")
        parser.set('transformer', 'cli_name', monolitheconfig.cli_name if monolitheconfig.cli_name else "")
        parser.set('transformer', 'doc_output', monolitheconfig.doc_output if monolitheconfig.doc_output else "")

        return parser

    # PRIVATE

    def _export_child_apis(self, specification, session_username):
        """
        """
        ret = []
        response = self._storage_controller.get_all(user_identifier=session_username, parent=specification, resource_name=self._sdk.SDChildAPI.rest_name)

        for child_api in response.data:

            mono_child_api = SpecificationAPI()
            response = self._storage_controller.get(user_identifier=session_username, resource_name=self._sdk.SDSpecification.rest_name, identifier=child_api.associated_specification_id)

            mono_child_api.rest_name = response.data.object_rest_name
            mono_child_api.deprecated = child_api.deprecated
            mono_child_api.relationship = child_api.relationship
            mono_child_api.allows_get = child_api.allows_get
            mono_child_api.allows_create = child_api.allows_create
            mono_child_api.allows_update = child_api.allows_update
            mono_child_api.allows_delete = child_api.allows_delete
            mono_child_api.allows_bulk_create = child_api.allows_bulk_create
            mono_child_api.allows_bulk_update = child_api.allows_bulk_update
            mono_child_api.allows_bulk_delete = child_api.allows_bulk_delete

            ret.append(mono_child_api)

        return sorted(ret, lambda x, y: cmp(x.rest_name, y.rest_name))

    def _export_attributes(self, specification, session_username):
        """
        """
        ret = []
        response = self._storage_controller.get_all(user_identifier=session_username, parent=specification, resource_name=self._sdk.SDAttribute.rest_name)

        for attribute in response.data:
            mono_attr = SpecificationAttribute()

            mono_attr.allowed_chars = attribute.allowed_chars
            mono_attr.allowed_choices = sorted(attribute.allowed_choices) if attribute.allowed_choices else None
            mono_attr.autogenerated = attribute.autogenerated
            mono_attr.availability = attribute.availability
            mono_attr.creation_only = attribute.creation_only
            mono_attr.default_order = attribute.default_order
            mono_attr.default_value = attribute.default_value
            mono_attr.deprecated = attribute.deprecated
            mono_attr.description = attribute.description
            mono_attr.exposed = attribute.exposed
            mono_attr.filterable = attribute.filterable
            mono_attr.format = attribute.format
            mono_attr.max_length = attribute.max_length
            mono_attr.max_value = attribute.max_value
            mono_attr.min_length = attribute.min_length
            mono_attr.min_value = attribute.min_value
            mono_attr.name = attribute.name
            mono_attr.orderable = attribute.orderable
            mono_attr.read_only = attribute.read_only
            mono_attr.required = attribute.required
            mono_attr.rest_name = attribute.name
            mono_attr.subtype = attribute.subtype
            mono_attr.transient = attribute.transient
            mono_attr.type = attribute.type
            mono_attr.unique = attribute.unique
            mono_attr.unique_scope = attribute.unique_scope
            if attribute.userlabel is None:
                defaultUserlabel = re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', attribute.name)[0:50]
                attribute.userlabel = defaultUserlabel[0].upper() + defaultUserlabel[1:]
            mono_attr.userlabel = attribute.userlabel

            ret.append(mono_attr)

        return sorted(ret, lambda x, y: cmp(x.name, y.name))
