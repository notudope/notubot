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
    action = event.pattern_match.group(1)
    if action in ["audio", "round", "video"]:
        action = "record-" + action

    seconds = event.pattern_match.group(2)
    if not (seconds or seconds.isdigit()):
        seconds = 60
    else:
        try:
            seconds = int(seconds)
        except BaseException:
            return await event.edit("`Format tidak valid.`")

    act = event.pattern_match.group(1).capitalize()
    await event.edit(f'`Memulai "Fake {act}" selama {seconds} detik.`')
    await asyncio.sleep(5)
    await event.delete()

    async with event.client.action(event.chat_id, action):
        await asyncio.sleep(seconds)


CMD_HELP.update(
    {
        "fakeaction": [
            "Fake Action",
            ">`.ftyping <detik>`\n"
            "↳ : Menampilkan aksi mengetik secara palsu.\n\n"
            ">`.faudio <detik>`\n"
            "↳ : Menampilkan aksi merekam secara palsu.\n\n"
            ">`.fvideo <detik>`\n"
            "↳ : Menampilkan aksi video secara palsu.\n\n"
            ">`.fgame <detik>`\n"
            "↳ : Menampilkan aksi bermain game secara palsu.\n\n"
            ">`.flocation <detik>`\n"
            "↳ : Menampilkan aksi lokasi secara palsu.\n\n"
            ">`.fcontact <detik>`\n"
            "↳ : Menampilkan aksi memilih kontak secara palsu.\n\n"
            ">`.fround <detik>`\n"
            "↳ : Menampilkan aksi pesan video secara palsu.\n\n"
            ">`.fphoto <detik>`\n"
            "↳ : Menampilkan mengirim foto secara palsu.\n\n"
            ">`.fdocument <detik>`\n"
            "↳ : Menampilkan mengirim dokumen secara palsu.",
        ]
    }
)
