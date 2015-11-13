import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import GASDKLibrary, GAThreadManager

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
        self._sdk                          = GASDKLibrary().get_sdk('default')
        self._push_controller              = self.core_controller.push_controller
        self._storage_controller           = self.core_controller.storage_controller
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def will_perform_write(self, context):
        """
        """
        job          = context.object
        job.status   = 'RUNNING'
        job.progress = 0.0

        return context

    def did_perform_write(self, context):
        """
        """
        job        = context.object
        repository = context.parent_object

        if job.command == 'pull':
            self._github_operations_controller.checkout_repository(repository=repository, job=job, session_username=context.session.root_object.id)

        return context
