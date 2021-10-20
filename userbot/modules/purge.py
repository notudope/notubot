import asyncio

from telethon.tl.functions.channels import DeleteUserHistoryRequest

from userbot import CMD_HELP, LOGS
from userbot.events import register


@register(outgoing=True, disable_errors=True, pattern=r"^(\.del|del|Del)$")
async def delete(event):
    """For .del command, delete the replied message."""
    reply = await event.get_reply_message()
    if reply:
        try:
            await reply.delete()
            await event.delete()
        except BaseException:
            await event.delete()
    else:
        await event.delete()


@register(outgoing=True, disable_errors=True, pattern=r"^\.purge(?: |$)(.*)")
async def purge(event):
    """For .purge command, purge all messages starting from the reply."""
    match = event.pattern_match.group(1)
    try:
        text = event.text[6]
    except IndexError:
        text = None

    if text and event.text[6] in ["m", "a"]:
        return

    if not event._client._bot and ((match) or (event.is_reply and event.is_private)):
        count = 0
        async for msg in event.client.iter_messages(
            event.chat_id,
            limit=int(match) if match else None,
            min_id=event.reply_to_msg_id if event.is_reply else None,
        ):
            await msg.delete()
            count += 1
        procs = await event.client.send_message(
            event.chat_id,
            f"`Purged {count} pesan.`",
        )
        await asyncio.sleep(1)
        await procs.delete()
        return

    if not event.reply_to_msg_id:
        await event.edit("`Balas pesan untuk menghapus dari?`")
        return

    try:
        await event.client.delete_messages(
            event.chat_id, [x for x in range(event.reply_to_msg_id, event.id + 1)]  # noqa: C416
        )
    except Exception as e:
        LOGS.info(e)

    procs = await event.client.send_message(event.chat_id, "`Purged complete!`")
    await asyncio.sleep(1)
    await procs.delete()


@register(outgoing=True, disable_errors=True, pattern=r"^\.purgeme(?: |$)(.*)")
async def purgeme(event):
    """For .purgeme, purge Only your messages from the replied message."""
    opts = event.pattern_match.group(1)
    if opts and not event.is_reply:
        try:
            num = int(opts)
        except BaseException:
            await event.edit("`Input tidak valid.`")
            return

        done = 0
        async for m in event.client.iter_messages(event.chat_id, limit=num, from_user="me"):
            await m.delete()
            done += 1

        procs = await event.client.send_message(
            event.chat_id,
            f"`Purged {done} pesan.`",
        )
        await asyncio.sleep(1)
        await event.delete()
        await procs.delete()
        return

    chat = await event.get_input_chat()
    msgs = []
    count = 0
    if not (event.reply_to_msg_id or opts):
        await event.edit("Membalas pesan untuk purge atau gunakan seperti `purgeme <num>`")
        return

    async for m in event.client.iter_messages(
        chat,
        from_user="me",
        min_id=event.reply_to_msg_id,
    ):
        msgs.append(m)
        count += 1
        msgs.append(event.reply_to_msg_id)
        if len(msgs) == 100:
            await event.client.delete_messages(chat, msgs)
            msgs = []

    if msgs:
        await event.client.delete_messages(chat, msgs)

    procs = await event.client.send_message(
        event.chat_id,
        f"`Purged {str(count)} pesan.`",
    )
    await asyncio.sleep(1)
    await procs.delete()


@register(outgoing=True, disable_errors=True, groups_only=True, pattern=r"^\.purgeall$")
async def purgeall(event):
    """For .purgeall, delete all messages of replied user."""
    if not event.is_reply:
        await event.edit("`Balas pesan seseorang untuk menghapusnya.`")
        return

    name = (await event.get_reply_message()).sender
    try:
        await event.client(DeleteUserHistoryRequest(event.chat_id, name.id))
        await event.edit(
            f"`Berhasil menghapus semua pesan dari {name.first_name}.`",
        )
    except BaseException:
        await event.delete()


@register(outgoing=True, disable_errors=True, pattern=r"^\.copy$")
async def copy(event):
    """For .copy command, copy replied message."""
    reply = await event.get_reply_message()
    if reply:
        try:
            await reply.reply(reply)
            await event.delete()
        except BaseException:
            await event.delete()
    else:
        await event.delete()


@register(outgoing=True, disable_errors=True, pattern=r"^\.edit")
async def edit(event):
    """For .edit command, edit your last message."""
    message = event.text
    chat = await event.get_input_chat()
    self_id = await event.client.get_peer_id("me")
    string = str(message[6:])
    index = 1

    async for message in event.client.iter_messages(chat, self_id):
        if index == 2:
            await message.edit(string)
            await event.delete()
            break
        index = index + 1


@register(outgoing=True, disable_errors=True, pattern=r"^\.sd")
async def selfd(event):
    """For .sd command, make seflf-destructable messages."""
    message = event.text
    counter = int(message[4:6])
    text = str(event.text[6:])
    await event.delete()

    procs = await event.client.send_message(event.chat_id, text)
    await asyncio.sleep(counter)
    await procs.delete()


CMD_HELP.update(
    {
        "purge": ">`.del`"
        "\nUsage: Menghapus pesan yang dibalas."
        "\n\n>`.purge`"
        "\nUsage: Menghapus semua pesan dari balasan."
        "\n\n>`.purgeme <x>`"
        "\nUsage: Menghapus <x> pesan dari yang terbaru."
        "\n\n>`.purgeall`"
        "\nUsage: Menghapus semua pesan pengguna yang dibalas."
        "\n\n>`.copy`"
        "\nUsage: Copy pesan yang dibalas."
        "\n\n>`.edit <newmessage>`"
        "\nUsage: Mengubah pesan terbaru dengan <newmessage>."
        "\n\n>`.sd <x> <message>`"
        "\nUsage: Membuat pesan menjadi selfdestructs dalam <x> detik."
        "\nUsahakan tetap dibawah 100 detik, untuk mengatasi UserBot tertidur."
    }
)
