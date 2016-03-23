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

logger = logging.getLogger('specsdirector.plugins.logic.specifications')


class SDAPIInfoLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='api logic', version=1.0, identifier="specsdirector.plugins.logic.apiinfos",
                                subscriptions={
                                    "apiinfo": [GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._sdk = GASDKLibrary().get_sdk('default')
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def will_perform_update(self, context):
        """
        """
        apiinfo = context.object

        if apiinfo.prefix[1] == '/':
            apiinfo.prefix = apiinfo.prefix[1:]

        if apiinfo.prefix[-1] == '/':
            apiinfo.prefix = apiinfo.prefix[:-1]

        if not apiinfo.version or not len(apiinfo.version):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute version is mandatory.', property_name='version'))

        try:
            float(apiinfo.version)
        except:
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Wrong attribute', description='Attribute version must be a float.', property_name='version'))

        if not apiinfo.root or not len(apiinfo.root):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute root is mandatory.', property_name='root'))

        if not apiinfo.prefix or not len(apiinfo.prefix):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute prefix is mandatory.', property_name='prefix'))

        return context

    def did_perform_update(self, context):
        """
        """
        apiinfo = context.object
        repository = context.parent_object
        session_username = context.session.root_object.id

        self._github_operations_controller.commit_apiinfo(repository=repository, apiinfo=apiinfo, commit_message="Updated api.info", session_username=session_username)

        return context
