# -*- coding: utf-8 -*-

import logging

from abc import ABC
from abc import abstractmethod
from typing import List

from dialect_map_gcp import DiffMessage
from dialect_map_gcp import PubSubQueueHandler

logger = logging.getLogger()


class BasePubSubSource(ABC):
    """Interface for the Pub/Sub source classes"""

    @abstractmethod
    def close(self) -> None:
        """Closes the Pub/Sub connection"""

        raise NotImplementedError()

    @abstractmethod
    def get_messages(self, num_messages: int) -> List[object]:
        """
        Retrieve messages from a Pub/Sub subscription and decode them as objects
        :param num_messages: maximum number of messages to retrieve
        :return: list of data objects
        """

        raise NotImplementedError()


class DiffPubSubSource(BasePubSubSource):
    """Pub/Sub source for the data diff messages"""

    msg_type = DiffMessage

    def __init__(self, handler: PubSubQueueHandler, subscription: str):
        """
        Initializes the Pub/Sub operator with a given handler
        :param handler: object to retrieve the Pub/Sub messages
        :param subscription: Pub/sub subscription to get messages from
        """

        self.queue_handler = handler
        self.queue_name = subscription

    def _parse_message(self, message: object) -> DiffMessage:
        """
        Parses a given Pub/Sub message raising ValueError if it is invalid
        :param message: Pub/Sub message object
        :return: decoded data-diff message object
        """

        if not isinstance(message, dict):
            raise TypeError("Received message is not a Python dictionary")

        try:
            data_diff = self.msg_type.from_pubsub(message)
        except Exception as error:
            logger.error(f"Cannot parse message: {message}")
            logger.error(f"Error detailed info: {error}")
            raise ValueError()
        else:
            return data_diff

    def close(self) -> None:
        """Closes the Pub/Sub connection"""

        self.queue_handler.close()

    def get_messages(self, num_messages: int) -> List[DiffMessage]:
        """
        Retrieve parsed diff messages from a Pub/Sub subscription
        :param num_messages: maximum number of messages to retrieve
        :return: list of data objects
        """

        diff_messages = self.queue_handler.pull_messages(self.queue_name, num_messages)
        diff_objects = []

        for msg in diff_messages:
            try:
                diff_object = self._parse_message(msg)
                diff_objects.append(diff_object)
            except ValueError:
                # TODO: Save acked messages locally
                self.close()
                raise
            except Exception:
                self.close()
                raise

        return diff_objects
