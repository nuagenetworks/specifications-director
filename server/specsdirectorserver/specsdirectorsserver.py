#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from garuda import Garuda
from garuda.channels.rest import GAFalconChannel, GAFlaskChannel
from garuda.plugins.storage import GAMongoStoragePlugin
from garuda.plugins.authentication import GASimpleAuthenticationPlugin

from plugins.logic.repositories import SDRepositoryLogicPlugin
from plugins.logic.apis import SDAPILogicPlugin
from plugins.logic.specifications import SDSpecificationLogicPlugin
from plugins.logic.attributes import SDAttributeLogicPlugin

def db_init(db, root_rest_name):
    """
    """
    from bson import ObjectId
    if not db[root_rest_name].count():
        db[root_rest_name].insert({'_id': ObjectId('111111111111111111111111') , 'userName': 'root', 'password': 'password'})

def auth_function(request, session, root_api, storage_controller):
    """
    """
    auth = storage_controller.get(root_api, '111111111111111111111111')

    # if request.username == auth.user_name and request.token == auth.password:
    auth.api_key = session.uuid
    auth.password = None
    return auth



def start():
    """
    """
    channel = GAFalconChannel()
    storage_plugin = GAMongoStoragePlugin(db_name='specsdirector', db_initialization_function=db_init)
    authentication_plugin = GASimpleAuthenticationPlugin(auth_function=auth_function)
    sdk_infos = [{'identifier': 'default', 'module': 'specdk.v1_0'}]
    repo_logic_plugin = SDRepositoryLogicPlugin()
    apis_logic_plugin = SDAPILogicPlugin()
    spec_logic_plugin = SDSpecificationLogicPlugin()
    attr_logic_plugin = SDAttributeLogicPlugin()

    plugins = [storage_plugin, authentication_plugin, repo_logic_plugin, apis_logic_plugin, spec_logic_plugin, attr_logic_plugin]

    garuda = Garuda(sdks_info=sdk_infos, channels=[channel], plugins=plugins, log_level=logging.DEBUG)
    garuda.start()


if __name__ == '__main__':
    start()

