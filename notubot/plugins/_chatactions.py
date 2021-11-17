# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from telethon.events import ChatAction
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import get_display_name

from notubot import bot
from notubot.database.gban_sql import is_gbanned
from notubot.database.gmute_sql import is_gmuted
from notubot.database.mute_sql import is_muted

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

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)


@bot.on(ChatAction)
async def ChatActionsHandler(event):
    if event.user_joined or event.user_added or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        mention = "[➥ {}](tg://user?id={})".format(get_display_name(user), user.id)

        if chat.admin_rights or chat.creator:
            gban = is_gbanned(user.id)
            if gban:
                try:
                    await event.delete()
                    await event.client(EditBannedRequest(chat.id, user.id, BANNED_RIGHTS))
                    text = "#GBanned_User Joined\n\n**User:** {}\n**Reason:** {}\n\n`User Banned`".format(
                        mention, gban.reason
                    )
                    await event.reply(text)
                except Exception:
                    pass

            if is_gmuted(user.id):
                try:
                    await event.delete()
                    await event.client(EditBannedRequest(chat.id, user.id, MUTE_RIGHTS))
                    text = "#GMuted_User Joined\n\n**User:** {}\n\n`User Muted`".format(mention)
                    await event.reply(text)
                except Exception:
                    pass

            muted = is_muted(user.id, chat.id)
            if muted:
                for m in muted:
                    if str(m.sender) == str(user.id):
                        try:
                            await event.delete()
                            await event.client(EditBannedRequest(chat.id, user.id, MUTE_RIGHTS))
                        except Exception:
                            pass
