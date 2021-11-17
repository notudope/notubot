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
    __botversion__,
    LOGS,
    bot,
    __botname__,
    LOOP,
    start_time,
    HEROKU_APP,
    ipchange,
)
from notubot.plugins import ALL_PLUGINS
from notubot.utils import time_formatter


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


class NotUBotCheck:
    def __init__(self):
        self.sucess = True


NotUBotCheck = NotUBotCheck()


async def startup_process() -> None:
    check = await ipchange()
    if check:
        NotUBotCheck.sucess = False
        return

    await bot.start()

    for plugins in ALL_PLUGINS:
        import_module("notubot.plugins.{}".format(plugins))

    LOGS.info("{} v{} Launched 🚀".format(__botname__, __botversion__))

    NotUBotCheck.sucess = True
    return


if __name__ == "__main__":
    try:
        LOGS.info("Took {} to start {}".format(time_formatter((time() - start_time) * 1000), __botname__))
        bot.loop.run_until_complete(startup_process())

        if len(sys.argv) not in (1, 3, 4):
            bot.disconnect()
        elif not NotUBotCheck.sucess:
            if HEROKU_APP:
                HEROKU_APP.restart()
        else:
            bot.run_until_disconnected()

    except (ConnectionError, NotImplementedError, KeyboardInterrupt, SystemExit):
        pass
    except (BaseException, Exception) as e:
        LOGS.exception("main : {}".format(e))
    finally:
        LOGS.info("{} Stopped...".format(__botname__))
        sys.exit()
