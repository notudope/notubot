# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from notubot import CMD_HELP, ALIVE_IG
from notubot.events import bot_cmd


@bot_cmd(pattern="ig|([iI][gG]|[iI]nstagram)$")
async def _(e):
    text = f"𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 [@{ALIVE_IG}](https://www.instagram.com/{ALIVE_IG})"
    await e.delete()
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)


@bot_cmd(pattern="p|([pP])$")
async def _(e):
    text = "`𝐇𝐄𝐘 𝐘𝐎𝐎 𝐀𝐒𝐒𝐀𝐋𝐀𝐌𝐔𝐀𝐋𝐀𝐈𝐊𝐔𝐌`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="l|([lL])$")
async def _(e):
    text = "`𝐖𝐀𝐒𝐀𝐏𝐏 𝐖𝐀𝐀𝐋𝐀𝐈𝐊𝐔𝐌𝐒𝐀𝐋𝐀𝐌`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="gk|([gG]blk)$")
async def _(e):
    text = "`𝐆𝐎𝐁𝐋𝐎𝐊𝐊𝐊𝐊`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="bc|([bB]ct)$")
async def _(e):
    text = "`𝐁𝐀𝐂𝐎𝐓 𝐍𝐆𝐄𝐍𝐓𝐎𝐓𝐓𝐓𝐓`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="an|([aA]jg|[aA]nj)$")
async def _(e):
    text = "`𝐀𝐍𝐉𝐈𝐍𝐆 𝐋𝐎𝐎𝐎𝐎`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="kn|([kK]ntl)$")
async def _(e):
    text = "`𝐊𝐎𝐍𝐓𝐎𝐋𝐋𝐋𝐋`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="mk|([mM]mk)$")
async def _(e):
    text = "`𝐌𝐄𝐌𝐄𝐊𝐊𝐊𝐊`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="nj|([nN]ajis)$")
async def _(e):
    text = "`𝐍𝐀𝐉𝐈𝐒 𝐂𝐔𝐈𝐇𝐇𝐇𝐇`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="sk|([sS]okap)$")
async def _(e):
    text = "`𝐆𝐀𝐔𝐒𝐀𝐇 𝐒𝐎𝐊𝐀𝐏 𝐀𝐍𝐉𝐈𝐍𝐆`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="bg|([bB]gst)$")
async def _(e):
    text = "`𝐁𝐀𝐍𝐆𝐒𝐀𝐓𝐓𝐓𝐓`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="al|([aA]liansi)$")
async def _(e):
    text = "`𝐀𝐋𝐈𝐀𝐍𝐆𝐒𝐈 𝐀𝐋𝐈𝐀𝐍𝐆𝐒𝐈 𝐀𝐋𝐀𝐘𝐘𝐘𝐘`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="ba|([bB]abu)$")
async def _(e):
    text = "`𝐍𝐘𝐀𝐃𝐀𝐑 𝐃𝐈𝐑𝐈 𝐋𝐎 𝐈𝐓𝐔 𝐂𝐔𝐌𝐀 𝐉𝐀𝐃𝐈 𝐁𝐀𝐁𝐔𝐔𝐔𝐔`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="jl|([jJ]lk)$")
async def _(e):
    text = "`𝐌𝐔𝐊𝐀 𝐏𝐈𝐍𝐓𝐄𝐑𝐄𝐒𝐓 𝐁𝐀𝐍𝐘𝐀𝐊 𝐆𝐀𝐘𝐀 𝐓𝐎𝐋𝐎𝐋𝐋𝐋𝐋`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="ln|([lL]onte|[pP]erek)$")
async def _(e):
    text = "`𝐋𝐎𝐍𝐓𝐄 𝐌𝐔𝐑𝐀𝐇𝐀𝐍𝐍𝐍𝐍`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="sl|([sS]enggol)$")
async def _(e):
    text = "`𝐒𝐄𝐍𝐆𝐆𝐎𝐋 𝐃𝐎𝐍𝐆, 𝐌𝐔𝐊𝐀 𝐋𝐎 𝐊𝐄𝐊 𝐀𝐍𝐉𝐈𝐍𝐆𝐆𝐆𝐆`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="gas|([gG][cC] ampas)$")
async def _(e):
    text = "`𝐆𝐂 𝐀𝐌𝐏𝐀𝐒 𝐁𝐔𝐁𝐀𝐑𝐈𝐍 𝐀𝐉𝐀 𝐒𝐀𝐌𝐏𝐀𝐇𝐇𝐇𝐇`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


@bot_cmd(pattern="wr|([wW]ar|WAR)$")
async def _(e):
    text = "`𝐖𝐀𝐑 𝐖𝐀𝐑 𝐓𝐀𝐈 𝐀𝐍𝐉𝐈𝐍𝐆, 𝐊𝐄𝐓𝐑𝐈𝐆𝐆𝐄𝐑 𝐌𝐈𝐍𝐓𝐀 𝐒𝐇𝐀𝐑𝐄𝐋𝐎𝐊, 𝐔𝐃𝐀𝐇 𝐒𝐇𝐀𝐑𝐄𝐋𝐎𝐊 𝐆𝐀 𝐍𝐘𝐀𝐌𝐏𝐄𝐑𝐈𝐍 𝐒𝐀𝐌𝐏𝐀𝐇𝐇𝐇𝐇`"
    await e.client.send_message(e.chat_id, text, reply_to=e.reply_to_msg_id if e.reply_to_msg_id else False)
    await e.delete()


CMD_HELP.update(
    {
        "mutualan": [
            "Mutualan",
            "`.ig|[iI][gG]|[iI]nstagram`\n"
            "↳ : Menampilkan akun Instagram.\n\n"
            "`.p|[pP]`\n"
            "↳ : Mengucapkan salam.\n\n"
            "`.l|[lL]`\n"
            "↳ : Menjawab salam.\n\n",
        ]
    }
)
