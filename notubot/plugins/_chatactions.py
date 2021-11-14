# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from telethon.events import ChatAction
from telethon.utils import get_display_name

from notubot import bot
from notubot.plugins.sql_helper.gban_sql import is_gbanned
from notubot.plugins.sql_helper.gmute_sql import is_gmuted
from notubot.plugins.sql_helper.mute_sql import is_muted


@bot.on(ChatAction)
async def ChatActionsHandler(event):
    if not event.user_joined or not event.user_added or not event.added_by:
        return

    user = await event.get_user()
    chat = await event.get_chat()
    mention = "[{}](tg://user?id={})".format(get_display_name(user), user.id)

    if chat.admin_rights or chat.creator:
        gban = is_gbanned(user.id)
        if gban:
            try:
                await event.client.edit_permissions(
                    chat.id,
                    user.id,
                    view_messages=False,
                )
                text = "#GBanned_User Joined.\n\n**User** : {}\n**Reason**: {}\n\n`User Banned.`".format(mention, gban)
                return await event.reply(text)
            except Exception:
                pass

        if is_gmuted(user.id):
            try:
                await event.client.edit_permissions(chat.id, user.id, until_date=None, send_messages=False)
                text = "#GMuted_User Joined.\n\n**User** : {}\n\n`User Muted.`".format(mention)
                return await event.reply(text)
            except Exception:
                pass

        muted = is_muted(user.id, chat.id)
        if muted:
            for i in muted:
                if str(i.sender) == str(user.id):
                    try:
                        await event.client.edit_permissions(
                            event.chat.id, user.id, until_date=None, send_messages=False
                        )
                    except Exception:
                        pass
