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
from time import time

from notubot import (
    BOT_VER,
    LOGS,
    bot,
    BOT_NAME,
    LOOP,
    start_time,
)
from notubot.plugins import ALL_PLUGINS
from notubot.utils.tools import time_formatter


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


async def main() -> None:
    await bot.start()

    for plugins in ALL_PLUGINS:
        import_module("notubot.plugins.{}".format(plugins))

    LOGS.info("{} v{} Launched 🚀".format(BOT_NAME, BOT_VER))

    if len(sys.argv) not in (1, 3, 4):
        await bot.disconnect()
    else:
        await bot.run_until_disconnected()


if __name__ == "__main__":
    try:
        LOGS.info("Took {} to start {}".format(time_formatter((time() - start_time)), BOT_NAME))
        LOOP.run_until_complete(main())
    except (NotImplementedError, KeyboardInterrupt, SystemExit):
        pass
    except (BaseException, Exception) as e:
        LOGS.exception("main : {}".format(e))
    finally:
        LOGS.info("{} Stopped...".format(BOT_NAME))
        sys.exit()
