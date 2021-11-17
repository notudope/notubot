# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from asyncio import sleep

from pytgcalls import GroupCallFactory
from telethon.tl.functions.channels import GetFullChannelRequest, DeleteMessagesRequest
from telethon.tl.functions.phone import (
    CreateGroupCallRequest,
    DiscardGroupCallRequest,
    InviteToGroupCallRequest,
    GetGroupCallRequest,
)

from notubot import CMD_HELP, bot, HANDLER
from notubot.events import bot_cmd

group_call_factory = GroupCallFactory(bot, GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON)
group_call = group_call_factory.get_file_group_call(None)


async def get_call(event):
    x = await event.client(GetFullChannelRequest(event.chat_id))
    xx = await event.client(GetGroupCallRequest(x.full_chat.call))
    return xx.call


def user_list(ls, n):
    for i in range(0, len(ls), n):
        yield ls[i : i + n]


@bot_cmd(disable_errors=True, groups_only=True, admins_only=True, pattern="startvc(?: |$)(.*)")
async def _(event):
    opts = event.pattern_match.group(1)
    args = opts.split(" ")

    silent = ["s", "silent"]
    stfu = True if args[0] in silent else False

    title = ""
    for i in args[1:]:
        title += i + " "

    _group = await event.client(
        CreateGroupCallRequest(
            event.chat_id,
            title=title,
        )
    )

    if not stfu:
        await event.edit("`Memulai Obrolan Suara...`")
        await sleep(3)
    else:
        await event.delete()
        if _group and _group.updates[1].id is not None:
            await event.client(DeleteMessagesRequest(event.chat_id, [_group.updates[1].id]))


@bot_cmd(disable_errors=True, groups_only=True, admins_only=True, pattern="(stopvc|endvc)(?: |$)(.*)")
async def _(event):
    opts = event.pattern_match.group(1)
    silent = ["s", "silent"]
    stfu = True if opts in silent else False

    try:
        call = await get_call(event)
    except BaseException:
        call = None

    if not call:
        await event.edit("`Tidak ada obrolan.`")
        await sleep(3)
        return await event.delete()

    _group = await event.client(DiscardGroupCallRequest(call))

    if not stfu:
        await event.edit("`Obrolan Suara dimatikan...`")
        await sleep(3)
        await event.delete()
    else:
        await event.delete()
        if _group and _group.updates[1].id is not None:
            await event.client(DeleteMessagesRequest(event.chat_id, [_group.updates[1].id]))


@bot_cmd(disable_errors=True, groups_only=True, admins_only=True, pattern="joinvc$")
async def _(event):
    await event.edit("`...`")

    try:
        call = await get_call(event)
    except BaseException:
        call = None

    if not call:
        await event.edit(f"`Tidak ada obrolan, mulai dengan {HANDLER}startvc`")
        await sleep(15)
        return await event.delete()

    if not (group_call and group_call.is_connected):
        await group_call.start(event.chat.id, enable_action=False)
        group_call.enable_action = False

    await event.edit("`joined`")
    await sleep(3)
    await event.delete()


@bot_cmd(disable_errors=True, groups_only=True, admins_only=True, pattern="leavevc$")
async def _(event):
    await event.edit("`...`")

    try:
        call = await get_call(event)
    except BaseException:
        call = None

    if not call:
        await event.edit(f"`Tidak ada obrolan, mulai dengan {HANDLER}startvc`")
        await sleep(15)
        return await event.delete()

    if group_call and group_call.is_connected:
        await group_call.stop()

    await event.edit("`leaved`")
    await sleep(3)
    await event.delete()


@bot_cmd(groups_only=True, admins_only=True, pattern="vcinvite$")
async def _(event):
    await event.edit("`Mengundang orang ke Obrolan Suara...`")
    await event.get_chat()
    users = []
    invited = 0

    try:
        call = await get_call(event)
    except BaseException:
        call = None

    if not call:
        return await event.delete()

    async for x in event.client.iter_participants(event.chat_id):
        if not (x.bot or x.deleted):
            users.append(x.id)

    for user in list(user_list(users, 6)):
        try:
            await event.client(InviteToGroupCallRequest(call=call, users=user))
            invited += 6
            await sleep(2)
        except BaseException:
            pass

    await event.edit(f"`Diundang {invited} orang.`")
    await sleep(15)
    await event.delete()


CMD_HELP.update(
    {
        "voicechat": [
            "Voice Chat",
            """`.startvc <silent/s> <judul>`
↳ : Memulai Obrolan Suara.

`.stopvc|endvc <silent/s>`
↳ : Mematikan Obrolan Suara.

`.joinvc`
↳ : Bergabung ke Obrolan Suara.

`.leavevc`
↳ : Keluar dari Obrolan Suara.

`.vcinvite`
↳ : Mengundang semua anggota grup ke Obrolan Suara.
""",
        ]
    }
)
