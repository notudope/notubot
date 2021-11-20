# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from asyncio import sleep
from io import BytesIO

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.messages import ReportSpamRequest
from telethon.tl.types import ChatBannedRights
from telethon.utils import get_display_name

from notubot import (
    CMD_HELP,
    BOTLOG_CHATID,
    BOTLOG,
    NOSPAM_GROUP,
    bot,
)
from notubot.database.gban_sql import (
    is_gbanned,
    gbaner,
    ungbaner,
    all_gbanned,
)
from notubot.database.gmute_sql import is_gmuted, gmute, ungmute
from notubot.events import bot_cmd
from notubot.functions import get_user_from_event, get_uinfo, get_user_id  # noqa: F401

from . import DEVLIST, NOSPAM_SUPERGROUP

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


@bot_cmd(pattern="gban(?: |$)(.*)")
async def gban(event):
    NotUBot = await event.edit("`Gbanning...`")
    reason = ""
    chat = await event.get_chat()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr, event)
        try:
            reason = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = chat.id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    else:
        return await NotUBot.edit(REQ_ID)

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(userid)), userid)
    success = failed = 0

    if userid == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")
    if userid in DEVLIST:
        return await NotUBot.edit("😑 **Gagal Global Banned, dia pembuatku!**")

    if is_gbanned(userid):
        return await NotUBot.edit(
            "`User sudah terkena Global Banned.`",
        )

    try:
        await event.client(ReportSpamRequest(int(userid)))
        await event.client(BlockRequest(int(userid)))
    except BaseException:
        pass

    async for x in event.client.iter_dialogs():
        if x.is_group or x.is_channel:
            try:
                await event.client(EditBannedRequest(x.id, userid, BANNED_RIGHTS))
                success += 1
                await sleep(0.5)
            except BaseException:
                failed += 1

    reason = reason if reason else "None given."
    gbaner(userid, reason)
    text = f"""**#Gbanned** by {mention}
**User:** {userlink}
**Aksi:** `Gbanned`
**Alasan:** `{reason}`
**Grup/Channel:** Berhasil `{success}` Gagal `{failed}`"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(pattern="ungban(?: |$)(.*)")
async def ungban(event):
    NotUBot = await event.edit("`UnGbanning...`")
    chat = await event.get_chat()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        usr = event.pattern_match.group(1)
        userid = await get_user_id(usr, event)
    elif event.is_private:
        userid = chat.id
    else:
        return await NotUBot.edit(REQ_ID)

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(userid)), userid)
    success = failed = 0

    if not is_gbanned(userid):
        return await NotUBot.edit("`User tidak terkena Global Banned.`")

    try:
        await event.client(UnblockRequest(int(userid)))
    except BaseException:
        pass

    async for x in event.client.iter_dialogs():
        if x.is_group or x.is_channel:
            try:
                await event.client(EditBannedRequest(x.id, userid, UNBAN_RIGHTS))
                success += 1
                await sleep(0.5)
            except BaseException:
                failed += 1

    ungbaner(userid)
    text = f"""**#UnGbanned** by {mention}
**User:** {userlink}
**Aksi:** `UnGbanned`
**Grup/Channel:** Berhasil `{success}` Gagal `{failed}`"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(pattern="listgban$")
async def listgban(event):
    NotUBot = await event.edit("`...`")
    chat_id = event.chat_id or event.from_id
    mention = "<a href=tg://user?id={}>{}</a>".format(bot.uid, bot.name)
    msg = f"<strong>GBanned by {mention}</strong>:\n\n"
    await event.get_chat()
    gbanned_users = all_gbanned()
    if len(gbanned_users) > 0:
        for user in gbanned_users:
            try:
                name = get_display_name(await event.client.get_entity(int(user.user_id)))
            except BaseException:
                name = user.user_id
            msg += f"<strong>User</strong>: <a href=tg://user?id={user.user_id}>{name}</a>\n"
            msg += f"<strong>Reason</strong>: {user.reason}\n\n"
    else:
        msg = "No Gbanned"

    if len(msg) > 4096:
        try:
            with BytesIO(
                str.encode(
                    msg.replace("<strong>", "")
                    .replace("</strong>", "")
                    .replace("<a href=tg://user?id=", "")
                    .replace("</a>", "")
                )
            ) as file:
                file.name = "gbanned.txt"
                await event.client.send_file(
                    chat_id,
                    file,
                    force_document=True,
                    allow_cache=False,
                    reply_to=event.id,
                    caption=f"GBanned by {mention}",
                    parse_mode="html",
                )
        except Exception:
            pass
        await NotUBot.delete()
    else:
        await NotUBot.edit(msg, parse_mode="html")


