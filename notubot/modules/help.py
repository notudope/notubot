# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio

from notubot import (
    CMD_HELP,
    BOT_VER,
    ALIVE_NAME,
    BOT_NAME,
)
from notubot.events import bot_cmd


@bot_cmd(outgoing=True, pattern=r"^\.help(?: |$)(.*)")
async def help(event):
    """For .help command."""
    args = event.pattern_match.group(1).lower()

    if args:
        if args in CMD_HELP:
            await event.edit(f"Module **{CMD_HELP[args][0]}**:\n\n" + str(CMD_HELP[args][1]))
        else:
            await event.edit(f"😐 Module [`{args}`] tidak ada! Ketik ```.help``` untuk melihat nama module yang benar.")
            await asyncio.sleep(200)
            await event.delete()
    else:
        modules = ""
        for index in CMD_HELP:
            modules += f"`{str(index)}`  |  "
        modules = modules[:-2]

        text = f"""`{BOT_NAME}`
[REPO](https://github.com/notudope/notubot)  /  [Channel](https://t.me/notudope)  /  [Grup](https://t.me/NOTUBOTS)

😎 **Owner :** __{ALIVE_NAME}__
🤖 **Version :** `v{BOT_VER}`
📦 **Module :** `{len(CMD_HELP)}`
👨‍💻 **Usage :** `.help <nama module>`

Daftar semua module beserta perintah tersedia dibawah ini:

{modules}

📌 **Gunakan perintah dengan bijak dan seperlunya, resiko ditanggung pengguna!**"""

        await event.edit("⚡")
        await asyncio.sleep(0.5)
        await event.delete()
        helper = await event.client.send_message(
            event.chat_id,
            text,
            link_preview=False,
        )
        await helper.reply(f"\n**Contoh** : Ketik <`.help admin`> Untuk informasi pengunaan.")
        await asyncio.sleep(1000)
        await helper.delete()
