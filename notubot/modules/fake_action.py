# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio

from notubot import CMD_HELP
from notubot.events import bot_cmd


@bot_cmd(
    outgoing=True,
    disable_errors=True,
    pattern="^.f(typing|audio|contact|document|game|location|photo|round|video)(?: |$)(.*)",
)
async def fakeaction(event):
    act = event.pattern_match.group(1)
    if act in ["audio", "round", "video"]:
        act = "record-" + act

    seconds = event.pattern_match.group(2)
    if not (seconds or seconds.isdigit()):
        seconds = 60
    else:
        try:
            seconds = int(seconds)
        except BaseException:
            try:
                seconds = await event.ban_time(seconds)
            except BaseException:
                return await event.edit("`Format salah.`")

    await event.edit(f'`Memulai "Fake {act.capitalize()}" selama {seconds} detik.`')
    await asyncio.sleep(5)
    await event.delete()
    async with event.client.action(event.chat_id, act):
        await asyncio.sleep(seconds)


CMD_HELP.update(
    {
        "fakeaction": [
            "Fake Action",
            " - `.ftyping <detik>` : Seakan akan sedang mengetik padahal tidak.\n"
            " - `.faudio <detik>` : Berfungsi sama seperti ftyping tapi ini fake audio.\n"
            " - `.fgame <detik>` : Berfungsi sama seperti ftyping tapi ini fake game.\n"
            " - `.fvideo <detik>` : Berfungsi sama seperti ftyping tapi ini fake video.\n",
        ]
    }
)
