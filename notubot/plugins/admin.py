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
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest, EditPhotoRequest
from telethon.tl.functions.messages import SetHistoryTTLRequest, EditChatDefaultBannedRightsRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantCreator,
    ChannelParticipantAdmin,
    ChatAdminRights,
    ChatBannedRights,
    MessageMediaPhoto,
    ChannelParticipantsKicked,
    InputMessagesFilterPinned,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)
from telethon.utils import get_display_name

from notubot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    DEVLIST,
    HANDLER,
)
from notubot.events import bot_cmd
from notubot.plugins.sql_helper.mute_sql import is_muted, mute, unmute

NO_PERM = "`Tidak memiliki izin!`"
FAILED = "`Gagal melakukan aksi!`"
REQ_ID = "`Wajib menyertakan ID User atau balas pesan tersebut.`"

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
                user = (await event.client.get_entity(usr)).id
            except BaseException:
                if usr.isnumeric():
                    user.id = usr
                    user.first_name = usr
                else:
                    pass

            if len(ok) == 2:
                data = ok[1]

    return user, data


@bot_cmd(groups_only=True, admins_only=True, pattern="promote ?(.*)")
async def promote(event):
    NotUBot = await event.edit("`Promoting...`")
    await event.get_chat()
    user, rank = await get_uinfo(event)
    rank = rank or "Admin"
    if user is None:
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


@bot_cmd(groups_only=True, admins_only=True, pattern="demote ?(.*)")
async def demote(event):
    NotUBot = await event.edit("`Demoting...`")
    await event.get_chat()
    user, rank = await get_uinfo(event)
    rank = rank or "Not Admin"
    if user is None:
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


@bot_cmd(groups_only=True, admins_only=True, pattern="(fpromote|fullpromote) ?(.*)")
async def fpromote(event):
    NotUBot = await event.edit("`Promoting...`")
    await event.get_chat()
    user, rank = await get_uinfo(event)
    rank = rank or "CoFounder"
    if user is None:
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


@bot_cmd(groups_only=True, admins_only=True, pattern="kick ?(.*)")
async def kick(event):
    NotUBot = await event.edit("`Kicking...`")
    await event.get_chat()
    user, reason = await get_uinfo(event)
    if user is None:
        return await NotUBot.edit(REQ_ID)

    if user.id == (await event.client.get_me()).id:
        return await NotUBot.edit("🥴 **Mabok?**")
    if int(user.id) in DEVLIST:
        return await NotUBot.edit("😑 **Tidak dapat Kick, karena dia pembuatku!**")

    try:
        await event.client.kick_participant(event.chat_id, user.id)
        await sleep(0.5)
    except BaseException:
        return await NotUBot.edit(FAILED)

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title} [`{event.chat_id}`]",
        )
    await NotUBot.edit("`kicked`")


@bot_cmd(groups_only=True, admins_only=True, pattern="ban ?(.*)")
async def ban(event):
    NotUBot = await event.edit("`Banning...`")
    await event.get_chat()
    user, reason = await get_uinfo(event)
    if user is None:
        return await NotUBot.edit(REQ_ID)

    if user.id == (await event.client.get_me()).id:
        return await NotUBot.edit("🥴 **Mabok?**")
    if int(user.id) in DEVLIST:
        return await NotUBot.edit("😑 **Tidak dapat Banned, karena dia pembuatku!**")

    try:
        await event.client.edit_permissions(event.chat_id, user.id, view_messages=False)
    except BaseException:
        return await NotUBot.edit(FAILED)

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title} [`{event.chat_id}`]",
        )
    await NotUBot.edit("`banned`")


@bot_cmd(groups_only=True, admins_only=True, pattern="unban ?(.*)")
async def unban(event):
    NotUBot = await event.edit("`Unbanning...`")
    await event.get_chat()
    user, reason = await get_uinfo(event)
    if user is None:
        return await NotUBot.edit(REQ_ID)

    try:
        await event.client.edit_permissions(event.chat_id, user.id, view_messages=True)
    except BaseException:
        return await NotUBot.edit(FAILED)

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#UNBAN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title} [`{event.chat_id}`]",
        )
    await NotUBot.edit("`unbanned`")


@bot_cmd(groups_only=True, admins_only=True, pattern="mute ?(.*)")
async def muter(event):
    NotUBot = await event.edit("`Muting...`")
    await event.get_chat()
    user, reason = await get_uinfo(event)
    if user is None:
        return await NotUBot.edit(REQ_ID)

    if user.id == (await event.client.get_me()).id:
        return await NotUBot.edit("🥴 **Mabok?**")
    if int(user.id) in DEVLIST:
        return await NotUBot.edit("😑 **Tidak dapat Mute, karena dia pembuatku!**")

    if is_muted(user.id, event.chat_id):
        return await NotUBot.edit("`User sudah terkena Mute.`")

    try:
        await event.client.edit_permissions(event.chat_id, user.id, until_date=None, send_messages=False)
        mute(user.id, event.chat_id)
    except BaseException:
        return await NotUBot.edit(FAILED)

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#MUTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title} [`{event.chat_id}`]",
        )
    await NotUBot.edit("`muted`")


@bot_cmd(groups_only=True, admins_only=True, pattern="unmute ?(.*)")
async def unmuter(event):
    NotUBot = await event.edit("`Unmuting...`")
    await event.get_chat()
    user, reason = await get_uinfo(event)
    if user is None:
        return await NotUBot.edit(REQ_ID)

    if not is_muted(user.id, event.chat_id):
        return NotUBot.edit("`User tidak terkena Mute.`")

    try:
        # await event.client.edit_permissions(event.chat_id, user.id, until_date=None, send_messages=True)
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        unmute(user.id, event.chat_id)
    except BaseException:
        return await NotUBot.edit(FAILED)

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#UNMUTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title} [`{event.chat_id}`]",
        )
    await NotUBot.edit("`unmuted`")


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
    match = (event.pattern_match.group(1)).strip()
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


