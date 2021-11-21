# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from notubot import CMD_HELP, ALIVE_IG
from notubot.events import bot_cmd


@bot_cmd(pattern="ig|([iI][gG]|[iI]nstagram)$")
async def ig(event):
    text = f"𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 [@{ALIVE_IG}](https://www.instagram.com/{ALIVE_IG})"
    await event.edit(text)
    """
    await event.client.send_message(
        event.chat_id, text, reply_to=event.reply_to_msg_id if event.reply_to_msg_id else False
    )
    await event.delete()
    """


@bot_cmd(pattern="p|([pP]|[sS]alam)$")
async def pp(event):
    text = "𝐇𝐄𝐘 𝐘𝐎𝐎 𝐀𝐒𝐒𝐀𝐋𝐀𝐌𝐔𝐀𝐋𝐀𝐈𝐊𝐔𝐌"
    await event.edit(text)


@bot_cmd(pattern="l|([lL]|[wW]askum)$")
async def was(event):
    text = "𝐖𝐀𝐒𝐀𝐏𝐏 𝐖𝐀𝐀𝐋𝐀𝐈𝐊𝐔𝐌𝐒𝐀𝐋𝐀𝐌"
    await event.edit(text)


@bot_cmd(pattern="wl|([kK]am)$")
async def wl(event):
    text = "𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐆𝐄𝐒𝐒𝐒𝐒"
    await event.edit(text)


@bot_cmd(pattern="be|([bB]wan)$")
async def be(event):
    text = "𝐁𝐄𝐖𝐀𝐍 𝐊𝐈𝐓𝐀 𝐏𝐀𝐍𝐓𝐄𝐄𝐄𝐄"
    await event.edit(text)


@bot_cmd(pattern="gk|([gG]blk|[bB]lok)$")
async def gk(event):
    text = "𝐆𝐎𝐁𝐋𝐎𝐊𝐊𝐊𝐊"
    await event.edit(text)


@bot_cmd(pattern="bc|([bB]ct)$")
async def bc(event):
    text = "𝐁𝐀𝐂𝐎𝐓 𝐍𝐆𝐄𝐍𝐓𝐎𝐓𝐓𝐓𝐓"
    await event.edit(text)


@bot_cmd(pattern="an|([aA]jg|[aA]nj|[aA]su)$")
async def an(event):
    text = "𝐀𝐍𝐉𝐈𝐍𝐆 𝐋𝐎𝐎𝐎𝐎"
    await event.edit(text)


@bot_cmd(pattern="kn|([kK]ntl)$")
async def kn(event):
    text = "𝐊𝐎𝐍𝐓𝐎𝐋𝐋𝐋𝐋"
    await event.edit(text)


@bot_cmd(pattern="mk|([mM]mk)$")
async def mk(event):
    text = "𝐌𝐄𝐌𝐄𝐊𝐊𝐊𝐊"
    await event.edit(text)


@bot_cmd(pattern="nj|([nN]ajis)$")
async def nj(event):
    text = "𝐍𝐀𝐉𝐈𝐒 𝐂𝐔𝐈𝐇𝐇𝐇𝐇"
    await event.edit(text)


@bot_cmd(pattern="sk|([sS]okap)$")
async def sk(event):
    text = "𝐆𝐀𝐔𝐒𝐀𝐇 𝐒𝐎𝐊𝐀𝐏 𝐀𝐍𝐉𝐈𝐍𝐆"
    await event.edit(text)


@bot_cmd(pattern="bg|([bB]gst)$")
async def bg(event):
    text = "𝐁𝐀𝐍𝐆𝐒𝐀𝐓𝐓𝐓𝐓"
    await event.edit(text)


@bot_cmd(pattern="al|([aA]liansi)$")
async def al(event):
    text = "𝐀𝐋𝐈𝐀𝐍𝐆𝐒𝐈 𝐀𝐋𝐈𝐀𝐍𝐆𝐒𝐈 𝐀𝐋𝐀𝐘𝐘𝐘𝐘"
    await event.edit(text)


@bot_cmd(pattern="ba|([bB]abu)$")
async def ba(event):
    text = "𝐍𝐘𝐀𝐃𝐀𝐑 𝐃𝐈𝐑𝐈 𝐋𝐎 𝐈𝐓𝐔 𝐂𝐔𝐌𝐀 𝐉𝐀𝐃𝐈 𝐁𝐀𝐁𝐔𝐔𝐔𝐔"
    await event.edit(text)


@bot_cmd(pattern="jl|([jJ]lk)$")
async def jl(event):
    text = "𝐏𝐏 𝐏𝐈𝐍𝐓𝐄𝐑𝐄𝐒𝐓 𝐀𝐉𝐀 𝐁𝐄𝐋𝐀𝐆𝐔 𝐍𝐆𝐄𝐍𝐓𝐎𝐓 𝐆𝐔𝐀 𝐓𝐀𝐔 𝐌𝐔𝐊𝐀 𝐋𝐎 𝐉𝐄𝐋𝐄𝐊 𝐉𝐀𝐍𝐆𝐀𝐍 𝐁𝐀𝐍𝐘𝐀𝐊 𝐆𝐀𝐘𝐀 𝐀𝐍𝐉𝐈𝐍𝐆"
    await event.edit(text)


