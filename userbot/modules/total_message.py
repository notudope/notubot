from telethon.utils import get_display_name

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.total(?: |$)(.*)")
async def total(event):
    match = event.pattern_match.group(1)
    await event.edit("`...`")

    if match:
        user = match
    elif event.is_reply:
        user = (await event.get_reply_message()).sender_id
    else:
        user = "me"

    a = await event.client.get_messages(event.chat_id, 0, from_user=user)
    user = await event.client.get_entity(user)
    await event.edit(f"Total pesan dari `{get_display_name(user)}` [`{a.total}`]")


CMD_HELP.update(
    {"totalmsg": ">`.total [username]/<reply>`" "\nUsage: Melihat total pesan pengguna dalam obrolan saat ini."}
)
