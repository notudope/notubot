# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import io
import os
import sys
from random import randint
from time import sleep

from notubot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    HEROKU_API_KEY,
    __botname__,
)
from notubot.events import bot_cmd
from notubot.utils import time_formatter
from notubot.utils.format import parse_pre
from notubot.utils.helper import bash, restart


@bot_cmd(outgoing=True, pattern="restart$")
async def restartbot(event):
    await event.edit("`Restarting {} ...`".format(__botname__))

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#bot #restart \n" "Restarting UserBot...")

    try:
        from notubot.plugins.sql_helper.globals import addgvar, delgvar

        delgvar("restartstatus")
        addgvar("restartstatus", f"{event.chat_id}\n{event.id}")
    except AttributeError:
        pass

    await event.client.disconnect()
    if HEROKU_API_KEY:
        return await restart(event)

    await bash("git pull && pip3 install -r requirements.txt")
    os.execl(sys.executable, sys.executable, "-m", "notubot")


@bot_cmd(outgoing=True, pattern="shutdown$")
async def shutdown(event):
    await event.edit("`Shutting down {} ...`".format(__botname__))

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#bot #shutdown \n" "Shutting down UserBot...")

    await event.client.disconnect()


@bot_cmd(outgoing=True, pattern="sleep ([0-9]+)$")
async def sleepy(event):
    counter = int(event.pattern_match.group(1))
    await event.edit("`😴 Tidur...`")

    sleep(2)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"Tidur selama {time_formatter(counter * 1000)}.",
        )

    sleep(counter)
    await event.edit("`Terbangun dari mimpi buruk 😪`")


@bot_cmd(outgoing=True, pattern="random")
async def randomise(event):
    itemo = (event.text[8:]).split()

    if len(itemo) < 2:
        return await event.edit("`2 item atau lebih diperlukan!`")

    index = randint(1, len(itemo) - 1)
    await event.edit("**Query: **\n`" + event.text[8:] + "`\n**Output: **\n`" + itemo[index] + "`")


@bot_cmd(outgoing=True, pattern="repeat ?(.*)")
async def repeat(event):
    count, text = event.pattern_match.group(1).split(" ", 1)
    replyCount = int(count)
    replyText = text + "\n"
    for _ in range(0, replyCount - 1):
        replyText += text + "\n"
    await event.edit(replyText)


@bot_cmd(outgoing=True, pattern="(json|raw)$")
async def json(event):
    chat_id = event.chat_id or event.from_id

    reply = await event.get_reply_message() if event.reply_to_msg_id else event
    raw = reply.stringify()

    if len(json) > 4096:
        with io.BytesIO(str.encode(raw)) as file:
            await event.client.send_file(
                chat_id,
                file,
                force_document=True,
                allow_cache=False,
                reply_to=event.id,
            )
            await event.delete()
    else:
        await event.edit(raw, parse_mode=parse_pre)


CMD_HELP.update(
    {
        "misc": [
            "Misc",
            ">`.restart`\n"
            "↳ : Muat ulang UserBot.\n\n"
            ">`.shutdown`\n"
            "↳ : Mematikan UserBot.\n\n"
            ">`.sleep <detik>`\n"
            "↳ : Menidurkan beberapa detik.\n\n"
            ">`.random <item1> <item2> ... <itemN>`\n"
            "↳ : Mengambil item acak dari daftar item.\n\n"
            ">`.repeat <nomor> <teks>`\n"
            "↳ : Mengulang teks untuk beberapa kali.\n\n"
            ">`.json|raw`\n"
            "↳ : Mengambil data json dari sebuah pesan, \n"
            "Balas pesan tersebut untuk menampilkannya!",
        ]
    }
)
