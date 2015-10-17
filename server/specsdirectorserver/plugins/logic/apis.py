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
        return GAPluginManifest(name='repository logic',
                                version=1.0,
                                identifier="specsdirector.plugins.logic.repository",
                                subscriptions={
                                    "childapi": [GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE],
                                    "parentapi": [GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE]
                                })

    def preprocess_write(self, context):
        """
        """
        sdk = SDKLibrary().get_sdk('default')
        api = context.object

        parent_specification_id = api.associated_specification_id
        parent_model = self.core_controller.storage_controller.get(resource_name=sdk.SDModel.rest_name, identifier=None, filter='parentID == %s' % parent_specification_id)

        associated_specification_id = context.request.resources[0].value if context.request.action == GARequest.ACTION_CREATE else api.parent_id
        associated_model = self.core_controller.storage_controller.get(resource_name=sdk.SDModel.rest_name, identifier=None, filter='parentID == %s' % associated_specification_id)

        remote_resource = associated_model.object_resource_name if associated_model and associated_model.object_resource_name else '<abstract>'

        if api.rest_name == sdk.SDParentAPI.rest_name:
            api.path = '/%s/id/%s' % (parent_model.object_resource_name, remote_resource)

        elif api.rest_name == sdk.SDChildAPI.rest_name:
            api.path = '/%s/id/%s' % (remote_resource, parent_model.object_resource_name)

        return context