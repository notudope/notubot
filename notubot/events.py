# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio
import inspect
import re
from datetime import datetime
from io import BytesIO
from pathlib import Path
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
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin as Admin
from telethon.tl.types import ChannelParticipantCreator as Creator
from telethon.utils import get_display_name

from notubot import (
    BOTLOG_CHATID,
    bot,
    __botversion__,
    __botname__,
    BOTLOG,
    LOGS,
    CMD_LIST,
    I_DEV,
    HANDLER,
)
from notubot.functions import time_formatter

FLOOD_WAIT = 0


def compile_pattern(data, handler):
    if HANDLER == " ":
        return re.compile("^" + data.replace("^", "").replace(".", ""))
    return (
        re.compile(handler + data.replace("^", "").replace(".", ""))
        if data.startswith("^")
        else re.compile(handler + data)
    )


def bot_cmd(**args):
    args["func"] = lambda e: not e.fwd_from and not e.via_bot_id
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    pattern: str = args.get("pattern", None)
    disable_edited: bool = args.get("disable_edited", False)
    admins_only: bool = args.get("admins_only", False)
    groups_only: bool = args.get("groups_only", False)
    private_only: bool = args.get("private_only", False)
    trigger_on_fwd: bool = args.get("trigger_on_fwd", False)
    disable_errors: bool = args.get("disable_errors", False)
    insecure: bool = args.get("insecure", False)
    only_devs: bool = args.get("only_devs", False)
    can_promote: bool = args.get("can_promote", False)
    can_ban: bool = args.get("can_ban", False)
    can_call: bool = args.get("can_call", False)
    # allow_sudo: bool = args.get("allow_sudo", False)

    if pattern:
        args["pattern"] = compile_pattern(pattern, "\\" + HANDLER)
        reg = re.compile("(.*)")
        try:
            cmd = re.search(reg, pattern)
            try:
                cmd = (
                    cmd.group(1)
                    .replace("$", "")
                    .replace("?(.*)", "")
                    .replace("(.*)", "")
                    .replace("(?: |)", "")
                    .replace("| ", "")
                    .replace("( |)", "")
                    .replace("?((.|//)*)", "")
                    .replace("?P<shortname>\\w+", "")
                )
            except BaseException:
                pass
            try:
                CMD_LIST[file_test].append(cmd)
            except BaseException:
                CMD_LIST.update({file_test: [cmd]})
        except BaseException:
            pass

    for i in [
        "admins_only",
        "groups_only",
        "private_only",
        "disable_edited",
        "trigger_on_fwd",
        "disable_errors",
        "insecure",
        "only_devs",
        "can_promote",
        "can_ban",
        "can_call",
        "allow_sudo",
    ]:
        if i in args:
            del args[i]

    def decorator(func):
        async def wrapper(event):
            send_to = BOTLOG_CHATID if BOTLOG else event.chat_id or event.from_id

            if not trigger_on_fwd and event.fwd_from:
                return

            if only_devs and not I_DEV:
                return await event.respond(
                    f"**⚠️ Developer Restricted!**\nHarap **tentukan variabel** `I_DEV` untuk mengaktifkan perintah developer.\n\nMungkin ini berbahaya."
                )

            if groups_only and event.is_private:
                await event.delete()
                return await event.respond("`Gunakan perintah itu dalam grup/channel!`")

            if private_only and not event.is_private:
                await event.delete()
                return await event.respond("`Gunakan perintah itu dalam obrolan pribadi!`")

            if admins_only:
                if event.is_private:
                    await event.delete()
                    return await event.respond("`Gunakan perintah itu dalam grup/channel!`")

                p = await event.client(GetParticipantRequest(event.chat_id, event.sender_id))
                if not isinstance(p.participant, (Admin, Creator)):
                    await event.delete()
                    return await event.respond("`Bukan admin disini!`")
                if can_promote and not p.participant.admin_rights.add_admins:
                    await event.delete()
                    return await event.respond("`Bukan Owner/Co-Founder disini!`")
                if can_ban and not p.participant.admin_rights.ban_users:
                    await event.delete()
                    return await event.respond("`Tidak punya izin mengeluarkan orang!`")
                if can_call and not p.participant.admin_rights.manage_call:
                    await event.delete()
                    return await event.respond("`Tidak punya izin akses obrolan!`")

            try:
                from notubot.database.blacklist_sql import get_blacklist

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
                    text += "**Teruskan pesan ini ke** @NOTUBOTS"
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

                    if BOTLOG:
                        await event.respond(f"`{__botname__} ERROR, Disimpan ke BOTLOG.`")
                    try:
                        with BytesIO(str.encode(ftext)) as file:
                            file.name = "logs.txt"
                            await event.client.send_file(
                                send_to,
                                file,
                                caption=text,
                                force_document=True,
                                allow_cache=False,
                            )
                    except Exception:
                        if not BOTLOG:
                            await event.respond(
                                f"`{__botname__} ERROR, nilai BOTLOG bukan True pada variabel config. Catatan kesalahan hanya bisa dilihat pada terminal atau views logs (heroku).`"
                            )
                        else:
                            pass
            else:
                pass

        args["outgoing"] = True
        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        del args["outgoing"]
        return wrapper

    return decorator
