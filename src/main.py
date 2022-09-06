#!/usr/bin/env python

import click

from click import Context
from click import Path

from dialect_map_gcp.auth import DefaultAuthenticator
from dialect_map_gcp.auth import OpenIDAuthenticator
from dialect_map_gcp.data_input import PubSubReader
from dialect_map_io.handlers import DialectMapAPIHandler

from job.input import DiffPubSubOperator
from job.mapping import SchemaRecordMapper
from job.mapping import CATEGORY_ROUTE
from job.mapping import GROUP_ROUTE
from job.mapping import JARGON_ROUTE
from job.output import DialectMapOperator
from logs import setup_logger
from routines import PubSubRoutine


@click.group()
@click.option(
    "--log-level",
    envvar="DIALECT_MAP_LOG_LEVEL",
    default="INFO",
    help="Log messages level",
    required=False,
    type=str,
)
@click.pass_context
def main(context: Context, log_level: str):
    """Default command group for the jobs"""

    setup_logger(log_level)

    params = context.ensure_object(dict)
    params["LOG_LEVEL"] = log_level


@main.command()
@click.option(
    "--gcp-project",
    help="GCP Project name",
    required=True,
    type=str,
)
@click.option(
    "--gcp-pubsub",
    help="GCP PubSub subscription",
    required=True,
    type=str,
)
@click.option(
    "--gcp-key-path",
    help="GCP Service Account key path",
    required=True,
    type=Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
    ),
)
@click.option(
    "--api-url",
    help="Private API base URL",
    required=True,
    type=str,
)
def data_diff_job(gcp_project: str, gcp_pubsub: str, gcp_key_path: str, api_url: str):
    """
    Starts a data ingestion job reading messages from Google Pub/sub.
    Stops when no more messages are read.

    The pipeline expects to receive DiffMessage object parsable messages.
    Ref: dialect_map_gcp.models.message.DiffMessage
    """

    # Initialize the Pub/Sub controller
    pubsub_auth = DefaultAuthenticator(gcp_key_path)
    pubsub_reader = PubSubReader(
        project_id=gcp_project,
        subscription=gcp_pubsub,
        auth_ctl=pubsub_auth,
    )
    pubsub_ctl = DiffPubSubOperator(pubsub_reader)

    # Initialize API controller
    api_auth = OpenIDAuthenticator(gcp_key_path, target_url=api_url)
    api_conn = DialectMapAPIHandler(api_auth, base_url=api_url)
    api_ctl = DialectMapOperator(api_conn)

    # Initialize and start the routine
    routine = PubSubRoutine(pubsub_ctl, api_ctl)
    routine.add_mapper("categories.json", SchemaRecordMapper([CATEGORY_ROUTE]))
    routine.add_mapper("jargons.json", SchemaRecordMapper([GROUP_ROUTE, JARGON_ROUTE]))
    routine.run()


if __name__ == "__main__":
    main()
