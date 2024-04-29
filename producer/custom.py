"""Module "producer"."""

from .body import Producer


class CustomProducer(Producer):
    """Custom producer class.
    Preferences for implimentation of custom
    functions for working with data that needs
    to be pushed into a queue inside RabbitMQ.
    """

    event_queues = {"alert": "alerts"}

    async def warn_alert(self, event, warns, total):
        queue = self.event_queues["alert"]
        data = {
            "alert_type": "warn",
            "user_id": event.get("target_id"),
            "user_name": event.get("target_name"),
            "moderator_name": event.get("author_id"),
            "moderator_id": event.get("author_name"),
            "peer_name": event.get("peer_name"),
            "peer_id": event.get("peer_id"),
            "warns": warns,
            "total_warns": total,
        }
        await self._send_data(data, queue)

    async def unwarn_alert(self, event, warns, total):
        queue = self.event_queues["alert"]
        data = {
            "alert_type": "unwarn",
            "user_id": event.get("target_id"),
            "user_name": event.get("target_name"),
            "moderator_name": event.get("author_id"),
            "moderator_id": event.get("author_name"),
            "peer_name": event.get("peer_name"),
            "peer_id": event.get("peer_id"),
            "warns": warns,
            "total_warns": total,
        }
        await self._send_data(data, queue)


producer = CustomProducer()
