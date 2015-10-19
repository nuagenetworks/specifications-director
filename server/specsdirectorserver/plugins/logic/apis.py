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

        self._allows_create = None
        self._allows_delete = None
        self._allows_get = None
        self._allows_update = None
        self._associated_specification_id = None
        self._deprecated = None
        self._issues = None
        self._path = None
        self._relationship = None

    def preprocess_write(self, context):
        """
        """
        sdk = SDKLibrary().get_sdk('default')
        api = context.object

        specification_id = api.associated_specification_id
        specification = self.core_controller.storage_controller.get(resource_name=sdk.SDSpecification.rest_name, identifier=specification_id)

        associated_specification_id = context.request.resources[0].value if context.request.action == GARequest.ACTION_CREATE else api.parent_id
        associated_specification = self.core_controller.storage_controller.get(resource_name=sdk.SDSpecification.rest_name, identifier=associated_specification_id)

        remote_resource = associated_specification.object_resource_name if associated_specification and associated_specification.object_resource_name else '<abstract>'

        if api.rest_name == sdk.SDParentAPI.rest_name:
            api.path = '/%s/id/%s' % (associated_specification.object_resource_name, remote_resource)
            childAPI = sdk.SDChildAPI(data=api.to_dict())
            childAPI.associated_specification_id = specification_id
            childAPI.path = '/%s/id/%s' % (remote_resource, associated_specification.object_resource_name)
            self.core_controller.storage_controller.create(childAPI, associated_specification)

        elif api.rest_name == sdk.SDChildAPI.rest_name:
            api.path = '/%s/id/%s' % (remote_resource, associated_specification.object_resource_name)
            parentAPI = sdk.SDChildAPI(data=api.to_dict())
            parentAPI.associated_specification_id = specification_id
            parentAPI.path = '/%s/id/%s' % (associated_specification.object_resource_name, remote_resource)
            self.core_controller.storage_controller.create(parentAPI, associated_specification)


        return context