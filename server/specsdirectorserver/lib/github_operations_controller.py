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
        self._specification_exporter    = SDSpecificationExporter(storage_controller=self._storage_controller, sdk=self._sdk)
        self._specification_importer    = SDSpecificationImporter(storage_controller=self._storage_controller, push_controller=self._push_controller, sdk=self._sdk)

    def start(self):
        """
        """
        self._thread = ThreadManager.start_thread(self._listen_to_operations)

    def stop(self):
        """
        """
        ThreadManager.stop_thread(self._thread)

    def enqueue_operation(self, action, repository, specification, commit_message):
        """
        """
        self._operation_queue.put((action, repository, specification, commit_message))


    def import_repository(self, repository):
        """
        """
        repo_manager = self._get_repository_manager_for_repository(repository=repository)

        self._specification_importer.import_apiinfo(repository=repository, manager=repo_manager)
        self._specification_importer.import_abstracts(repository=repository, manager=repo_manager)
        self._specification_importer.import_specifications(repository=repository, manager=repo_manager)


    ## PRIVATES

    def _listen_to_operations(self):
        """
        """
        while True:

            action, repository, specification, commit_message = self._operation_queue.get()

            repo_manager       = self._get_repository_manager_for_repository(repository=repository)
            mono_specification = self._specification_exporter.export_specification(repository=repository, specification=specification)

            specification.syncing = True
            self._storage_controller.update(specification)
            self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=specification)])

            repo_manager.save_specification(specification=mono_specification, message=commit_message, branch=repository.branch)

            specification.syncing = False
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