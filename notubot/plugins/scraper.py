# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio
import csv
import random

from telethon import events
from telethon.errors import ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError
from telethon.errors.rpcerrorlist import (
    UserAlreadyParticipantError,
    UserPrivacyRestrictedError,
    UserNotMutualContactError,
    YouBlockedUserError,
)
from telethon.tl.functions.channels import InviteToChannelRequest, GetFullChannelRequest, UnblockRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.types import InputPeerUser
from telethon.tl.types import ChannelParticipantsAdmins as Admins

from notubot import CMD_HELP, bot
from notubot.events import bot_cmd


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None

    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass

    if not chat:
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            if reply.fwd_from and reply.fwd_from.channel_id is not None:
                chat = reply.fwd_from.channel_id
        else:
            chat = None

    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Grup username/id tidak valid.`")
            return None
        except ChannelPrivateError:
            await event.reply("`Itu grup private atau dibanned dari sana.`")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Grup tujuan tidak ada.`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Input grup username/id tidak valid.`")
            return None
    return chat_info


@bot_cmd(groups_only=True, pattern="inviteall(?: |$)(.*)")
async def inviteall(event):
    NotUBot = await event.edit("`...`")
    chatinfo = await get_chatinfo(event)
    chat = await event.get_chat()
    success = failed = 0
    error = "None"

    if not chatinfo:
        await NotUBot.delete()
        await event.delete()
        return

    await NotUBot.edit("`Mengumpulkan member...`")
    async for x in event.client.iter_participants(chatinfo.full_chat.id, aggressive=True):
        if not (x.deleted or x.bot or isinstance(x.participant, Admins) or x.id == bot.uid):
            try:
                if error.startswith("Too"):
                    return await NotUBot.edit(
                        f"""**Selesai Dengan Kesalahan** (`mungkin akun terkena limit atau kesalahan dari Telethon, coba lagi nanti`)
**Kesalahan:**
`{error}`

• Diundang `{success}` orang.
• Gagal mengundang `{failed}` orang."""
                    )

                await event.client(InviteToChannelRequest(channel=chat, users=[x.id]))
                success = success + 1
                await NotUBot.edit(
                    f"""**Sedang Mengundang...**
• Diundang `{success}` orang.
• Gagal mengundang `{failed}` orang.

**Kesalahan:** `{error}`"""
                )
            except Exception as e:
                error = str(e)
                failed = failed + 1

    return await NotUBot.edit(
        f"""**Selesai Mengundang**
• Berhasil mengundang `{success}` orang.
• Gagal mengundang `{failed}` orang."""
    )


@bot_cmd(groups_only=True, pattern="getmemb$")
async def getmemb(event):
    NotUBot = await event.edit("`...`")
    members = await event.client.get_participants(event.chat_id, aggressive=True)

    with open("members.csv", "w", encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(["user_id", "hash"])

        for x in members:
            if not (x.deleted or x.bot or isinstance(x.participant, Admins) or x.id == bot.uid):
                writer.writerow([x.id, x.access_hash])

    await NotUBot.edit("`Berhasil mengumpulkan member.`")
    await NotUBot.delete()


@bot_cmd(groups_only=True, pattern="addmemb$")
async def addmemb(event):
    NotUBot = await event.edit("`...`")
    chat = await event.get_chat()
    users = []

    with open("members.csv", encoding="UTF-8") as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {"id": int(row[0]), "hash": int(row[1])}
            users.append(user)

    success = 0
    for user in users:
        success += 1
        if success % 30 == 0:
            await NotUBot.edit(f"`Mencapai 30 member, tunggu selama {900/60} menit.`")
            await asyncio.sleep(900)
        try:
            userin = InputPeerUser(user["id"], user["hash"])
            await event.client(InviteToChannelRequest(chat, [userin]))
            await asyncio.sleep(random.randrange(5, 7))
            await NotUBot.edit(f"`Prosess menambahkan {success} member...`")
        except TypeError:
            success -= 1
            continue
        except UserAlreadyParticipantError:
            success -= 1
            continue
        except UserPrivacyRestrictedError:
            success -= 1
            continue
        except UserNotMutualContactError:
            success -= 1
            continue


@bot_cmd(disable_errors=True, pattern="limit$")
async def limit(event):
    NotUBot = await event.edit("`...`")
    async with event.client.conversation("@SpamBot") as conv:
        try:
            res = conv.wait_event(events.NewMessage(incoming=True, from_users=178220800))
            await conv.send_message("/start")
            res = await res
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await NotUBot.edit("`Unblock @SpamBot`")
            await event.client(UnblockRequest("@SpamBot"))
            return
        await NotUBot.edit(f"~ {res.message.message}")


CMD_HELP.update(
    {
        "scraper": [
            "Scraper",
            "`.inviteall <id/username>`\n"
            "↳ : Mengundang orang dari grup dan ditambahkan ke grup.\n\n"
            "`.getmemb`\n"
            "↳ : Mendapatkan semua member dalam grup.\n\n"
            "`.addmemb`\n"
            "↳ : Menambahkan member ke target grup. Pertama, jalankan `getmemb` lalu gunakan perintah ini ke target grup.\n\n"
            "`.limit`\n"
            "↳ : Untuk cek akun kena limit.",
        ]
    }
)
