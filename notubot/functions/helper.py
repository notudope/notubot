# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio
import hashlib
import math
import os
import re
import sys
import time
from datetime import datetime

from html_telegraph_poster import TelegraphPoster

from notubot import HEROKU_APP, LOGS

from .FastTelethon import download_file as downloadable
from .FastTelethon import upload_file as uploadable


async def uploader(file, name, taime, event, msg):
    with open(file, "rb") as f:
        result = await uploadable(
            client=event.client,
            file=f,
            filename=name,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    event,
                    taime,
                    msg,
                ),
            ),
        )
    return result


async def downloader(filename, file, event, taime, msg):
    with open(filename, "wb") as fk:
        result = await downloadable(
            client=event.client,
            location=file,
            out=fk,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d,
                    t,
                    event,
                    taime,
                    msg,
                ),
            ),
        )
    return result


def utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


async def md5(fname: str) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def humanbytes(size: int) -> str:
    if size is None or isinstance(size, str):
        return ""

    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def human_to_bytes(size: str) -> int:
    units = {
        "M": 2 ** 20,
        "MB": 2 ** 20,
        "G": 2 ** 30,
        "GB": 2 ** 30,
        "T": 2 ** 40,
        "TB": 2 ** 40,
    }

    size = size.upper()
    if not re.match(r" ", size):
        size = re.sub(r"([KMGT])", r" \1", size)
    number, unit = (string.strip() for string in size.split())
    return int(float(number) * units[unit])


def time_formatter(milliseconds):
    minutes, seconds = divmod(int(milliseconds / 1000), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    tmp = (
        ((str(weeks) + "w:") if weeks else "")
        + ((str(days) + "d:") if days else "")
        + ((str(hours) + "h:") if hours else "")
        + ((str(minutes) + "m:") if minutes else "")
        + ((str(seconds) + "s") if seconds else "")
    )
    if tmp != "":
        if tmp.endswith(":"):
            return tmp[:-1]
        else:
            return tmp
    else:
        return "0 s"


async def progress(current, total, event, start, type_of_ps, file_name=None):
    diff = time.time() - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = round((total - current) / speed) * 1000
        progress_str = "`[{0}{1}] {2}%`\n\n".format(
            "".join("●" for i in range(math.floor(percentage / 5))),
            "".join("" for i in range(20 - math.floor(percentage / 5))),
            round(percentage, 2),
        )

        tmp = progress_str + "`{0} of {1}`\n\n`✦ Speed: {2}/s`\n\n`✦ ETA: {3}`\n\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            time_formatter(time_to_completion),
        )
        if file_name:
            await event.edit("`✦ {}`\n\n`File Name: {}`\n\n{}".format(type_of_ps, file_name, tmp))
        else:
            await event.edit("`✦ {}`\n\n{}".format(type_of_ps, tmp))


def post_to_telegraph(title, author, text):
    client = TelegraphPoster(use_api=True)
    client.create_api_token(title)
    page = client.post(
        title=title,
        author=author,
        author_url="https://t.me/notudope",
        text=text,
    )
    return page["url"]


def mediainfo(media):
    xx = str((str(media)).split("(", maxsplit=1)[0])
    m = ""
    if xx == "MessageMediaDocument":
        mim = media.document.mime_type
        if mim == "application/x-tgsticker":
            m = "sticker animated"
        elif "image" in mim:
            if mim == "image/webp":
                m = "sticker"
            elif mim == "image/gif":
                m = "gif as doc"
            else:
                m = "pic as doc"
        elif "video" in mim:
            if "DocumentAttributeAnimated" in str(media):
                m = "gif"
            elif "DocumentAttributeVideo" in str(media):
                i = str(media.document.attributes[0])
                if "supports_streaming=True" in i:
                    m = "video"
                m = "video as doc"
            else:
                m = "video"
        elif "audio" in mim:
            m = "audio"
        else:
            m = "document"
    elif xx == "MessageMediaPhoto":
        m = "pic"
    elif xx == "MessageMediaWebPage":
        m = "web"
    return m


async def run_cmd(cmd: str) -> (bytes, bytes):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


async def restart(event):
    if HEROKU_APP:
        try:
            await event.edit("`Restarting... Tunggu beberapa menit!`")
            HEROKU_APP.restart()
        except BaseException as e:
            LOGS.info(e)
            return await event.edit(
                "`HEROKU_API_KEY` atau `HEROKU_APP_NAME` salah! Cek ulang variabel config.",
            )
    else:
        os.execl(sys.executable, sys.executable, "-m", "notubot")


async def shutdown(event, dynotype="notubot"):
    if HEROKU_APP:
        try:
            await event.edit("`Shutting down app... Tunggu beberapa menit!`")
            HEROKU_APP.process_formation()[dynotype].scale(0)
        except BaseException as e:
            LOGS.info(e)
            return await event.edit(
                "`HEROKU_API_KEY` atau `HEROKU_APP_NAME` salah! Cek ulang variabel config.",
            )
    else:
        sys.exit(1)


async def heroku_logs(event):
    NotUBot = await event.edit("`Processing...`")
    if not HEROKU_APP:
        return await NotUBot.edit("Atur `HEROKU_API_KEY` dan `HEROKU_APP_NAME` pada variabel config!")

    await NotUBot.edit("`Downloading Logs...`")
    ok = HEROKU_APP.get_log()

    with open("notubot-heroku.log", "w") as log:
        log.write(ok)

    await event.client.send_file(
        event.chat_id,
        file="notubot-heroku.log",
        caption="**NOTUBOT Heroku Logs.**",
    )

    os.remove("notubot-heroku.log")
    await NotUBot.delete()


async def def_logs(event):
    await event.client.send_file(
        event.chat_id,
        file="notubot.log",
        caption="**NOTUBOT Logs.**",
    )
