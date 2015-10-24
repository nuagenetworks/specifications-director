import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.specifications')

class SDSpecificationLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='specifications logic', version=1.0, identifier="specsdirector.plugins.logic.specifications",
                                subscriptions={
                                    "specification": [GARequest.ACTION_DELETE, GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE, GARequest.ACTION_ASSIGN],
                                    "abstract": [GARequest.ACTION_DELETE, GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE, GARequest.ACTION_ASSIGN]
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

        repository    = context.parent_object
        specification = context.object

        objects, count = self._storage_controller.get_all(  parent=repository,
                                                            resource_name=specification.rest_name,
                                                            filter='name == %s' % specification.name)

        if count and objects[0].id != specification.id:
            context.report_error(GAError(   type=GAError.TYPE_CONFLICT,
                                            title='Duplicate Name',
                                            description='Another specification exists with the name %s' % specification.name,
                                            property_name='name'))
        return context

    def preprocess_write(self, context):
        """
        """
        specification        = context.object
        action               = context.request.action
        stored_specification = self._storage_controller.get(resource_name=self._sdk.SDSpecification.rest_name, identifier=specification.id)

        if action == GARequest.ACTION_UPDATE and stored_specification and stored_specification.name != specification.name:
            self._old_names[context.request.uuid] = stored_specification.name

        return context

    def did_perform_write(self, context):
        """
        """
        specification        = context.object
        repository           = context.parent_object
        action               = context.request.action

        if action == GARequest.ACTION_CREATE:
            self._github_operations_controller.commit_specification(repository=repository,
                                                                    specification=specification,
                                                                    commit_message="Created specification %s" % specification.name)

        elif action == GARequest.ACTION_UPDATE:

            if context.request.uuid in self._old_names:
                old_name = self._old_names[context.request.uuid]
                del self._old_names[context.request.uuid]

                self._github_operations_controller.rename_specification(repository=repository,
                                                                        specification=specification,
                                                                        old_name=old_name,
                                                                        commit_message="Renaming specification from %s to %s" % (old_name, specification.name))
            else:
                self._github_operations_controller.commit_specification(repository=repository,
                                                                        specification=specification,
                                                                        commit_message="Update specification %s" % specification.name)

        elif action == GARequest.ACTION_DELETE:
            self._github_operations_controller.delete_specification(repository=repository,
                                                                    specification=specification,
                                                                    commit_message="Delete specification %s" % specification.name)

        return context