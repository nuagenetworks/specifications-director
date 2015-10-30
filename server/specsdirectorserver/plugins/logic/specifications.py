import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import SDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.specifications')

class SDSpecificationLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='specifications logic', version=1.0, identifier="specsdirector.plugins.logic.specifications",
                                subscriptions={
                                    "specification": [GARequest.ACTION_DELETE, GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._old_names = {};
        self._sdk = SDKLibrary().get_sdk('default')
        self._storage_controller = self.core_controller.storage_controller
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def check_perform_write(self, context):
        """
        """

        if context.request.action in (GARequest.ACTION_DELETE, GARequest.ACTION_ASSIGN):
            return context

        repository     = context.parent_object
        specification  = context.object
        objects, count = self._storage_controller.get_all(parent=repository, resource_name=self._sdk.SDSpecification.rest_name, filter='name == %s' % specification.name)

        if count and objects[0].id != specification.id:
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Duplicate Name', description='Another specification exists with the name %s' % specification.name, property_name='name'))

        if not specification.object_rest_name or not len(specification.object_rest_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute objectRESTName is mandatory.', property_name='objectRESTName'))

        if not specification.object_resource_name or not len(specification.object_resource_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute objectResourceName is mandatory.', property_name='objectResourceName'))

        if not specification.entity_name or not len(specification.entity_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute entityName is mandatory.', property_name='entityName'))

        return context

    def preprocess_write(self, context):
        """
        """
        repository    = context.parent_object
        specification = context.object
        action        = context.request.action

        specification.name = '%s.spec' % specification.object_rest_name

        if action == GARequest.ACTION_UPDATE:

            stored_specification = self._storage_controller.get(resource_name=self._sdk.SDSpecification.rest_name, identifier=specification.id)

            if stored_specification and stored_specification.name != specification.name:
                self._old_names[context.request.uuid] = stored_specification.name

        objects, count = self._storage_controller.get_all(resource_name=self._sdk.SDAPIInfo.rest_name, parent=repository)
        apiinfo = objects[0] if count else None

        if specification.root:

            objects, count = self._storage_controller.get_all(resource_name=self._sdk.SDSpecification.rest_name, parent=repository, filter='name == %s.spec' % apiinfo.root)
            current_root_specification = objects[0] if count else None

            if current_root_specification and current_root_specification.id != specification.id:
                current_root_specification.root = False
                self._storage_controller.update(current_root_specification)
                context.add_event(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=current_root_specification))

                apis, count = self._storage_controller.get_all(resource_name=self._sdk.SDChildAPI.rest_name, parent=current_root_specification)

                for api in apis:
                    api.relationship = 'child'
                    self._storage_controller.update(api)
                    context.add_event(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=api))

            if apiinfo and apiinfo.root != specification.object_rest_name:
                apiinfo.root = specification.object_rest_name
                self._storage_controller.update(apiinfo)
                context.add_event(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=apiinfo))


            apis, count = self._storage_controller.get_all(resource_name=self._sdk.SDChildAPI.rest_name, parent=specification)
            for api in apis:
                api.relationship = 'root'
                self._storage_controller.update(api)
                context.add_event(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=api))

        return context

    def did_perform_write(self, context):
        """
        """
        action        = context.request.action
        specification = context.object
        repository    = context.parent_object

        if action == GARequest.ACTION_CREATE:

            self._github_operations_controller.commit_specification(repository=repository,
                                                                    specification=specification,
                                                                    commit_message="Added specification %s" % specification.name)

        elif action == GARequest.ACTION_UPDATE:

            if context.request.uuid in self._old_names:
                old_name = self._old_names[context.request.uuid]
                del self._old_names[context.request.uuid]

                self._github_operations_controller.rename_specification(repository=repository,
                                                                        specification=specification,
                                                                        old_name=old_name,
                                                                        commit_message="Renamed specification from %s to %s" % (old_name, specification.name))
            else:
                self._github_operations_controller.commit_specification(repository=repository,
                                                                        specification=specification,
                                                                        commit_message="Updated specification %s" % specification.name)

        elif action == GARequest.ACTION_DELETE:

            self._github_operations_controller.delete_specification(repository=repository,
                                                                    specification=specification,
                                                                    commit_message="Deleted specification %s" % specification.name)
        return context