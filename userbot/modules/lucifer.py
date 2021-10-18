import asyncio
import time

from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import EditBannedRequest, DeleteMessagesRequest
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin, ChatBannedRights

from userbot.events import register

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


@register(outgoing=True, groups_only=True, admins_only=True, pattern=r"^\.rocker(?: |$)(.*)")
async def rocker(event):
    user = await event.get_chat()
    me = await event.client.get_me()

    opts = event.pattern_match.group(1).strip()
    damnit = ["s", "silent"]
    rockers = True if opts in damnit else False

    if rockers is True:
        await event.delete()
    else:
        await event.edit("`Sedang memproses...`")
    async for user in event.client.iter_participants(event.chat_id):
        if user.id == me.id:
            pass
        try:
            if not (
                isinstance(user.participant, ChannelParticipantAdmin)
                or isinstance(user.participant, ChannelParticipantCreator)
            ):
                crying = await event.client(
                    EditBannedRequest(
                        event.chat_id, int(user.id), ChatBannedRights(until_date=None, view_messages=True)
                    )
                )
                if rockers is True and crying:
                    if crying.updates[0].id is not None:
                        await event.client(DeleteMessagesRequest(event.chat_id, [crying.updates[0].id]))
        except BaseException:
            pass
        except FloodWaitError as e:
            time.sleep(e.seconds)
        except Exception as e:
            await event.edit(str(e))
        await asyncio.sleep(1)
    if rockers is False:
        await event.edit(f"👏 Congratulations\nFrom now, you have no friends!")


@register(outgoing=True, groups_only=True, admins_only=True, pattern=r"^\.gohell(?: |$)(.*)")
async def gohell(event):
    user = await event.get_chat()
    me = await event.client.get_me()

    opts = event.pattern_match.group(1).strip()
    damnit = ["s", "silent"]
    lucifer = True if opts in damnit else False

    if lucifer is True:
        await event.delete()
    else:
        await event.edit("`Sedang memproses...`")
    async for user in event.client.iter_participants(event.chat_id):
        if user.id == me.id:
            pass
        try:
            if not (
                isinstance(user.participant, ChannelParticipantAdmin)
                or isinstance(user.participant, ChannelParticipantCreator)
            ):
                crying = await event.client(EditBannedRequest(event.chat_id, int(user.id), BANNED_RIGHTS))
                if lucifer is True and crying:
                    if crying.updates[0].id is not None:
                        await event.client(DeleteMessagesRequest(event.chat_id, [crying.updates[0].id]))
        except BaseException:
            pass
        except FloodWaitError as e:
            time.sleep(e.seconds)
        except Exception as e:
            await event.edit(str(e))
        await asyncio.sleep(1)
    if lucifer is False:
        await event.edit(f"You're Lucifer 👁️")
