import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.abstracts')

class SDAbstractLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name=' abstracts logic', version=1.0, identifier="specsdirector.plugins.logic.abstracts",
                                subscriptions={
                                    "abstract": [GARequest.ACTION_DELETE, GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._old_names = {};
        self._sdk = SDKLibrary().get_sdk('default')
        self._storage_controller = self.core_controller.storage_controller
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def check_perform_write(self, context):
        """
        """
        if context.request.action == GARequest.ACTION_DELETE:
            return context

        if context.request.action == GARequest.ACTION_ASSIGN:
            return context

        repository = context.parent_object
        abstract   = context.object

        objects, count = self._storage_controller.get_all(  parent=repository,
                                                            resource_name=abstract.rest_name,
                                                            filter='name == %s' % abstract.name)

        if count and objects[0].id !=  abstract.id:
            context.report_error(GAError(   type=GAError.TYPE_CONFLICT,
                                            title='Duplicate Name',
                                            description='Another abstract exists with the name %s' % abstract.name,
                                            property_name='name'))
        return context

    def preprocess_write(self, context):
        """
        """
        abstract = context.object
        action   = context.request.action

        if action == GARequest.ACTION_UPDATE:

            stored_abstract = self._storage_controller.get(resource_name=self._sdk.SDAbstract.rest_name, identifier=abstract.id)

            if stored_abstract and stored_abstract.name !=  abstract.name:
                self._old_names[context.request.uuid] = stored_abstract.name

        return context

    def did_perform_write(self, context):
        """
        """
        action = context.request.action

        if action == GARequest.ACTION_CREATE:

            abstract   = context.object
            repository = context.parent_object

            self._github_operations_controller.commit_specification(repository=repository,
                                                                    specification=abstract,
                                                                    commit_message="Added abstract %s" % abstract.name)

        elif action == GARequest.ACTION_UPDATE:

            abstract   = context.object
            repository = context.parent_object

            if context.request.uuid in self._old_names:
                old_name = self._old_names[context.request.uuid]
                del self._old_names[context.request.uuid]

                self._github_operations_controller.rename_specification(repository=repository,
                                                                        specification=abstract,
                                                                        old_name=old_name,
                                                                        commit_message="Renamed abstract from %s to %s" % (old_name,  abstract.name))
            else:
                self._github_operations_controller.commit_specification(repository=repository,
                                                                        specification=abstract,
                                                                        commit_message="Updated abstract %s" % abstract.name)

        elif action == GARequest.ACTION_DELETE:

            abstract   = context.object
            repository = context.parent_object

            self._github_operations_controller.delete_specification(repository=repository,
                                                                    specification=abstract,
                                                                    commit_message="Deleted  abstract %s" % abstract.name)
        return context