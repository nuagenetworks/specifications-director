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

logger = logging.getLogger('specsdirector.plugins.logic.attributes')


class SDAttributeLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='attributes logic', version=1.0, identifier="specsdirector.plugins.logic.attributes",
                                subscriptions={
                                    "attribute": [GARequest.ACTION_DELETE, GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE]
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

        specification = context.parent_object
        attribute = context.object

        response = self.core_controller.storage_controller.get_all(user_identifier=context.session.root_object.id, parent=specification, resource_name=self._sdk.SDAttribute.rest_name, filter='name == "%s"' % attribute.name)

        if response.count and response.data[0].id != attribute.id:
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Duplicate Name', description='Another attribute exists with the name %s' % attribute.name, property_name='name'))

        if not attribute.name or not len(attribute.name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute name is mandatory.', property_name='name'))

        if not attribute.type or not len(attribute.type):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute type is mandatory.', property_name='type'))

        if attribute.type != 'enum' and not (attribute.type == 'list' and attribute.subtype == 'enum'):
            attribute.allowed_choices = None

        if attribute.type != 'string':
            attribute.min_length = None
            attribute.max_length = None
            attribute.format = None
            attribute.allowed_chars = None

        if attribute.type != 'integer' and attribute.type != 'float':
            attribute.min_value = None
            attribute.max_value = None

        return context

    def did_perform_write(self, context):
        """
        """
        self._commit_specification_change(context)
        return context

    # Processing

    def _commit_specification_change(self, context):
        """
        """
        action = context.request.action
        attribute = context.object
        specification = context.parent_object
        session_username = context.session.root_object.id

        response = self.core_controller.storage_controller.get(user_identifier=context.session.root_object.id, resource_name=self._sdk.SDRepository.rest_name, identifier=specification.parent_id)

        if action == GARequest.ACTION_CREATE:
            message = "Added attribute %s to specification %s" % (attribute.name, specification.name)
        elif action == GARequest.ACTION_UPDATE:
            message = "Updated attribute %s in specification %s" % (attribute.name, specification.name)
        elif action == GARequest.ACTION_DELETE:
            message = "Deleted attribute %s from specification %s" % (attribute.name, specification.name)

        self._github_operations_controller.commit_specification(repository=response.data,
                                                                specification=specification,
                                                                commit_message=message,
                                                                session_username=session_username)
