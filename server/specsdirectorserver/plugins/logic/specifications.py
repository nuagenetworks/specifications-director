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

class SDSpecificationLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='specifications logic', version=1.0, identifier="specsdirector.plugins.logic.specifications",
                                subscriptions={
                                    "specification": [GARequest.ACTION_CREATE]
                                })

    def preprocess_write(self, context):
        """
        """
        sdk = SDKLibrary().get_sdk('default')
        repository = context.parent_object
        specification = context.object

        objects, count = self.core_controller.storage_controller.get_all(parent=repository, resource_name=sdk.SDAPIInfo.rest_name, filter='parentID == %s' % repository.id)

        if not count:
            raise Exception('cannot find API info. that should not happen')

        apiinfo = objects[0]
        specification.root_rest_name = apiinfo.root

        return context
