import asyncio

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, disable_errors=True, pattern="^.ftyping(?: |$)(.*)")
async def ftyping(event):
    seconds = event.pattern_match.group(1)
    if not (seconds or seconds.isdigit()):
        seconds = 100
    else:
        try:
            seconds = int(seconds)
        except BaseException:
            try:
                seconds = await event.ban_time(seconds)
            except BaseException:
                return await event.edit("`Format salah.`")

    await event.edit(f'`Memulai "Fake Typing" selama {seconds} detik.`')
    await asyncio.sleep(10)
    await event.delete()
    async with event.client.action(event.chat_id, "typing"):
        await asyncio.sleep(seconds)


@register(outgoing=True, disable_errors=True, pattern="^.faudio(?: |$)(.*)")
async def faudio(event):
    seconds = event.pattern_match.group(1)
    if not (seconds or seconds.isdigit()):
        seconds = 100
    else:
        try:
            seconds = int(seconds)
        except BaseException:
            try:
                seconds = await event.ban_time(seconds)
            except BaseException:
                return await event.edit("`Format salah.`")

    await event.edit(f'`Memulai "Fake Audio Recording" selama {seconds} detik.`')
    await asyncio.sleep(10)
    await event.delete()
    async with event.client.action(event.chat_id, "record-audio"):
        await asyncio.sleep(seconds)


@register(outgoing=True, disable_errors=True, pattern="^.fvideo(?: |$)(.*)")
async def fvideo(event):
    seconds = event.pattern_match.group(1)
    if not (seconds or seconds.isdigit()):
        seconds = 100
    else:
        try:
            seconds = int(seconds)
        except BaseException:
            try:
                seconds = await event.ban_time(seconds)
            except BaseException:
                return await event.edit("`Format salah.`")

    await event.edit(f'`Memulai "Fake Video Recording" selama {seconds} detik.`')
    await asyncio.sleep(10)
    await event.delete()
    async with event.client.action(event.chat_id, "record-video"):
        await asyncio.sleep(seconds)


@register(outgoing=True, disable_errors=True, pattern="^.fgame(?: |$)(.*)")
async def fgame(event):
    seconds = event.pattern_match.group(1)
    if not (seconds or seconds.isdigit()):
        seconds = 100
    else:
        try:
            seconds = int(seconds)
        except BaseException:
            try:
                seconds = await event.ban_time(seconds)
            except BaseException:
                return await event.edit("`Format salah.`")

    await event.edit(f'`Memulai "Fake Game Playing" selama {seconds} detik.`')
    await asyncio.sleep(10)
    await event.delete()
    async with event.client.action(event.chat_id, "game"):
        await asyncio.sleep(seconds)


CMD_HELP.update(
    {
        "fakeaction": ">`.ftyping` <jumlah teks>\
   \nUsage : Seakan akan sedang mengetik padahal tidak.\
   \n\n>`.faudio` <jumlah teks>\
   \nUsage : Berfungsi sama seperti ftyping tapi ini fake audio.\
   \n\n>`.fgame` <jumlah teks>\
   \nUsage : Berfungsi sama seperti ftyping tapi ini fake game.\
   \n\n>`.fvideo` <jumlah teks>\
   \nUsage : Berfungsi sama seperti ftyping tapi ini fake video."
    }
)