@bot_cmd(pattern="ln|([lL]onte|[pP]erek)$")
async def ln(event):
    text = "𝐋𝐎𝐍𝐓𝐄 𝐌𝐔𝐑𝐀𝐇𝐀𝐍𝐍𝐍𝐍"
    await event.edit(text)


@bot_cmd(pattern="sl|([sS]enggol)$")
async def sl(event):
    text = "𝐒𝐄𝐍𝐆𝐆𝐎𝐋 𝐃𝐎𝐍𝐆, 𝐌𝐔𝐊𝐀 𝐋𝐎 𝐊𝐄𝐊 𝐀𝐍𝐉𝐈𝐍𝐆𝐆𝐆𝐆"
    await event.edit(text)


@bot_cmd(pattern="gas|([gG][cC] ampas)$")
async def gas(event):
    text = "𝐆𝐂 𝐀𝐌𝐏𝐀𝐒 𝐁𝐔𝐁𝐀𝐑𝐈𝐍 𝐀𝐉𝐀 𝐒𝐀𝐌𝐏𝐀𝐇𝐇𝐇𝐇"
    await event.edit(text)


@bot_cmd(pattern="wr|([wW]ar|WAR)$")
async def wr(event):
    text = "𝐖𝐀𝐑 𝐖𝐀𝐑 𝐓𝐀𝐈 𝐀𝐍𝐉𝐈𝐍𝐆, 𝐊𝐄𝐓𝐑𝐈𝐆𝐆𝐄𝐑 𝐌𝐈𝐍𝐓𝐀 𝐒𝐇𝐀𝐑𝐄𝐋𝐎𝐊, 𝐔𝐃𝐀𝐇 𝐒𝐇𝐀𝐑𝐄𝐋𝐎𝐊 𝐆𝐀 𝐍𝐘𝐀𝐌𝐏𝐄𝐑𝐈𝐍 𝐒𝐀𝐌𝐏𝐀𝐇𝐇𝐇𝐇"
    await event.edit(text)


@bot_cmd(pattern="lm|([lL]imit)$")
async def lm(event):
    text = "𝐋𝐈𝐌𝐈𝐓 𝐋𝐈𝐌𝐈𝐓 𝐓𝐀𝐈 𝐀𝐍𝐉𝐈𝐍𝐆 𝐊𝐄𝐁𝐀𝐍𝐘𝐀𝐊𝐀𝐍 𝐀𝐋𝐈𝐁𝐈 𝐋𝐎 𝐒𝐄𝐆𝐀𝐏𝐔𝐍𝐆"
    await event.edit(text)


@bot_cmd(pattern="pc|([Pp][cC])$")
async def pc(event):
    text = "𝐏𝐂 𝐏𝐂 𝐌𝐀𝐓𝐀𝐌𝐔, 𝐆𝐔𝐀 𝐓𝐀𝐔 𝐋𝐎 𝐋𝐀𝐆𝐈 𝐒𝐀𝐍𝐆𝐄 𝐌𝐀𝐊𝐀𝐍𝐍𝐘𝐀 𝐌𝐈𝐍𝐓𝐀 𝐏𝐂 𝐊𝐀𝐍 𝐀𝐍𝐀𝐊 𝐀𝐍𝐉𝐈𝐍𝐆"
    await event.edit(text)


CMD_HELP.update(
    {
        "mutualan": [
            "Mutualan",
            "`.ig|[iI][gG]|[iI]nstagram`\n"
            "↳ : Menampilkan akun Instagram.\n\n"
            "`.p|[pP]|[sS]alam`\n"
            "`.l|[lL]|[wW]askum`\n"
            "`.wl|[kK]am`\n"
            "`.be|[bB]wan`\n"
            "`.gk|[gG]blk|[bB]lok`\n"
            "`.bc|[bB]ct`\n"
            "`.an|[aA]jg|[aA]nj|[aA]su`\n"
            "`.kn|[kK]ntl`\n"
            "`.mk|[mM]mk`\n"
            "`.nj|[nN]ajis`\n"
            "`.sk|[sS]okap`\n"
            "`.bg|[bB]gst`\n"
            "`.al|[aA]liansi`\n"
            "`.ba|[bB]abu`\n"
            "`.jl|[jJ]lk`\n"
            "`.ln|[lL]onte|[pP]erek`\n"
            "`.sl|[sS]enggol`\n"
            "`.gas|[gG][cC] ampas`\n"
            "`.wr|[wW]ar|WAR`\n"
            "`.lm|[lL]imit`\n"
            "`.pc|[Pp][cC]`\n",
        ]
    }
)
