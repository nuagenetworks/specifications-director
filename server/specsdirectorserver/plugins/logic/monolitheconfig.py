import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import GASDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.monolitheconfigs')

class SDMonolitheConfigLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='monolitheconfig logic', version=1.0, identifier="specsdirector.plugins.logic.monolitheconfigs",
                                subscriptions={
                                    "monolitheconfig": [GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._sdk = GASDKLibrary().get_sdk('default')
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def check_perform_write(self, context):
        """
        """
        monolithe_config = context.object

        if not monolithe_config.product_name or not len(monolithe_config.product_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute productName is mandatory.', property_name='productName'))

        if not monolithe_config.product_accronym or not len(monolithe_config.product_accronym):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute productAccronym is mandatory.', property_name='productAccronym'))

        if not monolithe_config.sdk_output or not len(monolithe_config.sdk_output):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKOutput is mandatory.', property_name='SDKOutput'))

        if not monolithe_config.sdk_name or not len(monolithe_config.sdk_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKName is mandatory.', property_name='SDKName'))

        if not monolithe_config.sdk_class_prefix or not len(monolithe_config.sdk_class_prefix):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKClassPrefix is mandatory.', property_name='SDKClassPrefix'))

        if not monolithe_config.sdk_bambou_version or not len(monolithe_config.sdk_bambou_version):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKBambouVersion is mandatory.', property_name='SDKBambouVersion'))

        if not monolithe_config.sdk_version or not len(monolithe_config.sdk_version):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKVersion is mandatory.', property_name='SDKVersion'))

        if not monolithe_config.sdk_revision_number or not len(monolithe_config.sdk_revision_number):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKRevisionNumber is mandatory.', property_name='SDKRevisionNumber'))

        if not monolithe_config.sdkcli_name or not len(monolithe_config.sdkcli_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKCLIName is mandatory.', property_name='SDKCLIName'))

        if not monolithe_config.api_doc_output or not len(monolithe_config.api_doc_output):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute APIDocOutput is mandatory.', property_name='APIDocOutput'))

        if not monolithe_config.sdk_doc_output or not len(monolithe_config.sdk_doc_output):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute SDKDocOutput is mandatory.', property_name='SDKDocOutput'))

        return context

    # def preprocess_write(self, context):
    #     """
    #     """
    #     apiinfo = context.object
    #
    #     if apiinfo.prefix[1] == '/':
    #         apiinfo.prefix = apiinfo.prefix[1:]
    #
    #     if apiinfo.prefix[-1] == '/':
    #         apiinfo.prefix = apiinfo.prefix[:-1]
    #
    #     return context

    def did_perform_write(self, context):
        """
        """
        monolitheconfig = context.object
        repository      = context.parent_object

        self._github_operations_controller.commit_monolitheconfig(repository=repository, monolitheconfig=monolitheconfig, commit_message="Updated Monolithe.ini")

        return context