# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio
from datetime import datetime
from os import remove
from platform import python_version
from sys import exc_info
from traceback import format_exc

from telethon import version, events
from telethon.errors.rpcerrorlist import (
    FloodWaitError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    MessageDeleteForbiddenError,
    ChatSendStickersForbiddenError,
    ChatSendMediaForbiddenError,
    ChatSendInlineForbiddenError,
    ChatSendGifsForbiddenError,
    ChatWriteForbiddenError,
)
from telethon.utils import get_display_name

from notubot import (
    BOTLOG_CHATID,
    bot,
    __botversion__,
    __botname__,
    BOTLOG,
    LOGS,
)
from notubot.utils.tools import time_formatter

FLOOD_WAIT = 0


def bot_cmd(**args):
    args["func"] = lambda e: not e.fwd_from and not e.via_bot_id
    pattern = args.get("pattern", None)
    disable_edited = args.get("disable_edited", False)
    ignore_unsafe = args.get("ignore_unsafe", False)
    unsafe_pattern = r"^[^/!#@\$A-Za-z]"
    groups_only = args.get("groups_only", False)
    admins_only = args.get("admins_only", False)
    trigger_on_fwd = args.get("trigger_on_fwd", False)
    disable_errors = args.get("disable_errors", False)
    insecure = args.get("insecure", False)

    if pattern is not None and not pattern.startswith("(?i)"):
        args["pattern"] = "(?i)" + pattern

    if "disable_edited" in args:
        del args["disable_edited"]

    if "ignore_unsafe" in args:
        del args["ignore_unsafe"]

    if "groups_only" in args:
        del args["groups_only"]

    if "admins_only" in args:
        del args["admins_only"]

    if "disable_errors" in args:
        del args["disable_errors"]

    if "trigger_on_fwd" in args:
        del args["trigger_on_fwd"]

    if "insecure" in args:
        del args["insecure"]

    if pattern:
        if not ignore_unsafe:
            args["pattern"] = pattern.replace("^.", unsafe_pattern, 1)

    def decorator(func):
        async def wrapper(event):
            if event.edit_date and event.is_channel and not event.is_group:
                return
            send_to = BOTLOG_CHATID if BOTLOG else event.chat_id or event.from_id

            if not trigger_on_fwd and event.fwd_from:
                return

            if admins_only:
                if not event.is_group:
                    return await event.respond("`Gunakan perintah itu dalam grup!`")
                gchat = await event.get_chat()
                if not (gchat.admin_rights or gchat.creator):
                    await event.delete()
                    return await event.respond("`Bukan admin disini!`")

            if groups_only and not event.is_group:
                return await event.respond("`Gunakan perintah itu dalam grup!`")

            try:
                from notubot.plugins.sql_helper.blacklist_sql import get_blacklist

                for blacklisted in get_blacklist():
                    if str(event.chat_id or event.from_id) == blacklisted.chat_id:
                        return
            except Exception:
                pass

            if event.via_bot_id and not insecure and event.out:
                return

            try:
                await func(event)
            except FloodWaitError as e:
                FLOOD_WAIT = e.seconds
                FLOOD_WAIT_HUMAN = time_formatter((FLOOD_WAIT + 10) * 1000)
                LOGS.error(
                    "A FloodWaitError of {}. Sleeping for {} and try again.".format(FLOOD_WAIT, FLOOD_WAIT_HUMAN)
                )
                await event.delete()
                await asyncio.sleep(FLOOD_WAIT + 10)
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "`{} sudah bisa digunakan, setelah terkena FloodWaitError selama {}`".format(
                            __botname__, FLOOD_WAIT_HUMAN
                        ),
                    )
                return
            except events.StopPropagation:
                raise events.StopPropagation
            except (
                MessageIdInvalidError,
                MessageNotModifiedError,
                MessageDeleteForbiddenError,
                ChatWriteForbiddenError,
                ChatSendMediaForbiddenError,
                ChatSendGifsForbiddenError,
                ChatSendStickersForbiddenError,
                ChatSendInlineForbiddenError,
                asyncio.exceptions.CancelledError,
                KeyboardInterrupt,
                SystemExit,
            ):
                pass

            except Exception as e:
                LOGS.exception(e)
                if not disable_errors:
                    date = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")
                    title = get_display_name(event.chat)
                    text = "**NOTUBOT ERROR REPORT**\n"
                    text += "Laporkan kesalahan **teruskan pesan ini ke** @NOTUBOTS"
                    ftext = "NOTUBOT ERROR REPORT: Laporkan ini ke @NOTUBOTS\n\n"

                    ftext += "--------START NOTUBOT CRASH LOG--------\n"
                    ftext += "\nNOTUBOT Version: " + str(__botversion__)
                    ftext += "\nPython Version: " + str(python_version())
                    ftext += "\nTelethon Version: " + str(version.__version__)
                    ftext += "\nDate: " + date
                    ftext += "\nChat: " + str(event.chat_id or event.from_id) + " " + str(title)
                    ftext += "\nSender ID: " + str(event.sender_id)
                    ftext += "\nReplied: " + str(event.is_reply)
                    ftext += "\n\nEvent Trigger:\n"
                    ftext += str(event.text)
                    ftext += "\n\nTraceback info:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nError text:\n"
                    ftext += str(exc_info()[1])
                    ftext += "\n\n--------END NOTUBOT CRASH LOG--------"

                    command = 'git log --pretty=format:"%an: %s" -5'

                    ftext += "\n\n\nLast 5 commits:\n"

                    # NotImplementedError
                    process = await asyncio.create_subprocess_shell(
                        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                    )
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
                    ftext += result

                    with open("error.log", "w+") as file:
                        file.write(ftext)
                    if BOTLOG:
                        await event.respond("`NOTUBOT-UserBot ERROR! Catatan disimpan pada BOTLOG.`")
                    try:
                        await event.client.send_file(send_to, "error.log", caption=text)
                    except Exception:
                        pass
                    remove("error.log")
            else:
                pass

        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator
