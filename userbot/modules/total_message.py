from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.tmsg (.*)")
async def _(event):
    k = await event.get_reply_message()

    if k:
        a = await bot.get_messages(event.chat_id, 0, from_user=k.sender_id)
        return await event.edit(f"Total pesan `{a.total}`")

    u = event.pattern_match.group(1)
    if not u:
        u = "me"

    a = await bot.get_messages(event.chat_id, 0, from_user=u)
    await event.edit(f"Total pesan dari {u} yaitu `{a.total}`")


CMD_HELP.update(
    {
        "totalmsg": ">`.tmsg` | `.tmsg` <username>"
        "\nUsage: Mengambil jumlah pesan total pengguna dalam obrolan saat ini."
    }
)
