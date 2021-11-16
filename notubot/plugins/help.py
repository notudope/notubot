# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio

from telethon.utils import get_display_name

from notubot import (
    CMD_HELP,
    __botversion__,
    __botname__,
    HANDLER,
)
from notubot.events import bot_cmd


@bot_cmd(pattern="help(?: |$)(.*)")
async def help(event):
    args = event.pattern_match.group(1).lower()
    me = await event.client.get_entity("me")

    if args:
        if args in CMD_HELP:
            await event.edit(
                f"📦 Plugin **{CMD_HELP[args][0]}** `{HANDLER}help {args}`\n\n"
                + str(CMD_HELP[args][1]).replace("`.", f"• `{HANDLER}")
            )
        else:
            await event.edit(
                f"😡 Plugin [`{args}`] tidak ada! Ketik `{HANDLER}help` untuk melihat nama plugin yang benar."
            )
    else:
        plugins = ""
        for p in CMD_HELP:
            plugins += f"`{str(p)}`  |  "
        plugins = plugins[:-3]

        text = f"""`{__botname__}`
[Repo](https://github.com/notudope/notubot)  •  [Channel](https://t.me/notudope)  •  [Support](https://t.me/NOTUBOTS)  •  [Mutualan](https://t.me/CariTemanOK)

😎 **Owner:** `{get_display_name(me)}`
🤖 **Version:** `v{__botversion__}`
📦 **Plugin:** `{len(CMD_HELP)}`
👨‍💻 **Usage:** `{HANDLER}help <plugin>`

Daftar semua plugin beserta perintah tersedia dibawah ini:

{plugins}

📌 **Gunakan perintah dengan bijak dan seperlunya, resiko ditanggung pengguna!**"""

        await event.edit("⚡")
        await asyncio.sleep(2)
        await event.delete()
        helper = await event.client.send_message(
            event.chat_id,
            text,
            link_preview=False,
        )
        await helper.reply(f"**Contoh :** Ketik `{HANDLER}help admin` Untuk informasi pengunaan.")
