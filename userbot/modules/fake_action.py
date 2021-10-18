import asyncio

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, disable_errors=True, pattern="^.ftyping(?: |$)(.*)")
async def ftyping(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Format tidak benar`")

    await event.edit(f'`Memulai "Fake Typing" selama {t} detik.`')
    async with event.client.action(event.chat_id, "typing"):
        await asyncio.sleep(t)


@register(outgoing=True, disable_errors=True, pattern="^.faudio(?: |$)(.*)")
async def faudio(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Format tidak benar`")

    await event.edit(f'`Memulai "Fake Audio Recording" selama {t} detik.`')
    async with event.client.action(event.chat_id, "record-audio"):
        await asyncio.sleep(t)


@register(outgoing=True, disable_errors=True, pattern="^.fvideo(?: |$)(.*)")
async def fvideo(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Format tidak benar`")

    await event.edit(f'`Memulai "Fake Video Recording" selama {t} detik.`')
    async with event.client.action(event.chat_id, "record-video"):
        await asyncio.sleep(t)


@register(outgoing=True, disable_errors=True, pattern="^.fgame(?: |$)(.*)")
async def fgame(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("`Format tidak benar`")

    await event.edit(f'`Memulai "Fake Game Playing" selama {t} detik.`')
    async with event.client.action(event.chat_id, "game"):
        await asyncio.sleep(t)


CMD_HELP.update(
    {
        "fakeaction": ">`.ftyping` <jumlah teks>\
   \nUsage : Seakan akan sedang mengetik padahal tidak\
   \n\n>`.faudio` <jumlah teks>\
   \nUsage : Berfungsi sama seperti ftyping tapi ini dalam bentuk fake audio\
   \n\n>`.fgame` <jumlah teks>\
   \nUsage : Berfungsi sama seperti ftyping tapi ini dalam bentuk fake game\
   \n\n>`.fvideo` <jumlah teks>\
   \nUsage : Berfungsi sama seperti ftyping tapi ini dalam bentuk fake video"
    }
)
