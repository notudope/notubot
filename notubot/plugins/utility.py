# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from asyncio.exceptions import TimeoutError
from io import BytesIO
from time import time

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.functions.contacts import GetBlockedRequest
from telethon.tl.functions.messages import GetAllStickersRequest
from telethon.tl.types import Chat, User, Channel
from telethon.utils import get_display_name

from notubot import CMD_HELP
from notubot.events import bot_cmd
from notubot.utils import parse_pre, yaml_format

REQ_ID = "`Kesalahan, dibutuhkan ID atau balas pesan itu.`"


@bot_cmd(pattern="(sa|sg)(?: |$)(.*)")
async def sa(event):
    NotUBot = await event.edit("`Searching...`")
    chat_id = event.chat_id or event.from_id
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        userid = None if reply.sender.bot else reply.sender_id
    elif event.pattern_match.group(1):
        match = event.pattern_match.group(1)
        userid = int(match) if match.isdigit() else None
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await NotUBot.edit(REQ_ID)

    if not userid:
        return await NotUBot.edit(REQ_ID)

    sangmata = "@SangMataInfo_bot"
    try:
        async with event.client.conversation(sangmata) as conv:
            try:
                msg = await conv.send_message(f"/search_id {userid}")
                r = await conv.get_response()
                response = await conv.get_response()
            except YouBlockedUserError:
                return await NotUBot.edit(f"`Unblock {sangmata}`")

            if r.text.startswith("Name"):
                respond = await conv.get_response()
                if len(r.message) > 4096:
                    try:
                        with BytesIO(str.encode(r.message)) as file:
                            file.name = "sangmata.txt"
                            await event.client.send_file(
                                chat_id,
                                file,
                                force_document=True,
                                allow_cache=False,
                                reply_to=event.id,
                            )
                    except Exception:
                        pass
                    await NotUBot.delete()
                else:
                    await NotUBot.edit(f"`{r.message}`")
                await event.client.delete_messages(conv.chat_id, [msg.id, r.id, response.id, respond.id])
                return

            if response.text.startswith("No records") or r.text.startswith("No records"):
                await NotUBot.edit("`Tidak ada riwayat nama.`")
                await event.client.delete_messages(conv.chat_id, [msg.id, r.id, response.id])
                return
            else:
                respond = await conv.get_response()
                if len(response.message) > 4096:
                    try:
                        with BytesIO(str.encode(response.message)) as file:
                            file.name = "sangmata.txt"
                            await event.client.send_file(
                                chat_id,
                                file,
                                force_document=True,
                                allow_cache=False,
                                reply_to=event.id,
                            )
                    except Exception:
                        pass
                    await NotUBot.delete()
                else:
                    await NotUBot.edit(f"```{response.message}```")

            await event.client.delete_messages(conv.chat_id, [msg.id, r.id, response.id, respond.id])
    except TimeoutError:
        return await NotUBot.edit("`Bot tidak merespon, coba lagi nanti!`")


@bot_cmd(
    pattern="stats$",
)
async def stats(
    event: NewMessage.Event,
) -> None:
    NotUBot = await event.edit("`Stats...`")
    start_time = time()
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

    stop_time = time() - start_time
    try:
        ct = (await event.client(GetBlockedRequest(1, 0))).count
    except AttributeError:
        ct = 0
    try:
        sp = await event.client(GetAllStickersRequest(0))
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


@bot_cmd(pattern="(json|raw)$")
async def json(event):
    chat_id = event.chat_id or event.from_id

    reply = await event.get_reply_message() if event.reply_to_msg_id else event
    raw = reply.stringify()

    if len(raw) > 4096:
        try:
            with BytesIO(str.encode(raw)) as file:
                file.name = "raw_data.txt"
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


@bot_cmd(pattern="(yaml|yml)$")
async def yaml(event):
    chat_id = event.chat_id or event.from_id

    reply = await event.get_reply_message() if event.reply_to_msg_id else event
    raw = yaml_format(reply)

    if len(raw) > 4096:
        try:
            with BytesIO(str.encode(raw)) as file:
                file.name = "raw_data.yaml"
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
        "utility": [
            "Utility",
            "`.sa|sg`\n"
            "↳ : Riwayat nama oleh sangmata.\n\n"
            "`.stats`\n"
            "↳ : Stats profile user.\n\n"
            "`.json|raw`\n"
            "↳ : Mengambil raw data format json dari sebuah pesan, \n\n"
            "Balas pesan tersebut untuk menampilkannya!\n\n"
            "`.yaml|yml`\n"
            "↳ : Mengambil raw data format yaml dari sebuah pesan",
        ]
    }
)
