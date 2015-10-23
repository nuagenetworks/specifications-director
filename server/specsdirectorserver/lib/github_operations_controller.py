import logging
import json
from Queue import Queue

from monolithe.specifications import Specification, RepositoryManager, SpecificationAttribute, SpecificationAPI, RepositoryManager
from garuda.core.models import GAController, GAPushEvent, GARequest
from garuda.core.lib import ThreadManager, SDKLibrary


class GitHubOperationsController(GAController):

    def __init__(self, core_controller, redis_conn):
        """
        """
        super(GitHubOperationsController, self).__init__(core_controller=core_controller, redis_conn=redis_conn)

        self._storage_controller  = None
        self._push_controller     = None
        self._sdk                 = None
        self._thread              = None
        self._repository_managers = {}
        self._operation_queue     = Queue()

    @classmethod
    def identifier(cls):
        """
        """
        return 'sd.controller.githuboperations'

    def ready(self):
        """
        """
        self._sdk                 = SDKLibrary().get_sdk('default')
        self._storage_controller  = self.core_controller.storage_controller
        self._push_controller     = self.core_controller.push_controller

    def start(self):
        """
        """
        self._thread = ThreadManager.start_thread(self._listen_to_operations)

    def stop(self):
        """
        """
        ThreadManager.stop_thread(self._thread)

    def enqueue_operation(self, action, repository, specification, commit_message):
        """
        """
        self._operation_queue.put((action, repository, specification, commit_message))

    def _listen_to_operations(self):
        """
        """
        while True:
            action, repository, specification, commit_message = self._operation_queue.get()
            repo_manager       = self.get_repository_manager_for_repository(repository=repository)
            mono_specification = self._convert_to_mono_specification(specification=specification)

            specification.syncing = True
            self._storage_controller.update(specification)
            self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=specification)])

            repo_manager.save_specification(specification=mono_specification, message=commit_message, branch=repository.branch)

            specification.syncing = False
            self._storage_controller.update(specification)
            self._push_controller.push_events(events=[GAPushEvent(action=GARequest.ACTION_UPDATE, entity=specification)])

    def get_repository_manager_for_repository(self, repository):
        """
        """
        key = repository.id

        if key in self._repository_managers:
            return self._repository_managers[key];

        repo_manager = RepositoryManager( monolithe_config=None,
                                          api_url=repository.url,
                                          login_or_token=repository.password,
                                          password=None,
                                          organization=repository.organization,
                                          repository=repository.repository,
                                          repository_path=repository.path)

        self._repository_managers[key] = repo_manager

        return repo_manager

    def _convert_to_mono_specification(self, specification):
        """
        """
        mono_spec = Specification(monolithe_config=None, filename=specification.name)

        mono_spec.description   = specification.description
        mono_spec.entity_name   = specification.entity_name
        mono_spec.package       = specification.package
        mono_spec.rest_name     = specification.object_rest_name
        mono_spec.resource_name = specification.object_resource_name
        mono_spec.allows_get    = specification.allows_get
        mono_spec.allows_update = specification.allows_update
        mono_spec.allows_create = specification.allows_create
        mono_spec.allows_delete = specification.allows_delete

        if specification.rest_name == self._sdk.SDSpecification.rest_name:
            abstracts, count = self._storage_controller.get_all(parent=specification, resource_name=self._sdk.SDAbstract.rest_name)
            mono_spec.extends = [abstract.name.replace(".spec", "") for abstract in abstracts]
            mono_spec.is_root = specification.root

        mono_spec.child_apis  = self._export_child_apis(specification=specification)
        mono_spec.attributes  = self._export_attributes(specification=specification)

        return mono_spec

    def _export_child_apis(self, specification):
        """
        """
        ret = []
        child_apis, count = self._storage_controller.get_all(parent=specification, resource_name=self._sdk.SDChildAPI.rest_name)

        for child_api in child_apis:

            mono_child_api = SpecificationAPI(remote_specification_name=specification.name)
            remote_specification = self._storage_controller.get(resource_name=self._sdk.SDSpecification.rest_name, identifier=child_api.associated_specification_id)

            mono_child_api.remote_specification_name = remote_specification.object_rest_name
            mono_child_api.deprecated    = child_api.deprecated
            mono_child_api.relationship  = child_api.relationship
            mono_child_api.allows_get    = child_api.allows_get
            mono_child_api.allows_create = child_api.allows_create
            mono_child_api.allows_update = child_api.allows_update
            mono_child_api.allows_delete = child_api.allows_delete

            ret.append(mono_child_api)

        return ret

    def _export_attributes(self, specification):
        """
        """
        ret = []
        attributes, count = self._storage_controller.get_all(parent=specification, resource_name=self._sdk.SDAttribute.rest_name)

        for attribute in attributes:
            mono_attr = SpecificationAttribute(rest_name=attribute.name)

            mono_attr.description     = attribute.description
            mono_attr.rest_name     = attribute.name
            mono_attr.type            = attribute.type
            mono_attr.allowed_chars   = attribute.allowed_chars
            mono_attr.allowed_choices = attribute.allowed_choices
            mono_attr.autogenerated   = attribute.autogenerated
            mono_attr.availability    = attribute.availability
            mono_attr.creation_only   = attribute.creation_only
            mono_attr.default_order   = attribute.default_order
            mono_attr.default_value   = attribute.default_value
            mono_attr.deprecated      = attribute.deprecated
            mono_attr.filterable      = attribute.filterable
            mono_attr.format          = attribute.format
            mono_attr.max_length      = attribute.max_length
            mono_attr.max_value       = attribute.max_value
            mono_attr.min_length      = attribute.min_length
            mono_attr.min_value       = attribute.min_value
            mono_attr.orderable       = attribute.orderable
            mono_attr.readonly        = attribute.read_only
            mono_attr.required        = attribute.required
            mono_attr.unique          = attribute.unique
            mono_attr.unique_scope    = attribute.unique_scope

            ret.append(mono_attr)

        return ret