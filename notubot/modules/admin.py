# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from asyncio import sleep
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    RightForbiddenError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError, UserIdInvalidError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest, EditPhotoRequest
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
    PeerChat,
    ChannelParticipantsKicked,
)
from telethon.tl.types import ChannelParticipantCreator as owner
from telethon.tl.types import ChannelParticipantAdmin as admin
from telethon.utils import get_display_name

from notubot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from notubot.events import bot_cmd

# =================== CONSTANT ===================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin!`"
NO_PERM = "`I don't have sufficient permissions!`"
NO_SQL = "`Running on Non-SQL mode!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = "`Some issue with updating the pic,`" "`maybe coz I'm not an admin,`" "`or don't have enough rights.`"
INVALID_MEDIA = "`Invalid Extension`"

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

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================


def user_list(ls, n):
    for i in range(0, len(ls), n):
        yield ls[i : i + n]


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.setgpic$")
async def set_group_photo(event):
    """For .setgpic command, changes the picture of a group"""
    if not event.is_group:
        await event.edit("`I don't think this is a group.`")
        return
    replymsg = await event.get_reply_message()
    photo = None

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await event.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await event.client.download_file(replymsg.media.document)
        else:
            await event.edit(INVALID_MEDIA)

    if photo:
        try:
            await event.client(EditPhotoRequest(event.chat_id, await event.client.upload_file(photo)))
            await event.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await event.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await event.edit(PP_ERROR)


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.promote(?: |$)(.*)")
async def promote(event):
    """For .promote command, promotes the replied/tagged person"""
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )

    await event.edit("`Promoting...`")
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "Administrator"  # Just in case.
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
        await event.edit("`Promoted Successfully!`")
    except RightForbiddenError:
        return await event.edit(NO_PERM)

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        return await event.edit(NO_PERM)

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)",
        )


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.demote(?: |$)(.*)")
async def demote(event):
    """For .demote command, demotes the replied/tagged person"""
    # If passing, declare that we're going to demote
    await event.edit("`Demoting...`")
    rank = "admeme"  # dummy rank, lol.
    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return

    # New rights after demotion
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    # Edit Admin Permission
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        return await event.edit(NO_PERM)
    await event.edit("`Demoted Successfully!`")

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)",
        )


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.ban(?: |$)(.*)")
async def ban(event):
    """For .ban command, bans the replied/tagged person"""
    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    # Announce that we're going to whack the pest
    await event.edit("`Whacking the pest!`")

    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await event.edit(NO_PERM)
    # Helps ban group join spammers more easily
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await event.edit("`I dont have message nuking rights! But still he was banned!`")
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later
    if reason:
        await event.edit(f"`{str(user.id)}` was banned !!\nReason: {reason}")
    else:
        await event.edit(f"`{str(user.id)}` was banned !!")
    # Announce to the logging group if we have banned the person
    # successfully!
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)",
        )


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.unban(?: |$)(.*)")
async def unban(event):
    """For .unban command, unbans the replied/tagged person"""
    # If everything goes well...
    await event.edit("`Unbanning...`")

    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await event.edit("```Unbanned Successfully```")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await event.edit("`Uh oh my unban logic broke!`")


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, pattern=r"^\.mute(?: |$)(.*)")
async def muter(event):
    """
    This function is basically muting peeps
    """
    # Check if the function running under SQL mode
    try:
        from notubot.modules.sql_helper.spam_mute_sql import mute
    except AttributeError:
        return await event.edit(NO_SQL)

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    self_user = await event.client.get_me()

    if user.id == self_user.id:
        return await event.edit("`Hands too short, can't duct tape myself...\n(ヘ･_･)ヘ┳━┳`")

    # If everything goes well, do announcing and mute
    await event.edit("`Gets a tape!`")
    if mute(event.chat_id, user.id) is False:
        return await event.edit("`Error! User probably already muted.`")
    else:
        try:
            await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))

            # Announce that the function is done
            if reason:
                await event.edit(f"`Safely taped !!`\nReason: {reason}")
            else:
                await event.edit("`Safely taped !!`")

            # Announce to logging group
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "#MUTE\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {event.chat.title}(`{event.chat_id}`)",
                )
        except UserIdInvalidError:
            return await event.edit("`Uh oh my mute logic broke!`")
        except UserAdminInvalidError:
            pass


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.unmute(?: |$)(.*)")
async def unmuter(event):
    """For .unmute command, unmute the replied/tagged person"""
    # Check if the function running under SQL mode
    try:
        from notubot.modules.sql_helper.spam_mute_sql import unmute
    except AttributeError:
        return await event.edit(NO_SQL)

    # If admin or creator, inform the user and start unmuting
    await event.edit("```Unmuting...```")
    user = await get_user_from_event(event)
    user = user[0]
    if user:
        pass
    else:
        return

    if unmute(event.chat_id, user.id) is False:
        return await event.edit("`Error! User probably already unmuted.`")
    else:

        try:
            await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
            await event.edit("```Unmuted Successfully```")
        except UserIdInvalidError:
            return await event.edit("`Uh oh my unmute logic broke!`")
        except UserAdminInvalidError:
            pass

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)",
            )


