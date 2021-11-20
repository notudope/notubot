# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio
import signal
import sys
from importlib import import_module
from platform import python_version
from time import time

from telethon import version

from notubot import (
    __botversion__,
    LOGS,
    bot,
    __botname__,
    LOOP,
    start_time,
)
from notubot.db import db
from notubot.functions import time_formatter
from notubot.plugins import ALL_PLUGINS

db.init()


THENOTUBOT = """
█▄░█ █▀█ ▀█▀ █░█ █▄▄ █▀█ ▀█▀
█░▀█ █▄█ ░█░ █▄█ █▄█ █▄█ ░█░
"""


async def shutdown_bot(signum: str) -> None:
    LOGS.warning("Received signal : {}".format(signum))
    await bot.disconnect()
    if LOOP.is_running():
        LOOP.stop()


def trap() -> None:
    for signame in {"SIGINT", "SIGTERM", "SIGABRT"}:
        sig = getattr(signal, signame)
        LOOP.add_signal_handler(sig, lambda s=sig: asyncio.create_task(shutdown_bot(s.name)))


trap()


async def startup_process() -> None:
    await bot.start()

    for plugins in ALL_PLUGINS:
        import_module("notubot.plugins.{}".format(plugins))

    LOGS.info("{} v{} Launched 🚀".format(__botname__, __botversion__))

    if len(sys.argv) not in (1, 3, 4):
        await bot.disconnect()
    else:
        await bot.run_until_disconnected()


if __name__ == "__main__":
    try:
        LOGS.info("🚀 Launch deployment...")
        LOGS.info(THENOTUBOT)
        LOGS.info("Version - v{}".format(__botversion__))
        LOGS.info("Telethon Version - {}".format(version.__version__))
        LOGS.info("Python Version - {}".format(python_version()))
        LOGS.info("Took {} to start {}".format(time_formatter((time() - start_time) * 1000), __botname__))
        bot.loop.run_until_complete(startup_process())
    except (ConnectionError, NotImplementedError, KeyboardInterrupt, SystemExit):
        pass
    except (BaseException, Exception) as e:
        LOGS.exception("main : {}".format(e))
    finally:
        LOGS.info("{} Stopped...".format(__botname__))
        sys.exit()
