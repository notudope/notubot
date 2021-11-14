# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import io
import time

from telethon.errors import ChatAdminRequiredError
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.functions.channels import LeaveChannelRequest, GetFullChannelRequest
from telethon.tl.functions.contacts import GetBlockedRequest
from telethon.tl.functions.messages import (
    AddChatUserRequest,
    GetFullChatRequest,
    ExportChatInviteRequest,
    GetAllStickersRequest,
)
from telethon.tl.types import Chat, User, Channel
from telethon.utils import get_display_name, pack_bot_file_id

from notubot import CMD_HELP, bot
from notubot.events import bot_cmd
from notubot.utils import parse_pre, yaml_format


@bot_cmd(outgoing=True, pattern="id$")
async def id(event):
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        if reply.media:
            bot_api_file_id = pack_bot_file_id(reply.media)
            await event.edit(
                "ID Grup: `{}`\nID Dari Pengguna: `{}`\nID Bot File API: `{}`".format(
                    str(event.chat_id), str(reply.from_id), bot_api_file_id
                )
            )
        else:
            await event.edit("ID Grup: `{}`\nID Dari Pengguna : `{}`".format(str(event.chat_id), str(reply.from_id)))
    else:
        await event.edit("ID Grup: `{}`".format(str(event.chat_id)))


@bot_cmd(outgoing=True, groups_only=True, pattern="(getlink|link)$")
async def getlink(event):
    chat = await event.get_chat()
    if chat.username:
        return await event.edit(f"Username: @{chat.username}")
    if isinstance(chat, Chat):
        FC = await event.client(GetFullChatRequest(chat.id))
    elif isinstance(chat, Channel):
        FC = await event.client(GetFullChannelRequest(chat.id))

    Inv = FC.full_chat.exported_invite
    if Inv and not Inv.revoked:
        link = Inv.link
    else:
        try:
            r = await event.client(
                ExportChatInviteRequest(event.chat_id),
            )
        except ChatAdminRequiredError:
            return await event.edit("`Tidak memiliki izin!`")
        link = r.link

    await event.edit(f"Link:- {link}")


@bot_cmd(outgoing=True, pattern="kickme$")
async def kickme(event):
    me = await event.client.get_me()
    mention = "[{}](tg://user?id={})".format(get_display_name(me), me.id)
    await event.edit(f"{mention} Goodbye!")
    await event.client(LeaveChannelRequest(event.chat_id))


@bot_cmd(outgoing=True, groups_only=True, pattern="invite ?(.*)")
async def invite(event):
    NotUBot = await event.edit("`...`")
    match = event.pattern_match.group(1)

    for user_id in match.split(" "):
        try:
            await event.client(
                AddChatUserRequest(
                    chat_id=event.chat_id,
                    user_id=user_id,
                    fwd_limit=1000000,
                ),
            )
            await NotUBot.edit(f"Invited `{user_id}`.")
        except Exception as e:
            await NotUBot.edit(str(e))


@bot_cmd(
    pattern="stats$",
)
async def stats(
    event: NewMessage.Event,
) -> None:
    NotUBot = await event.edit("`Collecting stats...`")
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog

    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1

        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1

        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1

        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count

    stop_time = time.time() - start_time
    try:
        ct = (await event.client(GetBlockedRequest(1, 0))).count
    except AttributeError:
        ct = 0
    try:
        sp = await bot(GetAllStickersRequest(0))
        sp_count = len(sp.sets)
    except BaseException:
        sp_count = 0

    me = await event.client.get_me()
    mention = "[{}](tg://user?id={})".format(get_display_name(me), me.id)

    res = f"🔸 **Stats for {mention}** \n\n"
    res += f"**Private Chats:** {private_chats} \n"
    res += f"**  •• **`Users: {private_chats - bots}` \n"
    res += f"**  •• **`Bots: {bots}` \n"
    res += f"**Groups:** {groups} \n"
    res += f"**Channels:** {broadcast_channels} \n"
    res += f"**Admin in Groups:** {admin_in_groups} \n"
    res += f"**  •• **`Creator: {creator_in_groups}` \n"
    res += f"**  •• **`Admin Rights: {admin_in_groups - creator_in_groups}` \n"
    res += f"**Admin in Channels:** {admin_in_broadcast_channels} \n"
    res += f"**  •• **`Creator: {creator_in_channels}` \n"
    res += f"**  •• **`Admin Rights: {admin_in_broadcast_channels - creator_in_channels}` \n"
    res += f"**Unread:** {unread} \n"
    res += f"**Unread Mentions:** {unread_mentions} \n"
    res += f"**Blocked Users:** {ct}\n"
    res += f"**Total Stickers Pack Installed :** `{sp_count}`\n\n"
    res += f"**__It Took:__** {stop_time:.02f}s \n"
    await NotUBot.edit(res)


@bot_cmd(outgoing=True, pattern="(json|raw)$")
async def json(event):
    chat_id = event.chat_id or event.from_id

    reply = await event.get_reply_message() if event.reply_to_msg_id else event
    raw = reply.stringify()

    if len(raw) > 4096:
        try:
            with io.BytesIO(str.encode(raw)) as file:
                await event.client.send_file(
                    chat_id,
                    file,
                    force_document=True,
                    allow_cache=False,
                    reply_to=event.id,
                )
        except Exception:
            pass
        await event.delete()
    else:
        await event.edit(raw, parse_mode=parse_pre)


@bot_cmd(outgoing=True, pattern="(yaml|yml)$")
async def yaml(event):
    chat_id = event.chat_id or event.from_id

    reply = await event.get_reply_message() if event.reply_to_msg_id else event
    raw = yaml_format(reply)

    if len(raw) > 4096:
        try:
            with io.BytesIO(str.encode(raw)) as file:
                await event.client.send_file(
                    chat_id,
                    file,
                    force_document=True,
                    allow_cache=False,
                    reply_to=event.id,
                )
        except Exception:
            pass
        await event.delete()
    else:
        await event.edit(raw, parse_mode=parse_pre)


CMD_HELP.update(
    {
        "chat": [
            "Chat",
            ">`.id`\n"
            "↳ : Mengambil ID obrolan saat ini.\n\n"
            ">`.getlink|link`\n"
            "↳ : Mengambil link obrolan saat ini.\n\n"
            ">`.kickme`\n"
            "↳ : Keluar dari grup sekarang.\n\n"
            ">`.invite`\n"
            "↳ : Mengundang orang ke grup.\n\n"
            ">`.stats`\n"
            "↳ : Stats profile user.\n\n"
            ">`.json|raw`\n"
            "↳ : Mengambil raw data format json dari sebuah pesan, \n\n"
            "Balas pesan tersebut untuk menampilkannya!\n\n"
            ">`.yaml|yml`\n"
            "↳ : Mengambil raw data format yaml dari sebuah pesan",
        ]
    }
)