@bot_cmd(pattern="gkick(?: |$)(.*)")
async def gkick(event):
    NotUBot = await event.edit("`Gkicking...`")
    reason = ""
    chat = await event.get_chat()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr, event)
        try:
            reason = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = chat.id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    else:
        return await NotUBot.edit(REQ_ID)

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(userid)), userid)
    success = failed = 0

    if userid == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")
    if userid in DEVLIST:
        return await NotUBot.edit("😑 **Gagal Global Kick, dia pembuatku!**")

    async for x in event.client.iter_dialogs():
        if x.is_group or x.is_channel:
            try:
                await event.client(EditBannedRequest(x.id, userid, KICK_RIGHTS))
                success += 1
                await sleep(0.5)
            except BaseException:
                failed += 1

    reason = reason if reason else "None given."
    text = f"""**#Gkicked** by {mention}
**User:** {userlink}
**Aksi:** `Gkicked`
**Alasan:** `{reason}`
**Grup/Channel:** Berhasil `{success}` Gagal `{failed}`"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(pattern="gmute(?: |$)(.*)")
async def gmuter(event):
    NotUBot = await event.edit("`Gmuting...`")
    reason = ""
    chat = await event.get_chat()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr, event)
        try:
            reason = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = chat.id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    else:
        return await NotUBot.edit(REQ_ID)

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(userid)), userid)
    success = failed = 0

    if userid == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")
    if userid in DEVLIST:
        return await NotUBot.edit("😑 **Gagal Global Mute, dia pembuatku!**")

    if is_gmuted(userid):
        return await NotUBot.edit("`User sudah terkena Global Mute.`")

    async for x in event.client.iter_dialogs():
        if x.is_group:
            try:
                await event.client(EditBannedRequest(x.id, userid, MUTE_RIGHTS))
                success += 1
                await sleep(0.5)
            except BaseException:
                failed += 1

    reason = reason if reason else "None given."
    gmute(userid)
    text = f"""**#Gmuted** by {mention}