@bot_cmd(incoming=True, disable_errors=True)
async def muters(event):
    """Used for deleting the messages of muted people"""
    try:
        from notubot.modules.sql_helper.gmute_sql import is_gmuted
        from notubot.modules.sql_helper.spam_mute_sql import is_muted
    except AttributeError:
        return
    muted = is_muted(event.chat_id)
    gmuted = is_gmuted(event.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(event.sender_id):
                try:
                    await event.delete()
                    await event.client(EditBannedRequest(event.chat_id, event.sender_id, rights))
                except (
                    BadRequestError,
                    UserAdminInvalidError,
                    ChatAdminRequiredError,
                    UserIdInvalidError,
                ):
                    await event.client.send_read_acknowledge(event.chat_id, event.id)
    for i in gmuted:
        if i.sender == str(event.sender_id):
            await event.delete()


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.ungmute(?: |$)(.*)")
async def ungmuter(event):
    """For .ungmute command, ungmutes the target in the userbot"""
    # Check if the function running under SQL mode
    try:
        from notubot.modules.sql_helper.gmute_sql import ungmute
    except AttributeError:
        await event.edit(NO_SQL)
        return

    user = await get_user_from_event(event)
    user = user[0]
    if not user:
        return

    # If pass, inform and start ungmuting
    await event.edit("```Ungmuting...```")

    if ungmute(user.id) is False:
        await event.edit("`Error! User probably not gmuted.`")
    else:
        # Inform about success
        await event.edit("```Ungmuted Successfully```")
        await sleep(3)
        await event.delete()

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNGMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)",
            )


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.gmute(?: |$)(.*)")
async def gmuter(event):
    """For .gmute command, globally mutes the replied/tagged person"""
    # Check if the function running under SQL mode
    try:
        from notubot.modules.sql_helper.gmute_sql import gmute
    except AttributeError:
        await event.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(event)
    if not user:
        return

    # If pass, inform and start gmuting
    await event.edit("`Grabs a huge, sticky duct tape!`")
    if gmute(user.id) is False:
        await event.edit("`Error! User probably already gmuted.\nRe-rolls the tape.`")
    else:
        if reason:
            await event.edit(f"`Globally taped!`\nReason: {reason}")
        else:
            await event.edit("`Globally taped!`")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)",
            )


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, pattern=r"^\.all($| (.*))")
async def all(event):
    text = (event.pattern_match.group(1)).strip()
    users = []
    limit = 0

    if event.fwd_from:
        return

    async for x in event.client.iter_participants(event.chat_id):
        if not (x.bot or x.deleted):
            if not (isinstance(x.participant, admin) or isinstance(x.participant, owner)):
                users.append(f"[{get_display_name(x)}](tg://user?id={x.id})")
            if isinstance(x.participant, admin):
                users.append(f"👮 [{get_display_name(x)}](tg://user?id={x.id})")
            if isinstance(x.participant, owner):
                users.append(f"🤴 [{get_display_name(x)}](tg://user?id={x.id})")

    mentions = list(user_list(users, 6))
    for mention in mentions:
        try:
            mention = " | ".join(map(str, mention))
            if text:
                mention = f"{text}\n{mention}"
            if event.reply_to_msg_id:
                await event.client.send_message(event.chat_id, mention, reply_to=event.message.reply_to_msg_id)
            else:
                await event.client.send_message(event.chat_id, mention)

            limit += 6
            await sleep(2)
        except BaseException:
            pass

    await event.delete()


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, pattern=r"^\.zombies(?: |$)(.*)")
async def rm_deletedacc(event):
    """For .zombies command, list all the ghost/deleted/zombie accounts in a chat."""

    con = event.pattern_match.group(1).lower()
    del_u = 0
    del_status = "`No deleted accounts found, Group is clean`"

    if con != "clean":
        await event.edit("`Searching for ghost/deleted/zombie accounts...`")
        async for user in event.client.iter_participants(event.chat_id):

            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = (
                f"`Found` **{del_u}** `ghost/deleted/zombie account(s) in this group,"
                "\nclean them by using .zombies clean`"
            )
        return await event.edit(del_status)

    await event.edit("`Deleting deleted accounts...\nOh I can do that?!?!`")
    del_u = 0
    del_a = 0

    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                return await event.edit("`I don't have ban rights in this group`")
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"

    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) " f"\n**{del_a}** deleted admin accounts are not removed"
    await event.edit(del_status)
    await sleep(2)
    await event.delete()

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#CLEANUP\n" f"Cleaned **{del_u}** deleted account(s) !!" f"\nCHAT: {event.chat.title}(`{event.chat_id}`)",
        )


