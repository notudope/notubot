# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio
import os

from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import ChatBannedRights, PeerUser
from telethon.utils import get_display_name

from notubot import (
    CMD_HELP,
    bot,
    BOTLOG_CHATID,
    BOTLOG,
    DEVLIST,
    NOSPAM_CHAT,
)
from notubot.events import bot_cmd
from notubot.plugins.sql_helper.gban_sql import (
    is_gbanned,
    gbaner,
    ungbaner,
    all_gbanned,
)
from notubot.plugins.sql_helper.gmute_sql import is_gmuted, gmute, ungmute

REQ_ID = "`Wajib menyertakan ID User atau balas pesan tersebut.`"

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


async def get_user_id(ids):
    return int(ids) if str(ids).isdigit() else (await bot.get_entity(PeerUser(ids))).id


@bot_cmd(outgoing=True, pattern="gban ?(.*)")
async def gban(event):
    me = await event.client.get_me()
    mention = "[{}](tg://user?id={})".format(get_display_name(me), me.id)

    NotUBot = await event.edit("`Gbanning...`")
    reason = ""
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", maxsplit=2)[1]
        userid = await get_user_id(usr)
        try:
            reason = event.text.split(" ", maxsplit=2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = (await event.get_chat()).id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    else:
        return await NotUBot.edit(REQ_ID)

    name = (await event.client.get_entity(userid)).first_name
    success = failed = 0

    if userid == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")
    if int(userid) in DEVLIST:
        return await NotUBot.edit("😑 **Tidak dapat Global Banned, karena dia pembuatku!**")

    if is_gbanned(userid):
        return await NotUBot.edit(
            "`User sudah terkena Global Banned.`",
        )

    try:
        await event.client(BlockRequest(int(userid)))
    except BaseException:
        pass

    async for x in event.client.iter_dialogs():
        if x.is_group or x.is_channel:
            try:
                await event.client.edit_permissions(x.id, userid, view_messages=False)
                success += 1
            except BaseException:
                failed += 1

    reason = reason if reason else "None given."
    gbaner(userid, reason)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "**#Gbanned** [{}](tg://user?id={}) {}".format(userid, userid, reason)
        )

    text = f"""**#Gbanned** oleh {mention}
**User :** [{name}](tg://user?id={userid})
**Aksi :** `Gbanned`
**Alasan :** `{reason}`
**Grup/Channel :** Berhasil `{success}` Gagal `{failed}`"""
    await NotUBot.edit(text)


