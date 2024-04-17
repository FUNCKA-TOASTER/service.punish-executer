"""Service "toaster.comman-handling-service".
About:
    ...

Author:
    Oidaho (Ruslan Bashinskii)
    oidahomain@gmail.com
"""

import asyncio
from consumer import consumer
from handler import punishment_executer
from logger import logger


async def main():
    """Entry point."""
    log_text = "Awaiting for the command to execute punishment..."
    await logger.info(log_text)

    for data in consumer.listen_queue("warns"):
        log_text = f"Recived new event: {data}"
        await logger.info(log_text)

        await punishment_executer(data)


if __name__ == "__main__":
    asyncio.run(main())
