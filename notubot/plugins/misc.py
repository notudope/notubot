# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import io
import sys
from os import environ, execle
from random import randint
from time import sleep

from notubot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    bot,
    __botname__,
)
from notubot.events import bot_cmd
from notubot.utils import time_formatter
from notubot.utils.format import parse_pre


@bot_cmd(outgoing=True, pattern=r"^\.restart$")
async def restart(event):
    await event.edit("`Restarting {} ...`".format(__botname__))

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#bot #restart \n" "Restarting UserBot...")

    try:
        from notubot.plugins.sql_helper.globals import addgvar, delgvar

        delgvar("restartstatus")
        addgvar("restartstatus", f"{event.chat_id}\n{event.id}")
    except AttributeError:
        pass

    args = [sys.executable, "-m", "notubot"]
    execle(sys.executable, *args, environ)


@bot_cmd(outgoing=True, pattern=r"^\.shutdown$")
async def shutdown(event):
    await event.edit("`Shutting down {} ...`".format(__botname__))

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#bot #shutdown \n" "Shutting down UserBot...")

    await bot.disconnect()


@bot_cmd(outgoing=True, pattern=r"^\.sleep ([0-9]+)$")
async def sleepy(event):
    counter = int(event.pattern_match.group(1))
    await event.edit("`I am sulking and snoozing...`")

    if BOTLOG:
        str_counter = time_formatter(counter * 1000)
        await event.client.send_message(
            BOTLOG_CHATID,
            f"You put the bot to sleep for {str_counter}.",
        )

    sleep(counter)
    await event.edit("`OK, I'm awake now.`")


@bot_cmd(outgoing=True, pattern=r"^\.random")
async def randomise(items):
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        return await items.edit("`2 or more items are required! Check .help random for more info.`")
    index = randint(1, len(itemo) - 1)
    await items.edit("**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" + itemo[index] + "`")


@bot_cmd(outgoing=True, pattern=r"^\.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(" ", 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for _ in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@bot_cmd(outgoing=True, pattern=r"^\.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit("`Check the userbot log for the decoded message data !!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Here's the decoded message data !!`",
        )


@bot_cmd(outgoing=True, pattern=r"^\.json$")
async def json(event):
    reply = await event.get_reply_message() if event.reply_to_msg_id else event
    await event.edit(reply.stringify(), parse_mode=parse_pre)


CMD_HELP.update(
    {
        "misc": [
            "Misc",
            ">`.restart`\n"
            "↳ : Restarts the bot.\n\n"
            ">`.shutdown`\n"
            "↳ : Shutdown bot.\n\n"
            ">`.sleep <detik>`\n"
            "↳ : Let yours snooze for a few seconds.\n\n"
            ">`.random <item1> <item2> ... <itemN>`\n"
            "↳ : Get a random item from the list of items.\n\n"
            ">`.repeat <no> <text>`\n"
            "↳ : Repeats the text for a number of times. Don't confuse this with spam tho.\n\n"
            ">`.raw`\n"
            "↳ : Get detailed JSON-like formatted data about replied message.\n\n"
            ">`.json`\n"
            "↳ : Mengambil data json dari sebuah pesan, \n"
            "Balas pesan tersebut untuk menampilkannya!",
        ]
    }
)
