# -*- coding: utf-8 -*-

from dialect_map_io.auth import DefaultAuthenticator
from dialect_map_io.auth import OpenIDAuthenticator
from dialect_map_io.data_input import PubSubReader
from dialect_map_io.data_output import RestOutputAPI

from mapping import API_ROUTES
from mapping import init_adapter
from mapping import init_mapper
from models import DATA_FILES
from models import DATA_TYPES
from operators import DialectMapOperator
from operators import DiffPubSubOperator


def init_all_mappers(mapped_field: str) -> dict:
    """
    Initializes all data file mappers
    :param mapped_field: field to use when inferring the type
    :return: dictionary file - mapper
    """

    mappers = {}

    for f in DATA_FILES:
        extra_args = {"field": mapped_field, "types": f.types}
        mappers[f.name] = init_mapper(f.name, **extra_args)

    return mappers


def init_api_operator(api_url: str, key_path: str) -> DialectMapOperator:
    """
    Initializes the Dialect map API operator
    :param api_url: Dialect map API base URL
    :param key_path: Service Account key path
    :return: initialized API operator
    """

    api_auth = OpenIDAuthenticator(key_path, api_url)
    api_conn = RestOutputAPI(api_url, api_auth)
    adapters = {t.name: init_adapter(t.name) for t in DATA_TYPES}

    return DialectMapOperator(api_conn, API_ROUTES, adapters)


def init_pubsub_operator(gcp_project: str, gcp_pubsub: str, key_path: str) -> DiffPubSubOperator:
    """
    Initializes the Pub/Sub subscription operator
    :param gcp_project: GCP project name
    :param gcp_pubsub: GCP Pub/Sub subscription
    :param key_path: GCP Service Account key path
    :return: initialized Pub/Sub operator
    """

    pubsub_auth = DefaultAuthenticator(key_path)
    pubsub_reader = PubSubReader(
        project_id=gcp_project,
        subscription=gcp_pubsub,
        auth_ctl=pubsub_auth,
    )

    return DiffPubSubOperator(pubsub_reader)
