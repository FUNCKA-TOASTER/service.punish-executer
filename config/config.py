"""Module "config".

File:
    config.py

About:
    This file defines the used variables
    and configuration objects.
"""

import os

BROKER_QUEUE_NAME = "punishment"

VK_GROUP_TOKEN: str = os.getenv("vk_group_token")

VK_GROUP_ID: int = int(os.getenv("vk_group_id"))

VK_API_VERSION: str = "5.199"

VK_PEER_ID_DELAY = 2000000000
