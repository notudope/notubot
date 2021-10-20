import asyncio

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.purge$")
async def fastpurger(event):
    """For .purge command, purge all messages starting from the reply."""
    chat = await event.get_input_chat()
    msgs = []
    itermsg = event.client.iter_messages(chat, min_id=event.reply_to_msg_id)
    count = 0

    if event.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count = count + 1
            msgs.append(event.reply_to_msg_id)
            if len(msgs) == 100:
                await event.client.delete_messages(chat, msgs)
                msgs = []
    else:
        return await event.edit("`Balas pesan itu untuk memulai menghapus!`")

    if msgs:
        await event.client.delete_messages(chat, msgs)
    done = await event.client.send_message(event.chat_id, f"`Purged {str(count)} pesan.`")

    await asyncio.sleep(2)
    await done.delete()


@register(outgoing=True, pattern=r"^\.purgeme")
async def purgeme(event):
    """For .purgeme, delete x count of your latest message."""
    message = event.text
    count = int(message[9:])
    i = 1

    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        if i > count + 1:
            break
        i = i + 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
        f"`Purged {str(count)} pesan.`",
    )

    await asyncio.sleep(1)
    i = 1
    await smsg.delete()


@register(outgoing=True, disable_errors=True, pattern=r"^(\.del|del)$")
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


@register(outgoing=True, pattern=r"^\.edit")
async def editer(event):
    """For .edit command, edit your last message."""
    message = event.text
    chat = await event.get_input_chat()
    self_id = await event.client.get_peer_id("me")
    string = str(message[6:])
    i = 1

    async for message in event.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await event.delete()
            break
        i = i + 1


@register(outgoing=True, pattern=r"^\.sd")
async def selfdestruct(event):
    """For .sd command, make seflf-destructable messages."""
    message = event.text
    counter = int(message[4:6])
    text = str(event.text[6:])
    await event.delete()

    smsg = await event.client.send_message(event.chat_id, text)
    await asyncio.sleep(counter)
    await smsg.delete()


CMD_HELP.update(
    {
        "purge": ">`.del`"
        "\nUsage: Menghapus pesan yang dibalas."
        "\n\n>`.purge`"
        "\nUsage: Menghapus semua pesan dari balasan."
        "\n\n>`.purgeme <x>`"
        "\nUsage: Menghapus <x> pesan dari yang terbaru."
        "\n\n>`.copy`"
        "\nUsage: Copy pesan yang dibalas."
        "\n\n>`.edit <newmessage>`"
        "\nUsage: Mengubah pesan terbaru dengan <newmessage>."
        "\n\n>`.sd <x> <message>`"
        "\nUsage: Membuat pesan menjadi selfdestructs dalam <x> detik."
        "\nUsahakan tetap dibawah 100 detik, untuk mengatasi bot tertidur."
    }
)
