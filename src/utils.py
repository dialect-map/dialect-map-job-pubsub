# -*- coding: utf-8 -*-

from dialect_map_gcp.auth import DefaultAuthenticator
from dialect_map_gcp.auth import OpenIDAuthenticator
from dialect_map_gcp.data_input import PubSubReader
from dialect_map_io.data_output import RestOutputAPI

from input import DiffPubSubOperator
from output import DialectMapOperator


def init_api_operator(api_url: str, key_path: str) -> DialectMapOperator:
    """
    Initializes the Dialect map API operator
    :param api_url: Dialect map API base URL
    :param key_path: Service Account key path
    :return: initialized API operator
    """

    api_auth = OpenIDAuthenticator(key_path, api_url)
    api_conn = RestOutputAPI(api_url, api_auth)

    return DialectMapOperator(api_conn)


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
