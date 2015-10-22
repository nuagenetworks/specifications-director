#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import ldap
from specdk.v1_0 import SDJob
from garuda import Garuda
from garuda.channels.rest import GAFalconChannel, GAFlaskChannel
from garuda.plugins.storage import GAMongoStoragePlugin
from garuda.plugins.authentication import GASimpleAuthenticationPlugin

from plugins.logic.jobs import SDJobLogicPlugin
from plugins.logic.apis import SDAPILogicPlugin
from plugins.logic.specifications import SDSpecificationLogicPlugin
from plugins.logic.attributes import SDAttributeLogicPlugin

def auth_function(request, session, root_object_class, storage_controller):
    """
    """
    auth = root_object_class()

    # try:
    #     base_dn = 'uid=%s,cn=users,cn=accounts,dc=us,dc=alcatel-lucent,dc=com' % request.username
    #     ldap_connection = ldap.open('nuageldap1.us.alcatel-lucent.com')
    #     ldap_connection.bind_s(base_dn, request.token)
    # except Exception as ex:
    #     return None

    auth.id = request.username
    auth.api_key = session.uuid
    auth.password = None
    auth.user_name = request.username
    return auth

def db_init(db, root_object_class):
    """
    """
    db[SDJob.rest_name].create_index('lastUpdatedDate', expireAfterSeconds=60)


def start():
    """
    """
    channel = GAFalconChannel(ssl_certificate='ssl/server.crt', ssl_key='ssl/server.key')
    storage_plugin = GAMongoStoragePlugin(db_name='specsdirector', db_initialization_function=db_init)
    authentication_plugin = GASimpleAuthenticationPlugin(auth_function=auth_function)
    sdk_infos = [{'identifier': 'default', 'module': 'specdk.v1_0'}]
    job_logic_plugin = SDJobLogicPlugin()
    apis_logic_plugin = SDAPILogicPlugin()
    spec_logic_plugin = SDSpecificationLogicPlugin()
    attr_logic_plugin = SDAttributeLogicPlugin()

    plugins = [storage_plugin, authentication_plugin, job_logic_plugin, apis_logic_plugin, spec_logic_plugin, attr_logic_plugin]

    garuda = Garuda(sdks_info=sdk_infos, channels=[channel], plugins=plugins, log_level=logging.DEBUG)
    garuda.start()


if __name__ == '__main__':
    start()

