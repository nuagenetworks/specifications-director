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
                                    "parentapi": [GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE, GARequest.ACTION_DELETE]
                                })

    def preprocess_write(self, context):
        """
        """
        sdk = SDKLibrary().get_sdk('default')
        specification = context.parent_object
        parent_api = context.object

        if not parent_api.associated_specification_id and parent_api.relationship == 'root':
            apiinfo = self.core_controller.storage_controller.get(resource_name=sdk.SDAPIInfo.rest_name, filter='parentID == %s' % specification.parent_id)
            root_specification = self.core_controller.storage_controller.get(resource_name=sdk.SDSpecification.rest_name, filter='name == %s.spec' % apiinfo.root)
            parent_api.associated_specification_id = root_specification.id

        return context

    def did_perform_write(self, context):
        """
        """
        sdk = SDKLibrary().get_sdk('default')
        parent_api = context.object

        if context.request.action == GARequest.ACTION_CREATE:
            self._create_associated_child_api(parent_api, sdk)

        elif context.request.action == GARequest.ACTION_UPDATE:
            self._delete_associated_child_api(parent_api, sdk)
            self._create_associated_child_api(parent_api, sdk)

        elif context.request.action == GARequest.ACTION_DELETE:
            self._delete_associated_child_api(parent_api, sdk)

        return context

    ## Utilities

    def _create_associated_child_api(self, parent_api, sdk):
        """
        """
        child_api = sdk.SDChildAPI(data=parent_api.to_dict())
        child_api.associated_specification_id = parent_api.parent_id
        child_api.associated_parent_apiid = parent_api.id

        associated_specification = sdk.SDSpecification(id=parent_api.associated_specification_id)
        self.core_controller.storage_controller.create(child_api, associated_specification)

    def _delete_associated_child_api(self, parent_api, sdk):
        """
        """
        associated_child_api = self.core_controller.storage_controller.get(resource_name=sdk.SDChildAPI.rest_name, filter='associatedParentAPIID == %s' % parent_api.id)
        self.core_controller.storage_controller.delete(resource=associated_child_api, cascade=True)

