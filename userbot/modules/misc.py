import io
import sys
from os import environ, execle
from random import randint
from time import sleep

from userbot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    bot,
)
from userbot.events import register
from userbot.utils import time_formatter
from userbot.utils.format import parse_pre


@register(outgoing=True, pattern=r"^\.random")
async def randomise(items):
    """For .random command, get a random item from the list of items."""
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        return await items.edit("`2 or more items are required! Check .help random for more info.`")
    index = randint(1, len(itemo) - 1)
    await items.edit("**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" + itemo[index] + "`")


@register(outgoing=True, pattern=r"^\.sleep ([0-9]+)$")
async def sleepybot(time):
    """For .sleep command, let the userbot snooze for a few second."""
    counter = int(time.pattern_match.group(1))
    await time.edit("`I am sulking and snoozing...`")
    if BOTLOG:
        str_counter = time_formatter(counter)
        await time.client.send_message(
            BOTLOG_CHATID,
            f"You put the bot to sleep for {str_counter}.",
        )
    sleep(counter)
    await time.edit("`OK, I'm awake now.`")


@register(outgoing=True, pattern=r"^\.shutdown$")
async def killthebot(event):
    """For .shutdown command, shut the bot down."""
    await event.edit("`Shutting down...`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n" "Bot shut down")
    await bot.disconnect()


@register(outgoing=True, pattern=r"^\.restart$")
async def killdabot(event):
    await event.edit("`*i would be back in a moment*`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n" "Restarting bot...")

    try:
        from userbot.modules.sql_helper.globals import addgvar, delgvar

        delgvar("restartstatus")
        addgvar("restartstatus", f"{event.chat_id}\n{event.id}")
    except AttributeError:
        pass

    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)


@register(outgoing=True, pattern=r"^\.readme$")
async def reedme(e):
    await e.edit(
        "Here's something for you to read:\n"
        "\n[notubot's README.md file](https://github.com/notudope/notubot/blob/main/README.md)"
        "\n[Setup Guide - Basic](https://telegra.ph/How-to-host-a-Telegram-Userbot-11-02)"
        "\n[Setup Guide - Google Drive](https://telegra.ph/How-To-Setup-Google-Drive-04-03)"
        "\n[Setup Guide - LastFM Module](https://telegra.ph/How-to-set-up-LastFM-module-for-Paperplane-userbot-11-02)"
        "\n[Setup Guide - How to get Deezer ARL TOKEN](https://notabug.org/RemixDevs/DeezloaderRemix/wiki/Login+via+userToken)"
        "\n[Special - Note](https://telegra.ph/Special-Note-11-02)"
    )


@register(outgoing=True, pattern=r"^\.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(" ", 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for _ in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern=r"^\.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit("`Check the userbot log for the decoded message data !!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Here's the decoded message data !!`",
        )


@register(outgoing=True, pattern=r"^\.json$")
async def json(event):
    "To get details of that message in json format."
    reply = await event.get_reply_message() if event.reply_to_msg_id else event

    await event.edit(reply.stringify(), parse_mode=parse_pre)


CMD_HELP.update(
    {
        "random": ">`.random <item1> <item2> ... <itemN>`" "\nUsage: Get a random item from the list of items.",
        "sleep": ">`.sleep <seconds>`" "\nUsage: Let yours snooze for a few seconds.",
        "shutdown": ">`.shutdown`" "\nUsage: Shutdown bot",
        "readme": ">`.readme`" "\nUsage: Provide links to setup the userbot and it's modules.",
        "repeat": ">`.repeat <no> <text>`"
        "\nUsage: Repeats the text for a number of times. Don't confuse this with spam tho.",
        "restart": ">`.restart`" "\nUsage: Restarts the bot !!",
        "raw": ">`.raw`" "\nUsage: Get detailed JSON-like formatted data about replied message.",
        "json": ">`.json`"
        "\nUsage: Mengambil data json dari sebuah pesan, "
        "Balas pesan tersebut untuk menampilkannya!",
    }
)
