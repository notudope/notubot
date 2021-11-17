# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import sys
import traceback
from io import BytesIO, StringIO
from os import remove
from pprint import pprint
from random import choice

from carbonnow import Carbon

from notubot import CMD_HELP
from notubot import bot as client
from notubot.events import bot_cmd
from notubot.utils import run_cmd

all_col = [
    "Black",
    "Navy",
    "DarkBlue",
    "MediumBlue",
    "Blue",
    "DarkGreen",
    "Green",
    "Teal",
    "DarkCyan",
    "DeepSkyBlue",
    "DarkTurquoise",
    "MediumSpringGreen",
    "Lime",
    "SpringGreen",
    "Aqua",
    "Cyan",
    "MidnightBlue",
    "DodgerBlue",
    "LightSeaGreen",
    "ForestGreen",
    "SeaGreen",
    "DarkSlateGray",
    "DarkSlateGrey",
    "LimeGreen",
    "MediumSeaGreen",
    "Turquoise",
    "RoyalBlue",
    "SteelBlue",
    "DarkSlateBlue",
    "MediumTurquoise",
    "Indigo  ",
    "DarkOliveGreen",
    "CadetBlue",
    "CornflowerBlue",
    "RebeccaPurple",
    "MediumAquaMarine",
    "DimGray",
    "DimGrey",
    "SlateBlue",
    "OliveDrab",
    "SlateGray",
    "SlateGrey",
    "LightSlateGray",
    "LightSlateGrey",
    "MediumSlateBlue",
    "LawnGreen",
    "Chartreuse",
    "Aquamarine",
    "Maroon",
    "Purple",
    "Olive",
    "Gray",
    "Grey",
    "SkyBlue",
    "LightSkyBlue",
    "BlueViolet",
    "DarkRed",
    "DarkMagenta",
    "SaddleBrown",
    "DarkSeaGreen",
    "LightGreen",
    "MediumPurple",
    "DarkViolet",
    "PaleGreen",
    "DarkOrchid",
    "YellowGreen",
    "Sienna",
    "Brown",
    "DarkGray",
    "DarkGrey",
    "LightBlue",
    "GreenYellow",
    "PaleTurquoise",
    "LightSteelBlue",
    "PowderBlue",
    "FireBrick",
    "DarkGoldenRod",
    "MediumOrchid",
    "RosyBrown",
    "DarkKhaki",
    "Silver",
    "MediumVioletRed",
    "IndianRed ",
    "Peru",
    "Chocolate",
    "Tan",
    "LightGray",
    "LightGrey",
    "Thistle",
    "Orchid",
    "GoldenRod",
    "PaleVioletRed",
    "Crimson",
    "Gainsboro",
    "Plum",
    "BurlyWood",
    "LightCyan",
    "Lavender",
    "DarkSalmon",
    "Violet",
    "PaleGoldenRod",
    "LightCoral",
    "Khaki",
    "AliceBlue",
    "HoneyDew",
    "Azure",
    "SandyBrown",
    "Wheat",
    "Beige",
    "WhiteSmoke",
    "MintCream",
    "GhostWhite",
    "Salmon",
    "AntiqueWhite",
    "Linen",
    "LightGoldenRodYellow",
    "OldLace",
    "Red",
    "Fuchsia",
    "Magenta",
    "DeepPink",
    "OrangeRed",
    "Tomato",
    "HotPink",
    "Coral",
    "DarkOrange",
    "LightSalmon",
    "Orange",
    "LightPink",
    "Pink",
    "Gold",
    "PeachPuff",
    "NavajoWhite",
    "Moccasin",
    "Bisque",
    "MistyRose",
    "BlanchedAlmond",
    "PapayaWhip",
    "LavenderBlush",
    "SeaShell",
    "Cornsilk",
    "LemonChiffon",
    "FloralWhite",
    "Snow",
    "Yellow",
    "LightYellow",
    "Ivory",
    "White",
]


@bot_cmd(
    pattern="(rc|c)arbon",
)
async def _(event):
    NotUBot = await event.edit("`Processing...`")
    te = event.text
    col = choice(all_col) if te[1] == "r" else None

    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            b = await event.client.download_media(temp)
            with open(b) as a:
                code = a.read()
            remove(b)
        else:
            code = temp.message
    else:
        try:
            code = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            return await NotUBot.edit("`Balasan pesan readable file.`")

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    carbon = Carbon(base_url="https://carbonara.vercel.app/api/cook", code=code, background=col)
    notubot_carbon = await carbon.memorize("notubot_carbon")
    await NotUBot.delete()
    await event.reply(
        f"Carbonised by {mention}",
        file=notubot_carbon,
    )