@bot_cmd(outgoing=True, groups_only=True, disable_errors=True, pattern=r"^\.admins$")
async def get_admin(event):
    """For .admins command, list all of the admins of the chat."""
    info = await event.client.get_entity(event.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f"<b>Admins in {title}:</b> \n"
    try:
        async for user in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                mentions += f"\n{link}"
            else:
                mentions += f"\nDeleted Account <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await event.edit(mentions, parse_mode="html")


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.pin(?: |$)(.*)")
async def pin(event):
    """For .pin command, pins the replied/tagged message on the top the chat."""
    to_pin = event.reply_to_msg_id

    if not to_pin:
        return await event.edit("`Reply to a message to pin it.`")

    options = event.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await event.client(UpdatePinnedMessageRequest(event.to_id, to_pin, is_silent))
    except BadRequestError:
        return await event.edit(NO_PERM)

    await event.edit("`Pinned Successfully!`")

    user = await get_user_from_id(event.sender_id, event)

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)\n"
            f"LOUD: {not is_silent}",
        )


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.kick(?: |$)(.*)")
async def kick(event):
    """For .kick command, kicks the replied/tagged person from the group."""
    user, reason = await get_user_from_event(event)
    if not user:
        return await event.edit("`Couldn't fetch user.`")

    await event.edit("`Kicking...`")

    try:
        await event.client.kick_participant(event.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        return await event.edit(NO_PERM + f"\n{str(e)}")

    if reason:
        await event.edit(f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}")
    else:
        await event.edit(f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)\n",
        )


