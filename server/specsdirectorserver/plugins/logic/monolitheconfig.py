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

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import GASDKLibrary


class SDMonolitheConfigLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='monolitheconfig logic', version=1.0, identifier="specsdirector.plugins.logic.monolitheconfigs",
                                subscriptions={
                                    "monolitheconfig": [GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._sdk = GASDKLibrary().get_sdk('default')
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def will_perform_write(self, context):
        """
        """
        monolithe_config = context.object

        if not monolithe_config.product_name or not len(monolithe_config.product_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute productName is mandatory.', property_name='productName'))

        if not monolithe_config.product_accronym or not len(monolithe_config.product_accronym):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute productAccronym is mandatory.', property_name='productAccronym'))

        if not monolithe_config.sdk_output or not len(monolithe_config.sdk_output):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKOutput is mandatory.', property_name='SDKOutput'))

        if not monolithe_config.sdk_name or not len(monolithe_config.sdk_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKName is mandatory.', property_name='SDKName'))

        if not monolithe_config.sdk_class_prefix or not len(monolithe_config.sdk_class_prefix):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKClassPrefix is mandatory.', property_name='SDKClassPrefix'))

        if not monolithe_config.sdk_bambou_version or not len(monolithe_config.sdk_bambou_version):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKBambouVersion is mandatory.', property_name='SDKBambouVersion'))

        if not monolithe_config.sdk_version or not len(monolithe_config.sdk_version):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKVersion is mandatory.', property_name='SDKVersion'))

        if not monolithe_config.sdk_revision_number or not len(monolithe_config.sdk_revision_number):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKRevisionNumber is mandatory.', property_name='SDKRevisionNumber'))

        if not monolithe_config.sdkcli_name or not len(monolithe_config.sdkcli_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKCLIName is mandatory.', property_name='SDKCLIName'))

        if not monolithe_config.api_doc_output or not len(monolithe_config.api_doc_output):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute APIDocOutput is mandatory.', property_name='APIDocOutput'))

        if not monolithe_config.sdk_doc_output or not len(monolithe_config.sdk_doc_output):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKDocOutput is mandatory.', property_name='SDKDocOutput'))

        return context

    def did_perform_write(self, context):
        """
        """
        monolitheconfig = context.object
        repository = context.parent_object
        session_username = context.session.root_object.id

        self._github_operations_controller.commit_monolitheconfig(repository=repository, monolitheconfig=monolitheconfig, commit_message="Updated Monolithe.ini", session_username=session_username)

        return context
