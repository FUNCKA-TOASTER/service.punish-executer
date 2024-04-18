"""VK keyboard button class description file."""

from .action import BaseAction
from .color import ButtonColor


class Button(object):
    """VK keyboard button class."""

    def __init__(self, action: BaseAction, color: ButtonColor, owner_id: int):
        self.action = action
        self.color = color
        self.owner_id = owner_id

    @property
    def data(self) -> dict:
        """Returns the data of the
        button as a dictionary.

        Returns:
            dict: Button data.
        """
        self.action.payload.setdefault("keyboard_owner", self.owner_id)

        data = {"action": self.action.data, "color": self.color.value}

        return data
