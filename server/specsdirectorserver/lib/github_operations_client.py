import logging
import msgpack
from garuda.core.models import GAController


class SDGitHubOperationsClient(GAController):

    def __init__(self, core_controller, redis_conn):
        """
        """
        super(SDGitHubOperationsClient, self).__init__(core_controller=core_controller, redis_conn=redis_conn)

    @classmethod
    def identifier(cls):
        """
        """
        return 'sd.controller.githuboperations.client'

    def checkout_repository(self, repository, job):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'action': 'checkout_repository',
            'repository': repository.to_dict(),
            'job': job.to_dict()}))

    def commit_specification(self, repository, specification, commit_message):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'action': 'commit_specification',
            'repository': repository.to_dict(),
            'specification': specification.to_dict(),
            'specification_type': specification.rest_name,
            'commit_message': commit_message}))

    def rename_specification(self, repository, specification, old_name, commit_message):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'action': 'rename_specification',
             'repository': repository.to_dict(),
             'specification': specification.to_dict(),
             'specification_type': specification.rest_name,
             'old_name': old_name,
             'commit_message': commit_message}))

    def delete_specification(self, repository, specification, commit_message):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'action': 'delete_specification',
            'repository': repository.to_dict(),
            'specification': specification.to_dict(),
            'specification_type': specification.rest_name,
            'commit_message': commit_message}))

    def commit_apiinfo(self, repository, apiinfo, commit_message):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'action': 'commit_apiinfo',
            'repository': repository.to_dict(),
            'apiinfo': apiinfo.to_dict(),
            'commit_message': commit_message}))

    def commit_monolitheconfig(self, repository, monolitheconfig, commit_message):
        """
        """
        self.publish('github-operation:new', msgpack.packb({
            'action': 'commit_monolitheconfig',
            'repository': repository.to_dict(),
            'monolitheconfig': monolitheconfig.to_dict(),
            'commit_message': commit_message}))