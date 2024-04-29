"""Module "producer"."""

import json
import pika
import config


class Producer(object):
    """Producer main class.
    Describes basic connection methods
    and sending data to RabbitMQ.
    """

    async def _send_data(self, data: dict, queue: str):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.QUEUE_BROKER_IP)
        )
        channel = connection.channel()

        json_string = json.dumps(data)

        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=await self._serialize(json_string),
        )

        connection.close()

    @staticmethod
    async def _serialize(string: str) -> bytes:
        return string.encode("utf-8")

    @staticmethod
    async def _deserialize(byte_string: bytes) -> str:
        return byte_string.decode("utf-8")
