# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio

from notubot import (
    CMD_HELP,
    __botversion__,
    __botname__,
    HANDLER,
    bot,
)
from notubot.events import bot_cmd


@bot_cmd(pattern="help(?: |$)(.*)")
async def help(event):
    args = event.pattern_match.group(1).lower()

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
            plugins += f"<code>{str(p)}</code>  |  "
        plugins = plugins[:-3]

        text = f"""<code>{__botname__}</code>
<a href=https://github.com/notudope/notubot>Repo</a>  •  <a href=https://t.me/notudope>Channel</a>  •  <a href=https://t.me/NOTUBOTS>Support</a>  •  <a href=https://t.me/CariTemanOK>Mutualan</a>

😎 <b>Owner:</b> <code>{bot.name}</code>
🤖 <b>Version:</b> <code>v{__botversion__}</code>
📦 <b>Plugin:</b> <code>{len(CMD_HELP)}</code>
👨‍💻 <b>Usage:</b> <code>{HANDLER}help <plugin></code>

Daftar semua plugin beserta perintah tersedia dibawah ini:

{plugins}

📌 <b>Gunakan perintah dengan bijak dan seperlunya, resiko ditanggung pengguna!</b>"""

        await event.edit("⚡")
        await asyncio.sleep(2)
        await event.delete()
        helper = await event.client.send_message(event.chat_id, text, link_preview=False, parse_mode="html")
        await helper.reply(f"**Contoh :** Ketik `{HANDLER}help admin` Untuk informasi pengunaan.")
