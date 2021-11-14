# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio
import os
import sys
from platform import python_version
from shutil import which
from time import time

from git import Repo
from telethon import version
from telethon.errors.rpcerrorlist import MediaEmptyError
from telethon.utils import get_display_name

from notubot import (
    ALIVE_LOGO,
    CMD_HELP,
    __botversion__,
    __botname__,
    start_time,
    BOTLOG,
    BOTLOG_CHATID,
    HEROKU_API_KEY,
)
from notubot.events import bot_cmd
from notubot.utils import time_formatter, restart, run_cmd


@bot_cmd(outgoing=True, pattern="(alive|on)$")
async def aliveon(event):
    # [Instagram]({IG_ALIVE})
    me = await event.client.get_me()
    user = await event.client.get_entity("me")
    uptime = time_formatter((time() - start_time) * 1000)
    b = Repo().active_branch
    g = Repo().remotes[0].config_reader.get("url")
    r = g.replace(".git", f"/tree/{b}")
    branch = f"[{b}]({r})"

    await event.edit(".")
    await event.edit("..")
    await event.edit("...")
    await event.edit("⚡")
    await asyncio.sleep(2)

    text = (
        f"`{__botname__}`\n"
        f"[REPO](https://github.com/notudope/notubot)  /  [Channel](https://t.me/notudope)  /  [Support](https://t.me/NOTUBOTS)  /  [Mutualan](https://t.me/CariTemanOK)\n\n"
        f"**Owner** - `{get_display_name(user)}`\n"
        f"**Username** - @{me.username}\n"
        f"**ID** - `{me.id}`\n"
        f"**Version** - `v{__botversion__}`\n"
        f"**Plugin** - `{len(CMD_HELP)}`\n"
        f"**Uptime** - `{uptime}`\n"
        f"**Python** - `{python_version()}`\n"
        f"**Telethon** - `{version.__version__}\n`"
        f"**Branch** - {branch}"
    )

    if ALIVE_LOGO:
        try:
            await event.client.send_file(event.chat_id, ALIVE_LOGO, caption=text)
            await event.delete()
        except MediaEmptyError:
            await event.edit(
                text + "\n\n `ALIVE_LOGO tidak valid.`",
            )
    else:
        await event.client.send_message(
            event.chat_id,
            text,
            link_preview=False,
        )
        await event.delete()


@bot_cmd(outgoing=True, pattern="restart$")
async def restartbot(event):
    await event.edit("`Restarting {} ...`".format(__botname__))

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#bot #restart \n" "Restarting UserBot...")

    try:
        from notubot.plugins.sql_helper.globals import addgvar, delgvar

        delgvar("restartstatus")
        addgvar("restartstatus", f"{event.chat_id}\n{event.id}")
    except AttributeError:
        pass

    await event.client.disconnect()
    if HEROKU_API_KEY:
        return await restart(event)

    await run_cmd("git pull && pip3 install -r requirements.txt")
    os.execl(sys.executable, sys.executable, "-m", "notubot")


@bot_cmd(outgoing=True, pattern="shutdown$")
async def shutdown(event):
    await event.edit("`Shutting down {} ...`".format(__botname__))

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#bot #shutdown \n" "Shutting down UserBot...")

    await event.client.disconnect()


@bot_cmd(outgoing=True, pattern="botver$")
async def botver(event):
    if which("git") is None:
        return await event.delete()

    ver = await asyncio.create_subprocess_exec(
        "git",
        "describe",
        "--all",
        "--long",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await ver.communicate()
    verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

    rev = await asyncio.create_subprocess_exec(
        "git",
        "rev-list",
        "--all",
        "--count",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await rev.communicate()
    revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

    await event.edit("`Version: " f"{verout}" "` \n" "`Revision: " f"{revout}" "`")


@bot_cmd(outgoing=True, pattern="sysd$")
async def sysd(event):
    try:
        neofetch = await asyncio.create_subprocess_exec(
            "neofetch",
            "--stdout",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        stdout, stderr = await neofetch.communicate()
        res = str(stdout.decode().strip()) + str(stderr.decode().strip())
        await event.edit("`" + res + "`")
    except FileNotFoundError:
        await event.edit("`neofetch tidak terinstall!`")


@bot_cmd(outgoing=True, disable_errors=True, pattern="ping$")
async def ping(event):
    if event.out:
        await event.delete()

    start = time()
    x = await event.respond("Pong !")
    end = round((time() - start) * 1000)
    uptime = time_formatter((time() - start_time) * 1000)
    await x.edit("**Pong !!** `{}ms`\n**Uptime** - `{}`".format(end, uptime))
    await asyncio.sleep(20)
    await x.delete()


CMD_HELP.update(
    {
        "system": [
            "System",
            "`.alive`\n"
            "↳ : Mengecek UserBot berjalan atau tidak.\n\n"
            "`.restart`\n"
            "↳ : Muat ulang UserBot.\n\n"
            "`.shutdown`\n"
            "↳ : Mematikan UserBot.\n\n"
            "`.botver`\n"
            "↳ : Menampilkan versi UserBot dari git.\n\n"
            "`.sysd`\n"
            "↳ : Menampilkan informasi sistem menggunakan neofetch.",
        ]
    }
)
