import logging
import base64
import json

from github import Github
from monolithe.specifications import Specification, RepositoryManager
from monolithe.specifications.repositorymanager import MODE_NORMAL, MODE_RAW_SPECS, MODE_RAW_ABSTRACTS

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary

from repository_importer import SDRepositoryImporter
from repository_exporter import SDRepositoryExporter


class SDJobLogicPlugin(GALogicPlugin):
    """

    """

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='job logic', version=1.0, identifier="specsdirector.plugins.logic.jobs",
                                subscriptions={
                                    "job": [GARequest.ACTION_CREATE]
                                })

    def did_perform_write(self, context):
        """
        """
        sdk = SDKLibrary().get_sdk('default')
        job = context.object
        repository = context.parent_object

        if job.command == "pull":
            importer = SDRepositoryImporter(repository=repository, storage_controller=self.core_controller.storage_controller, sdk=sdk)
            importer.import_specifications()
        elif job.command == "commit":
            exporter = SDRepositoryExporter(repository=repository, storage_controller=self.core_controller.storage_controller, sdk=sdk)
            exporter.export_specifications()

        return context