@bot_cmd(groups_only=True, admins_only=True, pattern="autodelete ?(.*)")
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


@bot_cmd(groups_only=True, admins_only=True, pattern="(zombies|delusers) ?(.*)")
async def zombies(event):
    match = event.pattern_match.group(1).lower()
    deleted_user = 0
    status = "`Tidak ada akun terhapus.`"
    await event.get_chat()
    if match != "clean":
        await event.edit("`Mencari akun terhapus...`")

        async for user in event.client.iter_participants(event.chat_id):
            if user.deleted:
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

    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
            except UserAdminInvalidError:
                deleted_user -= 1
                deleted_admin += 1

            await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
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


@bot_cmd(groups_only=True, disable_errors=True, pattern="(staff|adminlist)$")
async def get_admin(event):
    await event.get_chat()
    info = await event.client.get_entity(event.chat_id)
    title = info.title if info.title else "Grup"
    mentions = f"<b>Admin {title}:</b> \n"

    try:
        async for user in event.client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                mentions += f"\n{link}"
    except ChatAdminRequiredError as e:
        mentions += " " + str(e) + "\n"

    await event.edit(mentions, parse_mode="html")


@bot_cmd(groups_only=True, admins_only=True, pattern="(allunban|unbanall)$")
async def allunban(event):
    await event.edit("`...`")
    success = 0
    await event.get_chat()
    async for user in event.client.iter_participants(
        event.chat_id,
        filter=ChannelParticipantsKicked,
        aggressive=True,
    ):
        try:
            await event.client.edit_permissions(event.chat_id, user, view_messages=True)
            success += 1
            await sleep(1)
        except BaseException:
            pass

    await event.edit("`Berhasil unbanned semua daftar blokir.`")


@bot_cmd(groups_only=True, admins_only=True, disable_errors=True, pattern="all ?(.*)")
async def all(event):
    text = (event.pattern_match.group(1)).strip()
    users = []
    limit = 0
    await event.get_chat()
    async for user in event.client.iter_participants(event.chat_id):
        if not (user.bot or user.deleted):
            if not (
                isinstance(user.participant, ChannelParticipantAdmin)
                or isinstance(user.participant, ChannelParticipantCreator)
            ):
                users.append(f"[{get_display_name(user)}](tg://user?id={user.id})")
            if isinstance(user.participant, ChannelParticipantAdmin):
                users.append(f"👮 [{get_display_name(user)}](tg://user?id={user.id})")
            if isinstance(user.participant, ChannelParticipantCreator):
                users.append(f"🤴 [{get_display_name(user)}](tg://user?id={user.id})")

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
            await sleep(5)
        except BaseException:
            pass

    await event.delete()


@bot_cmd(
    pattern="rmusers ?(.*)",
    groups_only=True,
    admins_only=True,
)
async def rmusers(event):
    NotUBot = await event.edit("`...`")
    match = event.pattern_match.group(1)
    p, b, c, d, m, n, y, w, o, q, r = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    async for i in event.client.iter_participants(event.chat_id):
        p += 1
        if isinstance(i.status, UserStatusEmpty):
            if "empty" in match:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                y += 1
        if isinstance(i.status, UserStatusLastMonth):
            if "month" in match:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                m += 1
        if isinstance(i.status, UserStatusLastWeek):
            if "week" in match:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                w += 1
        if isinstance(i.status, UserStatusOffline):
            if "offline" in match:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                o += 1
        if isinstance(i.status, UserStatusOnline):
            if "online" in match:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                q += 1
        if isinstance(i.status, UserStatusRecently):
            if "recently" in match:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                r += 1
        if i.bot:
            if "bot" in match:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                b += 1
        elif i.deleted:
            if "deleted" in match:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
                except BaseException:
                    pass
            else:
                d += 1
        elif i.status is None:
            if "none" in match:
                try:
                    await event.client.kick_participant(event.chat_id, i)
                    c += 1
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
            "`.promote <id/username/reply> <title (optional)>`\n"
            "↳ : Promote user menjadi admin.\n\n"
            "`.demote <id/username/reply>`\n"
            "↳ : Demote seorang admin.\n\n"
            "`.fpromote|fullpromote <id/username/reply> <title (optional)>`\n"
            "↳ : Promote user menjadi cofounder.\n\n"
            "`.kick <id/username/reply> <reason (optional)>`\n"
            "↳ : Kick user dari grup.\n\n"
            "`.ban <id/username/reply> <reason (optional)>`\n"
            "↳ : Banned user dari grup.\n\n"
            "`.unban <id/username/reply>`\n"
            "↳ : Unbanned user dari grup.\n\n"
            "`.mute <id/username/reply> <reason (optional)>`\n"
            "↳ : Mute user dari grup.\n\n"
            "`.unmute <id/username/reply>`\n"
            "↳ : Unmute user dari grup.\n\n"
            "`.lock`\n"
            "↳ : Kunci grup, biarkan user hanya membaca.\n\n"
            "`.unlock`\n"
            "↳ : Buka kunci grup, user dapat mengirim pesan.\n\n"
            "`.pin`\n"
            "↳ : Pin pesan pada obrolan.\n\n"
            "`.unpin <all>`\n"
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
            "`.all`\n"
            "↳ : Mention semua member grup.\n\n"
            "`.rmusers`\n"
            "↳ : Membersihkan user spesial.",
        ]
    }
)
