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

logger = logging.getLogger('specsdirector.plugins.logic.abstracts')


class SDAbstractLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name=' abstracts logic', version=1.0, identifier="specsdirector.plugins.logic.abstracts",
                                subscriptions={
                                    "abstract": [GARequest.ACTION_DELETE, GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE, GARequest.ACTION_ASSIGN]
                                })

    def did_register(self):
        """
        """
        self._old_names = {}
        self._sdk = GASDKLibrary().get_sdk('default')
        self._storage_controller = self.core_controller.storage_controller
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def _check_valid_name(self, repository, abstract, context):
        """
        """
        if abstract.name[0] != '@':
            abstract.name = '@%s' % abstract.name

        if abstract.name[-5:] != '.spec':
            abstract.name = '%s.spec' % abstract.name

        response = self._storage_controller.get_all(user_identifier=context.session.root_object.id, parent=repository, resource_name=abstract.rest_name, filter='name == "%s"' % abstract.name)

        if response.count and response.data[0].id != abstract.id:
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Duplicate Name', description='Another abstract exists with the name %s' % abstract.name, property_name='name'))
            return False

        if not abstract.name or not len(abstract.name) or abstract.name == '.spec':
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute name is mandatory.', property_name='name'))
            return False

        return True

    def will_perform_create(self, context):
        """
        """
        repository = context.parent_object
        abstract = context.object

        self._check_valid_name(repository=repository, abstract=abstract, context=context)

        return context

    def will_perform_update(self, context):
        """
        """
        repository = context.parent_object
        abstract = context.object

        if not self._check_valid_name(repository=repository, abstract=abstract, context=context):
            return context

        response = self._storage_controller.get(user_identifier=context.session.root_object.id, resource_name=self._sdk.SDAbstract.rest_name, identifier=abstract.id)

        if response.data and response.data.name != abstract.name:
            self._old_names[context.request.uuid] = response.data.name

        return context

    def did_perform_create(self, context):
        """
        """
        abstract = context.object
        repository = context.parent_object
        session_username = context.session.root_object.id

        self._github_operations_controller.commit_specification(repository=repository,
                                                                specification=abstract,
                                                                commit_message="Added abstract %s" % abstract.name,
                                                                session_username=session_username)
        return context

    def did_perform_update(self, context):
        """
        """
        abstract = context.object
        repository = context.parent_object
        session_username = context.session.root_object.id

        if context.request.uuid in self._old_names:
            old_name = self._old_names[context.request.uuid]
            del self._old_names[context.request.uuid]

            self._github_operations_controller.rename_specification(repository=repository,
                                                                    specification=abstract,
                                                                    old_name=old_name,
                                                                    commit_message="Renamed abstract from %s to %s" % (old_name, abstract.name),
                                                                    session_username=session_username)
        else:
            self._github_operations_controller.commit_specification(repository=repository,
                                                                    specification=abstract,
                                                                    commit_message="Updated abstract %s" % abstract.name,
                                                                    session_username=session_username)
        return context

    def did_perform_delete(self, context):
        """
        """
        abstract = context.object
        repository = context.parent_object
        session_username = context.session.root_object.id

        self._github_operations_controller.delete_specification(repository=repository,
                                                                specification=abstract,
                                                                commit_message="Deleted  abstract %s" % abstract.name,
                                                                session_username=session_username)
        return context

    def did_perform_assign(self, context):
        """
        """
        specification = context.parent_object
        session_username = context.session.root_object.id

        response = self._storage_controller.get(user_identifier=context.session.root_object.id, resource_name=specification.parent_type, identifier=specification.parent_id)

        self._github_operations_controller.commit_specification(repository=response.data,
                                                                specification=specification,
                                                                commit_message="Updated extensions for specification %s" % specification.name,
                                                                session_username=session_username)
        return context
