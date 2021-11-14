# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio

from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.channels import EditBannedRequest, DeleteMessagesRequest
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin, ChatBannedRights

from notubot.events import bot_cmd

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


@bot_cmd(groups_only=True, admins_only=True, pattern="rocker ?(.*)")
async def rocker(event):
    me = await event.client.get_me()

    opts = event.pattern_match.group(1).strip()
    damnit = ["s", "silent"]
    rockers = True if opts in damnit else False

    if rockers is True:
        await event.delete()
    else:
        await event.edit("`...`")

    async for x in event.client.iter_participants(event.chat_id):
        if x.id == me.id:
            pass
        try:
            if not (
                isinstance(x.participant, ChannelParticipantAdmin)
                or isinstance(x.participant, ChannelParticipantCreator)
            ):
                crying = await event.client(
                    EditBannedRequest(event.chat_id, int(x.id), ChatBannedRights(until_date=None, view_messages=True))
                )
                if rockers is True and crying:
                    if crying.updates[0].id is not None:
                        await event.client(DeleteMessagesRequest(event.chat_id, [crying.updates[0].id]))
        except BaseException:
            pass
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 10)
        await asyncio.sleep(5)

    if rockers is False:
        await event.edit("👏 Congratulations\nFrom now, you have no friends!")


@bot_cmd(groups_only=True, admins_only=True, pattern="gohell ?(.*)")
async def gohell(event):
    me = await event.client.get_me()

    opts = event.pattern_match.group(1).strip()
    damnit = ["s", "silent"]
    lucifer = True if opts in damnit else False

    if lucifer is True:
        await event.delete()
    else:
        await event.edit("`...`")

    async for x in event.client.iter_participants(event.chat_id):
        if x.id == me.id:
            pass
        try:
            if not (
                isinstance(x.participant, ChannelParticipantAdmin)
                or isinstance(x.participant, ChannelParticipantCreator)
            ):
                crying = await event.client(EditBannedRequest(event.chat_id, int(x.id), BANNED_RIGHTS))
                if lucifer is True and crying:
                    if crying.updates[0].id is not None:
                        await event.client(DeleteMessagesRequest(event.chat_id, [crying.updates[0].id]))
        except BaseException:
            pass
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 10)
        await asyncio.sleep(5)

    if lucifer is False:
        await event.edit("You're Lucifer 👁️")
