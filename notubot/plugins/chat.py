# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from telethon.errors import ChatAdminRequiredError
from telethon.tl.functions.channels import LeaveChannelRequest, GetFullChannelRequest, InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest, GetFullChatRequest, ExportChatInviteRequest
from telethon.tl.types import Chat, Channel
from telethon.utils import pack_bot_file_id, get_display_name

from notubot import CMD_HELP, bot
from notubot.events import bot_cmd


@bot_cmd(pattern="(getid|id)$")
async def getid(event):
    NotUBot = await event.edit("`...`")
    chat_id = event.chat_id or event.from_id
    if event.reply_to_msg_id:
        await event.get_input_chat()
        reply = await event.get_reply_message()
        userid = reply.sender_id
        if reply.media:
            bot_api_file_id = pack_bot_file_id(reply.media)
            await NotUBot.edit(
                "**Chat ID:** `{}`\n**User ID:** `{}`\n**Bot API File ID:** `{}`\n**Message ID:** `{}`".format(
                    chat_id, userid, bot_api_file_id, reply.id
                )
            )
        else:
            text = (
                f"**User ID:** `{userid}`" if event.is_private else f"**Chat ID:** `{chat_id}`\n**User ID:** `{userid}`"
            )
            text = text + f"\n**Message ID:** `{reply.id}`"
            await NotUBot.edit(text)
    else:
        text = "**User ID:** " if event.is_private else "**Chat ID:** "
        text = f"{text}`{chat_id}`" + f"\n**Message ID:** `{event.id}`"
        await NotUBot.edit(text)


@bot_cmd(groups_only=True, pattern="(getlink|link)$")
async def getlink(event):
    NotUBot = await event.edit("`...`")
    chat = await event.get_chat()
    if chat.username:
        return await NotUBot.edit(f"Username: @{chat.username}")
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
            return await NotUBot.edit("`Tidak memiliki izin!`")
        link = r.link

    await NotUBot.edit(f"Link:- {link}")


@bot_cmd(pattern="uname$")
async def uname(event):
    NotUBot = await event.edit("`...`")
    reply = await event.get_reply_message()
    if not reply:
        return await NotUBot.edit("`Balas pesan dia untuk mendapatkan usernamenya.`")

    username = reply.sender.username or None
    mention = f"@{username}" if username else f"[{reply.sender_id}](tg://user?id={reply.sender_id})"
    await NotUBot.edit(mention)


@bot_cmd(pattern="kickme$")
async def kickme(event):
    NotUBot = await event.edit("`...`")
    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    await NotUBot.edit(f"{mention} `Leaved!`")
    await event.client(LeaveChannelRequest(event.chat_id))


@bot_cmd(groups_only=True, pattern="invite(?: |$)(.*)")
async def inviteuser(event):
    NotUBot = await event.edit("`...`")
    to_add_users = event.pattern_match.group(1)
    if not event.is_channel and event.is_group:
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    AddChatUserRequest(
                        chat_id=event.chat_id,
                        user_id=user_id,
                        fwd_limit=1000000,
                    ),
                )
                await NotUBot.edit(f"Invited `{user_id}` to `{event.chat_id}`")
            except Exception as e:
                await NotUBot.edit(str(e))
    else:
        for user_id in to_add_users.split(" "):
            try:
                await event.client(
                    InviteToChannelRequest(
                        channel=event.chat_id,
                        users=[user_id],
                    ),
                )
                await NotUBot.edit(f"Invited `{user_id}` to `{event.chat_id}`")
            except Exception as e:
                await NotUBot.edit(str(e))


@bot_cmd(pattern="total(?: |$)(.*)")
async def total(event):
    NotUBot = await event.edit("`...`")
    match = event.pattern_match.group(1)

    if match:
        user = match
    elif event.is_reply:
        user = (await event.get_reply_message()).sender_id
    else:
        user = "me"

    a = await event.client.get_messages(event.chat_id, 0, from_user=user)
    user = await event.client.get_entity(user)
    await NotUBot.edit(f"Total pesan dari `{get_display_name(user)}` [`{a.total}`]")


CMD_HELP.update(
    {
        "chat": [
            "Chat",
            "`.getid|id`\n"
            "↳ : Mengambil ID obrolan saat ini.\n\n"
            "`.getlink|link`\n"
            "↳ : Mengambil link obrolan saat ini.\n\n"
            "`.uname`\n"
            "↳ : Mengambil username orang yang dibalas.\n\n"
            "`.kickme`\n"
            "↳ : Keluar dari grup sekarang.\n\n"
            "`.invite`\n"
            "↳ : Mengundang orang ke grup.\n\n"
            "`.total <username/reply>`\n"
            "↳ : Melihat total pesan pengguna dalam obrolan saat ini.\n\n",
        ]
    }
)
