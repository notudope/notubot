# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from os import remove
from platform import python_version
from shutil import which

from git import Repo
from telethon import version, Button
from telethon.errors.rpcerrorlist import MediaEmptyError

from notubot import (
    ALIVE_LOGO,
    ALIVE_NAME,
    CMD_HELP,
    BOT_VER,
    BOT_NAME,
    IG_ALIVE,
)
from notubot.events import bot_cmd

DEFAULTUSER = ALIVE_NAME


@bot_cmd(outgoing=True, pattern=r"^\.sysd$")
async def sysdetails(sysd):
    """For .sysd command, get system info using neofetch."""
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Install neofetch first !!`")


@bot_cmd(outgoing=True, pattern=r"^\.botver$")
async def bot_ver(event):
    """For .botver command, get the bot version."""
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if which("git") is not None:
            ver = await asyncrunapp(
                "git",
                "describe",
                "--all",
                "--long",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

            rev = await asyncrunapp(
                "git",
                "rev-list",
                "--all",
                "--count",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

            await event.edit("`Userbot Version: " f"{verout}" "` \n" "`Revision: " f"{revout}" "`")
        else:
            await event.edit("Shame that you don't have git, you're running - 'v1.beta.4' anyway!")


@bot_cmd(outgoing=True, pattern=r"^\.pip(?: |$)(.*)")
async def pipcheck(pip):
    """For .pip command, do a pip search."""
    if not pip.text[0].isalpha() and pip.text[0] not in ("/", "#", "@", "!"):
        pipmodule = pip.pattern_match.group(1)
        if pipmodule:
            await pip.edit("`Searching . . .`")
            pipc = await asyncrunapp(
                "pip3",
                "search",
                pipmodule,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await pipc.communicate()
            pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())

            if pipout:
                if len(pipout) > 4096:
                    await pip.edit("`Output too large, sending as file`")
                    file = open("output.txt", "w+")
                    file.write(pipout)
                    file.close()
                    await pip.client.send_file(
                        pip.chat_id,
                        "output.txt",
                        reply_to=pip.id,
                    )
                    remove("output.txt")
                    return
                await pip.edit("**Query: **\n`" f"pip3 search {pipmodule}" "`\n**Result: **\n`" f"{pipout}" "`")
            else:
                await pip.edit(
                    "**Query: **\n`" f"pip3 search {pipmodule}" "`\n**Result: **\n`No Result Returned/False`"
                )
        else:
            await pip.edit("`Use .help pip to see an example`")


@bot_cmd(outgoing=True, pattern=r"^\.(alive|on)$")
async def amireallyalive(event):
    """For .alive command, check if the bot is running."""
    logo = ALIVE_LOGO
    text = (
        f"`{BOT_NAME}`\n"
        f"[REPO](https://github.com/notudope/notubot)  /  [Channel](https://t.me/notudope)  /  [Grup](https://t.me/NOTUBOTS)  /  [Instagram]({IG_ALIVE})\n\n"
        f"😎 **Owner :** __{DEFAULTUSER}__\n"
        f"🤖 **Version :** `v{BOT_VER}`\n"
        f"🐍 **Python :** `v{python_version()}`\n"
        f"📦 **Telethon :** `v{version.__version__}\n`"
        f"⚙️ **Branch :** `{Repo().active_branch.name}`"
    )

    buttons = [
        [
            Button.url("REPO", "https://github.com/notudope/notubot"),
            Button.url("Channel", "https://t.me/notudope"),
            Button.url("Grup", "https://t.me/NOTUBOTS"),
        ],
    ]

    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await event.client.send_file(event.chat_id, logo, caption=text)
            await event.delete()
        except MediaEmptyError:
            await event.edit(
                text + "\n\n *`The provided logo is invalid." "\nMake sure the link is directed to the logo picture`",
            )
    else:
        await event.delete()
        await event.client.send_message(event.chat_id, text, link_preview=False, buttons=buttons)


@bot_cmd(outgoing=True, pattern="^.aliveu")
async def amireallyaliveuser(username):
    """For .aliveu command, change the username in the .alive command."""
    if not username.text[0].isalpha() and username.text[0] not in ("/", "#", "@", "!"):
        message = username.text
        output = ".aliveu [new user without brackets] nor can it be empty"
        if not (message == ".aliveu" or message[7:8] != " "):
            newuser = message[8:]
            global DEFAULTUSER
            DEFAULTUSER = newuser
            output = "Successfully changed user to " + newuser + "!"
        await username.edit("`" f"{output}" "`")


@bot_cmd(outgoing=True, pattern=r"^\.resetalive$")
async def amireallyalivereset(ureset):
    """For .resetalive command, reset the username in the .alive command."""
    if not ureset.text[0].isalpha() and ureset.text[0] not in ("/", "#", "@", "!"):
        global DEFAULTUSER
        DEFAULTUSER = ALIVE_NAME
        await ureset.edit("`" "Successfully reset user for alive!" "`")


CMD_HELP.update(
    {
        "system": [
            "System",
            " - `.sysd` : Show system information using neofetch.\n"
            " - `.botver` : Show NOTUBOT version.\n"
            " - `.pip <module(s)>` : Search module(s) in PyPI.\n"
            " - `.alive` : Check if NOTUBOT is running. \n"
            " - `.aliveu <new_user>` : Change the user name in .alive command (aesthetics change only)\n"
            " - `.resetalive` : Reset the user name in the .alive command to default (aesthetics change only)\n",
        ]
    }
)
