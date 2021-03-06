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
from random import choice
from shutil import which
from time import time

from carbonnow import Carbon
from git import Repo
from telethon import version
from telethon.errors.rpcerrorlist import MediaEmptyError, ChatSendMediaForbiddenError, ChatSendGifsForbiddenError

from notubot import (
    ALIVE_LOGO,
    CMD_HELP,
    __botversion__,
    __botname__,
    start_time,
    BOTLOG,
    bot,
    BOTLOG_CHATID,
    ALIVE_TEXT,
    ALIVE_IG,
)
from notubot.events import bot_cmd
from notubot.functions import (
    time_formatter,
    restart,
    shutdown,
    run_cmd,
    heroku_logs,
    def_logs,
)

from . import ATRA_COL

alive_text = """<code>{}</code>

<b>{}</b>

┏━━━━━━━━━━━━━━━━━━━━━━━
┣  <b>Owner</b> - <code>{}</code>
┣  <b>Username</b> - {}
┣  <b>ID</b> - <code>{}</code>
┣  <b>Instagram</b> - <a href=https://www.instagram.com/{}>@{}</a>
┣  <b>Version</b> - <code>v{}</code>
┣  <b>Plugin</b> - <code>{}</code>
┣  <b>Ping</b> - <code>{}ms</code>
┣  <b>Uptime</b> - <code>{}</code>
┣  <b>Python</b> - <code>{}</code>
┣  <b>Telethon</b> - <code>{}</code>
┣  <b>Branch</b> - {}
┗━━━━━━━━━━━━━━━━━━━━━━━

<a href=https://github.com/notudope/notubot>Repo</a>  •  <a href=https://t.me/notudope>Channel</a>  •  <a href=https://t.me/NOTUBOTS>Support</a>  •  <a href=https://t.me/CariTemanOK>Mutualan</a>"""


@bot_cmd(disable_errors=True, pattern="(alive|on)$")
async def aliveon(event):
    start = time()
    await event.edit("ㅤ")
    ms = round((time() - start) * 1000)
    # me = await event.client.get_me()
    # user = await event.client.get_entity("me")
    uptime = time_formatter((time() - start_time) * 1000)
    b = Repo().active_branch
    g = Repo().remotes[0].config_reader.get("url")
    r = g.replace(".git", f"/tree/{b}")
    branch = f"<a href={r}>{b}</a>"
    username_or_mention = f"@{bot.me.username}" if bot.me.username else f"<a href=tg://user?id={bot.uid}>{bot.uid}</a>"

    await event.edit(".")
    await event.edit("..")
    await event.edit("...")
    await event.edit("⚡")
    await asyncio.sleep(2)

    text = alive_text.format(
        __botname__,
        ALIVE_TEXT,
        bot.name,
        username_or_mention,
        bot.uid,
        ALIVE_IG,
        ALIVE_IG,
        __botversion__,
        len(CMD_HELP),
        ms,
        uptime,
        python_version(),
        version.__version__,
        branch,
    )

    if ALIVE_LOGO:
        try:
            await event.client.send_file(event.chat_id, ALIVE_LOGO, caption=text, parse_mode="html")
        except MediaEmptyError:
            await event.client.send_message(
                event.chat_id, text + "\n\n <code>ALIVE_LOGO tidak valid.</code>", link_preview=False, parse_mode="html"
            )
        except (ChatSendMediaForbiddenError, ChatSendGifsForbiddenError):
            await event.client.send_message(event.chat_id, text, link_preview=False, parse_mode="html")
    else:
        await event.client.send_message(event.chat_id, text, link_preview=False, parse_mode="html")

    await event.delete()


@bot_cmd(pattern="restart$")
async def restarting(event):
    await event.edit("`{} Restarting...`".format(__botname__))

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#bot #restart \n" "Restarting notubot...")

    try:
        from notubot.database.globals import addgv, delgv

        delgv("restartstatus")
        addgv("restartstatus", f"{event.chat_id}\n{event.id}")
    except AttributeError:
        pass

    await event.client.disconnect()
    await restart(event)

    await run_cmd("git pull && pip3 install -U -r requirements.txt")
    os.execl(sys.executable, sys.executable, "-m", "notubot")


@bot_cmd(pattern="shutdown$")
async def shuttingdown(event):
    await event.edit("`{} Shutting down...`".format(__botname__))

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#bot #shutdown \n" "Shutting down notubot...")

    await event.client.disconnect()
    await shutdown(event)


@bot_cmd(pattern="logs(?: |$)(.*)")
async def logsys(event):
    opt = event.pattern_match.group(1)

    if opt == "heroku":
        await heroku_logs(event)
    elif opt == "carbon" and Carbon:
        event = await event.edit("`...`")
        code = open("notubot.log", "r").read()[-2500:]
        file = await Carbon(
            base_url="https://carbonara.vercel.app/api/cook",
            code=code,
            background=choice(ATRA_COL),
        ).memorize("notubot-logs")

        await event.reply("**NOTUBOT Logs**", file=file)
    else:
        await def_logs(event)

    await event.delete()


@bot_cmd(pattern="botver$")
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


@bot_cmd(pattern="sysd$")
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


@bot_cmd(disable_errors=True, pattern="ping|([pP]ing)$")
async def ping(event):
    if event.out:
        await event.delete()

    start = time()
    NotUBot = await event.respond("Pong !")
    end = round((time() - start) * 1000)
    uptime = time_formatter((time() - start_time) * 1000)
    await NotUBot.edit("**Pong !!** `{}ms`\n**Uptime** - `{}`".format(end, uptime))
    await asyncio.sleep(15)
    await NotUBot.delete()


CMD_HELP.update(
    {
        "bot": [
            "Bot",
            "`.alive`\n"
            "↳ : Mengecek notubot berjalan atau tidak.\n\n"
            "`.restart`\n"
            "↳ : Muat ulang notubot.\n\n"
            "`.shutdown`\n"
            "↳ : Mematikan notubot.\n\n"
            "`.logs`\n"
            "↳ : Mengambil full terminal logs.\n\n"
            "`.logs carbon`\n"
            "↳ : Mengambil carbonized sys logs.\n\n"
            "`.logs heroku`\n"
            "↳ : Mengambil 100 baris terbaru dari heroku logs.\n\n"
            "`.botver`\n"
            "↳ : Menampilkan versi notubot dari git.\n\n"
            "`.sysd`\n"
            "↳ : Menampilkan informasi sistem menggunakan neofetch.\n\n"
            "`.ping|[pP]ing`\n"
            "↳ : Cek waktu respon notubot.",
        ]
    }
)
