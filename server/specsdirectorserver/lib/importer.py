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

import logging
import ssl

from specsrepositorymanager import MODE_RAW_SPECS, MODE_RAW_ABSTRACTS


logger = logging.getLogger('specsdirector.specification_importer')


class SDSpecificationImporter():
    """

    """
    def __init__(self, storage_controller, push_controller, sdk):
        """
        """
        self._sdk = sdk
        self._storage_controller = storage_controller
        self._push_controller = push_controller
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

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

            monolithe_config.product_name = parser.get('monolithe', 'product_name')
            monolithe_config.product_accronym = parser.get('monolithe', 'product_accronym')
            monolithe_config.copyright = parser.get('monolithe', 'copyright')

            monolithe_config.output = parser.get('transformer', 'output')
            monolithe_config.user_vanilla = parser.get('transformer', 'user_vanilla')
            monolithe_config.name = parser.get('transformer', 'name')
            monolithe_config.class_prefix = parser.get('transformer', 'class_prefix')
            monolithe_config.bambou_version = parser.get('transformer', 'bambou_version')
            monolithe_config.version = parser.get('transformer', 'version')
            monolithe_config.revision_number = parser.get('transformer', 'revision_number')
            monolithe_config.url = parser.get('transformer', 'url')
            monolithe_config.author = parser.get('transformer', 'author')
            monolithe_config.email = parser.get('transformer', 'email')
            monolithe_config.description = parser.get('transformer', 'description')
            monolithe_config.license_name = parser.get('transformer', 'license_name')
            monolithe_config.cli_name = parser.get('transformer', 'cli_name')
            monolithe_config.doc_output = parser.get('transformer', 'doc_output')

        except Exception as ex:
            logger.warning('Unable to parse monolithe.ini: %s. Using default value' % ex)
            monolithe_config.output = './codegen'
            monolithe_config.class_prefix = 'GA'
            monolithe_config.bambou_version = '2.0.0'
            monolithe_config.version = '1.0'
            monolithe_config.revision_number = '1'
            monolithe_config.doc_output = './sdkdocgen'

        self._storage_controller.create(user_identifier=session_username, resource=monolithe_config, parent=repository)

    def import_specifications(self, repository, manager, session_username):
        """
        """
        self._import_specs(repository=repository, manager=manager, mode=MODE_RAW_SPECS, session_username=session_username)

    def import_abstracts(self, repository, manager, session_username):
        """
        """
        self._import_specs(repository=repository, manager=manager, mode=MODE_RAW_ABSTRACTS, session_username=session_username)

    # PRIVATE

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

            specification.name = mono_specification.filename
            specification.description = mono_specification.description
            specification.package = mono_specification.package
            specification.allows_create = mono_specification.allows_create
            specification.allows_get = mono_specification.allows_get
            specification.allows_update = mono_specification.allows_update
            specification.allows_delete = mono_specification.allows_delete

            if specification.rest_name == self._sdk.SDSpecification.rest_name:
                specification.object_rest_name = mono_specification.rest_name
                specification.object_resource_name = mono_specification.resource_name
                specification.entity_name = mono_specification.entity_name
                specification.root = mono_specification.is_root
                specification.userlabel = mono_specification.userlabel
                specification.template = mono_specification.template
                specification.allowed_job_commands = sorted(mono_specification.allowed_job_commands) if mono_specification.allowed_job_commands else None

            self._storage_controller.create(user_identifier=session_username, resource=specification, parent=repository)

            self._import_extends(repository=repository, mono_specification=mono_specification, specification=specification, session_username=session_username)
            self._import_attributes(mono_specification=mono_specification, specification=specification, session_username=session_username)

            specs_info[mono_specification.rest_name] = {'mono_specification': mono_specification, 'specification': specification}

        self._import_apis(specification_info=specs_info, mode=mode, session_username=session_username)

    def _import_apis(self, specification_info, mode, session_username):
        """
        """
        for rest_name, spec_info in specification_info.iteritems():

            mono_specification = spec_info['mono_specification']
            specification = spec_info['specification']

            for mono_api in sorted(mono_specification.child_apis, lambda x, y: cmp(x.rest_name, y.rest_name)):

                api = self._sdk.SDChildAPI()

                api.remote_rest_name = mono_api.rest_name
                api.deprecated = mono_api.deprecated
                api.relationship = mono_api.relationship
                api.allows_create = mono_api.allows_create
                api.allows_get = mono_api.allows_get
                api.allows_update = mono_api.allows_update
                api.allows_delete = mono_api.allows_delete
                api.allows_bulk_create = mono_api.allows_bulk_create
                api.allows_bulk_update = mono_api.allows_bulk_update
                api.allows_bulk_delete = mono_api.allows_bulk_delete

                if mode == MODE_RAW_SPECS:
                    remote_specification = specification_info[mono_api.rest_name]['specification']
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

        for mono_attribute in sorted(mono_specification.attributes, lambda x, y: cmp(x.name, y.name)):

            attr = self._sdk.SDAttribute()

            attr.allowed_chars = mono_attribute.allowed_chars
            attr.allowed_choices = sorted(mono_attribute.allowed_choices) if mono_attribute.allowed_choices else None
            attr.autogenerated = mono_attribute.autogenerated
            attr.channel = mono_attribute.channel
            attr.creation_only = mono_attribute.creation_only
            attr.default_order = mono_attribute.default_order
            attr.default_value = mono_attribute.default_value
            attr.deprecated = mono_attribute.deprecated
            attr.description = mono_attribute.description
            attr.exposed = mono_attribute.exposed
            attr.filterable = mono_attribute.filterable
            attr.format = mono_attribute.format
            attr.issues = []
            attr.max_length = mono_attribute.max_length
            attr.max_value = mono_attribute.max_value
            attr.min_length = mono_attribute.min_length
            attr.min_value = mono_attribute.min_value
            attr.name = mono_attribute.name
            attr.orderable = mono_attribute.orderable
            attr.read_only = mono_attribute.read_only
            attr.required = mono_attribute.required
            attr.subtype = mono_attribute.subtype
            attr.transient = mono_attribute.transient
            attr.type = mono_attribute.type
            attr.unique = mono_attribute.unique
            attr.unique_scope = mono_attribute.unique_scope
            attr.userlabel = mono_attribute.userlabel

            if not attr.validate():

                specification.issues.append('Some attributes were not declared correctly. Please review attributes')
                self._storage_controller.update(user_identifier=session_username, resource=specification)

                for property_name, error in attr.errors.iteritems():
                    attr.issues.append('Some error has been found in attribute %s declaration: Type has been reverted to "string". please review' % attr.name)
                    attr.type = 'string'

            self._storage_controller.create(user_identifier=session_username, resource=attr, parent=specification)

            ret.append(attr)
