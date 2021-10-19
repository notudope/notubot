import asyncio
from platform import uname

from telethon import Button

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
            await event.edit(f"😖 Perintah [`{args}`] tidak ada, ketikan dengan benar!")
            await asyncio.sleep(200)
            await event.delete()
    else:
        head = f"`⚡NOTUBOT UserBot⚡ v{BOT_VER}`"
        head2 = f"😎 **User :** __{DEFAULTUSER}__"
        head3 = f"📦 **Module :** `{len(CMD_HELP)}`"
        head4 = "👨‍💻 **Usage :** `.help` `<nama module>`"
        head5 = "Daftar semua perintah tersedia di bawah ini: "
        head6 = "📌 **Gunakan perintah diatas dengan bijak dan seperlunya, resiko ditanggung pengguna!**"

        string = ""

        for i in sorted(CMD_HELP):
            string += "`" + str(i)
            string += "`  |  "
        string = string.rstrip(" |")

        await event.edit("⚡")
        await asyncio.sleep(1)
        await event.delete()

        markup = event.client.build_reply_markup(
            [
                Button.url("📢 Follow Channel", "https://t.me/notudope"),
                Button.url("🤖 UserBot REPO", "https://github.com/notudope/notubot"),
            ]
        )
        helper = await event.client.send_message(
            event.chat_id,
            f"{head}\
              \n\n{head2}\
              \n{head3}\
              \n{head4}\
              \n\n{head5}\
              \n\n{string}\
              \n\n{head6}",
            link_preview=False,
            buttons=markup,
        )

        await helper.reply(f"\n**Contoh** : Ketik <`.help limit`> Untuk informasi pengunaan.")
        await asyncio.sleep(1000)
        await helper.delete()
