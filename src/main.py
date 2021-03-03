#!/usr/bin/env python

import click
import logging

from dialect_map_io import DialectMapAPI
from dialect_map_io import OpenIDAuthenticator

from mapping import BaseRecordMapper
from mapping import PropertyRecordMapper
from operators import DialectMapOperator

from logs import setup_logger
from files import DATA_FILES
from paths import build_differ_file_path
from paths import build_module_file_path

logger = logging.getLogger()


@click.group()
def main():
    pass


@main.command()
@click.option(
    "--api-url",
    envvar="DIALECT_MAP_API_URL",
    default="https://dialect-map-private-api-ms4sotrd6q-uk.a.run.app",
    help="Private API base URL",
    type=str,
)
@click.option(
    "--key-path",
    envvar="DIALECT_MAP_KEY_PATH",
    default="~/.config/gcloud/service_accounts/dialect_map/ds3-dialect-map.json",
    help="Path to the Service Account key",
    type=str,
)
@click.option(
    "--log-level",
    envvar="DIALECT_MAP_LOG_LEVEL",
    default="INFO",
    help="Severity level for the logging messages",
    type=str,
)
def run(api_url: str, key_path: str, log_level: str):
    """ Run the static data ingestion job """

    setup_logger(log_level)

    api_auth = OpenIDAuthenticator(key_path, api_url)
    api_conn = DialectMapAPI(api_url, api_auth)

    for file in DATA_FILES:
        mapper = init_mapper("id", file.types)
        dispatch(api_conn, mapper, file.name)


def init_mapper(field: str, types: list) -> PropertyRecordMapper:
    """
    Instantiates a property-based record mapper using the provided field name
    :param field: name of the data field
    :param types: list of data types to map
    :return: Property-based record mapper
    """

    mapper = PropertyRecordMapper()
    mapper.property = field
    mapper.mappings = types

    return mapper


def dispatch(api: DialectMapAPI, mapper: BaseRecordMapper, file_name: str):
    """
    Perform operations on the provided API given a static data file
    :param api: API object to operate with
    :param mapper: record to data-type mapper
    :param file_name: static data file name
    """

    data_path = build_module_file_path(file_name)
    diff_path = build_differ_file_path(file_name)

    operator = DialectMapOperator(api, mapper)
    inserted = operator.create_records(data_path, diff_path)
    archived = operator.archive_records(data_path, diff_path)

    logger.info(f"Number of created records: {inserted}")
    logger.info(f"Number of archived records: {archived}")


if __name__ == "__main__":
    main()
