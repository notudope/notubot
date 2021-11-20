# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from notubot import CMD_HELP, ALIVE_IG
from notubot.events import bot_cmd


@bot_cmd(pattern="ig|([iI][gG]|[iI]nstagram)$")
async def _(event):
    await event.edit(f"ɪɴsᴛᴀɢʀᴀᴍ: [@{ALIVE_IG}](https://www.instagram.com/{ALIVE_IG})")


@bot_cmd(pattern="p|([pP])$")
async def _(event):
    await event.edit("`👏 ʜᴇʏ ʏᴏ, ᴀssᴀʟᴀᴍᴜᴀʟᴀɪᴋᴜᴍ...`")


@bot_cmd(pattern="l|([lL])$")
async def _(event):
    await event.edit("`👏 ᴡʜᴀᴛ's ᴜᴘ, ᴡᴀᴀʟᴀɪᴋᴜᴍsᴀʟᴀᴍ...`")


@bot_cmd(pattern="gk|(gblk|Gblk)$")
async def _(event):
    await event.edit("`𝐆𝐎𝐁𝐋𝐎𝐊𝐊𝐊𝐊 !!!`")


@bot_cmd(pattern="bc|(bct|Bct)$")
async def _(event):
    await event.edit("`𝐁𝐀𝐂𝐎𝐓 𝐍𝐆𝐄𝐍𝐓𝐎𝐓𝐓𝐓𝐓 !!!`")


@bot_cmd(pattern="an|(ajg|Ajg|anj|Anj)$")
async def _(event):
    await event.edit("`𝐀𝐍𝐉𝐈𝐍𝐆 𝐋𝐎𝐎𝐎𝐎 !!!`")


@bot_cmd(pattern="kn|(kntl|Kntl)$")
async def _(event):
    await event.edit("`𝐊𝐎𝐍𝐓𝐎𝐋𝐋𝐋𝐋 !!!`")


@bot_cmd(pattern="mk|(mmk|Mmk)$")
async def _(event):
    await event.edit("`𝐌𝐄𝐌𝐄𝐊𝐊𝐊𝐊 !!!`")


@bot_cmd(pattern="nj|(najis|Najis)$")
async def _(event):
    await event.edit("`𝐍𝐀𝐉𝐈𝐒 𝐂𝐔𝐈𝐇𝐇𝐇𝐇 !!!`")


@bot_cmd(pattern="sk|(sokap|Sokap)$")
async def _(event):
    await event.edit("`𝐆𝐀𝐔𝐒𝐀𝐇 𝐒𝐎𝐊𝐀𝐏 𝐀𝐍𝐉𝐈𝐍𝐆 !!!`")


@bot_cmd(pattern="bg|(bgst|Bgst)$")
async def _(event):
    await event.edit("`𝐁𝐀𝐍𝐆𝐒𝐀𝐓𝐓𝐓𝐓 !!!`")


@bot_cmd(pattern="al|(aliansi|Aliansi)$")
async def _(event):
    await event.edit("`𝐀𝐋𝐈𝐀𝐍𝐆𝐒𝐈 𝐀𝐋𝐈𝐀𝐍𝐆𝐒𝐈 𝐀𝐋𝐀𝐘𝐘𝐘𝐘 !!!`")


@bot_cmd(pattern="ba|(babu|Babu)$")
async def _(event):
    await event.edit("`𝐍𝐘𝐀𝐃𝐀𝐑 𝐃𝐈𝐑𝐈 𝐋𝐎 𝐈𝐓𝐔 𝐂𝐔𝐌𝐀 𝐉𝐀𝐃𝐈 𝐁𝐀𝐁𝐔𝐔𝐔𝐔 !!!`")


@bot_cmd(pattern="jl|(jlk|Jlk)$")
async def _(event):
    await event.edit("`𝐌𝐔𝐊𝐀 𝐏𝐈𝐍𝐓𝐄𝐑𝐄𝐒𝐓 𝐁𝐀𝐍𝐘𝐀𝐊 𝐆𝐀𝐘𝐀 𝐓𝐎𝐋𝐎𝐋𝐋𝐋𝐋 !!!`")


@bot_cmd(pattern="ln|(lonte|Lonte|perek|Perek)$")
async def _(event):
    await event.edit("`𝐋𝐎𝐍𝐓𝐄 𝐌𝐔𝐑𝐀𝐇𝐀𝐍𝐍𝐍𝐍 !!!`")


@bot_cmd(pattern="sl|(senggol|Senggol)$")
async def _(event):
    await event.edit("`𝐒𝐄𝐍𝐆𝐆𝐎𝐋 𝐃𝐎𝐍𝐆, 𝐌𝐔𝐊𝐀 𝐋𝐎 𝐊𝐄𝐊 𝐀𝐍𝐉𝐈𝐍𝐆𝐆𝐆𝐆 !!!`")


@bot_cmd(pattern="gas|(gc ampas|GC ampas)$")
async def _(event):
    await event.edit("`𝐆𝐂 𝐀𝐌𝐏𝐀𝐒 𝐁𝐔𝐁𝐀𝐑𝐈𝐍 𝐀𝐉𝐀 𝐒𝐀𝐌𝐏𝐀𝐇𝐇𝐇𝐇 !!!`")


@bot_cmd(pattern="wr|(war|War|WAR)$")
async def _(event):
    await event.edit("`𝐖𝐀𝐑 𝐖𝐀𝐑 𝐓𝐀𝐈 𝐀𝐍𝐉𝐈𝐍𝐆, 𝐊𝐄𝐓𝐑𝐈𝐆𝐆𝐄𝐑 𝐌𝐈𝐍𝐓𝐀 𝐒𝐇𝐀𝐑𝐄𝐋𝐎𝐊, 𝐔𝐃𝐀𝐇 𝐒𝐇𝐀𝐑𝐄𝐋𝐎𝐊 𝐆𝐀 𝐍𝐘𝐀𝐌𝐏𝐄𝐑𝐈𝐍 𝐒𝐀𝐌𝐏𝐀𝐇𝐇𝐇𝐇 !!!`")


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
