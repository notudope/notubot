# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from asyncio import sleep, create_subprocess_exec, subprocess
from platform import python_version
from shutil import which

from git import Repo
from telethon import version, Button
from telethon.errors.rpcerrorlist import MediaEmptyError
from telethon.utils import get_display_name

from notubot import (
    ALIVE_LOGO,
    ALIVE_NAME,
    CMD_HELP,
    __botversion__,
    __botname__,
)
from notubot.events import bot_cmd

DEFAULTUSER = ALIVE_NAME


@bot_cmd(outgoing=True, pattern=r"^\.sysd$")
async def sysd(event):
    try:
        fetch = await create_subprocess_exec(
            "neofetch",
            "--stdout",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = await fetch.communicate()
        res = str(stdout.decode().strip()) + str(stderr.decode().strip())

        await event.edit("`" + res + "`")
    except FileNotFoundError:
        await event.edit("`neofetch tidak terinstall!`")


@bot_cmd(outgoing=True, pattern=r"^\.botver$")
async def botver(event):
    if which("git") is not None:
        ver = await create_subprocess_exec(
            "git",
            "describe",
            "--all",
            "--long",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        rev = await create_subprocess_exec(
            "git",
            "rev-list",
            "--all",
            "--count",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        await event.edit("`Version: " f"{verout}" "` \n" "`Revision: " f"{revout}" "`")
    else:
        await event.delete()


@bot_cmd(outgoing=True, pattern=r"^\.(alive|on)$")
async def aliveon(event):
    # [Instagram]({IG_ALIVE})
    me = await event.client.get_me()
    user = await event.client.get_entity("me")

    await event.edit("__Reconnect.__")
    await event.edit("__Reconnect..__")
    await event.edit("__Reconnect.__")
    await event.edit("__Reconnect..__")
    await event.edit("__Connecting...__")
    await event.edit("__Connecting..__")
    await event.edit("__Connecting...__")
    await event.edit("⚡")
    await sleep(1)

    text = (
        f"`{__botname__}`\n"
        f"[REPO](https://github.com/notudope/notubot)  /  [Channel](https://t.me/notudope)  /  [Support](https://t.me/NOTUBOTS)  /  [Mutualan](https://t.me/CariTeman_Asik)\n\n"
        f"😎 **Owner :** {DEFAULTUSER}\n"
        f"👥 **Fullname :** {get_display_name(user)}\n"
        f"🔖 **Username :** @{me.username}\n"
        f"👁️‍🗨️ **ID :** `{me.id}`\n"
        f"🤖 **Version :** `v{__botversion__}`\n"
        f"📦 **Plugin :** `{len(CMD_HELP)}`\n"
        f"🐍 **Python :** `v{python_version()}`\n"
        f"📦 **Telethon :** `v{version.__version__}\n`"
        f"⚙️ **Branch :** `{Repo().active_branch.name}`"
    )

    buttons = [
        [
            Button.url("REPO", "https://github.com/notudope/notubot"),
            Button.url("Channel", "https://t.me/notudope"),
            Button.url("Support", "https://t.me/NOTUBOTS"),
            Button.url("Mutualan", "https://t.me/CariTeman_Asik"),
        ],
    ]

    if ALIVE_LOGO:
        try:
            await event.delete()
            await event.client.send_file(event.chat_id, ALIVE_LOGO, caption=text)
        except MediaEmptyError:
            await event.edit(
                text + "\n\n `ALIVE_LOGO tidak valid.`",
            )
    else:
        await event.delete()
        await event.client.send_message(event.chat_id, text, link_preview=False, buttons=buttons)


@bot_cmd(outgoing=True, pattern="^.aliveu")
async def aliveonuser(event):
    message = event.text
    output = ".aliveu [ALIVE_NAME] tidak boleh kosong"
    if not (message == ".aliveu" or message[7:8] != " "):
        newuser = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = newuser

        output = "Berhasil mengubah ALIVE_NAME ke " + newuser
    await event.edit("`" f"{output}" "`")


@bot_cmd(outgoing=True, pattern=r"^\.resetalive$")
async def aliveonreset(event):
    global DEFAULTUSER
    DEFAULTUSER = ALIVE_NAME
    await event.edit("`Berhasil mengatur ulang ALIVE_NAME.`")


CMD_HELP.update(
    {
        "system": [
            "System",
            ">`.sysd`\n"
            "↳ : Menampilkan informasi sistem menggunakan neofetch.\n\n"
            ">`.botver`\n"
            "↳ : Menampilkan versi UserBot dari git.",
        ]
    }
)

CMD_HELP.update(
    {
        "alive": [
            "Alive",
            ">`.alive`\n"
            "↳ : Mengecek UserBot berjalan atau tidak.\n\n"
            ">`.aliveu <alive_name>`\n"
            "↳ : Mengubah nama user pada perintah .alive\n\n"
            ">`.resetalive`\n"
            "↳ : Mengatur ulang nama user alive.",
        ]
    }
)
