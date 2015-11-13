import logging
import msgpack
from garuda.core.models import GAController


class SDGitHubOperationsClient(GAController):

    def __init__(self, core_controller):
        """
        """
        super(SDGitHubOperationsClient, self).__init__(core_controller=core_controller)

    @classmethod
    def identifier(cls):
        """
        """
        return 'sd.controller.githuboperations.client'

    def checkout_repository(self, repository, job, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'checkout_repository',
            'repository': repository.to_dict(),
            'job': job.to_dict()}))

    def commit_specification(self, repository, specification, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'commit_specification',
            'repository': repository.to_dict(),
            'specification': specification.to_dict(),
            'specification_type': specification.rest_name,
            'commit_message': commit_message}))

    def rename_specification(self, repository, specification, old_name, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'rename_specification',
            'repository': repository.to_dict(),
            'specification': specification.to_dict(),
            'specification_type': specification.rest_name,
            'old_name': old_name,
            'commit_message': commit_message}))

    def delete_specification(self, repository, specification, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'delete_specification',
            'repository': repository.to_dict(),
            'specification': specification.to_dict(),
            'specification_type': specification.rest_name,
            'commit_message': commit_message}))

    def commit_apiinfo(self, repository, apiinfo, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'commit_apiinfo',
            'repository': repository.to_dict(),
            'apiinfo': apiinfo.to_dict(),
            'commit_message': commit_message}))

    def commit_monolitheconfig(self, repository, monolitheconfig, commit_message, session_username):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'garuda_uuid': self.core_controller.garuda_uuid,
            'session_username': session_username,
            'action': 'commit_monolitheconfig',
            'repository': repository.to_dict(),
            'monolitheconfig': monolitheconfig.to_dict(),
            'commit_message': commit_message}))