@bot_cmd(
    pattern="ccarbon(?: |$)(.*)",
)
async def crbn(event):
    match = event.pattern_match.group(1)
    if not match:
        return await event.edit("`Berikan Custom Color untuk membuat Carbon...`")

    NotUBot = await event.edit("`Processing...`")
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            b = await event.client.download_media(temp)
            with open(b) as a:
                code = a.read()
            remove(b)
        else:
            code = temp.message
    else:
        try:
            match = match.split(" ", maxsplit=1)
            code = match[1]
            match = match[0]
        except IndexError:
            return await NotUBot.edit("`Balasan pesan readable file.`")

    carbon = Carbon(base_url="https://carbonara.vercel.app/api/cook", code=code, background=match)
    try:
        notubot_carbon = await carbon.memorize("notubot_carbon")
    except Exception as e:
        return await NotUBot.edit(str(e))

    mention = "[{}](tg://user?id={})".format(bot.name, bot.uid)
    await NotUBot.delete()
    await event.reply(
        f"Carbonised by {mention}",
        file=notubot_carbon,
    )


@bot_cmd(pattern="sysinfo$")
async def _(event):
    NotUBot = await event.edit("`Processing...`")
    x, y = await run_cmd("neofetch|sed 's/\x1B\\[[0-9;\\?]*[a-zA-Z]//g' >> neo.txt")

    with open("neo.txt", "r") as neo:
        p = (neo.read()).replace("\n\n", "")
    res = Carbon(base_url="https://carbonara.vercel.app/api/cook", code=p)

    notubot_neofetch = await res.memorize("notubot_neofetch")
    await event.reply(file=notubot_neofetch)
    await NotUBot.delete()
    remove("neo.txt")


@bot_cmd(pattern="bash", only_devs=True)
async def _(event):
    NotUBot = await event.edit("`Processing...`")
    try:
        cmd = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await NotUBot.edit("`Tidak ada perintah.`")

    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    stdout, stderr = await run_cmd(cmd)
    final_output = f"**☞ BASH\n\n• COMMAND:**\n`{cmd}` \n\n"
    if stderr:
        final_output += f"**• ERROR:** \n`{stderr}`\n\n"

    if stdout:
        _o = stdout.split("\n")
        o = "\n".join(_o)
        final_output += f"**• OUTPUT:**\n`{o}`"

    if not stderr and not stdout:
        final_output += "**• OUTPUT:**\n`Success`"

    if len(final_output) > 4096:
        xx = final_output.replace("`", "").replace("**", "").replace("__", "")
        try:
            with BytesIO(str.encode(xx)) as file:
                file.name = "bash.txt"
                await event.client.send_file(
                    event.chat_id,
                    file,
                    force_document=True,
                    allow_cache=False,
                    caption=f"`{cmd}`" if len(cmd) < 998 else None,
                    reply_to=reply_to_id,
                )
        except Exception:
            pass
        await NotUBot.delete()
    else:
        await NotUBot.edit(final_output)


p, pp = print, pprint
bot = client


@bot_cmd(pattern="eval", only_devs=True)
async def _(event):
    if len(event.text) > 5 and event.text[5] != " ":
        return

    NotUBot = await event.edit("`Processing...`")
    try:
        cmd = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await NotUBot.edit("`Masukan python code.`")

    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    reply_to_id = event.message.id

    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "__►__ **EVALPy**\n```{}``` \n\n __►__ **OUTPUT**: \n```{}``` \n".format(
        cmd,
        evaluation,
    )

    if len(final_output) > 4096:
        xx = final_output.replace("`", "").replace("**", "").replace("__", "")
        try:
            with BytesIO(str.encode(xx)) as file:
                file.name = "eval.txt"
                await event.client.send_file(
                    event.chat_id,
                    file,
                    force_document=True,
                    allow_cache=False,
                    caption=f"```{cmd}```" if len(cmd) < 998 else None,
                    reply_to=reply_to_id,
                )
        except Exception:
            pass
        await NotUBot.delete()
    else:
        await NotUBot.edit(final_output)


async def aexec(code, event):
    exec(
        (
            (
                ("async def __aexec(e, client): " + "\n message = event = e")
                + "\n reply = await event.get_reply_message()"
            )
            + "\n chat = (await event.get_chat()).id"
        )
        + "".join(f"\n {ln}" for ln in code.split("\n"))
    )

    return await locals()["__aexec"](event, event.client)


CMD_HELP.update(
    {
        "dev": [
            "Dev Tools",
            "`.carbon <text/reply to msg/reply to document>`\n"
            "↳ : Carbonise teks dengan pengaturan default.\n\n"
            "`.rcarbon <text/reply to msg/reply to document>`\n"
            "↳ : Carbonise teks, dengan acak warna background.\n\n"
            "`.ccarbon <color> <text/reply to msg/reply to document>`\n"
            "↳ : Carbonise teks, dengan kustom warna background.\n\n"
            "`.sysinfo`\n"
            "↳ : Menampilkan informasi sistem.\n\n"
            "`.bash <cmds>`\n"
            "↳ : Menjalankan perintah linux di Telegram.\n\n"
            "`.eval <code>`\n"
            "↳ : Eksekusi perintah python di Telegram, \n\n"
            """Pintasan:
        client = bot = event.client
        e = event
        p = print
        reply = await event.get_reply_message()
        chat = event.chat_id\n\n"""
            "`.yaml|yml`\n"
            "↳ : Mengambil raw data format yaml dari sebuah pesan",
        ]
    }
)
