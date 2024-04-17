from .body import Consumer


class CustomConsumer(Consumer):
    """Custom consumer class.
    Preferences for implimentation of custom
    functions for working with data that recived
    from a queue inside RabbitMQ.
    """

    # Write custom functions under this line


consumer = CustomConsumer()