@bot_cmd(outgoing=True, pattern="ungban ?(.*)")
async def ungban(event):
    me = await event.client.get_me()
    mention = "[{}](tg://user?id={})".format(get_display_name(me), me.id)

    NotUBot = await event.edit("`UnGbanning...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await NotUBot.edit(REQ_ID)

    name = (await event.client.get_entity(userid)).first_name
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
                await event.client.edit_permissions(x.id, userid, view_messages=True)
                success += 1
            except BaseException:
                failed += 1

    ungbaner(userid)
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**#UnGbanned** [{}](tg://user?id={})".format(userid, userid))

    text = f"""**#UnGbanned** oleh {mention}
**User :** [{name}](tg://user?id={userid})
**Aksi :** `UnGbanned`
**Grup/Channel :** Berhasil `{success}` Gagal `{failed}`"""
    await NotUBot.edit(text)


@bot_cmd(outgoing=True, pattern="listgban$")
async def listgban(event):
    me = await event.client.get_me()
    mention = "[{}](tg://user?id={})".format(get_display_name(me), me.id)
    msg = f"<strong>GBanned by {get_display_name(me)}</strong>:\n\n"
    gbanned_users = all_gbanned()

    if len(gbanned_users) > 0:
        for user in gbanned_users:
            name = (await bot.get_entity(int(user))).first_name
            msg += f"<strong>User</strong>: <a href=tg://user?id={user.user_id}>{name}</a>\n"
            msg += f"<strong>Reason</strong>: {user.reason}\n\n"
    else:
        msg = "No Gbanned !!"

    if len(msg) > 4096:
        with open("gbanned.txt", "w") as f:
            f.write(
                gbanned_users.replace("<strong>", "")
                .replace("</strong>", "")
                .replace("<a href=tg://user?id=", "")
                .replace("</a>", "")
            )

        await event.reply(
            file="gbanned.txt",
            message=f"GBanned by {mention}",
        )

        os.remove("gbanned.txt")
        await event.delete()
    else:
        await event.edit(msg, parse_mode="html")


@bot_cmd(outgoing=True, pattern="gkick ?(.*)")
async def gkick(event):
    me = await event.client.get_me()
    mention = "[{}](tg://user?id={})".format(get_display_name(me), me.id)

    NotUBot = await event.edit("`Gkicking...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await NotUBot.edit(REQ_ID)

    name = (await event.client.get_entity(userid)).first_name
    success = failed = 0

    if userid == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")
    if int(userid) in DEVLIST:
        return await NotUBot.edit("😑 **Tidak dapat Global Kick, karena dia pembuatku!**")

    async for x in event.client.iter_dialogs():
        if x.is_group or x.is_channel:
            try:
                await event.client.kick_participant(x.id, userid)
                success += 1
            except BaseException:
                failed += 1

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**#Gkicked** [{}](tg://user?id={})".format(userid, userid))

    text = f"""**#Gkicked** oleh {mention}
**User :** [{name}](tg://user?id={userid})
**Aksi :** `Gkicked`
**Grup/Channel :** Berhasil `{success}` Gagal `{failed}`"""
    await NotUBot.edit(text)


@bot_cmd(outgoing=True, pattern="gmute ?(.*)")
async def gmuter(event):
    me = await event.client.get_me()
    mention = "[{}](tg://user?id={})".format(get_display_name(me), me.id)

    NotUBot = await event.edit("`Gmuting...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await NotUBot.edit(REQ_ID)

    name = (await event.client.get_entity(userid)).first_name
    success = failed = 0

    if userid == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")
    if int(userid) in DEVLIST:
        return await NotUBot.edit("😑 **Tidak dapat Global Mute, karena dia pembuatku!**")

    if is_gmuted(userid):
        return await NotUBot.edit("`User sudah terkena Global Mute.`")

    async for x in event.client.iter_dialogs():
        if x.is_group:
            try:
                await event.client.edit_permissions(x.id, userid, until_date=None, send_messages=False)
                success += 1
            except BaseException:
                failed += 1

    gmute(userid)
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**#Gmuted** [{}](tg://user?id={})".format(userid, userid))

    text = f"""**#Gmuted** oleh {mention}
**User :** [{name}](tg://user?id={userid})
**Aksi :** `Gmuted`
**Grup/Channel :** Berhasil `{success}` Gagal `{failed}`"""
    await NotUBot.edit(text)


@bot_cmd(outgoing=True, pattern="ungmute ?(.*)")
async def ungmuter(event):
    me = await event.client.get_me()
    mention = "[{}](tg://user?id={})".format(get_display_name(me), me.id)

    NotUBot = await event.edit("`UnGmuting...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await NotUBot.edit(REQ_ID)

    name = (await event.client.get_entity(userid)).first_name
    success = failed = 0

    if not is_gmuted(userid):
        return await NotUBot.edit("`User tidak terkena Global Mute.`")

    async for x in event.client.iter_dialogs():
        if x.is_group:
            try:
                # await event.client.edit_permissions(x.id, userid, until_date=None, send_messages=True)
                await event.client(EditBannedRequest(x.id, userid, UNBAN_RIGHTS))
                success += 1
            except BaseException:
                failed += 1

    ungmute(userid)
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "**#Ungmuted** [{}](tg://user?id={})".format(userid, userid))

    text = f"""**#Ungmuted** oleh {mention}
**User :** [{name}](tg://user?id={userid})
**Aksi :** `Ungmuted`
**Grup/Channel :** Berhasil `{success}` Gagal `{failed}`"""
    await NotUBot.edit(text)


@bot_cmd(outgoing=True, pattern="gcast ?(.*)")
async def gcast(event):
    xx = event.pattern_match.group(1)
    if xx:
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await event.edit("`Berikan sebuah pesan atau balas pesan tersebut...`")

    NotUBot = await event.edit("`Mengirim pesan broadcast ke grup secara global 📢`")
    success = failed = 0

    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.entity.id
            if not int("-100" + str(chat)) in NOSPAM_CHAT:
                try:
                    success += 1
                    await event.client.send_message(chat, msg)
                except BaseException:
                    failed += 1

        await asyncio.sleep(2)

    await NotUBot.edit(
        f"Berhasil mengirim pesan broadcast grup ke `{success}` obrolan, gagal mengirim ke `{failed}` obrolan."
    )


@bot_cmd(outgoing=True, pattern="gucast ?(.*)")
async def gucast(event):
    xx = event.pattern_match.group(1)
    if xx:
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await event.edit("`Berikan sebuah pesan atau balas pesan tersebut...`")

    NotUBot = await event.edit("`Mengirim pesan broadcast ke pribadi secara global 📢`")
    success = failed = 0

    async for x in event.client.iter_dialogs():
        if x.is_user and not (x.entity.bot or x.id == 777000):
            try:
                success += 1
                await event.client.send_message(x.id, msg)
            except BaseException:
                failed += 1

        await asyncio.sleep(2)

    await NotUBot.edit(
        f"Berhasil mengirim pesan broadcast pribadi ke `{success}` obrolan, gagal mengirim ke `{failed}` obrolan."
    )


@bot_cmd(outgoing=True, pattern="gsend ?(.*)")
async def gsend(event):
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
        await event.edit("`Pesan diteruskan ke grup tujuan, coba cek!`")

    for index in args[1:]:
        msg += index + " "
    if msg == "":
        return

    try:
        await event.client.send_message(chat_id, msg)
        await event.edit("`Pesan diteruskan ke grup tujuan, coba cek!`")
    except BaseException:
        pass


CMD_HELP.update(
    {
        "global": [
            "Global Tools",
            "`.gban`\n"
            "↳ : Global Banned ke semua grup yang menjadi admin,\n"
            "Gunakan perintah ini dengan bijak.\n\n"
            "`.ungban`\n"
            "↳ : Membatalkan Global Banned.\n\n"
            "`.listgban`\n"
            "↳ : Daftar semua user Global Banned.\n\n"
            "`.gkick`\n"
            "↳ : Global Kick ke semua grup yang menjadi admin.\n\n"
            "`.gmute`\n"
            "↳ : Global Mute ke semua grup yang menjadi admin.\n\n"
            "`.ungmute`\n"
            "↳ : Membatalkan Global Mute.\n\n"
            "`.gcast`\n"
            "↳ : Mengirim Pesan Group secara global,\n"
            "Gak usah idiot, jangan berlebihan, resiko (limit, kena kick/banned/fban) ditanggung pengguna!\n\n"
            "`.gucast`\n"
            "↳ : Mengirim Pesan Pribadi secara global,\n"
            "Gak usah spam, seperlunya aja!\n\n"
            "`.gsend <link grup> <pesan>`\n"
            "↳ : Mengirim pesan jarak jauh ke grup lain.",
        ]
    }
)
