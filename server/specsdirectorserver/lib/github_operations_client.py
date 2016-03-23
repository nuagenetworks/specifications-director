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

import msgpack
from garuda.core.models import GAController


class SDGitHubOperationsClient(GAController):

    def __init__(self, core_controller):
        """
        """
        super(SDGitHubOperationsClient, self).__init__(core_controller=core_controller)

    @classmethod
    def identifier(cls):
        """
        """
        return 'sd.controller.githuboperations.client'

    def checkout_repository(self, repository, job, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'checkout_repository',
            'repository': repository.to_dict(),
            'job': job.to_dict()}))

    def commit_specification(self, repository, specification, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'commit_specification',
            'repository': repository.to_dict(),
            'specification': specification.to_dict(),
            'specification_type': specification.rest_name,
            'commit_message': commit_message}))

    def rename_specification(self, repository, specification, old_name, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'rename_specification',
            'repository': repository.to_dict(),
            'specification': specification.to_dict(),
            'specification_type': specification.rest_name,
            'old_name': old_name,
            'commit_message': commit_message}))

    def delete_specification(self, repository, specification, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'delete_specification',
            'repository': repository.to_dict(),
            'specification': specification.to_dict(),
            'specification_type': specification.rest_name,
            'commit_message': commit_message}))

    def commit_apiinfo(self, repository, apiinfo, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'commit_apiinfo',
            'repository': repository.to_dict(),
            'apiinfo': apiinfo.to_dict(),
            'commit_message': commit_message}))

    def commit_monolitheconfig(self, repository, monolitheconfig, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'commit_monolitheconfig',
            'repository': repository.to_dict(),
            'monolitheconfig': monolitheconfig.to_dict(),
            'commit_message': commit_message}))

    def merge_upstream_master(self, repository, job, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'merge_upstream_master',
            'repository': repository.to_dict(),
            'job': job.to_dict(),
            'commit_message': commit_message}))
