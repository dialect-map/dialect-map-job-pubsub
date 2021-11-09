# -*- coding: utf-8 -*-

import logging

from abc import ABC
from abc import abstractmethod
from typing import List

from dialect_map_gcp import DiffMessage
from dialect_map_gcp import PubSubReader
from dialect_map_io import BaseDataParser
from dialect_map_io import JSONDataParser

logger = logging.getLogger()


class BasePubSubOperator(ABC):
    """Interface for the Pub/Sub operator classes"""

    msg_type: str

    @abstractmethod
    def get_messages(self, num_messages: int) -> List[object]:
        """
        Retrieve messages from a Pub/Sub subscription and decode them as objects
        :param num_messages: maximum number of messages to retrieve
        :return: list of data objects
        """

        raise NotImplementedError()


class DiffPubSubOperator(BasePubSubOperator):
    """Pub/Sub operator for the data diff messages"""

    msg_type = "data-diff"

    def __init__(self, reader: PubSubReader, parser: BaseDataParser = None):
        """
        Initializes the Pub/Sub operator with a given parser and reader
        :param reader: object to retrieve the Pub/Sub messages
        :param parser: object to parse and decode the messages data
        """

        if parser is None:
            parser = JSONDataParser()

        self.reader = reader
        self.parser = parser

    def _check_message_type(self, message_id: str, message_meta: dict) -> None:
        """
        Checks whether the message metadata type matches the desired one
        :param message_id: message unique identifier
        :param message_meta: message custom attributes
        """

        if not message_meta["msgType"] == self.msg_type:
            logger.warning(f"Unexpected type. Ignoring message: {message_id}")
            raise TypeError(f"Unexpected type")

    def _parse_message(self, message: object) -> DiffMessage:
        """
        Parses a given Pub/Sub message raising ValueError if it is invalid
        :param message: Pub/Sub message object
        :return: decoded data-diff message object
        """

        msg_id = self.reader.get_message_id(message)
        msg_data = self.reader.get_message_data(message)
        msg_meta = self.reader.get_message_metadata(message)

        self._check_message_type(msg_id, msg_meta)

        try:
            data_dict = self.parser.parse_bytes(msg_data)
            data_diff = DiffMessage.from_pubsub(data_dict)
        except Exception as error:
            logger.error(f"Cannot parse message {msg_id} with data: {msg_data}")
            logger.error(f"Error detailed info: {error}")
            raise ValueError()
        else:
            return data_diff

    def get_messages(self, num_messages: int) -> List[DiffMessage]:
        """
        Retrieve messages from a Pub/Sub subscription and decode them as objects
        :param num_messages: maximum number of messages to retrieve
        :return: list of data objects
        """

        read_messages = self.reader.pull_messages(num_messages)
        good_messages = []
        data_diffs = []

        for msg in read_messages:
            try:
                data_diff = self._parse_message(msg)
                data_diffs.append(data_diff)
            except TypeError:
                continue
            except ValueError:
                raise
            else:
                good_messages.append(msg)

        # Only properly decoded messages are acknowledged
        self.reader.ack_messages(good_messages)
        return data_diffs
