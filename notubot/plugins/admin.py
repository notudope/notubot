# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from asyncio import sleep

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    RightForbiddenError,
    UserAdminInvalidError,
    ChatNotModifiedError,
)
from telethon.tl.functions.channels import GetParticipantRequest  # noqa: F401
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest, EditPhotoRequest
from telethon.tl.functions.messages import SetHistoryTTLRequest, EditChatDefaultBannedRightsRequest
from telethon.tl.types import (
    ChannelParticipantsKicked,
    ChatAdminRights,
    ChatBannedRights,
    MessageMediaPhoto,
    InputMessagesFilterPinned,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)
from telethon.tl.types import ChannelParticipantsAdmins as Admins
from telethon.tl.types import ChannelParticipantAdmin as Admin
from telethon.tl.types import ChannelParticipantCreator as Creator
from telethon.utils import get_display_name

from notubot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    DEVLIST,
    HANDLER,
    bot,
)
from notubot.database.mute_sql import is_muted, mute, unmute
from notubot.events import bot_cmd
from notubot.utils import get_user_from_event, get_uinfo, get_user_id  # noqa: F401

NO_PERM = "`Tidak memiliki izin!`"
FAILED = "`Gagal melakukan aksi!`"
REQ_ID = "`Kesalahan, dibutuhkan ID atau balas pesan itu.`"

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

KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

CHATLOCK_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    send_polls=True,
    invite_users=True,
    change_info=True,
    pin_messages=True,
)

CHATUNLOCK_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    send_polls=None,
    invite_users=True,
    change_info=True,
    pin_messages=True,
)


def user_list(ls, n):
    for i in range(0, len(ls), n):
        yield ls[i : i + n]


@bot_cmd(groups_only=True, admins_only=True, can_promote=True, pattern="promote(?: |$)(.*)")
async def promote(event):
    NotUBot = await event.edit("`Promoting...`")
    await event.get_chat()
    user, rank = await get_uinfo(event)
    rank = rank or "Admin"
    if not user:
        return await NotUBot.edit(REQ_ID)

    try:
        new_rights = ChatAdminRights(
            add_admins=False,
            invite_users=True,
            change_info=False,
            ban_users=True,
            delete_messages=True,
            pin_messages=False,
            anonymous=False,
            manage_call=True,
        )

        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except RightForbiddenError:
        return await NotUBot.edit(NO_PERM)
    except BadRequestError:
        return await NotUBot.edit(NO_PERM)

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title} [`{event.chat_id}`]",
        )

    await NotUBot.edit("`promoted`")


@bot_cmd(groups_only=True, admins_only=True, can_promote=True, pattern="demote(?: |$)(.*)")
async def demote(event):
    NotUBot = await event.edit("`Demoting...`")
    await event.get_chat()
    user, rank = await get_uinfo(event)
    rank = rank or "Not Admin"
    if not user:
        return await NotUBot.edit(REQ_ID)

    try:
        new_rights = ChatAdminRights(
            add_admins=None,
            invite_users=None,
            change_info=None,
            ban_users=None,
            delete_messages=None,
            pin_messages=None,
            anonymous=None,
            manage_call=None,
        )
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await NotUBot.edit(NO_PERM)

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title} [`{event.chat_id}`]",
        )

    await NotUBot.edit("`demoted`")


@bot_cmd(groups_only=True, admins_only=True, can_promote=True, pattern="(fpromote|fullpromote)(?: |$)(.*)")
async def fpromote(event):
    NotUBot = await event.edit("`Promoting...`")
    await event.get_chat()
    user, rank = await get_uinfo(event)
    rank = rank or "CoFounder"
    if not user:
        return await NotUBot.edit(REQ_ID)

    try:
        new_rights = ChatAdminRights(
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True,
            anonymous=False,
            manage_call=True,
        )

        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except RightForbiddenError:
        return await NotUBot.edit(NO_PERM)
    except BadRequestError:
        return await NotUBot.edit(NO_PERM)

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#FULLPROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title} [`{event.chat_id}`]",
        )

    await NotUBot.edit("`promoted`")


