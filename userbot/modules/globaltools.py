import asyncio

from telethon.events import ChatAction
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_display_name

from userbot import (
    CMD_HELP,
    bot,
    BOTLOG_CHATID,
    BOTLOG,
)
from userbot.events import register


async def get_full_user(event):
    args = event.pattern_match.group(1).split(":", 1)
    extra = None

    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Wajib menyertakan ID user!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj

        try:
            user_obj = await event.client.get_entity(user)
        except Exception as e:
            raise e

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as e:
        await event.edit(str(e))
        return None

    return user_obj


@bot.on(ChatAction)
async def handler(event):
    if not event.user_joined or not event.user_added:
        return

    try:
        from userbot.modules.sql_helper.gmute_sql import is_gmuted

        guser = await event.get_user()
        gmuted = is_gmuted(guser.id)
    except BaseException:
        return

    if not gmuted:
        return

    for user in gmuted:
        if user.sender == str(guser.id):
            chat = await event.get_chat()
            admin = chat.admin_rights
            creator = chat.creator

            if admin or creator:
                try:
                    await event.client.edit_permissions(event.chat_id, guser.id, view_messages=False)
                    await event.reply(
                        f"""**User Gban Bergabung Ke Grup!**
**Grup :** `{event.chat.title}`
**User :** [{guser.id}](tg://user?id={guser.id})
**Aksi :** `Banned`"""
                    )
                except BaseException:
                    return


@register(outgoing=True, pattern="^.gban(?: |$)(.*)")
async def gban(event):
    sender = await event.get_sender()
    me = await event.client.get_me()

    if not sender.id == me.id:
        procs = await event.edit("`...`")
    else:
        procs = await event.edit("`Global Banned user ini!`")
    await procs.edit("`Gbanning...`")

    mention = "[{}](tg://user?id={})".format(get_display_name(me), me.id)
    success = failed = 0

    if event.is_private:
        user = event.chat
        reason = event.pattern_match.group(1)

    try:
        user, reason = await get_full_user(event)
    except BaseException:
        pass

    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await procs.edit("`Wajib menyertakan ID user!`")

    if user:
        if user.id in [2006788653, 2003361410]:
            await procs.edit("`Tidak dapat melakukan Global Banned karena dia pembuatku!`")
            return

        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except BaseException:
            pass

        try:
            await event.client(BlockRequest(user))
        except BaseException:
            pass

        async for x in event.client.iter_dialogs():
            if x.is_group or x.is_channel:
                try:
                    # x.entity.id
                    await event.client.edit_permissions(x.id, user, view_messages=False)
                    success += 1
                except BaseException:
                    failed += 1

    try:
        if gmute(user.id) is False:
            return await procs.edit("`User sudah terkena Global Banned.`")
    except BaseException:
        pass

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "**#Gbanned** [user.id](tg://user?id={}) {}".format(user.id, reason)
        )

    text = f"""**#Gbanned** oleh {mention}
**User :** [{user.first_name}](tg://user?id={user.id})
**Aksi :** `Global Banned`
**Grup/Channel :** Berhasil `{success}` Gagal `{failed}`"""
    if reason:
        text += f"\n**Reason :** `{reason}`"
    return await procs.edit(text)


@register(outgoing=True, pattern="^.ungban(?: |$)(.*)")
async def ungban(event):
    sender = await event.get_sender()
    me = await event.client.get_me()

    if not sender.id == me.id:
        procs = await event.edit("`...`")
    else:
        procs = await event.edit("`Membatalkan Global Banned user ini!`")
    await procs.edit(f"`UnGbanning...`")

    mention = "[{}](tg://user?id={})".format(get_display_name(me), me.id)
    success = failed = 0

    if event.is_private:
        user = event.chat
        reason = event.pattern_match.group(1)

    try:
        user, reason = await get_full_user(event)
    except BaseException:
        pass

    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await procs.edit("`Wajib menyertakan ID user!`")

    if user:
        if user.id in [2006788653, 2003361410]:
            await procs.edit("`Tidak dapat membatalkan Global Banned karena dia pembuatku!`")
            return

        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except BaseException:
            pass

        try:
            await event.client(UnblockRequest(user))
        except BaseException:
            pass

        async for x in event.client.iter_dialogs():
            if x.is_group or x.is_channel:
                try:
                    # x.entity.id
                    await event.client.edit_permissions(x.id, user, send_messages=True)
                    success += 1
                except BaseException:
                    failed += 1

    try:
        if ungmute(user.id) is False:
            return await procs.edit("`User tidak terkena Global Banned.`")
    except BaseException:
        pass

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "**#UnGbanned** [user.id](tg://user?id={}) {}".format(user.id, reason)
        )

    text = f"""**#UnGbanned** oleh {mention}
**User :** [{user.first_name}](tg://user?id={user.id})
**Aksi :** `Membatalkan Global Banned`
**Grup/Channel :** Berhasil `{success}` Gagal `{failed}`"""
    return await procs.edit(text)


@register(outgoing=True, pattern=r"^\.gcast ?(.*)")
async def gcast(event):
    xx = event.pattern_match.group(1)
    if xx:
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await event.edit("`Berikan sebuah pesan atau balas pesan tersebut...`")

    procs = await event.edit("`Sedang mengirim Pesan Grup secara global... 📢`")
    success = failed = 0

    async for x in event.client.iter_dialogs():
        if x.is_group:
            # chat = x.id
            chat = x.entity.id
            # if not is_gblacklisted(chat) and not int("-100" + str(chat)) in NOSPAM_CHAT:
            try:
                success += 1
                await event.client.send_message(chat, msg)
            except BaseException:
                failed += 1

        await asyncio.sleep(0.3)

    await procs.edit(f"Berhasil mengirim Pesan Grup ke `{success}` obrolan, gagal mengirim ke `{failed}` obrolan.")


@register(outgoing=True, pattern=r"^\.gucast ?(.*)")
async def gucast(event):
    xx = event.pattern_match.group(1)
    if xx:
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await event.edit("`Berikan sebuah pesan atau balas pesan tersebut...`")

    procs = await event.edit("`Sedang mengirim Pesan Pribadi secara global... 📢`")
    success = failed = 0

    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                success += 1
                await event.client.send_message(chat, msg)
            except BaseException:
                failed += 1

        await asyncio.sleep(0.3)

    await procs.edit(f"Berhasil mengirim Pesan Pribadi ke `{success}` obrolan, gagal mengirim ke `{failed}` obrolan.")


CMD_HELP.update(
    {
        "globaltools": ">`.gban`"
        "\nUsage: Global Banned ke semua grup yang menjadi admin, "
        "Gunakan perintah ini dengan bijak!"
        "\n\n>`.ungban`"
        "\nUsage: Membatalkan global Banned."
        "\n\n>`.gcast`"
        "\nUsage: Mengirim Pesan Group secara global, "
        "Gak usah idiot, jangan berlebihan, resiko (limit, kena kick/banned/fban) ditanggung pengguna!"
        "\n\n>`.gucast`"
        "\nUsage: Mengirim Pesan Pribadi secara global, "
        "Gak usah spam, seperlunya aja!"
    }
)
