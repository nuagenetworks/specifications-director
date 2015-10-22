import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary, ThreadManager

from repository_importer import SDRepositoryImporter
from repository_exporter import SDRepositoryExporter


class SDJobLogicPlugin(GALogicPlugin):
    """

    """

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='job logic', version=1.0, identifier='specsdirector.plugins.logic.jobs',
                                subscriptions={
                                    'job': [GARequest.ACTION_CREATE]
                                })

    def preprocess_write(self, context):
        """
        """
        sdk        = SDKLibrary().get_sdk('default')
        job        = context.object
        repository = context.parent_object

        if job.command == 'pull':

            importer = SDRepositoryImporter(repository=repository,
                                            storage_controller=self.core_controller.storage_controller,
                                            push_controller=self.core_controller.push_controller,
                                            job=job,
                                            sdk=sdk)

            ThreadManager.start_thread(importer.import_specifications)

        elif job.command == 'commit':

            exporter = SDRepositoryExporter(repository=repository,
                                            storage_controller=self.core_controller.storage_controller,
                                            push_controller=self.core_controller.push_controller,
                                            job=job,
                                            sdk=sdk)

            ThreadManager.start_thread(exporter.export_specifications)

        job.status = 'RUNNING'
        job.progress = 0.0
        return context