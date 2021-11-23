# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.


async def answer(event, text, **args):
    link_preview = args.get("link_preview", False)
    parse_mode = args.get("parse_mode", "md")
    edit = args.get("edit", False)
    if not edit:
        reply = event.reply_to_msg_id if event.reply_to_msg_id else False
        await event.delete()
        await event.client.send_message(
            event.chat_id, text, link_preview=link_preview, parse_mode=parse_mode, reply_to=reply
        )
    else:
        await event.edit(text, link_preview=link_preview, parse_mode=parse_mode)
