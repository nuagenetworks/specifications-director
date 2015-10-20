import logging
import base64
import json

from github import Github
from monolithe.specifications import Specification, RepositoryManager
from monolithe.specifications.repositorymanager import MODE_NORMAL, MODE_RAW_SPECS, MODE_RAW_ABSTRACTS

from garuda.core.models import GAError, GAPluginManifest, GARequest
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
                                    "attribute": [GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE]
                                })

    def check_perform_write(self, context):
        """
        """
        sdk = SDKLibrary().get_sdk('default')
        specification = context.parent_object
        attribute = context.object

        objects, count = self.core_controller.storage_controller.get_all(parent=specification, resource_name=sdk.SDAttribute.rest_name, filter='name == %s' % attribute.name)

        if count and objects[0].id != attribute.id:
            context.report_error(GAError(   type=GAError.TYPE_CONFLICT,
                                            title='Duplicate Name',
                                            description='Another attribute exists with the name %s' % attribute.name,
                                            property_name='name'))

        return context
