import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.apis')

class SDAPILogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='apis logic', version=1.0, identifier="specsdirector.plugins.logic.apis",
                                subscriptions={
                                    "childapi": [   GARequest.ACTION_READALL,
                                                    GARequest.ACTION_READ,
                                                    GARequest.ACTION_UPDATE,
                                                    GARequest.ACTION_CREATE,
                                                    GARequest.ACTION_DELETE]
                                })

    def did_register(self):
        """
        """
        self._sdk = SDKLibrary().get_sdk('default')
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def preprocess_readall(self, context):
        """
        """
        for api in context.objects:
            self._update_path(specification=context.parent_object, api=api)

        return context

    def preprocess_read(self, context):
        """
        """
        self._update_path(specification=context.parent_object, api=context.object)

        return context

    def did_perform_write(self, context):
        """
        """
        self._commit_specification_change(context)
        return context

    ## processing

    def _commit_specification_change(self, context):
        """
        """
        specification = context.parent_object
        repository    = self.core_controller.storage_controller.get(resource_name=self._sdk.SDRepository.rest_name, identifier=specification.parent_id)

        self._github_operations_controller.commit_specification(repository=repository, specification=specification, commit_message="Update child api %s" % context.object.path)

    def _update_path(self, specification, api):
        """
        """
        sdk = SDKLibrary().get_sdk('default')

        associated_specification = self.core_controller.storage_controller.get(resource_name=self._sdk.SDSpecification.rest_name, identifier=api.associated_specification_id)
        local_resource_name      = specification.object_resource_name
        associated_resource_name = associated_specification.object_resource_name

        if api.parent_type == self._sdk.SDAbstract.rest_name and not local_resource_name:
            local_resource_name = '[[resource_name]]'

        if api.relationship == 'root':
            api.path = '/%s' % associated_resource_name
        else:
            api.path = '/%s/id/%s' % (local_resource_name, associated_resource_name)

