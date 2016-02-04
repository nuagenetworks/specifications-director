import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import GASDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.tokens')

class SDTokenLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='token logic', version=1.0, identifier="specsdirector.plugins.logic.tokens",
                                subscriptions={
                                    "token": [GARequest.ACTION_DELETE, GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._sdk = GASDKLibrary().get_sdk('default')
        self._storage_controller = self.core_controller.storage_controller
        self._push_controller = self.core_controller.push_controller

    def will_perform_delete(self, context):
        """
        """
        token            = context.object
        session_username = context.session.root_object.id
        events           = []

        response = self._storage_controller.get_all(user_identifier=session_username,
                                                    resource_name=self._sdk.SDRepository.rest_name,
                                                    parent=None,
                                                    filter="associatedTokenID == '%s'" % token.id)

        if response.count:
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Token in use', description='This token is in used.'))

        return context

    def did_perform_update(self, context):
        """
        """
        token            = context.object
        session_username = context.session.root_object.id
        events           = []

        response = self._storage_controller.get_all(user_identifier=session_username,
                                                    resource_name=self._sdk.SDRepository.rest_name,
                                                    parent=None,
                                                    filter="associatedTokenID == '%s'" % token.id)

        for repository in response.data:
            repository.status = 'NEEDS_PULL'
            self._storage_controller.update(user_identifier=session_username, resource=repository);
            events.append(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=repository))

        if len(events):
            self._push_controller.push_events(events=events)

        return context