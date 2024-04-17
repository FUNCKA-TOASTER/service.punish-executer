"""Module "consumer"."""

import json
import pika
import config


class Consumer(object):
    """Consumer main class.
    Describes basic connection methods
    and reciving data from RabbitMQ.
    """

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.QUEUE_BROKER_IP)
    )
    channel = connection.channel()

    def listen_queue(self, queue: str) -> dict:
        """Listen to the queue inside RabbitMQ.
        When receiving data, decodes and converts
        from JSON to dcit object.

        Args:
            queue (str): Queue name in RabbitMQ.

        Yields:
            Iterator[dict]: JSON log data.
        """
        self.channel.queue_declare(queue=queue, durable=True)

        for data in self.channel.consume(queue=queue, auto_ack=True):
            decoded = self._deserialize(data[2])

            yield json.loads(decoded)

    @staticmethod
    def _serialize(string: str) -> bytes:
        return string.encode("utf-8")

    @staticmethod
    def _deserialize(byte_string: bytes) -> str:
        return byte_string.decode("utf-8")
