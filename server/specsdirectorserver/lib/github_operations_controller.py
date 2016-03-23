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

from monolithe.specifications import RepositoryManager
from garuda.core.models import GAController, GAPushEvent, GARequest
from garuda.core.lib import GASDKLibrary

from exporter import SDSpecificationExporter
from importer import SDSpecificationImporter


class SDGitHubOperationsController(GAController):

    def __init__(self, core_controller):
        """
        """
        super(SDGitHubOperationsController, self).__init__(core_controller=core_controller)

        self._storage_controller = None
        self._push_controller = None
        self._sdk = None

    @classmethod
    def identifier(cls):
        """
        """
        return 'sd.controller.githuboperations'

    def ready(self):
        """
        """
        self._sdk = GASDKLibrary().get_sdk('default')
        self._storage_controller = self.core_controller.storage_controller
        self._push_controller = self.core_controller.push_controller
        self._specification_exporter = SDSpecificationExporter(storage_controller=self._storage_controller, push_controller=self._push_controller, sdk=self._sdk)
        self._specification_importer = SDSpecificationImporter(storage_controller=self._storage_controller, push_controller=self._push_controller, sdk=self._sdk)

        self.subscribe(channel='github-operation:new', handler=self._on_github_operation)

    def start(self):
        """
        """
        self.start_listening_to_events()

    def stop(self):
        """
        """
        self.stop_listening_to_events()

    # PRIVATES

    def _on_github_operation(self, data):
        """
        """

        try:
            info = msgpack.unpackb(data)
            action = info['action']
            garuda_uuid = info['garuda_uuid']
            session_username = info['session_username']

            # let initiator handle the request
            if garuda_uuid != self.core_controller.garuda_uuid:
                return

            repository = self._sdk.SDRepository(data=info['repository'])

            if action == 'checkout_repository':

                job = self._sdk.SDJob(data=info['job'])

                self._peform_checkout_repository(repository=repository,
                                                 job=job,
                                                 session_username=session_username)

            elif action == 'commit_specification':

                klass = self._sdk.SDSpecification if info['specification_type'] == self._sdk.SDSpecification.rest_name else self._sdk.SDAbstract

                specification = klass(data=info['specification'])

                self._perform_commit_specification(repository=repository,
                                                   specification=specification,
                                                   commit_message=info['commit_message'],
                                                   session_username=session_username)

            elif action == 'rename_specification':

                klass = self._sdk.SDSpecification if info['specification_type'] == self._sdk.SDSpecification.rest_name else self._sdk.SDAbstract

                specification = klass(data=info['specification'])

                self._perform_rename_specification(repository=repository,
                                                   specification=specification,
                                                   old_name=info['old_name'],
                                                   commit_message=info['commit_message'],
                                                   session_username=session_username)

            elif action == 'delete_specification':

                klass = self._sdk.SDSpecification if info['specification_type'] == self._sdk.SDSpecification.rest_name else self._sdk.SDAbstract
                specification = klass(data=info['specification'])

                self._perform_delete_specification(repository=repository,
                                                   specification=specification,
                                                   commit_message=info['commit_message'],
                                                   session_username=session_username)

            elif action == 'commit_apiinfo':

                apiinfo = self._sdk.SDAPIInfo(data=info['apiinfo'])

                self._perform_commit_apiinfo(repository=repository,
                                             apiinfo=apiinfo,
                                             commit_message=info['commit_message'],
                                             session_username=session_username)

            elif action == 'commit_monolitheconfig':

                monolitheconfig = self._sdk.SDMonolitheConfig(data=info['monolitheconfig'])

                self._perform_commit_monolitheconfig(repository=repository,
                                                     monolitheconfig=monolitheconfig,
                                                     commit_message=info['commit_message'],
                                                     session_username=session_username)

            elif action == 'merge_upstream_master':

                job = self._sdk.SDJob(data=info['job'])

                self._perform_merge_upstream_master(repository=repository,
                                                    job=job,
                                                    commit_message=info['commit_message'],
                                                    session_username=session_username)

        except Exception as ex:
            print "Exception while executing git operation: %s" % ex

    def _peform_checkout_repository(self, repository, job, session_username):
        """
        """
        repository.status = 'PULLING'
        self._storage_controller.update(user_identifier=session_username, resource=repository)
        self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=repository)])

        try:
            manager = self._get_repository_manager_for_repository(repository=repository, session_username=session_username)

            self._specification_importer.clean_repository(repository=repository, session_username=session_username)
            self._specification_importer.import_repository_info(repository=repository, manager=manager, session_username=session_username)
            self._specification_importer.import_apiinfo(repository=repository, manager=manager, session_username=session_username)
            self._specification_importer.import_abstracts(repository=repository, manager=manager, session_username=session_username)
            self._specification_importer.import_specifications(repository=repository, manager=manager, session_username=session_username)
            self._specification_importer.import_monolitheconfig(repository=repository, manager=manager, session_username=session_username)

            job.progress = 1.0
            job.status = 'SUCCESS'

            repository.status = 'READY'

        except Exception as ex:

            job.progress = 1.0
            job.status = 'FAILED'
            job.result = 'Unable to pull repository.\n\nReason:\n%s' % ex

            repository.status = 'ERROR'

        finally:

            self._storage_controller.update(user_identifier=session_username, resource=job)
            self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=job)])

            self._storage_controller.update(user_identifier=session_username, resource=repository)
            self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=repository)])

    def _perform_merge_upstream_master(self, repository, job, commit_message, session_username):
        """
        """
        repository.status = 'MERGING'
        self._storage_controller.update(user_identifier=session_username, resource=repository)
        self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=repository)])

        try:

            manager = self._get_repository_manager_for_repository(repository=repository, session_username=session_username)
            manager.merge_upstream_master(local_branch=repository.branch,
                                          upstream_branch="master",
                                          commit_message="Merged upstream master branch")
            job.progress = 1.0
            job.status = 'SUCCESS'

            repository.status = 'NEEDS_PULL'

        except Exception as ex:

            job.progress = 1.0
            job.status = 'FAILED'
            job.result = 'Unable to merge repository.\n\nReason:\n%s' % ex

            repository.status = 'ERROR'

        finally:

            self._storage_controller.update(user_identifier=session_username, resource=job)
            self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=job)])

            self._storage_controller.update(user_identifier=session_username, resource=repository)
            self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=repository)])

    def _perform_commit_specification(self, repository, specification, commit_message, session_username):
        """
        """
        manager = self._get_repository_manager_for_repository(repository=repository, session_username=session_username)
        mono_spec = self._specification_exporter.export_specification(specification=specification, session_username=session_username)

        self._set_specification_syncing(specification=specification, syncing=True, session_username=session_username)
        manager.save_specification(specification=mono_spec, message=commit_message, branch=repository.branch)
        self._set_specification_syncing(specification=specification, syncing=False, session_username=session_username)

    def _perform_rename_specification(self, repository, specification, old_name, commit_message, session_username):
        """
        """
        manager = self._get_repository_manager_for_repository(repository=repository, session_username=session_username)
        mono_spec = self._specification_exporter.export_specification(specification=specification, session_username=session_username)

        self._set_specification_syncing(specification=specification, syncing=True, session_username=session_username)
        manager.rename_specification(specification=mono_spec, old_name=old_name, message=commit_message, branch=repository.branch)
        self._set_specification_syncing(specification=specification, syncing=False, session_username=session_username)

    def _perform_delete_specification(self, repository, specification, commit_message, session_username):
        """
        """
        manager = self._get_repository_manager_for_repository(repository=repository, session_username=session_username)
        mono_spec = self._specification_exporter.export_specification(specification=specification, session_username=session_username)

        manager.delete_specification(specification=mono_spec, message=commit_message, branch=repository.branch)

    def _perform_commit_apiinfo(self, repository, apiinfo, commit_message, session_username):
        """
        """
        manager = self._get_repository_manager_for_repository(repository=repository, session_username=session_username)

        manager.save_apiinfo(version=apiinfo.version,
                             root_api=apiinfo.root,
                             prefix=apiinfo.prefix,
                             message=commit_message,
                             branch=repository.branch)

    def _perform_commit_monolitheconfig(self, repository, monolitheconfig, commit_message, session_username):
        """
        """
        manager = self._get_repository_manager_for_repository(repository=repository, session_username=session_username)
        parser = self._specification_exporter.export_monolithe_config(monolitheconfig=monolitheconfig)
        manager.save_monolithe_config(monolithe_config_parser=parser,
                                      message=commit_message,
                                      branch=repository.branch)

    def _set_specification_syncing(self, specification, syncing, session_username):
        """
        """
        specification.syncing = syncing
        self._storage_controller.update(user_identifier=session_username, resource=specification)
        self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=specification)])

    def _get_repository_manager_for_repository(self, repository, session_username):
        """
        """
        response = self._storage_controller.get(user_identifier=session_username, resource_name=self._sdk.SDToken.rest_name, identifier=repository.associated_token_id)
        github_token = response.data.value

        repo_manager = RepositoryManager(monolithe_config=None,
                                         api_url=repository.url,
                                         login_or_token=github_token,
                                         password=None,
                                         organization=repository.organization,
                                         repository=repository.repository,
                                         repository_path=repository.path)
        return repo_manager
