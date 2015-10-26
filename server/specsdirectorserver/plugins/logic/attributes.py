import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.attributes')


class SDAttributeLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='attributes logic', version=1.0, identifier="specsdirector.plugins.logic.attributes",
                                subscriptions={
                                    "attribute": [GARequest.ACTION_DELETE, GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._sdk = SDKLibrary().get_sdk('default')
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def check_perform_write(self, context):
        """
        """
        action = context.request.action

        if action == GARequest.ACTION_CREATE:
            self._check_unique_name(context)

        elif action == GARequest.ACTION_UPDATE:
            self._check_unique_name(context)

        return context

    def did_perform_write(self, context):
        """
        """
        self._commit_specification_change(context)
        return context


    ## Processing

    def _commit_specification_change(self, context):
        """
        """
        action        = context.request.action
        attribute     = context.object
        specification = context.parent_object
        repository    = self.core_controller.storage_controller.get(resource_name=self._sdk.SDRepository.rest_name, identifier=specification.parent_id)

        if action == GARequest.ACTION_CREATE:
            message = "Added attribute %s to specification %s" % (attribute.name, specification.name)
        elif action == GARequest.ACTION_UPDATE:
            message = "Updated attribute %s in specification %s" % (attribute.name, specification.name)
        elif action == GARequest.ACTION_DELETE:
            message = "Deleted attribute %s from specification %s" % (attribute.name, specification.name)

        self._github_operations_controller.commit_specification(repository=repository, specification=specification, commit_message=message)

    def _check_unique_name(self, context):
        """
        """
        specification = context.parent_object
        attribute = context.object

        objects, count = self.core_controller.storage_controller.get_all(parent=specification, resource_name=self._sdk.SDAttribute.rest_name, filter='name == %s' % attribute.name)

        if count and objects[0].id != attribute.id:
            context.report_error(GAError(   type=GAError.TYPE_CONFLICT,
                                            title='Duplicate Name',
                                            description='Another attribute exists with the name %s' % attribute.name,
                                            property_name='name'))
