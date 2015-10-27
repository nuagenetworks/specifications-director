import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.repositories')

class SDRepositoryLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='repositories logic', version=1.0, identifier="specsdirector.plugins.logic.repositories",
                                subscriptions={
                                    "repository": [GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._sdk = SDKLibrary().get_sdk('default')

    def check_perform_write(self, context):
        """
        """
        repository = context.object

        if not repository.name or not len(repository.name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute name is mandatory.', property_name='name'))

        if not repository.url or not len(repository.url):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute url is mandatory.', property_name='url'))

        if not repository.password or not len(repository.password):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute password is mandatory.', property_name='password'))

        if not repository.organization or not len(repository.organization):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute organization is mandatory.', property_name='organization'))

        if not repository.repository or not len(repository.repository):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute repository is mandatory.', property_name='repository'))

        if not repository.branch or not len(repository.branch):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute branch is mandatory.', property_name='branch'))

        if not repository.path or not len(repository.path):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute path is mandatory.', property_name='path'))

        return context
