# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from telethon.errors import ChatAdminRequiredError
from telethon.tl.functions.channels import LeaveChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest, GetFullChatRequest, ExportChatInviteRequest
from telethon.tl.types import Chat, Channel
from telethon.utils import pack_bot_file_id, get_display_name

from notubot import CMD_HELP, bot
from notubot.events import bot_cmd


@bot_cmd(pattern="(getid|id)$")
async def id(event):
    chat_id = event.chat_id or event.from_id
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        userid = reply.sender_id
        if reply.media:
            bot_api_file_id = pack_bot_file_id(reply.media)
            await event.edit(f"Group: `{chat_id}`\nUser: `{userid}`\nBot File API: `{bot_api_file_id}`")
        else:
            text = f"User: `{userid}`" if event.is_private else f"Group: `{chat_id}`\nUser: `{userid}`"
            await event.edit(text)
    else:
        text = "User: " if event.is_private else "Group: "
        await event.edit(f"{text}`{chat_id}`")


@bot_cmd(groups_only=True, pattern="(getlink|link)$")
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


@bot_cmd(pattern="kickme$")
async def kickme(event):
    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    await event.edit(f"{mention} `Leaved!`")
    await event.client(LeaveChannelRequest(event.chat_id))


@bot_cmd(groups_only=True, pattern="invite(?: |$)(.*)")
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


@bot_cmd(pattern="total(?: |$)(.*)")
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
        "chat": [
            "Chat",
            "`.getid|id`\n"
            "↳ : Mengambil ID obrolan saat ini.\n\n"
            "`.getlink|link`\n"
            "↳ : Mengambil link obrolan saat ini.\n\n"
            "`.kickme`\n"
            "↳ : Keluar dari grup sekarang.\n\n"
            "`.invite`\n"
            "↳ : Mengundang orang ke grup.\n\n"
            "`.total <username/reply>`\n"
            "↳ : Melihat total pesan pengguna dalam obrolan saat ini.\n\n",
        ]
    }
)
