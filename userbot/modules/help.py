import asyncio
from platform import uname

from userbot import CMD_HELP, BOT_VER, ALIVE_NAME
from userbot.events import register

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node


@register(outgoing=True, pattern=r"^\.help(?: |$)(.*)")
async def help_handler(event):
    """For .help command."""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit(f"Perintah `{args}` tidak benar, harap ketikan dengan benar.")
            await asyncio.sleep(20)
            await event.delete()
    else:
        head = f"**⚡NOTUBOT UserBot⚡ V{BOT_VER}**"
        head2 = f"UserBot untuk **{DEFAULTUSER}**"
        head3 = f"📦 Loaded Modules : {len(CMD_HELP)}"
        head4 = "👨‍💻 Usage: `.help` `<nama module>`"
        head5 = "Daftar semua perintah tersedia di bawah ini: "
        string = ""

        for i in sorted(CMD_HELP):
            string += "`" + str(i)
            string += "`  |  "

        await event.edit(
            f"{head}\
              \n\n{head2}\
              \n{head3}\
              \n{head4}\
              \n{head5}\
              \n\n{string.rstrip('|')}"
        )
        await event.reply(f"\n**Contoh** : Ketik <`.help gban`> Untuk informasi pengunaan.")
        await asyncio.sleep(100)
        await event.delete()
