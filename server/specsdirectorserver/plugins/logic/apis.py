import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import GASDKLibrary

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
        self._sdk = GASDKLibrary().get_sdk('default')
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def will_perform_write(self, context):
        """
        """
        if context.request.action in (GARequest.ACTION_DELETE):
            return context

        api = context.object

        if not api.associated_specification_id or not len(api.associated_specification_id):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute associatedSpecificationID is mandatory.', property_name='associatedSpecificationID'))

        self._update_path(specification=context.parent_object, api=api, session_username=context.session.root_object.id)

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
        session_username = context.session.root_object.id

        response = self.core_controller.storage_controller.get(user_identifier=context.session.root_object.id, resource_name=self._sdk.SDRepository.rest_name, identifier=specification.parent_id)

        if action == GARequest.ACTION_CREATE:
            message = "Added child specification api to specification %s" % (specification.name)
        elif action == GARequest.ACTION_UPDATE:
            message = "Updated child specification api in specification %s" % (specification.name)
        elif action == GARequest.ACTION_DELETE:
            message = "Deleted child specification api from specification %s" % (specification.name)

        self._github_operations_controller.commit_specification(repository=response.data, specification=specification, commit_message=message, session_username=session_username)

    def _update_path(self, specification, api, session_username):
        """
        """
        sdk = GASDKLibrary().get_sdk('default')

        response = self.core_controller.storage_controller.get(user_identifier=session_username, resource_name=self._sdk.SDSpecification.rest_name, identifier=api.associated_specification_id)

        if not response.data:
            return

        associated_resource_name = response.data.object_resource_name

        if specification.rest_name == self._sdk.SDAbstract.rest_name:
            local_resource_name = '<abstract>'
        else:
            local_resource_name = specification.object_resource_name

        if api.relationship == 'root':
            api.path = '/%s' % associated_resource_name
        else:
            api.path = '/%s/id/%s' % (local_resource_name, associated_resource_name)


