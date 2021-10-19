import os
import sys
from asyncio import create_subprocess_shell, subprocess
from time import gmtime, strftime, sleep
from traceback import format_exc

from telethon import events
from telethon.errors.rpcerrorlist import FloodWaitError, MessageIdInvalidError

from userbot import BOTLOG_CHATID, LOGSPAMMER, bot
from userbot.utils.tools import time_formatter as tf

# from userbot.utils.pastebin import PasteBin


def register(**args):
    """Register a new event."""
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
        async def wrapper(chat):
            if chat.edit_date and chat.is_channel and not chat.is_group:
                return
            if not LOGSPAMMER:
                send_to = chat.chat_id
            else:
                send_to = BOTLOG_CHATID

            if not trigger_on_fwd and chat.fwd_from:
                return

            if admins_only:
                if not chat.is_group:
                    return await chat.respond("`Gunakan perintah itu dalam grup!`")
                gchat = await chat.get_chat()
                if not (gchat.admin_rights or gchat.creator):
                    return await chat.respond("`Lo bukan admin disini!`")

            if groups_only and not chat.is_group:
                return await chat.respond("`Gunakan perintah itu dalam grup!`")

            try:
                from userbot.modules.sql_helper.blacklist_sql import get_blacklist

                for blacklisted in get_blacklist():
                    if str(chat.chat_id) == blacklisted.chat_id:
                        return
            except Exception:
                pass

            if chat.via_bot_id and not insecure and chat.out:
                return

            try:
                await func(chat)
            except FloodWaitError as fe:
                await chat.client.send_message(
                    send_to,
                    f"`FloodWaitError:\n{str(fe)}\n\nSleeping for {tf(fe.seconds)}`",
                )
                sleep(fe.seconds + 10)
                await chat.client.send_message(
                    send_to,
                    "`UserBot sudah bisa digunakan lagi!`",
                )
            except MessageIdInvalidError:
                pass
            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException:
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**USERBOT ERROR REPORT**\n"
                    text += "Nothing is logged except the fact of error and date."

                    ftext = "========== DISCLAIMER =========="
                    ftext += "\nThis file uploaded ONLY here,"
                    ftext += "\nwe logged only fact of error and date,"
                    ftext += "\nwe respect your privacy,"
                    ftext += "\nyou may not report this error if you've"
                    ftext += "\nany confidential data here, no one will see your data\n"
                    ftext += "================================\n\n"
                    ftext += "--------BEGIN USERBOT TRACEBACK LOG--------\n"
                    ftext += "\nDate: " + date
                    ftext += "\nChat ID: " + str(chat.chat_id)
                    ftext += "\nSender ID: " + str(chat.sender_id)
                    ftext += "\n\nEvent Trigger:\n"
                    ftext += str(chat.text)
                    ftext += "\n\nTraceback info:\n"
                    ftext += str(format_exc())
                    ftext += "\n\nError text:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------END USERBOT TRACEBACK LOG--------"

                    command = 'git log --pretty=format:"%an: %s" -10'

                    ftext += "\n\n\nLast 10 commits:\n"

                    process = await create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) + str(stderr.decode().strip())

                    ftext += result

                    with open("error.txt", "w+") as file:
                        file.write(ftext)

                    if LOGSPAMMER:
                        await chat.respond("`UserBot ERROR! Catatan disimpan pada BOTLOG.`")

                        """
                        async with PasteBin(ftext) as client:
                            await client.post()
                            if client:
                                text += f"\n\nPasted to : [URL]({client.raw_link})"
                        """

                        await chat.client.send_file(send_to, "error.txt", caption=text)
                        os.remove("error.txt")
            else:
                pass

        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator
