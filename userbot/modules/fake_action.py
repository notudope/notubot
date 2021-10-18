import asyncio

from userbot import CMD_HELP
from userbot.events import register


@register(
    outgoing=True,
    disable_errors=True,
    pattern="^.f(typing|audio|contact|document|game|location|photo|round|video)(?: |$)(.*)",
)
async def fakeaction(event):
    act = event.pattern_match.group(1)
    if act in ["audio", "round", "video"]:
        act = "record-" + act

    seconds = event.pattern_match.group(2)
    if not (seconds or seconds.isdigit()):
        seconds = 60
    else:
        try:
            seconds = int(seconds)
        except BaseException:
            try:
                seconds = await event.ban_time(seconds)
            except BaseException:
                return await event.edit("`Format salah.`")

    await event.edit(f'`Memulai "Fake Action" selama {seconds} detik.`')
    await asyncio.sleep(5)
    await event.delete()
    async with event.client.action(event.chat_id, act):
        await asyncio.sleep(seconds)


CMD_HELP.update(
    {
        "fakeaction": ">`.ftyping <detik>`"
        "\nUsage : Seakan akan sedang mengetik padahal tidak."
        "\n\n>`.faudio <detik>`"
        "\nUsage : Berfungsi sama seperti ftyping tapi ini fake audio."
        "\n\n>`.fgame <detik>`"
        "\nUsage : Berfungsi sama seperti ftyping tapi ini fake game."
        "\n\n>`.fvideo <detik>`"
        "\nUsage : Berfungsi sama seperti ftyping tapi ini fake video."
    }
)
