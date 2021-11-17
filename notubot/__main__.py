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
    setup_me_bot,
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


try:
    bot.loop.run_until_complete(setup_me_bot())
except Exception as e:
    LOGS.error(f"{e}")


class NotUBotCheck:
    def __init__(self):
        self.sucess = True


NotUBotCheck = NotUBotCheck()


async def main() -> None:
    check = await ipchange()
    if check is not None:
        NotUBotCheck.sucess = False
        return

    await bot.start()

    NotUBotCheck.sucess = True

    for plugins in ALL_PLUGINS:
        import_module("notubot.plugins.{}".format(plugins))

    LOGS.info("{} v{} Launched 🚀".format(__botname__, __botversion__))

    if len(sys.argv) not in (1, 3, 4):
        await bot.disconnect()
    elif not NotUBotCheck.sucess:
        if HEROKU_APP is not None:
            HEROKU_APP.restart()
    else:
        try:
            await bot.run_until_disconnected()
        except ConnectionError:
            pass


if __name__ == "__main__":
    try:
        LOGS.info("Took {} to start {}".format(time_formatter((time() - start_time) * 1000), __botname__))
        LOOP.run_until_complete(main())
    except (NotImplementedError, KeyboardInterrupt, SystemExit):
        pass
    except (BaseException, Exception) as e:
        LOGS.exception("main : {}".format(e))
    finally:
        LOGS.info("{} Stopped...".format(__botname__))
        sys.exit()
