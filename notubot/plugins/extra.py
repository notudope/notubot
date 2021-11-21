# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio

from telethon.events import NewMessage
from telethon.tl.functions.channels import DeleteUserHistoryRequest

from notubot import (
    CMD_HELP,
    LOGS,
    HANDLER,
    bot,
)
from notubot.events import bot_cmd

_new_msgs = {}


@bot.on(
    NewMessage(
        outgoing=True,
    ),
)
async def newmsg(event):
    if event.message.message == f"{HANDLER}reply":
        return
    _new_msgs[event.chat_id] = event.message


@bot_cmd(disable_errors=True, pattern="del|(d|D|del|Del)$")
async def _(event):
    reply = await event.get_reply_message()
    if reply:
        try:
            await reply.delete()
        except BaseException:
            pass
    await event.delete()


@bot_cmd(disable_errors=True, pattern="purge(?: |$)(.*)")
async def _(event):
    match = event.pattern_match.group(1)
    try:
        text = event.text[6]
    except IndexError:
        text = None

    if text and event.text[6] in ["m", "a"]:
        return

    if not event._client._bot and ((match) or (event.is_reply and event.is_private)):
        count = 0
        async for msg in event.client.iter_messages(
            event.chat_id,
            limit=int(match) if match else None,
            min_id=event.reply_to_msg_id if event.is_reply else None,
        ):
            await msg.delete()
            count += 1
        NotUBot = await event.client.send_message(
            event.chat_id,
            f"`Purged {count}`",
        )
        await asyncio.sleep(1)
        await NotUBot.delete()
        return

    if not event.reply_to_msg_id:
        await event.edit("`Balas pesan untuk menghapus dari?`")
        return

    try:
        await event.client.delete_messages(
            event.chat_id, [x for x in range(event.reply_to_msg_id, event.id + 1)]  # noqa: C416
        )
    except Exception as e:
        LOGS.exception(e)

    NotUBot = await event.client.send_message(event.chat_id, "`purged`")
    await asyncio.sleep(1)
    await NotUBot.delete()


@bot_cmd(disable_errors=True, pattern="purgeme(?: |$)(.*)")
async def _(event):
    opts = event.pattern_match.group(1)
    if opts and not event.is_reply:
        try:
            num = int(opts)
        except BaseException:
            await event.edit("`Input tidak valid.`")
            return

        done = 0
        async for m in event.client.iter_messages(event.chat_id, limit=num, from_user="me"):
            await m.delete()
            done += 1
        NotUBot = await event.client.send_message(
            event.chat_id,
            f"`Purged {done}`",
        )
        await asyncio.sleep(1)
        await event.delete()
        await NotUBot.delete()
        return

    chat = await event.get_input_chat()
    msgs = []
    count = 0
    if not (event.reply_to_msg_id or opts):
        await event.edit("Membalas pesan untuk purge atau gunakan seperti `purgeme <num>`")
        return
    async for m in event.client.iter_messages(
        chat,
        from_user="me",
        min_id=event.reply_to_msg_id,
    ):
        msgs.append(m)
        count += 1
        msgs.append(event.reply_to_msg_id)
        if len(msgs) == 100:
            await event.client.delete_messages(chat, msgs)
            msgs = []
    if msgs:
        await event.client.delete_messages(chat, msgs)
    NotUBot = await event.client.send_message(
        event.chat_id,
        f"`Purged {str(count)}`",
    )
    await asyncio.sleep(1)
    await event.delete()
    await NotUBot.delete()


@bot_cmd(disable_errors=True, groups_only=True, pattern="purgeall$")
async def _(event):
    if not event.is_reply:
        await event.edit("`Balas pesan seseorang untuk menghapusnya.`")
        return
    sender = (await event.get_reply_message()).sender
    try:
        await event.client(DeleteUserHistoryRequest(event.chat_id, sender.id))
        await event.edit(
            f"`Berhasil menghapus semua pesan {sender.first_name}`",
        )
        await asyncio.sleep(2)
    except BaseException:
        pass
    await event.delete()


@bot_cmd(disable_errors=True, pattern="copy$")
async def _(event):
    reply = await event.get_reply_message()
    if reply:
        try:
            await reply.reply(reply)
        except BaseException:
            pass
    await event.delete()


@bot_cmd(disable_errors=True, pattern="edit")
async def _(event):
    chat = await event.get_input_chat()
    me = await event.client.get_peer_id("me")
    new_message = str(event.text[6:])
    reply = await event.get_reply_message()
    if reply and reply.text:
        try:
            await reply.edit(new_message)
            await event.delete()
        except BaseException:
            pass
    else:
        index = 1
        async for m in event.client.iter_messages(chat, me):
            if index == 2:
                await m.edit(new_message)
                await event.delete()
                break
            index = index + 1


@bot_cmd(disable_errors=True, pattern="sd")
async def _(event):
    counter = int(event.text[4:6])
    text = str(event.text[6:])
    await event.delete()
    NotUBot = await event.client.send_message(event.chat_id, text)
    await asyncio.sleep(counter)
    await NotUBot.delete()


@bot_cmd(disable_errors=True, pattern="reply$")
async def _(event):
    if event.reply_to_msg_id and event.chat_id in _new_msgs:
        msg = _new_msgs[event.chat_id]
        chat = await event.get_input_chat()
        await asyncio.wait(
            [
                event.client.delete_messages(chat, [event.id, msg.id]),
                event.client.send_message(chat, msg, reply_to=event.reply_to_msg_id),
            ]
        )
    else:
        await event.delete()


CMD_HELP.update(
    {
        "extra": [
            "Extra",
            "`.del|d|D|del|Del <reply to message>`\n"
            "↳ : Menghapus pesan yang dibalas.\n\n"
            "`.purge <reply to message>`\n"
            "↳ : Menghapus semua pesan dari balasan.\n\n"
            "`.purgeme <reply to message>`\n"
            "↳ : Menghapus <x> pesan dari yang terbaru.\n\n"
            "`.purgeall`\n"
            "↳ : Menghapus semua pesan pengguna yang dibalas.\n\n"
            "`.copy <reply to message>`\n"
            "↳ : Copy pesan yang dibalas.\n\n"
            "`.edit <new message>`\n"
            "↳ : Mengubah pesan terbaru atau balasan pesan.\n\n"
            "`.sd <x> <message>`\n"
            "↳ : Membuat pesan menjadi selfdestructs dalam <x> detik.\n"
            "Usahakan tetap dibawah 100 detik, untuk mengatasi notubot tertidur.\n\n"
            "`.reply`\n"
            "↳ : Balas pesan terakhir ke balasan pesan user.",
        ]
    }
)
