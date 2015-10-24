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

        job.status = 'RUNNING'
        job.progress = 0.0

        if job.command == 'pull':
            self._github_operations_controller.checkout_repository(repository=repository, job=job)

        return context
