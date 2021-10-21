# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from telethon.utils import get_display_name

from notubot import CMD_HELP
from notubot.events import bot_cmd


@bot_cmd(outgoing=True, pattern=r"^\.total(?: |$)(.*)")
async def total(event):
    match = event.pattern_match.group(1)
    await event.edit("`...`")

    if match:
        user = match
    elif event.is_reply:
        user = (await event.get_reply_message()).sender_id
    else:
        user = "me"

    a = await event.client.get_messages(event.chat_id, 0, from_user=user)
    user = await event.client.get_entity(user)
    await event.edit(f"Total pesan dari `{get_display_name(user)}` [`{a.total}`]")


CMD_HELP.update(
    {
        "totalmsg": [
            "Total Message",
            " - `.total [username]/<reply>`: Melihat total pesan pengguna dalam obrolan saat ini.\n",
        ]
    }
)
