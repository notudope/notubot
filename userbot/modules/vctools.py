from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from userbot import CMD_HELP
from userbot.events import register


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call


def user_list(ls, n):
    for i in range(0, len(ls), n):
        yield ls[i : i + n]


@register(outgoing=True, groups_only=True, admins_only=True, pattern=r"^\.startvc$")
async def vcstart(e):
    try:
        await e.client(
            startvc(
                peer=e.chat_id,
                title="",
            )
        )
        await e.edit("`Memulai Obrolan Video...`")
    except BaseException:
        pass


@register(outgoing=True, groups_only=True, admins_only=True, pattern=r"^\.stopvc$")
async def vcstop(e):
    try:
        await e.client(stopvc(await get_call(e)))
        await e.edit("`Obrolan Video dimatikan...`")
    except BaseException:
        pass


@register(outgoing=True, groups_only=True, admins_only=True, pattern=r"^\.vcinvite$")
async def vcinvite(e):
    ok = await e.edit("`Mengundang semua anggota grup ke Obrolan Video...`")
    users = []
    z = 0

    async for x in e.client.iter_participants(e.chat_id):
        if not x.bot:
            users.append(x.id)
    hmm = list(user_list(users, 6))

    for p in hmm:
        try:
            await e.client(invitetovc(call=await get_call(e), users=p))
            z += 6
        except BaseException:
            pass

    await ok.edit(f"`Diundang {z} anggota`")


CMD_HELP.update(
    {
        "startvc": ">`.startvc`"
        "\nUsage: Memulai Obrolan Video (admin)."
        "\n\n>`.stopvc`"
        "\nUsage: Mematikan Obrolan Video (admin)."
        "\n\n>`.vcinvite`"
        "\nUsage: Mengundang semua anggota grup ke Obrolan Video (admin)."
    }
)
