import logging
import json
from Queue import Queue

from monolithe.specifications import Specification, RepositoryManager, SpecificationAttribute, SpecificationAPI, RepositoryManager
from garuda.core.models import GAController, GAPushEvent, GARequest
from garuda.core.lib import ThreadManager, SDKLibrary

from exporter import SDSpecificationExporter
from importer import SDSpecificationImporter


class SDGitHubOperationsController(GAController):

    def __init__(self, core_controller, redis_conn):
        """
        """
        super(SDGitHubOperationsController, self).__init__(core_controller=core_controller, redis_conn=redis_conn)

        self._storage_controller  = None
        self._push_controller     = None
        self._sdk                 = None
        self._thread              = None
        self._repository_managers = {}
        self._operation_queue     = Queue()

    @classmethod
    def identifier(cls):
        """
        """
        return 'sd.controller.githuboperations'

    def ready(self):
        """
        """
        self._sdk                       = SDKLibrary().get_sdk('default')
        self._storage_controller        = self.core_controller.storage_controller
        self._push_controller           = self.core_controller.push_controller
        self._specification_exporter    = SDSpecificationExporter(storage_controller=self._storage_controller, push_controller=self._push_controller, sdk=self._sdk)
        self._specification_importer    = SDSpecificationImporter(storage_controller=self._storage_controller, push_controller=self._push_controller, sdk=self._sdk)

    def start(self):
        """
        """
        self._thread = ThreadManager.start_thread(self._listen_to_operations)

    def stop(self):
        """
        """
        ThreadManager.stop_thread(self._thread)

    def checkout_repository(self, repository, job):
        """
        """
        self._operation_queue.put({ 'action': 'checkout_repository',
                                    'repository': repository,
                                    'job': job})

    def commit_specification(self, repository, specification, commit_message):
        """
        """
        self._operation_queue.put({ 'action': 'commit_specification',
                                    'repository': repository,
                                    'specification': specification,
                                    'commit_message': commit_message})

    def create_specification(self, repository, specification, commit_message):
        """
        """
        self._operation_queue.put({ 'action': 'create_specification',
                                    'repository': repository,
                                    'specification': specification,
                                    'commit_message': commit_message})

    def delete_specification(self, repository, specification, commit_message):
        """
        """
        self._operation_queue.put({ 'action': 'delete_specification',
                                    'repository': repository,
                                    'specification': specification,
                                    'commit_message': commit_message})

    def commit_apiinfo(self, repository, apiinfo, commit_message):
        """
        """
        self._operation_queue.put({ 'action': 'commit_apiinfo',
                                    'repository': repository,
                                    'apiinfo': apiinfo,
                                    'commit_message': commit_message})

    ## PRIVATES

    def _listen_to_operations(self):
        """
        """
        while True:

            info = self._operation_queue.get()

            action     = info['action']
            repository = info['repository']

            if action == 'checkout_repository':

                self._peform_checkout_repository(repository=repository,
                                                 job=info['job'])

            elif action == 'commit_specification':

                self._perform_commit_specification(repository=repository,
                                                   specification=info['specification'],
                                                   commit_message=info['commit_message'])

            elif action == 'create_specification':

                self._perform_create_specification(repository=repository,
                                                   specification=info['specification'],
                                                   commit_message=info['commit_message'])

            elif action == 'delete_specification':

                self._perform_delete_specification(repository=repository,
                                                   specification=info['specification'],
                                                   commit_message=info['commit_message'])

            elif action == 'commit_apiinfo':

                self._perform_commit_apiinfo(repository=repository,
                                             apiinfo=info['apiinfo'],
                                             commit_message=info['commit_message'])


    def _peform_checkout_repository(self, repository, job):
        """
        """
        manager = self._get_repository_manager_for_repository(repository=repository)

        self._specification_importer.clean_repository(repository=repository)
        self._specification_importer.import_apiinfo(repository=repository, manager=manager)
        self._specification_importer.import_abstracts(repository=repository, manager=manager)
        self._specification_importer.import_specifications(repository=repository, manager=manager)

        job.progress = 1.0
        job.status = 'SUCCESS'
        self._storage_controller.update(job)
        self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=job)])

    def _perform_commit_specification(self, repository, specification, commit_message):
        """
        """
        manager = self._get_repository_manager_for_repository(repository=repository)
        mono_spec = self._specification_exporter.export_specification(specification=specification)

        self._set_specification_syncing(specification=specification, syncing=True)
        manager.save_specification(specification=mono_spec, message=commit_message, branch=repository.branch)
        self._set_specification_syncing(specification=specification, syncing=False)

    def _perform_create_specification(self, repository, job):
        """
        """
        manager = self._get_repository_manager_for_repository(repository=repository)
        mono_spec = self._specification_exporter.export_specification(specification=specification)

        manager.create_specification(specification=mono_spec, message=commit_message, branch=repository.branch)

    def _perform_delete_specification(self, repository, job):
        """
        """
        manager = self._get_repository_manager_for_repository(repository=repository)
        mono_spec = self._specification_exporter.export_specification(specification=specification)

        manager.delete_specification(specification=mono_spec, message=commit_message, branch=repository.branch)

    def _perform_commit_apiinfo(self, repository, apiinfo, commit_message):
        """
        """
        manager = self._get_repository_manager_for_repository(repository=repository)

        manager.save_apiinfo(   version=apiinfo.version,
                                root_api=apiinfo.root,
                                prefix=apiinfo.prefix,
                                message=commit_message,
                                branch=repository.branch)

    def _set_specification_syncing(self, specification, syncing):
        """
        """
        specification.syncing = syncing
        self._storage_controller.update(specification)
        self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=specification)])

    def _get_repository_manager_for_repository(self, repository):
        """
        """
        key = repository.id

        if key in self._repository_managers:
            return self._repository_managers[key];

        repo_manager = RepositoryManager( monolithe_config=None,
                                          api_url=repository.url,
                                          login_or_token=repository.password,
                                          password=None,
                                          organization=repository.organization,
                                          repository=repository.repository,
                                          repository_path=repository.path)

        self._repository_managers[key] = repo_manager

        return repo_manager