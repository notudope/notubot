# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from telethon.tl.types import MessageEntityMentionName

from notubot import LOGS


async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None

    try:
        if args:
            user = args[0]
            if len(args) > 1:
                extra = "".join(args[1:])
            if user.isnumeric() or (user.startswith("-") and user[1:].isnumeric()):
                user = int(user)

            if event.message.entities:
                probable_mention = event.message.entities[0]
                if isinstance(probable_mention, MessageEntityMentionName):
                    user_id = probable_mention.user_id
                    user_obj = await event.client.get_entity(user_id)
                    return user_obj, extra

            if isinstance(user, int) or user.startswith("@"):
                user_obj = await event.client.get_entity(user)
                return user_obj, extra
    except Exception as e:
        LOGS.error(str(e))

    try:
        extra = event.pattern_match.group(1)
        if event.is_private:
            user_obj = await event.get_chat()
            return user_obj, extra

        if event.reply_to_msg_id:
            prev_msg = await event.get_reply_message()
            if not prev_msg.from_id:
                return None, None

            user_obj = await event.client.get_entity(prev_msg.sender_id)
            return user_obj, extra

        if not args:
            return None, None
    except Exception as e:
        LOGS.error(str(e))

    return None, None


async def get_uinfo(event):
    user, data = None, None
    if event.reply_to:
        user = (await event.get_reply_message()).sender
        data = event.pattern_match.group(1)
    else:
        ok = event.pattern_match.group(1).split(maxsplit=1)
        if len(ok) >= 1:
            usr = ok[0]
            if usr.isdigit():
                usr = int(usr)
            try:
                user = await event.client.get_entity(usr)
            except BaseException:
                if str(usr).isdigit():
                    user.id = usr
                    user.first_name = usr
                else:
                    pass
            if len(ok) == 2:
                data = ok[1]

    return user, data


async def get_user_id(id, event):
    if str(id).isdigit() or str(id).startswith("-"):
        if str(id).startswith("-100"):
            userid = int(str(id).replace("-100", ""))
        elif str(id).startswith("-"):
            userid = int(str(id).replace("-", ""))
        else:
            userid = int(id)
    else:
        try:
            userid = (await event.client.get_entity(id)).id
        except BaseException:
            userid = None

    return userid
