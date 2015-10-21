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
        return GAPluginManifest(name='apis logic', version=1.0, identifier="specsdirector.plugins.logic.apis",
                                subscriptions={
                                    "childapi": [GARequest.ACTION_READALL, GARequest.ACTION_READ]
                                })

    def preprocess_readall(self, context):
        """
        """
        for api in context.objects: self._update_path(specification=context.parent_object, api=api)
        return context

    def preprocess_read(self, context):
        """
        """
        self._update_path(specification=context.parent_object, api=context.object)
        return context

    def _update_path(self, specification, api):
        """
        """
        sdk = SDKLibrary().get_sdk('default')

        associated_specification = self.core_controller.storage_controller.get(resource_name=sdk.SDSpecification.rest_name, identifier=api.associated_specification_id)

        local_resource_name = specification.object_resource_name
        associated_resource_name = associated_specification.object_resource_name

        if api.parent_type == sdk.SDAbstract.rest_name and not local_resource_name:
            local_resource_name = '[[resource_name]]'

        if api.relationship == 'root':
            api.path = '/%s' % associated_resource_name
        else:
            api.path = '/%s/id/%s' % (local_resource_name, associated_resource_name)

