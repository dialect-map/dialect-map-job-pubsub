#!/usr/bin/env python

import click
import logging

from click import Context

from logs import setup_logger
from mapping import BaseRecordMapper
from operators import BaseAPIOperator
from operators import DiffMessageOperator
from utils import init_all_mappers
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

    context.ensure_object(dict)
    context.obj["API_URL"] = api_url
    context.obj["LOG_LEVEL"] = log_level


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
    type=str,
)
@click.pass_context
def pubsub_job(context: Context, gcp_project: str, gcp_pubsub: str, gcp_key_path: str):
    """
    Starts a data ingestion job reading messages from Google Pub/sub.
    Stops when no more messages are read.

    The pipeline expects to receive DiffMessage object parsable messages.
    Ref: dialect_map_io.models.pubsub.DiffMessage
    """

    api_url = context.obj["API_URL"]

    pub_ctl = init_pubsub_operator(gcp_project, gcp_pubsub, gcp_key_path)
    api_ctl = init_api_operator(api_url, gcp_key_path)
    mappers = init_all_mappers(mapped_field="id")

    while True:
        logger.info(f"Reading messages from subscription: {gcp_pubsub}")
        messages = pub_ctl.read_messages(10)

        if len(messages) == 0:
            logger.info("No more Pub/Sub messages")
            logger.info("Stopping Pub/Sub job...")
            pub_ctl.reader.close()
            break

        for message in messages:
            mapper = mappers[message.source_file]
            dispatch_records(api_ctl, mapper, message)


def dispatch_records(api: BaseAPIOperator, mapper: BaseRecordMapper, message) -> None:
    """
    Dispatch message records using the provided API operator
    :param api: Dialect map API operator
    :param mapper: diff message records mapper
    :param message: diff message to dispatch
    """

    msg_ctl = DiffMessageOperator()
    records = msg_ctl.get_enriched_records(message)

    num_created = 0
    num_archived = 0

    for record in records:
        try:
            record_type = mapper.infer_type(record)

            if message.is_creation:
                api.create_record(record, record_type)
                num_created += 1
            if message.is_edition:
                api.archive_record(record, record_type)
                num_archived += 1

        except Exception as error:
            logger.error(f"Dispatch process stopped: {error}")
            break

    logger.info(f"Number of created records: {num_created}")
    logger.info(f"Number of archived records: {num_archived}")


if __name__ == "__main__":
    main(obj={})
