from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.total(?: |$)(.*)")
async def total(event):
    user = await event.get_reply_message()
    await event.edit("`...`")

    if user:
        t = await bot.get_messages(event.chat_id, 0, from_user=user.sender_id)
        return await event.edit(f"Total pesan `{t.total}`")

    name = event.pattern_match.group(1)
    if not name:
        name = "me"

    t = await bot.get_messages(event.chat_id, 0, from_user=name)
    await event.edit(f"Total pesan dari {name} yaitu `{t.total}`")


CMD_HELP.update(
    {"totalmsg": ">`.total` | `.total` <username>" "\nUsage: Mengambil total pesan pengguna dalam obrolan saat ini."}
)
