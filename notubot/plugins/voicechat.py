# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from asyncio import sleep

from pytgcalls import GroupCallFactory
from telethon.tl.functions.channels import GetFullChannelRequest, DeleteMessagesRequest
from telethon.tl.functions.phone import CreateGroupCallRequest, DiscardGroupCallRequest, InviteToGroupCallRequest

from notubot import (
    CMD_HELP,
    bot,
    HANDLER,
    GROUP_CALLS,
)
from notubot.events import bot_cmd


async def get_call(event):
    call = await event.client(GetFullChannelRequest(event.chat.id))
    return call.full_chat.call


def user_list(ls, n):
    for i in range(0, len(ls), n):
        yield ls[i : i + n]


@bot_cmd(disable_errors=True, admins_only=True, can_call=True, pattern="startvc(?: |$)(.*)")
async def startvc(event):
    NotUBot = await event.edit("`...`")
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
        await NotUBot.edit("`Memulai Obrolan Suara...`")
        await sleep(3)
    else:
        await NotUBot.delete()
        if _group and _group.updates[1].id is not None:
            await event.client(DeleteMessagesRequest(event.chat_id, [_group.updates[1].id]))


@bot_cmd(disable_errors=True, admins_only=True, can_call=True, pattern="(stopvc|endvc)(?: |$)(.*)")
async def endvc(event):
    NotUBot = await event.edit("`...`")
    opts = event.pattern_match.group(1)
    silent = ["s", "silent"]
    stfu = True if opts in silent else False

    try:
        call = await get_call(event)
    except BaseException:
        call = None

    if not call:
        await NotUBot.edit("`Tidak ada obrolan.`")
        await sleep(3)
        return await NotUBot.delete()

    _group = await event.client(DiscardGroupCallRequest(call))

    if not stfu:
        await NotUBot.edit("`Obrolan Suara dimatikan...`")
        await sleep(3)
        await NotUBot.delete()
    else:
        await NotUBot.delete()
        if _group and _group.updates[1].id is not None:
            await event.client(DeleteMessagesRequest(event.chat_id, [_group.updates[1].id]))


@bot_cmd(disable_errors=True, groups_only=True, admins_only=True, pattern="joinvc$")
async def joinvc(event):
    NotUBot = await event.edit("`...`")

    try:
        call = await get_call(event)
    except BaseException:
        call = None

    if not call:
        await NotUBot.edit(f"`Tidak ada obrolan, mulai dengan {HANDLER}startvc`")
        await sleep(15)
        return await NotUBot.delete()

    group_call = GROUP_CALLS.get(event.chat.id)
    if group_call is None:
        group_call = GroupCallFactory(
            event.client,
            GroupCallFactory.MTPROTO_CLIENT_TYPE.TELETHON,
            enable_logs_to_console=False,
            path_to_log_file=None,
        ).get_file_group_call(None)
        GROUP_CALLS[event.chat.id] = group_call

    if not (group_call and group_call.is_connected):
        await group_call.start(event.chat.id, enable_action=False)

    await NotUBot.edit("`joined`")
    await sleep(3)
    await NotUBot.delete()


@bot_cmd(disable_errors=True, groups_only=True, admins_only=True, pattern="leavevc$")
async def leavevc(event):
    NotUBot = await event.edit("`...`")

    try:
        call = await get_call(event)
    except BaseException:
        call = None

    if not call:
        await NotUBot.edit(f"`Tidak ada obrolan, mulai dengan {HANDLER}startvc`")
        await sleep(15)
        return await NotUBot.delete()

    group_call = GROUP_CALLS.get(event.chat.id)
    if group_call and group_call.is_connected:
        await group_call.leave_current_group_call()
        await group_call.stop()

    await NotUBot.edit("`leaved`")
    await sleep(3)
    await NotUBot.delete()


@bot_cmd(groups_only=True, admins_only=True, pattern="vcinvite$")
async def vcinvite(event):
    NotUBot = await event.edit("`...`")
    users = []
    invited = 0

    try:
        call = await get_call(event)
    except BaseException:
        call = None

    if not call:
        return await NotUBot.delete()
    await NotUBot.edit("`Mengundang orang ke Obrolan Suara...`")

    chat = await event.get_chat()
    async for x in event.client.iter_participants(chat, aggressive=True):
        if not (x.bot or x.deleted or x.id == bot.uid):
            users.append(x.id)

    for user in list(user_list(users, 6)):
        try:
            await event.client(InviteToGroupCallRequest(call=call, users=user))
            invited += 6
            await sleep(2)
        except BaseException:
            pass

    await NotUBot.edit(f"`Diundang {invited} orang.`")
    await sleep(15)
    await NotUBot.delete()


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
