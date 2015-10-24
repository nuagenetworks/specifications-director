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
                                    "specification": [GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE, GARequest.ACTION_ASSIGN],
                                    "abstract": [GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._sdk = SDKLibrary().get_sdk('default')
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations')

    def check_perform_write(self, context):
        """
        """
        repository    = context.parent_object
        specification = context.object

        objects, count = self.core_controller.storage_controller.get_all(parent=repository,
                                                                         resource_name=specification.rest_name,
                                                                         filter='name == %s' % specification.name)

        if count and objects[0].id != specification.id:
            context.report_error(GAError(   type=GAError.TYPE_CONFLICT,
                                            title='Duplicate Name',
                                            description='Another specification exists with the name %s' % specification.name,
                                            property_name='name'))
        return context

    def did_perform_write(self, context):
        """
        """
        specification = context.object
        repository    = context.parent_object

        self._github_operations_controller.commit_specification(repository=repository, specification=specification, commit_message="Update specification model %s" % specification.name)

        return context