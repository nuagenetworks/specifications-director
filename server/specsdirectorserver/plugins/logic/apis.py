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


    def check_perform_write(self, context):
        """
        """

        if context.request.action in (GARequest.ACTION_DELETE):
            return context

        api = context.object

        if not api.associated_specification_id or not len(api.associated_specification_id):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute associatedSpecificationID is mandatory.', property_name='associatedSpecificationID'))

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
        action        = context.request.action
        api           = context.object
        specification = context.parent_object
        repository    = self.core_controller.storage_controller.get(resource_name=self._sdk.SDRepository.rest_name, identifier=specification.parent_id)

        if action == GARequest.ACTION_CREATE:
            message = "Added child specification api to specification %s" % (specification.name)
        elif action == GARequest.ACTION_UPDATE:
            message = "Updated child specification api in specification %s" % (specification.name)
        elif action == GARequest.ACTION_DELETE:
            message = "Deleted child specification api from specification %s" % (specification.name)

        self._github_operations_controller.commit_specification(repository=repository, specification=specification, commit_message=message)

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

