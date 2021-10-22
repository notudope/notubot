# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import sys
from importlib import import_module

from telethon.errors.rpcerrorlist import PhoneNumberInvalidError

from notubot import BOT_VER, LOGS, bot
from notubot.modules import ALL_MODULES

INVALID_PH = "ERROR: The Phone No. entered is INVALID\nTip: Use Country Code along with number.\nor check your phone number and try again!"


try:
    bot.start()

    for module_name in ALL_MODULES:
        import_module("notubot.modules.{}".format(module_name))

    LOGS.info("⚡NOTUBOT UserBot⚡ v{} Launched 🚀".format(BOT_VER))

    if len(sys.argv) not in (1, 3, 4):
        bot.disconnect()
    else:
        bot.run_until_disconnected()
except PhoneNumberInvalidError:
    LOGS.exception(INVALID_PH)
    sys.exit(1)
except (KeyboardInterrupt, SystemExit):
    sys.exit()
except Exception as e:
    LOGS.exception("main : {}".format(e))
