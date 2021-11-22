# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from notubot import CMD_HELP, ALIVE_IG
from notubot.events import bot_cmd
from notubot.functions.wrappers import answer


@bot_cmd(func=lambda x: x.is_private or x.is_group)
async def matchings_words(e):
    text = ""
    xx = e.text.lower()
    if xx in ["ig", "instagram"]:
        text = f"𝐈𝐍𝐒𝐓𝐀𝐆𝐑𝐀𝐌 [@{ALIVE_IG}](https://www.instagram.com/{ALIVE_IG})"
    elif xx in ["p", "salam"]:
        text = "𝐇𝐄𝐘 𝐘𝐎𝐎 𝐀𝐒𝐒𝐀𝐋𝐀𝐌𝐔𝐀𝐋𝐀𝐈𝐊𝐔𝐌"
    elif xx in ["l", "waskum"]:
        text = "𝐖𝐀𝐒𝐀𝐏𝐏 𝐖𝐀𝐀𝐋𝐀𝐈𝐊𝐔𝐌𝐒𝐀𝐋𝐀𝐌"
    elif xx in ["kam", "welkam"]:
        text = "𝐖𝐄𝐋𝐊𝐀𝐀𝐌 𝐆𝐄𝐒𝐒𝐒𝐒"
    elif xx in ["bewan", "gelut"]:
        text = "𝐁𝐄𝐖𝐀𝐍 𝐊𝐈𝐓𝐀 𝐏𝐀𝐍𝐓𝐄𝐄𝐄𝐄"
    elif xx in ["gblk", "goblok"]:
        text = "𝐆𝐎𝐁𝐋𝐎𝐊𝐊𝐊𝐊𝐊𝐊𝐊𝐊"
    elif xx in ["bct", "bacot"]:
        text = "𝐁𝐀𝐂𝐎𝐓 𝐍𝐆𝐄𝐍𝐓𝐎𝐓𝐓𝐓𝐓𝐓𝐓𝐓𝐓"
    elif xx in ["ajg", "anj"]:
        text = "𝐀𝐍𝐉𝐈𝐍𝐆 𝐋𝐎𝐎𝐎𝐎𝐎𝐎𝐎𝐎"
    elif xx in ["bewan", "gelut"]:
        text = "𝐁𝐄𝐖𝐀𝐍 𝐊𝐈𝐓𝐀 𝐏𝐀𝐍𝐓𝐄𝐄𝐄𝐄"
    elif xx in ["kntl", "kontol"]:
        text = "𝐊𝐎𝐍𝐓𝐎𝐋𝐋𝐋𝐋𝐋𝐋𝐋𝐋"
    elif xx in ["mmk", "memek"]:
        text = "𝐌𝐄𝐌𝐄𝐊𝐊𝐊𝐊𝐊𝐊𝐊𝐊"
    elif xx in ["njs", "najis"]:
        text = "𝐍𝐀𝐉𝐈𝐒 𝐂𝐔𝐈𝐇𝐇𝐇𝐇"
    elif xx in ["sokap"]:
        text = "𝐆𝐀𝐔𝐒𝐀𝐇 𝐒𝐎𝐊𝐀𝐏 𝐀𝐍𝐉𝐈𝐍𝐆"
    elif xx in ["bgst", "bangsat"]:
        text = "𝐁𝐀𝐍𝐆𝐒𝐀𝐓𝐓𝐓𝐓𝐓𝐓𝐓𝐓"
    elif xx in ["aliansi", "aliangsi"]:
        text = "𝐀𝐋𝐈𝐀𝐍𝐆𝐒𝐈 𝐀𝐋𝐈𝐀𝐍𝐆𝐒𝐈 𝐀𝐋𝐀𝐘𝐘𝐘𝐘"
    elif xx in ["babu"]:
        text = "𝐍𝐘𝐀𝐃𝐀𝐑 𝐃𝐈𝐑𝐈 𝐋𝐎 𝐈𝐓𝐔 𝐂𝐔𝐌𝐀 𝐉𝐀𝐃𝐈 𝐁𝐀𝐁𝐔𝐔𝐔𝐔"
    elif xx in ["jlk", "pinterest"]:
        text = "𝐏𝐏 𝐏𝐈𝐍𝐓𝐄𝐑𝐄𝐒𝐓 𝐀𝐉𝐀 𝐁𝐄𝐋𝐀𝐆𝐔 𝐍𝐆𝐄𝐍𝐓𝐎𝐓 𝐆𝐔𝐀 𝐓𝐀𝐔 𝐌𝐔𝐊𝐀 𝐋𝐎 𝐉𝐄𝐋𝐄𝐊 𝐉𝐀𝐍𝐆𝐀𝐍 𝐁𝐀𝐍𝐘𝐀𝐊 𝐆𝐀𝐘𝐀 𝐀𝐍𝐉𝐈𝐍𝐆"
    elif xx in ["lonte", "perek"]:
        text = "𝐋𝐎𝐍𝐓𝐄 𝐌𝐔𝐑𝐀𝐇𝐀𝐍𝐍𝐍𝐍"
    elif xx in ["senggol"]:
        text = "𝐒𝐄𝐍𝐆𝐆𝐎𝐋 𝐃𝐎𝐍𝐆, 𝐌𝐔𝐊𝐀 𝐋𝐎 𝐊𝐄𝐊 𝐀𝐍𝐉𝐈𝐍𝐆𝐆𝐆𝐆"
    elif xx in ["gc ampas"]:
        text = "𝐆𝐂 𝐀𝐌𝐏𝐀𝐒 𝐁𝐔𝐁𝐀𝐑𝐈𝐍 𝐀𝐉𝐀 𝐒𝐀𝐌𝐏𝐀𝐇𝐇𝐇𝐇"
    elif xx in ["war"]:
        text = "𝐖𝐀𝐑 𝐖𝐀𝐑 𝐓𝐀𝐈 𝐀𝐍𝐉𝐈𝐍𝐆, 𝐊𝐄𝐓𝐑𝐈𝐆𝐆𝐄𝐑 𝐌𝐈𝐍𝐓𝐀 𝐒𝐇𝐀𝐑𝐄𝐋𝐎𝐊, 𝐔𝐃𝐀𝐇 𝐒𝐇𝐀𝐑𝐄𝐋𝐎𝐊 𝐆𝐀 𝐍𝐘𝐀𝐌𝐏𝐄𝐑𝐈𝐍 𝐒𝐀𝐌𝐏𝐀𝐇𝐇𝐇𝐇"
    elif xx in ["limit"]:
        text = "𝐋𝐈𝐌𝐈𝐓 𝐋𝐈𝐌𝐈𝐓 𝐓𝐀𝐈 𝐀𝐍𝐉𝐈𝐍𝐆 𝐊𝐄𝐁𝐀𝐍𝐘𝐀𝐊𝐀𝐍 𝐀𝐋𝐈𝐁𝐈 𝐋𝐎 𝐒𝐄𝐆𝐀𝐏𝐔𝐍𝐆"
    elif xx in ["pc"]:
        text = "𝐏𝐂 𝐏𝐂 𝐌𝐀𝐓𝐀𝐌𝐔, 𝐆𝐔𝐀 𝐓𝐀𝐔 𝐋𝐎 𝐋𝐀𝐆𝐈 𝐒𝐀𝐍𝐆𝐄 𝐌𝐀𝐊𝐀𝐍𝐍𝐘𝐀 𝐌𝐈𝐍𝐓𝐀 𝐏𝐂 𝐊𝐀𝐍 𝐀𝐍𝐀𝐊 𝐀𝐍𝐉𝐈𝐍𝐆"

    if text != "":
        return await answer(e, text)


CMD_HELP.update(
    {
        "mutualan": [
            "Mutualan",
            "`ig|instagram`\n"
            "`p|salam`\n"
            "`l|waskum`\n"
            "`kam|welkam`\n"
            "`bewan|gelut`\n"
            "`gblk|goblok`\n"
            "`bct|bacot`\n"
            "`ajg|anj`\n"
            "`kntl|kontol`\n"
            "`mmk|memek`\n"
            "`njs|najis`\n"
            "`sokap`\n"
            "`bgst|bangsat`\n"
            "`aliansi|aliangsi`\n"
            "`babu`\n"
            "`jlk|pinterest`\n"
            "`lonte|perek`\n"
            "`seggol`\n"
            "`gc ampas`\n"
            "`war`\n"
            "`limit`\n"
            "`pc`\n",
        ]
    }
)
