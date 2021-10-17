from userbot import CMD_HELP
from userbot.events import register
from userbot.utils.format import parse_pre


@register(outgoing=True, pattern=r"^\.json$")
async def json(event):
    "To get details of that message in json format."
    reply = await event.get_reply_message() if event.reply_to_msg_id else event

    await event.edit(reply.stringify(), parse_mode=parse_pre)


CMD_HELP.update(
    {"json": ">`.json`" "\nUsage: Mengambil data json dari sebuah pesan, " "Balas pesan tersebut untuk menampilkannya!"}
)
