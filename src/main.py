#!/usr/bin/env python

import click
import logging

from click import Context
from click import Path

from logs import setup_logger
from mapping import BaseRecordMapper
from mapping import init_all_mappers
from output import BaseAPIOperator
from utils import init_api_operator
from utils import init_pubsub_operator

logger = logging.getLogger()


@click.group()
@click.option(
    "--api-url",
    envvar="DIALECT_MAP_API_URL",
    help="Private API base URL",
    required=True,
    type=str,
)
@click.option(
    "--log-level",
    envvar="DIALECT_MAP_LOG_LEVEL",
    default="INFO",
    help="Log messages level",
    required=False,
    type=str,
)
@click.pass_context
def main(context: Context, api_url: str, log_level: str):
    """Default command group for the jobs"""

    setup_logger(log_level)

    params = context.ensure_object(dict)
    params["API_URL"] = api_url
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
@click.pass_context
def pubsub_job(context: Context, gcp_project: str, gcp_pubsub: str, gcp_key_path: str):
    """
    Starts a data ingestion job reading messages from Google Pub/sub.
    Stops when no more messages are read.

    The pipeline expects to receive DiffMessage object parsable messages.
    Ref: dialect_map_gcp.models.message.DiffMessage
    """

    params = context.ensure_object(dict)
    api_url = params["API_URL"]

    pub_ctl = init_pubsub_operator(gcp_project, gcp_pubsub, gcp_key_path)
    api_ctl = init_api_operator(api_url, gcp_key_path)
    mappers = init_all_mappers()

    while True:
        logger.info(f"Reading messages from subscription: {gcp_pubsub}")
        messages = pub_ctl.get_messages(10)

        if len(messages) == 0:
            logger.info("No more Pub/Sub messages")
            logger.info("Stopping Pub/Sub job...")
            pub_ctl.reader.close()
            break

        for message in messages:
            try:
                mapper = mappers[message.source_file]
                dispatch_record(api_ctl, mapper, message)
            except Exception as error:
                logger.error(f"Dispatch process stopped: {error}")
                break


def dispatch_record(api: BaseAPIOperator, mapper: BaseRecordMapper, message) -> None:
    """
    Dispatch message inner data record using the provided API operator
    :param api: Dialect map API operator
    :param mapper: diff message records mapper
    :param message: diff message to dispatch
    """

    record_data = message.record
    record_route = mapper.infer_route(record_data)

    if message.is_creation:
        api.create_record(record_data, record_route)
        logger.info(f"Created record: {record_route}")

    if message.is_edition:
        api.archive_record(record_data, record_route)
        logger.info(f"Archived record: {record_route}")


if __name__ == "__main__":
    main()
