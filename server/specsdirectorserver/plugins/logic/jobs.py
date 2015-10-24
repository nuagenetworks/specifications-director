import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary, ThreadManager

class SDJobLogicPlugin(GALogicPlugin):
    """

    """

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='job logic', version=1.0, identifier='specsdirector.plugins.logic.jobs',
                                subscriptions={
                                    'job': [GARequest.ACTION_CREATE]
                                })

    def did_register(self):
        """
        """
        self._sdk                          = SDKLibrary().get_sdk('default')
        self._push_controller              = self.core_controller.push_controller
        self._storage_controller           = self.core_controller.storage_controller
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations')

    def preprocess_write(self, context):
        """
        """
        job        = context.object
        repository = context.parent_object

        if job.command == 'pull':
            ThreadManager.start_thread(self._run_import, job=job, repository=repository)

        job.status = 'RUNNING'
        job.progress = 0.0
        return context

    def _run_import(self, job, repository):
        """
        """
        self._clean_repository(repository=repository)

        self._github_operations_controller.import_repository(repository=repository)

        job.progress = 1.0
        job.status = 'SUCCESS'
        self._storage_controller.update(job)
        self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=job)])


    def _clean_repository(self, repository):
        """
        """
        specifications, count = self._storage_controller.get_all(resource_name=self._sdk.SDSpecification.rest_name, parent=repository)
        if count:
            self._storage_controller.delete_multiple(resources=specifications, cascade=True)
            events = []
            for specification in specifications:
                events.append(GAPushEvent(action=GARequest.ACTION_DELETE, entity=specification))
            self._push_controller.push_events(events=events)

        abstracts, count = self._storage_controller.get_all(resource_name=self._sdk.SDAbstract.rest_name, parent=repository)
        if count:
            self._storage_controller.delete_multiple(resources=abstracts, cascade=True)
            events = []
            for asbtract in abstracts:
                events.append(GAPushEvent(action=GARequest.ACTION_DELETE, entity=asbtract))
            self._push_controller.push_events(events=events)

        apiinfos, count = self._storage_controller.get_all(resource_name=self._sdk.SDAPIInfo.rest_name, parent=repository)
        if count: self._storage_controller.delete_multiple(resources=apiinfos, cascade=True)