@bot_cmd(groups_only=True, admins_only=True, can_ban=True, pattern="kick(?: |$)(.*)")
async def kick(event):
    if "kickme" in event.text:
        return

    NotUBot = await event.edit("`Kicking...`")
    await event.get_chat()
    user, reason = await get_uinfo(event)
    if not user:
        return await NotUBot.edit(REQ_ID)

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(user.id)), user.id)
    location = "{} [`{}`]".format((await event.get_chat()).title, event.chat_id)

    if user.id == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")
    if user.id in DEVLIST:
        return await NotUBot.edit("😑 **Gagal Kick, dia pembuatku!**")

    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, KICK_RIGHTS))
    except BaseException:
        return await NotUBot.edit(FAILED)

    reason = reason if reason else "None given."
    text = f"""**#Kicked** by {mention}
**User:** {userlink}
**Aksi:** `Kicked`
**Alasan:** `{reason}`
**Grup:** {location}"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(groups_only=True, admins_only=True, can_ban=True, pattern="ban(?: |$)(.*)")
async def ban(event):
    NotUBot = await event.edit("`Banning...`")
    await event.get_chat()
    user, reason = await get_uinfo(event)
    if not user:
        return await NotUBot.edit(REQ_ID)

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(user.id)), user.id)
    location = "{} [`{}`]".format((await event.get_chat()).title, event.chat_id)

    if user.id == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")
    if user.id in DEVLIST:
        return await NotUBot.edit("😑 **Gagal Banned, dia pembuatku!**")

    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BaseException:
        return await NotUBot.edit(FAILED)

    reason = reason if reason else "None given."
    text = f"""**#Banned** by {mention}
**User:** {userlink}
**Aksi:** `Banned`
**Alasan:** `{reason}`
**Grup:** {location}"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(groups_only=True, admins_only=True, can_ban=True, pattern="unban(?: |$)(.*)")
async def unban(event):
    NotUBot = await event.edit("`Unbanning...`")
    await event.get_chat()
    user, reason = await get_uinfo(event)
    if not user:
        return await NotUBot.edit(REQ_ID)

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(user.id)), user.id)
    location = "{} [`{}`]".format((await event.get_chat()).title, event.chat_id)

    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
    except BaseException:
        return await NotUBot.edit(FAILED)

    text = f"""**#UnBanned** by {mention}
**User:** {userlink}
**Aksi:** `UnBanned`
**Grup:** {location}"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(groups_only=True, admins_only=True, pattern="mute(?: |$)(.*)")
async def muter(event):
    NotUBot = await event.edit("`Muting...`")
    await event.get_chat()
    user, reason = await get_uinfo(event)
    if not user:
        return await NotUBot.edit(REQ_ID)

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(user.id)), user.id)
    location = "{} [`{}`]".format((await event.get_chat()).title, event.chat_id)

    if user.id == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")
    if user.id in DEVLIST:
        return await NotUBot.edit("😑 **Gagal Mute, dia pembuatku!**")

    if is_muted(user.id, event.chat_id):
        return await NotUBot.edit("`User sudah terkena Mute.`")

    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
        mute(user.id, event.chat_id)
    except BaseException:
        return await NotUBot.edit(FAILED)

    reason = reason if reason else "None given."
    text = f"""**#Muted** by {mention}
