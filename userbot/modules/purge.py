import asyncio

from telethon.errors import rpcbaseerrors

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
        return await event.edit("`I need a mesasge to start purging from.`")

    if msgs:
        await event.client.delete_messages(chat, msgs)
    done = await event.client.send_message(event.chat_id, "`Fast purge complete!`" f"\nPurged {str(count)} messages")

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
        "`Purge complete!` Purged " + str(count) + " messages.",
    )

    await asyncio.sleep(2)
    i = 1
    await smsg.delete()


@register(outgoing=True, disable_errors=True, pattern=r"^\.del$")
async def delit(event):
    """For .del command, delete the replied message."""
    msg_src = await event.get_reply_message()
    if event.reply_to_msg_id:
        try:
            await msg_src.delete()
            await event.delete()
        except rpcbaseerrors.BadRequestError:
            await event.edit("Well, I can't delete a message")


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
        "purge": ">`.purge`" "\nUsage: Purges all messages starting from the reply.",
        "purgeme": ">`.purgeme <x>`" "\nUsage: Deletes x amount of your latest messages.",
        "del": ">`.del`" "\nUsage: Deletes the message you replied to.",
        "edit": ">`.edit <newmessage>`" "\nUsage: Replace your last message with <newmessage>.",
        "sd": ">`.sd <x> <message>`"
        "\nUsage: Creates a message that selfdestructs in x seconds."
        "\nKeep the seconds under 100 since it puts your bot to sleep.",
    }
)
