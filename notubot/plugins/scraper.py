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
from telethon.tl.functions.channels import InviteToChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.types import InputPeerUser, ChannelParticipantCreator, ChannelParticipantAdmin

from notubot import CMD_HELP
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


@bot_cmd(outgoing=True, groups_only=True, pattern="inviteall ?(.*)")
async def inviteall(event):
    sender = await event.get_sender()
    me = await event.client.get_me()

    if not sender.id == me.id:
        NotUBot = await event.reply("`...`")
    else:
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
    async for user in event.client.iter_participants(chatinfo.full_chat.id):
        if not (
            user.bot
            or user.deleted
            or isinstance(user.participant, ChannelParticipantAdmin)
            or isinstance(user.participant, ChannelParticipantCreator)
        ):
            try:
                if error.startswith("Too"):
                    return await NotUBot.edit(
                        f"""**Selesai Dengan Kesalahan** (`mungkin akun terkena limit atau kesalahan dari Telethon, coba lagi nanti`)
**Kesalahan:**
`{error}`

• Diculik `{success}` orang.
• Gagal mengundang `{failed}` orang."""
                    )

                await event.client(InviteToChannelRequest(channel=chat, users=[user.id]))
                success = success + 1
                await NotUBot.edit(
                    f"""**Sedang Mengundang...**
• Diculik `{success}` orang.
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


@bot_cmd(outgoing=True, groups_only=True, pattern="getmemb$")
async def getmemb(event):
    await event.edit("`...`")
    members = await event.client.get_participants(event.chat_id, aggressive=True)
    with open("members.csv", "w", encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(["user_id", "hash"])
        for member in members:
            writer.writerow([member.id, member.access_hash])

    await event.edit("`Berhasil mengumpulkan member.`")
    await event.delete()


@bot_cmd(outgoing=True, groups_only=True, pattern="addmemb$")
async def addmemb(event):
    await event.edit("`Proses menambahkan 0 member...`")
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
            await event.edit(f"`Mencapai 30 member, tunggu selama {900/60} menit.`")
            await asyncio.sleep(900)
        try:
            userin = InputPeerUser(user["id"], user["hash"])
            await event.client(InviteToChannelRequest(chat, [userin]))
            await asyncio.sleep(random.randrange(5, 7))
            await event.edit(f"`Prosess menambahkan {success} member...`")
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


@bot_cmd(outgoing=True, disable_errors=True, pattern="limit$")
async def limit(event):
    await event.edit("`...`")
    async with event.client.conversation("@SpamBot") as cov:
        try:
            res = cov.wait_event(events.NewMessage(incoming=True, from_users=178220800))
            await cov.send_message("/start")
            res = await res
            await event.client.send_read_acknowledge(cov.chat_id)
        except YouBlockedUserError:
            await event.edit("`Unblock @SpamBot !!`")
            return
        await event.edit(f"~ {res.message.message}")


CMD_HELP.update(
    {
        "scraper": [
            "Scraper",
            ">`.inviteall <id/username>`\n"
            "↳ : Mengundang orang dari grup dan ditambahkan ke grup.\n\n"
            ">`.getmemb`\n"
            "↳ : Mendapatkan semua member dalam grup.\n\n"
            ">`.addmemb`\n"
            "↳ : Menambahkan member ke target grup. Pertama, jalankan `.getmemb` lalu gunakan perintah ini ke target grup.\n\n"
            ">`.limit`\n"
            "↳ : Untuk cek akun kena limit.",
        ]
    }
)
