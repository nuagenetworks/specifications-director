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

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import GASDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.apis')


class SDAPILogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='apis logic', version=1.0, identifier="specsdirector.plugins.logic.apis",
                                subscriptions={
                                    "childapi": [GARequest.ACTION_READALL,
                                                 GARequest.ACTION_READ,
                                                 GARequest.ACTION_UPDATE,
                                                 GARequest.ACTION_CREATE,
                                                 GARequest.ACTION_DELETE]
                                })

    def did_register(self):
        """
        """
        self._sdk = GASDKLibrary().get_sdk('default')
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def will_perform_write(self, context):
        """
        """
        if context.request.action in (GARequest.ACTION_DELETE):
            return context

        api = context.object

        if not api.associated_specification_id or not len(api.associated_specification_id):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute associatedSpecificationID is mandatory.', property_name='associatedSpecificationID'))

        self._update_path(specification=context.parent_object, api=api, session_username=context.session.root_object.id)

        return context

    def did_perform_write(self, context):
        """
        """
        self._commit_specification_change(context)
        return context

    # processing

    def _commit_specification_change(self, context):
        """
        """
        action = context.request.action
        specification = context.parent_object
        session_username = context.session.root_object.id

        response = self.core_controller.storage_controller.get(user_identifier=context.session.root_object.id, resource_name=self._sdk.SDRepository.rest_name, identifier=specification.parent_id)

        if action == GARequest.ACTION_CREATE:
            message = "Added child specification api to specification %s" % (specification.name)
        elif action == GARequest.ACTION_UPDATE:
            message = "Updated child specification api in specification %s" % (specification.name)
        elif action == GARequest.ACTION_DELETE:
            message = "Deleted child specification api from specification %s" % (specification.name)

        self._github_operations_controller.commit_specification(repository=response.data, specification=specification, commit_message=message, session_username=session_username)

    def _update_path(self, specification, api, session_username):
        """
        """

        response = self.core_controller.storage_controller.get(user_identifier=session_username, resource_name=self._sdk.SDSpecification.rest_name, identifier=api.associated_specification_id)

        if not response.data:
            return

        associated_resource_name = response.data.object_resource_name

        if specification.rest_name == self._sdk.SDAbstract.rest_name:
            local_resource_name = '<abstract>'
        else:
            local_resource_name = specification.object_resource_name

        if api.relationship == 'root':
            api.path = '/%s' % associated_resource_name
        else:
            api.path = '/%s/id/%s' % (local_resource_name, associated_resource_name)