**User:** {userlink}
**Aksi:** `Muted`
**Alasan:** `{reason}`
**Grup:** {location}"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(groups_only=True, admins_only=True, pattern="unmute(?: |$)(.*)")
async def unmuter(event):
    NotUBot = await event.edit("`Unmuting...`")
    await event.get_chat()
    user, reason = await get_uinfo(event)
    if not user:
        return await NotUBot.edit(REQ_ID)

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(user.id)), user.id)
    location = "{} [`{}`]".format((await event.get_chat()).title, event.chat_id)

    if not is_muted(user.id, event.chat_id):
        return NotUBot.edit("`User tidak terkena Mute.`")

    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        unmute(user.id, event.chat_id)
    except BaseException:
        return await NotUBot.edit(FAILED)

    text = f"""**#UnMuted** by {mention}
**User:** {userlink}
**Aksi:** `UnMuted`
**Grup:** {location}"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(groups_only=True, admins_only=True, pattern="lock$")
async def lock(event):
    NotUBot = await event.edit("`Locking...`")
    try:
        await event.client(EditChatDefaultBannedRightsRequest(event.chat_id, CHATLOCK_RIGHTS))
    except ChatNotModifiedError:
        return await NotUBot.edit("`Grup sudah dikunci.`")

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#LOCK\n" f"CHAT: {event.chat.title} [`{event.chat_id}`]")

    await NotUBot.edit("`locked`")


@bot_cmd(groups_only=True, admins_only=True, pattern="unlock$")
async def unlock(event):
    NotUBot = await event.edit("`Unlocking...`")
    try:
        await event.client(EditChatDefaultBannedRightsRequest(event.chat_id, CHATUNLOCK_RIGHTS))
    except ChatNotModifiedError:
        return await NotUBot.edit("`Grup sudah dibuka.`")

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#UNLOCK\n" f"CHAT: {event.chat.title} [`{event.chat_id}`]")

    await NotUBot.edit("`unlocked`")


@bot_cmd(pattern="pin$")
async def pin(event):
    if not event.is_reply:
        return await event.edit("`Balas pesan tersebut!`")

    reply = await event.get_reply_message()
    try:
        await event.client.pin_message(event.chat_id, reply.id, notify=False)
    except BadRequestError:
        return await event.edit(NO_PERM)

    await event.edit("`pinned`")
    await sleep(5)
    await event.delete()


@bot_cmd(pattern="unpin($| (.*))")
async def unpin(event):
    NotUBot = await event.edit("`...`")
    match = event.pattern_match.group(1)
    msg = None
    if event.is_reply:
        msg = event.reply_to_msg_id
    elif match != "all":
        return await NotUBot.edit("Balas pesan tersebut, atau, gunakan `.unpin all`")

    try:
        await event.client.unpin_message(event.chat_id, msg)
    except BadRequestError:
        return await NotUBot.edit(NO_PERM)

    await NotUBot.edit("`unpinned`")
    await sleep(5)
    await NotUBot.delete()


@bot_cmd(pattern="listpinned$")
async def get_all_pinned(event):
    NotUBot = await event.edit("`...`")
    chat_id = (str(event.chat_id)).replace("-100", "")
    chat_name = (await event.get_chat()).title
    a = ""
    c = 1

    async for i in event.client.iter_messages(event.chat_id, filter=InputMessagesFilterPinned):
        if i.message:
            t = " ".join(i.message.split()[0:4])
            txt = "{}....".format(t)
        else:
            txt = "Pergi ke pesan"
        a += f"{c}. <a href=https://t.me/c/{chat_id}/{i.id}>{txt}</a>\n"
        c += 1

    if c == 1:
        m = f"<b>Pinned {chat_name}:</b>\n\n"
    else:
        m = f"<b>Pesan Pinned di {chat_name}:</b>\n\n"

    if a == "":
        return await NotUBot.edit("`no pinned`")

    await NotUBot.edit(m + a, parse_mode="html")


@bot_cmd(groups_only=True, admins_only=True, pattern="autodelete(?: |$)(.*)")
async def autodelte(event):
    match = event.pattern_match.group(1)
    if not match or match not in ["24h", "7d", "1m", "off"]:
        return event.edit("`Gunakan sesuai format.`")

    if match == "24h":
        tt = 3600 * 24
    elif match == "7d":
        tt = 3600 * 24 * 7
    elif match == "1m":
        tt = 3600 * 24 * 31
    else:
        tt = 0

    try:
        await event.client(SetHistoryTTLRequest(event.chat_id, period=tt))
    except ChatNotModifiedError:
        return event.edit(f"Auto Delete sama dengan `{match}`")

    await event.edit(f"Auto Delete `{match}`")


@bot_cmd(groups_only=True, admins_only=True, disable_errors=True, pattern="(setgpic|setpic)$")
async def set_group_photo(event):
    NotUBot = await event.edit("`...`")
    reply = await event.get_reply_message()
    photo = None

    if reply and reply.media:
        if isinstance(reply.media, MessageMediaPhoto):
            photo = await event.client.download_media(message=reply.photo)
        elif "image" in reply.media.document.mime_type.split("/"):
            photo = await event.client.download_file(reply.media.document)
        else:
            await NotUBot.edit("`Media tidak valid.`")

    if photo:
        try:
            await event.client(EditPhotoRequest(event.chat_id, await event.client.upload_file(photo)))
            await NotUBot.edit("`Berhasil mengubah profile grup.`")
        except PhotoCropSizeSmallError:
            await NotUBot.edit("`Gambar terlalu kecil.`")
        except ImageProcessFailedError:
            await NotUBot.edit("`Gagal memproses gambar.`")


@bot_cmd(groups_only=True, admins_only=True, can_ban=True, pattern="(zombies|delusers)(?: |$)(.*)")
async def zombies(event):
    match = event.pattern_match.group(1).lower()
    deleted_user = 0
    status = "`Tidak ada akun terhapus.`"
    await event.get_chat()
    if match != "clean":
        await event.edit("`Mencari akun terhapus...`")

        async for x in event.client.iter_participants(event.chat_id, aggressive=True):
            if x.deleted:
                deleted_user += 1
                await sleep(1)

        if deleted_user > 0:
            status = (
                f"Menemukan `{deleted_user}` akun terhapus di grup ini,"
                "\nBersihkan itu dengan `{HANDLER}zombies clean`"
            )
        return await event.edit(status)

    await event.edit("🧹 `Membersihkan akun terhapus...`")
    deleted_user = 0
    deleted_admin = 0

    async for x in event.client.iter_participants(event.chat_id, aggressive=True):
        if x.deleted:
            try:
                await event.client(EditBannedRequest(event.chat_id, x.id, BANNED_RIGHTS))
            except UserAdminInvalidError:
                deleted_user -= 1
                deleted_admin += 1

            await event.client(EditBannedRequest(event.chat_id, x.id, UNBAN_RIGHTS))
            deleted_user += 1

    if deleted_user > 0:
        status = f"Dibersihkan `{deleted_user}` akun terhapus"

    if deleted_admin > 0:
        status = (
            f"Dibersihkan `{deleted_user}` akun terhapus "
            f"\n`{deleted_admin}` akun terhapus admin tidak dapat dibersihkan."
        )

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#ZOMBIES\n" f"CLEANED: `{deleted_user}`\n" f"CHAT: {event.chat.title} [`{event.chat_id}`]",
        )

    await event.edit(status)


@bot_cmd(groups_only=True, admins_only=True, can_ban=True, pattern="(allunban|unbanall)$")
async def allunban(event):
    await event.edit("`...`")
    success = 0
    title = (await event.get_chat()).title
    async for x in event.client.iter_participants(
        event.chat_id,
        filter=ChannelParticipantsKicked,
        aggressive=True,
    ):
        try:
            await event.client(EditBannedRequest(event.chat_id, x, UNBAN_RIGHTS))
            success += 1
            await sleep(2)
        except BaseException:
            pass

    await event.edit(f"{title}: `{success}` unbanned.")


@bot_cmd(groups_only=True, pattern="(staff|adminlist)$")
async def staff(event):
    await event.edit("`...`")
    title = (await event.get_chat()).title
    mentions = f"<b>Admin {title}</b>\n"

    try:
        async for x in event.client.iter_participants(event.chat_id, filter=Admins):
            if not (x.deleted or x.participant.admin_rights.anonymous):
                link = f"<a href=tg://user?id={x.id}>{get_display_name(x)}</a>"
                mentions += f"\n{link}"
    except ChatAdminRequiredError as e:
        mentions += " " + str(e) + "\n"

    await event.edit(mentions, parse_mode="html")


@bot_cmd(groups_only=True, pattern="member$")
async def member(event):
    await event.edit("`...`")
    title = (await event.get_chat()).title
    mentions = f"<b>Member {title}</b>\n"

    try:
        async for x in event.client.iter_participants(event.chat_id, 100):
            if not (x.deleted or x.bot or x.participant.admin_rights.anonymous):
                link = f"<a href=tg://user?id={x.id}>{get_display_name(x)}</a>"
                mentions += f"\n{link}"
    except ChatAdminRequiredError as e:
        mentions += " " + str(e) + "\n"

    await event.edit(mentions, parse_mode="html")


@bot_cmd(groups_only=True, admins_only=True, pattern="evo|@everyone$")
async def everyone(event):
    """
    await event.delete()
    mentions = "@everyone"
    chat = await event.get_input_chat()

    async for x in event.client.iter_participants(chat):
        mentions += f"[\u2063](tg://user?id={x.id})"

    await event.client.send_message(chat, mentions, reply_to=event.message.reply_to_msg_id)
    """

    tag = "\U000e0020everyone"
    mention_text = f"@{tag}"
    mention_slots = 4096 - len(mention_text)

    chat = await event.get_chat()
    async for x in event.client.iter_participants(chat, aggressive=True):
        if not (x.deleted or x.bot or x.participant.admin_rights.anonymous or x.id == bot.uid):
            mention_text += f"[\u200b](tg://user?id={x.id})"
            mention_slots -= 1
            if mention_slots == 0:
                break

    await event.respond(mention_text, mode="repost")


@bot_cmd(groups_only=True, admins_only=True, pattern="all(?: |$)(.*)|@all(?: |$)(.*)")
async def all(event):
    text = event.pattern_match.group(1)
    users = []
    limit = 0
    await event.get_chat()

    async for x in event.client.iter_participants(event.chat_id, aggressive=True):
        if not (x.deleted or x.bot or x.participant.admin_rights.anonymous or x.id == bot.uid):
            if not (isinstance(x.participant, (Admin, Creator))):
                users.append(f" <a href=tg://user?id={x.id}>{get_display_name(x)}</a> ")
            if isinstance(x.participant, Admin):
                users.append(f"\n👮 Admin: <a href=tg://user?id={x.id}>{get_display_name(x)}</a> ")
            if isinstance(x.participant, Creator):
                users.append(f"\n🤴 Owner: <a href=tg://user?id={x.id}>{get_display_name(x)}</a> ")

    for mention in list(user_list(users, 6)):
        mention = "  |  ".join(map(str, mention))
        mention = f"{text}\n{mention}" if text else mention

        if event.reply_to_msg_id:
            await event.client.send_message(event.chat_id, mention, reply_to=event.reply_to_msg_id, parse_mode="html")
        else:
            await event.client.send_message(event.chat_id, mention, parse_mode="html")

        limit += 6
        await sleep(5)

    await event.delete()


@bot_cmd(
    pattern="rmusers(?: |$)(.*)",
    groups_only=True,
    admins_only=True,
)
async def rmusers(event):
    NotUBot = await event.edit("`...`")
    match = event.pattern_match.group(1)
    p, b, c, d, m, n, y, w, o, q, r = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    async for x in event.client.iter_participants(event.chat_id, aggressive=True):
        p += 1
        if isinstance(x.status, UserStatusEmpty):
            if "empty" in match:
                try:
                    await event.client(EditBannedRequest(event.chat_id, x, KICK_RIGHTS))
                    c += 1
                    await sleep(0.5)
                except BaseException:
                    pass
            else:
                y += 1
        if isinstance(x.status, UserStatusLastMonth):
            if "month" in match:
                try:
                    await event.client(EditBannedRequest(event.chat_id, x, KICK_RIGHTS))
                    c += 1
                    await sleep(0.5)
                except BaseException:
                    pass
            else:
                m += 1
        if isinstance(x.status, UserStatusLastWeek):
            if "week" in match:
                try:
                    await event.client(EditBannedRequest(event.chat_id, x, KICK_RIGHTS))
                    c += 1
                    await sleep(0.5)
                except BaseException:
                    pass
            else:
                w += 1
        if isinstance(x.status, UserStatusOffline):
            if "offline" in match:
                try:
                    await event.client(EditBannedRequest(event.chat_id, x, KICK_RIGHTS))
                    c += 1
                    await sleep(0.5)
                except BaseException:
                    pass
            else:
                o += 1
        if isinstance(x.status, UserStatusOnline):
            if "online" in match:
                try:
                    await event.client(EditBannedRequest(event.chat_id, x, KICK_RIGHTS))
                    c += 1
                    await sleep(0.5)
                except BaseException:
                    pass
            else:
                q += 1
        if isinstance(x.status, UserStatusRecently):
            if "recently" in match:
                try:
                    await event.client(EditBannedRequest(event.chat_id, x, KICK_RIGHTS))
                    c += 1
                    await sleep(0.5)
                except BaseException:
                    pass
            else:
                r += 1
        if x.bot:
            if "bot" in match:
                try:
                    await event.client(EditBannedRequest(event.chat_id, x, KICK_RIGHTS))
                    c += 1
                    await sleep(0.5)
                except BaseException:
                    pass
            else:
                b += 1
        elif x.deleted:
            if "deleted" in match:
                try:
                    await event.client(EditBannedRequest(event.chat_id, x, KICK_RIGHTS))
                    c += 1
                    await sleep(0.5)
                except BaseException:
                    pass
            else:
                d += 1
        elif x.status is None:
            if "none" in match:
                try:
                    await event.client(EditBannedRequest(event.chat_id, x, KICK_RIGHTS))
                    c += 1
                    await sleep(0.5)
                except BaseException:
                    pass
            else:
                n += 1
    if match:
        res = f"**>> Kicked** `{c} / {p}` **users**\n\n"
    else:
        res = f"**>> Total** `{p}` **users**\n\n"
    res += f"  `{HANDLER}rmusers deleted`  **••**  `{d}`\n"
    res += f"  `{HANDLER}rmusers empty`  **••**  `{y}`\n"
    res += f"  `{HANDLER}rmusers month`  **••**  `{m}`\n"
    res += f"  `{HANDLER}rmusers week`  **••**  `{w}`\n"
    res += f"  `{HANDLER}rmusers offline`  **••**  `{o}`\n"
    res += f"  `{HANDLER}rmusers online`  **••**  `{q}`\n"
    res += f"  `{HANDLER}rmusers recently`  **••**  `{r}`\n"
    res += f"  `{HANDLER}rmusers bot`  **••**  `{b}`\n"
    res += f"  `{HANDLER}rmusers none`  **••**  `{n}`"
    await NotUBot.edit(res)


CMD_HELP.update(
    {
        "admin": [
            "Admin",
            "`.promote <username/id/reply> <title (optional)>`\n"
            "↳ : Promote user menjadi admin.\n\n"
            "`.demote <username/id/reply>`\n"
            "↳ : Demote seorang admin.\n\n"
            "`.fpromote|fullpromote <username/id/reply> <title (optional)>`\n"
            "↳ : Promote user menjadi cofounder.\n\n"
            "`.kick <username/id/reply> <reason (optional)>`\n"
            "↳ : Kick user dari grup.\n\n"
            "`.ban <username/id/reply> <reason (optional)>`\n"
            "↳ : Banned user dari grup.\n\n"
            "`.unban <username/id/reply>`\n"
            "↳ : Unbanned user dari grup.\n\n"
            "`.mute <username/id/reply> <reason (optional)>`\n"
            "↳ : Mute user dari grup.\n\n"
            "`.unmute <username/id/reply>`\n"
            "↳ : Unmute user dari grup.\n\n"
            "`.lock`\n"
            "↳ : Kunci grup, biarkan user hanya membaca.\n\n"
            "`.unlock`\n"
            "↳ : Buka kunci grup, user dapat mengirim pesan.\n\n"
            "`.pin <reply to message>`\n"
            "↳ : Pin pesan pada obrolan.\n\n"
            "`.unpin <all> <reply to message>`\n"
            "↳ : Unpin pesan pada obrolan.\n\n"
            "`.listpinned`\n"
            "↳ : Menampilkan semua pesan pinned.\n\n"
            "`.autodelete <24h/7d/1m/off>`\n"
            "↳ : Mengaktifkan Auto Delete pesan pada grup.\n\n"
            "`.setgpic|setpic`\n"
            "↳ : Mengubah profile grup.\n\n"
            "`.zombies <clean>`\n"
            "↳ : Mencari dan menghapus akun terhapus pada grup.\n\n"
            "`.staff|adminlist`\n"
            "↳ : Cek daftar admin grup.\n\n"
            "`.allunban|unbanall`\n"
            "↳ : Unbanned semua member grup yang diblokir.\n\n"
            "`.all|@all`\n"
            "↳ : Mention semua member grup.\n\n"
            "`.rmusers`\n"
            "↳ : Membersihkan user spesial.",
        ]
    }
)
