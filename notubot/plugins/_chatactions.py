# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from telethon.events import ChatAction
from telethon.utils import get_display_name

from notubot import bot
from notubot.database.gban_sql import is_gbanned
from notubot.database.gmute_sql import is_gmuted
from notubot.database.mute_sql import is_muted


@bot.on(ChatAction)
async def ChatActionsHandler(event):
    if event.user_joined or event.user_added or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        mention = "[{}](tg://user?id={})".format(get_display_name(user), user.id)

        if chat.admin_rights or chat.creator:
            if is_gbanned(user.id):
                try:
                    await event.client.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    text = "#GBanned_User Joined.\n\n**User** : {}\n**Reason**: {}\n\n`User Banned.`".format(
                        mention, is_gbanned(user.id).reason
                    )
                    await event.reply(text)
                except Exception:
                    pass

            if is_gmuted(user.id):
                try:
                    await event.client.edit_permissions(chat.id, user.id, until_date=None, send_messages=False)
                    text = "#GMuted_User Joined.\n\n**User** : {}\n\n`User Muted.`".format(mention)
                    await event.reply(text)
                except Exception:
                    pass

            muted = is_muted(user.id, chat.id)
            if muted:
                for m in muted:
                    if str(m.sender) == str(user.id):
                        try:
                            await event.client.edit_permissions(
                                event.chat.id, user.id, until_date=None, send_messages=False
                            )
                        except Exception:
                            pass