@bot_cmd(outgoing=True, groups_only=True, disable_errors=True, pattern=r"^\.users ?(.*)")
async def get_users(event):
    """For .users command, list all of the users in a chat."""
    info = await event.client.get_entity(event.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f"Users in {title}: \n"
    try:
        if not event.pattern_match.group(1):
            async for user in event.client.iter_participants(event.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = event.pattern_match.group(1)
            async for user in event.client.iter_participants(event.chat_id, search=f"{searchq}"):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await event.edit(mentions)
    except MessageTooLongError:
        await event.edit("Damn, this is a huge group. Uploading users lists as file.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await event.client.send_file(
            event.chat_id,
            "userslist.txt",
            caption=f"Users in {title}",
            reply_to=event.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """Get the user from argument or replied message."""
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.edit("`Pass the user's username, id or reply!`")

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.edit(str(err))

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))

    return user_obj


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, disable_errors=True, pattern=r"^\.usersdel ?(.*)")
async def get_usersdel(event):
    """For .usersdel command, list all of the deleted users in a chat."""
    info = await event.client.get_entity(event.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f"deletedUsers in {title}: \n"
    try:
        if not event.pattern_match.group(1):
            async for user in event.client.iter_participants(event.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
        #       else:
        #                mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = event.pattern_match.group(1)
            async for user in event.client.iter_participants(event.chat_id, search=f"{searchq}"):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
        #       else:
    #              mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await event.edit(mentions)
    except MessageTooLongError:
        await event.edit("Damn, this is a huge group. Uploading deletedusers lists as file.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await event.client.send_file(
            event.chat_id,
            "deleteduserslist.txt",
            caption=f"Users in {title}",
            reply_to=event.id,
        )
        remove("deleteduserslist.txt")


async def get_userdel_from_event(event):
    """Get the deleted user from argument or replied message."""
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.edit("`Pass the deleted user's username, id or reply!`")

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.edit(str(err))

    return user_obj, extra


async def get_userdel_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        return await event.edit(str(err))

    return user_obj


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, pattern=r"^\.bots$")
async def get_bots(event):
    """For .bots command, list all of the bots of the chat."""
    info = await event.client.get_entity(event.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f"<b>Bots in {title}:</b>\n"
    try:
        if isinstance(event.to_id, PeerChat):
            return await event.edit("`I heard that only Supergroups can have bots.`")
        else:
            async for user in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsBots):
                if not user.deleted:
                    link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                    userid = f"<code>{user.id}</code>"
                    mentions += f"\n{link} {userid}"
                else:
                    mentions += f"\nDeleted Bot <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await event.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await event.edit("Damn, too many bots here. Uploading bots list as file.")
        file = open("botlist.txt", "w+")
        file.write(mentions)
        file.close()
        await event.client.send_file(
            event.chat_id,
            "botlist.txt",
            caption=f"Bots in {title}",
            reply_to=event.id,
        )
        remove("botlist.txt")


@bot_cmd(outgoing=True, groups_only=True, admins_only=True, pattern=r"^\.(allunban|unbanall)(?: |$)(.*)")
async def allunban(event):
    await event.edit("`Mencari daftar blokir...`")
    p = 0
    (await event.get_chat()).title
    async for i in event.client.iter_participants(
        event.chat_id,
        filter=ChannelParticipantsKicked,
        aggressive=True,
    ):
        try:
            await event.client.edit_permissions(event.chat_id, i, view_messages=True)
            p += 1
        except BaseException:
            pass

    await event.edit("`Berhasil unbanned semua daftar blokir.`")


CMD_HELP.update(
    {
        "admin": [
            "Admin",
            " - `.promote <username/reply> <custom rank (optional)>` : Provides admin rights to the person in the chat.\n"
            " - `.demote <username/reply>` : Revokes the person's admin permissions in the chat.\n"
            " - `.ban <username/reply> <reason (optional)>` : Bans the person off your chat.\n"
            " - `.unban <username/reply>` : Removes the ban from the person in the chat.\n"
            " - `.mute <username/reply> <reason (optional)>` : Mutes the person in the chat, works on admins too.\n"
            " - `.unmute <username/reply>` : Removes the person from the muted list.\n"
            " - `.gmute <username/reply> <reason (optional)>` : Mutes the person in all groups you have in common with them.\n"
            " - `.ungmute <username/reply>` : Reply someone's message with .ungmute to remove them from the gmuted list.\n"
            " - `.zombies` : Searches for deleted accounts in a group.\n"
            "Use .zombies clean to remove deleted accounts from the group.\n"
            " - `.all` : Tag all member in the group chat.\n"
            " - `.admins` : Retrieves a list of admins in the chat.\n"
            " - `.bots` : Retrieves a list of bots in the chat.\n"
            " - `.users <name of member>` : Retrieves all (or queried) users in the chat.\n"
            " - `.setgppic <reply to image>` : Changes the group's display picture.\n"
            " - `.allunban` : Unbanned all members thought group.\n",
        ]
    }
)