**User:** {userlink}
**Aksi:** `Gmuted`
**Alasan:** `{reason}`
**Grup/Channel:** Berhasil `{success}` Gagal `{failed}`"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(pattern="ungmute(?: |$)(.*)")
async def ungmuter(event):
    NotUBot = await event.edit("`UnGmuting...`")
    chat = await event.get_chat()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        usr = event.pattern_match.group(1)
        userid = await get_user_id(usr, event)
    elif event.is_private:
        userid = chat.id
    else:
        return await NotUBot.edit(REQ_ID)

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(userid)), userid)
    success = failed = 0

    if not is_gmuted(userid):
        return await NotUBot.edit("`User tidak terkena Global Mute.`")

    async for x in event.client.iter_dialogs():
        if x.is_group:
            try:
                await event.client(EditBannedRequest(x.id, userid, UNBAN_RIGHTS))
                success += 1
                await sleep(0.5)
            except BaseException:
                failed += 1

    ungmute(userid)
    text = f"""**#UnGmuted** by {mention}
**User:** {userlink}
**Aksi:** `UnGmuted`
**Grup/Channel:** Berhasil `{success}` Gagal `{failed}`"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(pattern="gcast(?: |$)(.*)")
async def gcast(event):
    NotUBot = await event.edit("`...`")
    match = event.pattern_match.group(1)
    if match:
        msg = match
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await NotUBot.edit("`Berikan sebuah pesan atau balas pesan tersebut...`")

    await NotUBot.edit("`Mengirim pesan broadcast ke grup 📢`")
    success = failed = 0

    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.entity.id
            if not int("-100" + str(chat)) in list(set(NOSPAM_SUPERGROUP + NOSPAM_GROUP)):
                try:
                    await event.client.send_message(chat, msg)
                    success += 1
                    await sleep(2)
                except BaseException:
                    failed += 1

    text = f"**#Gcast** Berhasil mengirim pesan broadcast grup ke `{success}` obrolan, gagal mengirim ke `{failed}` obrolan."
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(pattern="gucast(?: |$)(.*)")
async def gucast(event):
    NotUBot = await event.edit("`...`")
    match = event.pattern_match.group(1)
    if match:
        msg = match
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await NotUBot.edit("`Berikan sebuah pesan atau balas pesan tersebut...`")

    await NotUBot.edit("`Mengirim pesan broadcast ke pribadi 📢`")
    success = failed = 0

    async for x in event.client.iter_dialogs():
        if x.is_user and not (x.entity.bot or x.id == 777000):
            try:
                await event.client.send_message(x.id, msg)
                success += 1
                await sleep(2)
            except BaseException:
                failed += 1

    text = f"**#Gucast** Berhasil mengirim pesan broadcast pribadi ke `{success}` obrolan, gagal mengirim ke `{failed}` obrolan."
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(pattern="gsend(?: |$)(.*)")
async def gsend(event):
    NotUBot = await event.edit("`...`")
    opts = event.pattern_match.group(1)
    args = opts.split(" ")
    chat_id = args[0]

    try:
        chat_id = int(chat_id)
    except BaseException:
        pass

    msg = ""
    reply = await event.get_reply_message()
    if event.reply_to_msg_id:
        await event.client.send_message(chat_id, reply)
        await NotUBot.edit("`Pesan diteruskan ke grup tujuan, coba cek!`")

    for index in args[1:]:
        msg += index + " "
    if msg == "":
        return

    try:
        await event.client.send_message(chat_id, msg)
        await NotUBot.edit("`Pesan diteruskan ke grup tujuan, coba cek!`")
    except BaseException:
        pass


CMD_HELP.update(
    {
        "global": [
            "Global Tools",
            "`.gban <username/id/reply> <reason (optional)>`\n"
            "↳ : Global Banned ke semua grup yang menjadi admin,\n"
            "Gunakan perintah ini dengan bijak.\n\n"
            "`.ungban <username/id/reply>`\n"
            "↳ : Membatalkan Global Banned.\n\n"
            "`.listgban`\n"
            "↳ : Daftar semua user Global Banned.\n\n"
            "`.gkick <username/id/reply> <reason (optional)>`\n"
            "↳ : Global Kick ke semua grup yang menjadi admin.\n\n"
            "`.gmute <username/id/reply> <reason (optional)>`\n"
            "↳ : Global Mute ke semua grup yang menjadi admin.\n\n"
            "`.ungmute <username/id/reply>`\n"
            "↳ : Membatalkan Global Mute.\n\n"
            "`.gcast`\n"
            "↳ : Mengirim Pesan Group secara global,\n"
            "Gak usah idiot, jangan berlebihan, resiko (limit, kena kick/banned/fban) ditanggung pengguna!\n\n"
            "`.gucast`\n"
            "↳ : Mengirim Pesan Pribadi secara global,\n"
            "Gak usah spam, seperlunya aja!\n\n"
            "`.gsend <username> <message>`\n"
            "↳ : Mengirim pesan jarak jauh ke grup lain.",
        ]
    }
)
