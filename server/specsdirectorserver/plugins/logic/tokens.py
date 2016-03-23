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

from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import GASDKLibrary


class SDTokenLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='token logic', version=1.0, identifier="specsdirector.plugins.logic.tokens",
                                subscriptions={
                                    "token": [GARequest.ACTION_DELETE, GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._sdk = GASDKLibrary().get_sdk('default')
        self._storage_controller = self.core_controller.storage_controller
        self._push_controller = self.core_controller.push_controller

    def will_perform_delete(self, context):
        """
        """
        token = context.object
        session_username = context.session.root_object.id

        response = self._storage_controller.get_all(user_identifier=session_username,
                                                    resource_name=self._sdk.SDRepository.rest_name,
                                                    parent=None,
                                                    filter="associatedTokenID == '%s'" % token.id)

        if response.count:
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Token in use', description='This token is in used.'))

        return context

    def did_perform_update(self, context):
        """
        """
        token = context.object
        session_username = context.session.root_object.id
        events = []

        response = self._storage_controller.get_all(user_identifier=session_username,
                                                    resource_name=self._sdk.SDRepository.rest_name,
                                                    parent=None,
                                                    filter="associatedTokenID == '%s'" % token.id)

        for repository in response.data:
            repository.status = 'NEEDS_PULL'
            self._storage_controller.update(user_identifier=session_username, resource=repository)
            events.append(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=repository))

        if len(events):
            self._push_controller.push_events(events=events)

        return context
