from abc import ABC, abstractmethod
from vk_api import VkApi
from logger import logger
import config


class ABCHandler(ABC):
    """Abstract Handler class.
    The Handling Hub acts as a “machine” that accepts input
    object of a custom event, after which it applies everything one by one
    handlers available to her for this event. If at least one event is triggered -
    the Handling Hub will stop its work and determine the event as handled.

    Args:
        event (BaseEvent): Modified VKBotLongpoll event.

    Returns:
        bool: Handling status. Returns True if was handled.
            True - the event did not trigger anything
            False - if event triggered something, it means event achieved goal
    """

    def __init__(self):
        # VK api object
        self.__api: VkApi = (
            VkApi(token=config.TOKEN, api_version=config.API_VERSION).get_api() or None
        )

    async def __call__(self, event: dict, **kwargs) -> bool:
        """Calls the class as a function,
        handling the received input
        BaseEvent object.
        """
        if self.__api is not None:
            return await self._handle(event, kwargs)

        else:
            log_text = (
                "Unable to execute punishment. Handler does not have an API object."
            )
            await logger.info(log_text)

        return False

    @abstractmethod
    async def _handle(self, event: dict, kwargs) -> bool:
        """Handle a custom event, returning the processing result.
        Applies all handlers one by one to the custom event object.

        Args:
            event (BaseEvent): Modified VKBotLongpoll event.

        Returns:
            bool: Handling status. Returns True if was handled.
        """

    @property
    def api(self):
        """Returns the VKontakte API object from the parent class.

        Returns:
            VkApi: vk api object.
        """
        return self.__api
