# -* coding: utf-8 -*-

import logging

from abc import ABC
from abc import abstractmethod
from typing import override

from job.input import BasePubSubSource
from job.mapping import BaseRecordMapper
from job.output import BaseAPIOperator

logger = logging.getLogger()


class BaseRoutine(ABC):
    """Base class for the job routines"""

    @abstractmethod
    def run(self, batch_size: int) -> None:
        """
        Main routine to move data from a source to a destination
        :param batch_size: number of data records to move at once
        """

        raise NotImplementedError()


class PubSubRoutine(BaseRoutine):
    """Routine moving Pub/Sub messages to an API REST"""

    def __init__(self, pub_ctl: BasePubSubSource, api_ctl: BaseAPIOperator):
        """
        Initializes the Google Pub/Sub - REST API routine
        :param pub_ctl: Pub/Sub operator to be used as input
        :param api_ctl: API REST operator to be used as output
        """

        self.pub_ctl = pub_ctl
        self.api_ctl = api_ctl
        self.mappers = {}  # type: ignore

    def _dispatch_record(self, message) -> None:
        """
        Dispatch message inner data record to the destination API
        :param message: Pub/Sub message to dispatch
        """

        msg_mapper = self.get_mapper(message.source_file)
        msg_route = msg_mapper.infer_route(message.record)

        if message.is_creation:
            self.api_ctl.create_record(msg_route, message.record)
            logger.info(f"Created record: {msg_route}")

        if message.is_edition:
            self.api_ctl.archive_record(msg_route, message.record)
            logger.info(f"Archived record: {msg_route}")

    def add_mapper(self, file_name: str, msg_mapper: BaseRecordMapper) -> None:
        """
        Adds a message mapper to the dict of mappers, using a file name as key
        :param file_name: message source file to be used as key
        :param msg_mapper: message mapper object to infer the API route
        """

        self.mappers[file_name] = msg_mapper

    def get_mapper(self, file_name: str) -> BaseRecordMapper:
        """
        Gets a message mapper given a certain message source file
        :param file_name: message source file to be used as key
        """

        try:
            return self.mappers[file_name]
        except KeyError:
            logger.error(f"Invalid message source file: {file_name}")
            raise

    @override
    def run(self, batch_size: int = 10) -> None:
        """
        Main routine to move messages from a Pub/Sub topic to a REST API
        :param batch_size: maximum number of Pub/Sub messages to retrieve at once
        """

        while True:
            logger.info(f"Reading messages from Pub/Sub subscription")
            messages = self.pub_ctl.get_messages(batch_size)

            if len(messages) == 0:
                logger.info("No more Pub/Sub messages")
                logger.info("Stopping Pub/Sub routine...")
                self.pub_ctl.close()
                break

            for message in messages:
                try:
                    self._dispatch_record(message)
                except Exception as error:
                    logger.error(f"Dispatch process stopped: {error}")
                    break
