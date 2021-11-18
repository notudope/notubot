# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from asyncio import sleep

from sqlalchemy.exc import IntegrityError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.utils import get_display_name

from notubot import (
    CMD_HELP,
    BOTLOG_CHATID,
    BOTLOG,
    DEVLIST,
    bot,
)
from notubot.database.fban_sql import (
    get_flist,
    add_flist,
    del_flist,
    del_flist_all,
)
from notubot.events import bot_cmd
from notubot.utils import get_user_from_event, get_uinfo, get_user_id  # noqa: F401

fbot = "@MissRose_bot"
REQ_ID = "`Kesalahan, dibutuhkan ID atau balas pesan itu.`"


@bot_cmd(pattern="fban(?: |$)(.*)")
async def fban(event):
    NotUBot = await event.edit("`Fbanning...`")
    reason = ""
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        userid = event.text.split(" ", maxsplit=2)[1]
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

    try:
        userid = await event.client.get_peer_id(userid)
    except BaseException:
        pass

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(userid)), userid)
    location = "{} [`{}`]".format((await event.get_chat()).title or "Private", event.chat_id or event.from_id)
    failed = []
    total = int(0)

    if userid == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")
    if userid in DEVLIST:
        return await NotUBot.edit("😑 **Gagal fban, dia pembuatku!**")

    if len(fed_list := get_flist()) == 0:
        return await NotUBot.edit("`Tidak ada federasi yang terhubung.`")

    for i in fed_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with event.client.conversation(chat) as conv:
                await conv.send_message(f"/fban {userlink} {reason}")
                reply = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id, message=reply, clear_mentions=True)

                if (
                    ("New FedBan" not in reply.text)
                    and ("Starting a federation ban" not in reply.text)
                    and ("Start a federation ban" not in reply.text)
                    and ("FedBan reason updated" not in reply.text)
                ):
                    failed.append(i.fed_name)
                await sleep(0.1)
        except BaseException:
            failed.append(i.fed_name)

    reason = reason if reason else "None given."
    if failed:
        status = f"Gagal fban `{len(failed)}/{total}` feds.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Berhasil fban `{total}` feds."

    text = f"""**#Fbanned** by {mention}
**User:** {userlink}
**Aksi:** `Fbanned`
**Alasan:** `{reason}`
**Lokasi:** {location}
**Status:** {status}"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(pattern="unfban(?: |$)(.*)")
async def unfban(event):
    NotUBot = await event.edit("`UnFbanning...`")
    reason = ""
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        userid = event.text.split(" ", maxsplit=2)[1]
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

    try:
        userid = await event.client.get_peer_id(userid)
    except BaseException:
        pass

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    userlink = "[➥ {}](tg://user?id={})".format(get_display_name(await event.client.get_entity(userid)), userid)
    location = "{} [`{}`]".format((await event.get_chat()).title or "Private", event.chat_id or event.from_id)
    failed = []
    total = int(0)

    if userid == bot.uid:
        return await NotUBot.edit("🥴 **Mabok?**")

    if len(fed_list := get_flist()) == 0:
        return await NotUBot.edit("`Tidak ada federasi yang terhubung.`")

    for i in fed_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with event.client.conversation(chat) as conv:
                await conv.send_message(f"/unfban {userlink} {reason}")
                reply = await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id, message=reply, clear_mentions=True)

                if (
                    ("New un-FedBan" not in reply.text)
                    and ("I'll give" not in reply.text)
                    and ("Un-FedBan" not in reply.text)
                ):
                    failed.append(i.fed_name)
                await sleep(0.1)
        except BaseException:
            failed.append(i.fed_name)

    reason = reason if reason else "None given."
    if failed:
        status = f"Gagal unfban `{len(failed)}/{total}` feds.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Berhasil unfban `{total}` feds."

    text = f"""**#UnFbanned** by {mention}
**User:** {userlink}
**Aksi:** `UnFbanned`
**Alasan:** `{reason}`
**Lokasi:** {location}
**Status:** {status}"""
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, text)

    await NotUBot.edit(text)


@bot_cmd(pattern="addfed(?: |$)(.*)")
async def addfed(event):
    if not (fed_name := event.pattern_match.group(1)):
        return await event.edit("`Sertakan nama untuk menghubungkan grup ini.`")

    try:
        add_flist(event.chat_id, fed_name)
    except IntegrityError:
        return await event.edit("`Grup ini sudah terhubung ke federasi.`")

    await event.edit("`Menambahkan grup ini ke daftar federasi.`")


@bot_cmd(pattern="delfed$")
async def delfed(event):
    await event.edit("`...`")
    del_flist(event.chat_id)
    await event.edit("`Menghapus grup ini dari daftar federasi.`")


@bot_cmd(pattern="listfed$")
async def listfed(event):
    if len(fed_list := get_flist()) == 0:
        return await event.edit("`Tidak ada federasi yang terhubung.`")

    msg = "**Federasi:**\n\n"
    for i in fed_list:
        msg += "• " + str(i.fed_name) + "\n"
    await event.edit(msg)


@bot_cmd(pattern="clearfed$")
async def clearfed(event):
    await event.edit("`...`")
    del_flist_all()
    await event.edit("`unfederations`")


@bot_cmd(pattern="fstat(?: |$)(.*)")
async def fstat(event):
    NotUBot = await event.edit("`Fstat....`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = event.pattern_match.group(1)
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await NotUBot.edit(REQ_ID)

    async with event.client.conversation(fbot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fedstat " + str(userid))
            res = await conv.get_response()
            await NotUBot.edit(res.text)
        except YouBlockedUserError:
            await NotUBot.edit(f"`Unblock {fbot}`")


@bot_cmd(pattern="fedinfo(?: |$)(.*)")
async def fedinfo(event):
    NotUBot = await event.edit("`Fetching...`")
    match = event.pattern_match.group(1)

    async with event.client.conversation(fbot) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/fedinfo " + match)
            res = await conv.get_response()
            await NotUBot.edit(res.text)
        except YouBlockedUserError:
            await NotUBot.edit(f"`Unblock {fbot}`")


CMD_HELP.update(
    {
        "fban": [
            f"{fbot} Federation",
            "`.fban <username/id/reply> <reason (optional)>`\n"
            "↳ : Fban user dari federasi yang terhubung.\n\n"
            "`.unfban <username/id/reply> <reason (optional)>`\n"
            "↳ : Melepas user dari fban.\n\n"
            "`.addfed <name>`\n"
            "↳ : Tambahkan grup saat ini dengan <name> di federasi yang terhubung.\n\n"
            "`.delfed`\n"
            "↳ : Menghapus grup saat ini dari daftar federasi.\n\n"
            "`.listfed`\n"
            "↳ : Daftar federasi yang terhubung.\n\n"
            "`.clearfed`\n"
            "↳ : Memutuskan semua federasi yang terhubung.\n\n"
            "`.fstat <username/id>`\n"
            "↳ : Mengambil fban stats dari rose.\n\n"
            "`.fedinfo <fed id>`\n"
            "↳ : Menampilkan informasi terkait federasi tersebut.\n\n",
        ]
    }
)
