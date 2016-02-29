import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import GASDKLibrary

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
        self._sdk = GASDKLibrary().get_sdk('default')
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def will_perform_update(self, context):
        """
        """
        apiinfo = context.object

        if apiinfo.prefix[1] == '/':
            apiinfo.prefix = apiinfo.prefix[1:]

        if apiinfo.prefix[-1] == '/':
            apiinfo.prefix = apiinfo.prefix[:-1]

        if not apiinfo.version or not len(apiinfo.version):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute version is mandatory.', property_name='version'))

        try:
            float(apiinfo.version)
        except:
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Wrong attribute', description='Attribute version must be a float.', property_name='version'))

        if not apiinfo.root or not len(apiinfo.root):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute root is mandatory.', property_name='root'))

        if not apiinfo.prefix or not len(apiinfo.prefix):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute prefix is mandatory.', property_name='prefix'))

        return context

    def did_perform_update(self, context):
        """
        """
        apiinfo = context.object
        repository = context.parent_object
        session_username = context.session.root_object.id

        self._github_operations_controller.commit_apiinfo(repository=repository, apiinfo=apiinfo, commit_message="Updated api.info", session_username=session_username)

        return context
