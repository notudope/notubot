import asyncio

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.gcast ?(.*)")
async def gcast(event):
    xx = event.pattern_match.group(1)
    if xx:
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await event.edit("`Berikan sebuah pesan atau balas pesan tersebut...`")

    wait = await event.edit("`Sedang mengirim Pesan Grup secara global... 📢`")
    er = 0
    done = 0

    async for x in bot.iter_dialogs():
        if x.is_group:
            # chat = x.id
            chat = x.entity.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
        await asyncio.sleep(0.5)

    await wait.edit(f"Berhasil mengirim Pesan Grup ke `{done}` obrolan, gagal mengirim ke `{er}` obrolan.")


@register(outgoing=True, pattern=r"^\.gucast ?(.*)")
async def gucast(event):
    xx = event.pattern_match.group(1)
    if xx:
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await event.edit("`Berikan sebuah pesan atau balas pesan tersebut...`")

    wait = await event.edit("`Sedang mengirim Pesan Pribadi secara global... 📢`")
    er = 0
    done = 0

    async for x in bot.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await bot.send_message(chat, msg)
            except BaseException:
                er += 1
        await asyncio.sleep(0.5)

    await wait.edit(f"Berhasil mengirim Pesan Pribadi ke `{done}` obrolan, gagal mengirim ke `{er}` obrolan.")


CMD_HELP.update(
    {
        "gcast": ">`.gcast`"
        "\nUsage: Mengirim Pesan Group secara global, "
        "Gak usah idiot, jangan berlebihan, resiko ditanggung pengguna!"
        "\n\n>`.gucast`"
        "\nUsage: Mengirim Pesan Pribadi secara global, "
        "Gak usah spam, seperlunya aja!"
    }
)
