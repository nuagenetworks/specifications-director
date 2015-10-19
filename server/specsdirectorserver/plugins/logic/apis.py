import logging
import base64
import json

from github import Github
from monolithe.specifications import Specification, RepositoryManager
from monolithe.specifications.repositorymanager import MODE_NORMAL, MODE_RAW_SPECS, MODE_RAW_ABSTRACTS

from garuda.core.models import GAError, GAPluginManifest, GARequest
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
        return GAPluginManifest(name='apis logic',
                                version=1.0,
                                identifier="specsdirector.plugins.logic.apis",
                                subscriptions={
                                    "parentapi": [GARequest.ACTION_CREATE, GARequest.ACTION_DELETE, GARequest.ACTION_UPDATE]
                                })

    def preprocess_write(self, context):
        """
        """
        sdk = SDKLibrary().get_sdk('default')

        if context.request.action == GARequest.ACTION_CREATE:
            return self._update_parent_api_path(context, sdk)

        elif context.request.action == GARequest.ACTION_DELETE:
            return self._delete_associated_child_api(context, sdk)

        elif context.request.action == GARequest.ACTION_UPDATE:
            self._delete_associated_child_api(context, sdk)
            self._update_parent_api_path(context, sdk)
            self._create_associated_child_api(context, sdk)

        return context

    def did_perform_write(self, context):
        """
        """
        sdk = SDKLibrary().get_sdk('default')

        if context.request.action == GARequest.ACTION_CREATE:
            return self._create_associated_child_api(context, sdk)

        return context


    ## Utilities

    def _update_parent_api_path(self, context, sdk):
        """
        """
        parent_api = context.object

        specification_id = context.request.resources[0].value if context.request.action == GARequest.ACTION_CREATE else parent_api.parent_id
        specification = self.core_controller.storage_controller.get(resource_name=sdk.SDSpecification.rest_name, identifier=specification_id)

        associated_specification_id = parent_api.associated_specification_id
        associated_specification = self.core_controller.storage_controller.get(resource_name=sdk.SDSpecification.rest_name, identifier=associated_specification_id)

        remote_resource_name = associated_specification.object_resource_name if associated_specification and associated_specification.object_resource_name else '<abstract>'

        if parent_api.relationship == 'root':
            parent_api.path = '/%s' % (specification.object_resource_name)
        else:
            parent_api.path = '/%s/id/%s' % (remote_resource_name, specification.object_resource_name)

        return context

    def _delete_associated_child_api(self, context, sdk):
        """
        """
        parent_api = context.object

        associated_child_api = self.core_controller.storage_controller.get(resource_name=sdk.SDChildAPI.rest_name, filter='associatedParentAPIID == %s' % parent_api.id)
        self.core_controller.storage_controller.delete(resource=associated_child_api, cascade=True)

        return context

    def _create_associated_child_api(self, context, sdk):
        """
        """
        parent_api = context.object

        child_api = sdk.SDChildAPI(data=parent_api.to_dict())
        child_api.associated_specification_id = parent_api.parent_id
        child_api.associated_parent_apiid = parent_api.id

        associated_specification = sdk.SDSpecification(id=parent_api.associated_specification_id)
        self.core_controller.storage_controller.create(child_api, associated_specification)

        return context







