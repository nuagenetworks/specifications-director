import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.specifications')

class SDAPIInfoLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='api logic', version=1.0, identifier="specsdirector.plugins.logic.apiinfos",
                                subscriptions={
                                    "apiinfo": [GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._sdk = SDKLibrary().get_sdk('default')
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def did_perform_write(self, context):
        """
        """
        apiinfo    = context.object
        repository = context.parent_object

        self._github_operations_controller.commit_apiinfo(repository=repository, apiinfo=apiinfo, commit_message="Update apiinfo")

        return context