from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.utils.format import parse_pre


@register(outgoing=True, pattern=r"^\.json$")
async def json(event):
    "To get details of that message in json format."
    reply = await event.get_reply_message() if event.reply_to_msg_id else event

    text = reply.stringify()
    if event.reply_to_msg_id:
        await event.delete()
        await event.reply(text, parse_mode=parse_pre)
    else:
        await event.edit(text, parse_mode=parse_pre)


CMD_HELP.update(
    {"json": ">`.json`" "\nUsage: Mengambil data json dari sebuah pesan, " "Balas pesan tersebut untuk menampilkannya!"}
)
