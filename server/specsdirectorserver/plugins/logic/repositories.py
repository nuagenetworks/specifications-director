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
                                    "repository": [GARequest.ACTION_CREATE,
                                                   GARequest.ACTION_UPDATE,
                                                   GARequest.ACTION_READ,
                                                   GARequest.ACTION_READALL,
                                                   GARequest.ACTION_DELETE]
                                })

    def did_register(self):
        """
        """
        self._sdk = SDKLibrary().get_sdk('default')
        self._permissions_controller = self.core_controller.permissions_controller

    def preprocess_readall(self, context):
        """
        """
        final_repo_list = []

        for repository in context.objects:
            if self._permissions_controller.has_permission(resource=context.session.root_object.user_name, target=repository, permission='all'):
                final_repo_list.append(repository)

        context.objects = final_repo_list

        return context

    def check_perform_read(self, context):
        """
        """
        user_name = context.session.root_object.user_name

        if not context.object.owner == user_name and not self._permissions_controller.has_permission(resource=user_name, target=context.object, permission='read'):
            context.add_error(GAError(type=GAError.TYPE_UNAUTHORIZED, title='Not Authorized', description='You do not have permission to read this resource.'))

        return context

    def check_perform_write(self, context):
        """
        """

        if context.request.action in (GARequest.ACTION_DELETE):
            return context

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

    def preprocess_write(self, context):
        """
        """

        if context.request.action in (GARequest.ACTION_DELETE):
            return context

        context.object.valid = False
        context.object.owner = context.request.username

        return context

    def did_perform_write(self, context):
        """
        """

        if context.request.action == GARequest.ACTION_CREATE:
            self._permissions_controller.create_permission(resource=context.request.username, target=context.object, permission='all')


        # TODO: if I remove the permission here as I should, the push triggered operation won't work as the user
        # won't have any permissions anymore. We need to figure out a way to make this work.

        # elif context.request.action == GARequest.ACTION_DELETE:
        #     self._permissions_controller.remove_permission(resource=context.request.username, target=context.object, permission='all')

        return context

