# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from asyncio import sleep, create_subprocess_exec, subprocess
from platform import python_version
from shutil import which
from time import time

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
    start_time,
)
from notubot.events import bot_cmd
from notubot.utils.tools import time_formatter

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
    uptime = time_formatter((time() - start_time) * 1000)
    b = Repo().active_branch
    g = Repo().remotes[0].config_reader.get("url")
    r = g.replace(".git", f"/tree/{b}")
    branch = f" `[{b}]({r})` "

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
        f"**Owner** - {DEFAULTUSER}\n"
        f"**Fullname** - `{get_display_name(user)}`\n"
        f"**Username** - @{me.username}\n"
        f"**ID** - `{me.id}`\n"
        f"**Version** - `v{__botversion__}`\n"
        f"**Plugin** - `{len(CMD_HELP)}`\n"
        f"**UpTime** - `{uptime}`\n"
        f"**Python** - `{python_version()}`\n"
        f"**Telethon** - `{version.__version__}\n`"
        f"**Branch** - {branch}"
    )

    buttons = [
        [
            Button.url("REPO", "https://github.com/notudope/notubot"),
            Button.url("Channel", "https://t.me/notudope"),
        ],
        [
            Button.url("Support", "https://t.me/NOTUBOTS"),
            Button.url("Mutualan", "https://t.me/CariTeman_Asik"),
        ],
    ]

    if ALIVE_LOGO:
        try:
            await event.delete()
            await event.client.send_file(event.chat_id, ALIVE_LOGO, caption=text, buttons=buttons)
        except MediaEmptyError:
            await event.edit(
                text + "\n\n `ALIVE_LOGO tidak valid.`",
            )
    else:
        await event.delete()
        await event.client.send_message(
            event.chat_id,
            text,
            buttons=buttons,
            link_preview=False,
        )


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


@bot_cmd(outgoing=True, pattern=r"^\.ping$")
async def ping(event):
    if event.out:
        await event.delete()

    start = time()
    x = await event.respond("Pong !")
    end = round((time() - start) * 1000)
    uptime = time_formatter((time() - start_time) * 1000)
    await x.edit("**Pong !!** `{}ms`\n**Uptime** - `{}`".format(end, uptime))
    await sleep(15)
    await x.delete()
    await event.delete()


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
