#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import simpleldap
import argparse
import specdk.v1_0 as specdk

from garuda import Garuda
from garuda.channels.rest import GAFalconChannel
from garuda.plugins.storage import GAMongoStoragePlugin
from garuda.plugins.authentication import GASimpleAuthenticationPlugin

from plugins.logic.jobs import SDJobLogicPlugin
from plugins.logic.apis import SDAPILogicPlugin
from plugins.logic.specifications import SDSpecificationLogicPlugin
from plugins.logic.abstracts import SDAbstractLogicPlugin
from plugins.logic.attributes import SDAttributeLogicPlugin
from plugins.logic.apiinfo import SDAPIInfoLogicPlugin
from plugins.logic.repositories import SDRepositoryLogicPlugin
from plugins.logic.monolitheconfig import SDMonolitheConfigLogicPlugin

from lib import SDGitHubOperationsController, SDGitHubOperationsClient

def auth_function(request, session, root_object_class, storage_controller):
    """
    """
    auth = root_object_class()

    base_dn = 'uid=%s,cn=users,cn=accounts,dc=us,dc=alcatel-lucent,dc=com' % request.username
    ldap_connection = simpleldap.Connection('nuageldap1.us.alcatel-lucent.com')

    if not ldap_connection.authenticate(base_dn, request.token):
        return None

    auth.id = request.username
    auth.api_key = session.uuid
    auth.password = None
    auth.user_name = request.username
    return auth

def db_init(db, root_object_class):
    """
    """
    import pymongo
    db[specdk.SDJob.rest_name].create_index('lastUpdatedDate', expireAfterSeconds=60)
    db[specdk.SDSpecification.rest_name].create_index([('name', pymongo.TEXT)])



def start(mongo_host, mongo_port, mongo_db, redis_host, redis_port, redis_db):
    """
    """
    # redis
    redis_info = {'host': redis_host, 'port': redis_port, 'db': redis_db}

    #mongo
    mongo_uri = 'mongodb://%s:%d' % (mongo_host, mongo_port)

    channel = GAFalconChannel(ssl_certificate='ssl/server.crt', ssl_key='ssl/server.key')
    storage_plugin = GAMongoStoragePlugin(db_name=mongo_db, mongo_uri=mongo_uri, db_initialization_function=db_init)
    authentication_plugin = GASimpleAuthenticationPlugin(auth_function=auth_function)
    sdk_infos = [{'identifier': 'default', 'module': 'specdk.v1_0'}]

    plugins = [ storage_plugin,
                authentication_plugin,
                SDJobLogicPlugin(),
                SDAPILogicPlugin(),
                SDSpecificationLogicPlugin(),
                SDAbstractLogicPlugin(),
                SDAttributeLogicPlugin(),
                SDAPIInfoLogicPlugin(),
                SDRepositoryLogicPlugin(),
                SDMonolitheConfigLogicPlugin()]

    garuda = Garuda(sdks_info=sdk_infos,
                    redis_info=redis_info,
                    channels=[channel],
                    additional_controller_classes=[SDGitHubOperationsClient],
                    additional_master_controller_classes=[SDGitHubOperationsController],
                    plugins=plugins,
                    log_level=logging.DEBUG)

    garuda.start()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Bladerunner")

    parser.add_argument('--mongo-host',
                        dest='mongo_host',
                        help='the hostname of the mongodb',
                        default='127.0.0.1',
                        type=str)

    parser.add_argument('--mongo-port',
                        dest='mongo_port',
                        help='the port name for mongodb',
                        default=27017,
                        type=int)

    parser.add_argument('--mongo-db',
                        dest='mongo_db',
                        help='the db name for mongodb',
                        default='specsdirector',
                        type=str)


    parser.add_argument('--redis-host',
                        dest='redis_host',
                        help='the hostname of the redis',
                        default='127.0.0.1',
                        type=str)

    parser.add_argument('--redis-port',
                        dest='redis_port',
                        help='the port name for redis',
                        default=6379,
                        type=int)

    parser.add_argument('--redis-db',
                        dest='redis_db',
                        help='the db number for redis',
                        default=0,
                        type=int)

    args = parser.parse_args()

    start(  mongo_host=args.mongo_host,
            mongo_port=args.mongo_port,
            mongo_db=args.mongo_db,
            redis_host=args.redis_host,
            redis_port=args.redis_port,
            redis_db=args.redis_db)

