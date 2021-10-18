import asyncio
import csv
import random

from telethon.errors import ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError
from telethon.errors.rpcerrorlist import (
    UserAlreadyParticipantError,
    UserPrivacyRestrictedError,
    UserNotMutualContactError,
)
from telethon.tl.functions.channels import InviteToChannelRequest, GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.types import InputPeerUser

from userbot import CMD_HELP
from userbot.events import register


async def get_chat_id(event):
    chat = event.pattern_match.group(1).strip()
    chat_id = None

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
            chat = event.chat_id

    try:
        chat_id = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_id = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Group tidak valid!`")
            return None
        except ChannelPrivateError:
            await event.reply("`Ini adalah grup private atau dibanned dari sana.`")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Grup tidak ada!`")
            return None
        except (TypeError, ValueError):
            await event.reply("`Group tidak valid!`")
            return None
    return chat_id


@register(outgoing=True, groups_only=True, pattern=r"^\.inviteall(?: |$)(.*)")
async def get_users(event):
    sender = await event.get_sender()
    me = await event.client.get_me()

    if not sender.id == me.id:
        proc = await event.reply("`...`")
    else:
        proc = await event.edit("`...`")

    chat_id = await get_chat_id(event)
    chat = await event.get_chat()

    s = 0
    f = 0
    error = "None"

    await proc.edit("`Mengumpulkan member...`")

    async for user in event.client.iter_participants(chat_id.full_chat.id):
        try:
            if error.startswith("Too"):
                return await proc.edit(
                    f"""Berhasil menculik orang [`Limit dari telethon, coba lagi nanti!`].
**ERROR :**
`{error}`

• Diculik `{s}` orang.
• Gagal menculik `{f}` orang."""
                )

            await event.client(InviteToChannelRequest(channel=chat, users=[user.id]))
            s = s + 1

            await proc.edit(
                f"""• Diculik `{s}` orang.
• Gagal menculik `{f}` orang.

**ERROR :** `{error}`"""
            )
        except Exception as e:
            error = str(e)
            f = f + 1
    return await proc.edit(f"Berhasil menculik `{s}` orang. Gagal menculik `{f}` orang.")


@register(outgoing=True, groups_only=True, pattern=r"^\.getmemb$")
async def scrapmem(event):
    chat = event.chat_id
    await event.edit("`...`")

    members = await event.client.get_participants(chat, aggressive=True)
    with open("members.csv", "w", encoding="UTF-8") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(["user_id", "hash"])
        for member in members:
            writer.writerow([member.id, member.access_hash])

    await event.edit("`Berhasil mengumpulkan member..`")
    await event.delete()


@register(outgoing=True, groups_only=True, pattern=r"^\.addmemb$")
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

    n = 0
    for user in users:
        n += 1
        if n % 30 == 0:
            await event.edit(f"`Mencapai 30 member, tunggu selama {900/60} menit.`")
            await asyncio.sleep(900)
        try:
            userin = InputPeerUser(user["id"], user["hash"])
            await event.client(InviteToChannelRequest(chat, [userin]))
            await asyncio.sleep(random.randrange(5, 7))
            await event.edit(f"`Prosess menambahkan {n} member...`")
        except TypeError:
            n -= 1
            continue
        except UserAlreadyParticipantError:
            n -= 1
            continue
        except UserPrivacyRestrictedError:
            n -= 1
            continue
        except UserNotMutualContactError:
            n -= 1
            continue


CMD_HELP.update(
    {
        "scraper": ">`.inviteall <id/username>`"
        "\nUsage: Menculik pengguna dari grup dan ditambahkan ke grup."
        "\n\n>`.getmemb`"
        "\nUsage: Mendapatkan semua member dalam grup."
        "\n\n>`.addmemb`"
        "\nUsage: Menambahkan member ke target grup, "
        "Pertama, jalankan `.getmemb` lalu gunakan perintah ini ke target grup."
    }
)
