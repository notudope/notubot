# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio
from random import randint
from time import sleep

from notubot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from notubot.events import bot_cmd
from notubot.utils import time_formatter


@bot_cmd(pattern="sleep ([0-9]+)$")
async def sleepy(event):
    counter = int(event.pattern_match.group(1))
    await event.edit("`😴 Tidur...`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"Tidur selama {time_formatter(counter * 1000)}.",
        )

    sleep(counter)
    await event.edit("`Terbangun dari mimpi buruk 😪`")


@bot_cmd(pattern="random")
async def randomise(event):
    itemo = (event.text[8:]).split()

    if len(itemo) < 2:
        return await event.edit("`2 item atau lebih diperlukan!`")

    index = randint(1, len(itemo) - 1)
    await event.edit("**Query: **\n`" + event.text[8:] + "`\n**Output: **\n`" + itemo[index] + "`")


@bot_cmd(pattern="repeat(?: |$)(.*)")
async def repeat(event):
    count, text = event.pattern_match.group(1).split(" ", 1)
    replyCount = int(count)
    replyText = text + "\n"
    for _ in range(0, replyCount - 1):
        replyText += text + "\n"
    await event.edit(replyText)


@bot_cmd(pattern="type(?: |$)(.*)")
async def typing(event):
    match = event.pattern_match.group(1)
    if not match:
        return await event.edit("`Ketikan sebuah pesan.`")

    text = "\u2060" * 602
    NotUBot = await event.edit(text)
    typing_symbol = "|"
    previous_text = ""
    await NotUBot.edit(typing_symbol)
    await asyncio.sleep(0.4)

    for character in match:
        previous_text = previous_text + "" + character
        typing_text = previous_text + "" + typing_symbol
        await NotUBot.edit(typing_text)
        await asyncio.sleep(0.4)
        await NotUBot.edit(previous_text)
        await asyncio.sleep(0.4)


CMD_HELP.update(
    {
        "misc": [
            "Misc",
            "`.sleep <detik>`\n"
            "↳ : Menidurkan beberapa detik.\n\n"
            "`.random <item1> <item2> ... <itemN>`\n"
            "↳ : Mengambil item acak dari daftar item.\n\n"
            "`.repeat <nomor> <teks>`\n"
            "↳ : Mengulang teks untuk beberapa kali.\n\n"
            "`.type <teks>`\n"
            "↳ : Menampilkan seperti mengetik.",
        ]
    }
)
