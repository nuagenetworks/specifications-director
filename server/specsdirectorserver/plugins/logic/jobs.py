from garuda.core.models import GAPluginManifest, GARequest, GAPushEvent
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import GASDKLibrary


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

    def did_register(self):
        """
        """
        self._sdk = GASDKLibrary().get_sdk('default')
        self._push_controller = self.core_controller.push_controller
        self._storage_controller = self.core_controller.storage_controller
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def will_perform_write(self, context):
        """
        """
        job = context.object
        job.status = 'RUNNING'
        job.progress = 0.0

        return context

    def did_perform_write(self, context):
        """
        """
        job = context.object
        repository = context.parent_object
        session_username = context.session.root_object.id
        command = job.command

        if command == 'commit':

            repository.status = 'NEEDS_PULL'
            self._storage_controller.update(user_identifier=session_username, resource=repository)
            self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=repository)])

            response = self._storage_controller.get_all(user_identifier=session_username,
                                                        parent=repository,
                                                        resource_name=self._sdk.SDSpecification.rest_name)

            for specification in response.data:
                self._github_operations_controller.commit_specification(repository=repository,
                                                                        specification=specification,
                                                                        commit_message="Bulk saved specification %s" % specification.name,
                                                                        session_username=session_username)

            response = self._storage_controller.get_all(user_identifier=session_username,
                                                        parent=repository,
                                                        resource_name=self._sdk.SDAbstract.rest_name)

            for abstract in response.data:
                self._github_operations_controller.commit_specification(repository=repository,
                                                                        specification=abstract,
                                                                        commit_message="Bulk saved abstract %s" % abstract.name,
                                                                        session_username=session_username)

        else:
            repository.status = 'QUEUED'
            self._storage_controller.update(user_identifier=session_username, resource=repository)
            self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=repository)])

            if command == 'merge_master':
                self._github_operations_controller.merge_upstream_master(repository=repository,
                                                                         job=job,
                                                                         commit_message="Merged upstream master into %s" % repository.branch,
                                                                         session_username=session_username)

            elif command == 'pull':
                self._github_operations_controller.checkout_repository(repository=repository,
                                                                       job=job,
                                                                       session_username=session_username)
        return context
