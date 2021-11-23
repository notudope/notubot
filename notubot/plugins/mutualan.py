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
        text = f"INSTAGRAM [@{ALIVE_IG}](https://www.instagram.com/{ALIVE_IG})"
    elif xx in ["p", "salam"]:
        text = "ASSALAMUALAIKUM"
    elif xx in ["l", "waskum"]:
        text = "WAALAIKUMSALAM"
    elif xx in ["kam", "welkam"]:
        text = "WELKAAM GESSSS"
    elif xx in ["bewan", "gelut"]:
        text = "BEWAN KITA PANTEEEE"
    elif xx in ["gblk", "goblok"]:
        text = "GOBLOKKKKKKKKKKK"
    elif xx in ["bct", "bacot"]:
        text = "BACOT NGENTOTTTTTTTTT"
    elif xx in ["ajg", "anj"]:
        text = "ANJING LOOOOOOOO"
    elif xx in ["kntl", "kontol"]:
        text = "KONTOLLLLLLLLLLL"
    elif xx in ["mmk", "memek"]:
        text = "MEMEKKKKKKKKKKKK"
    elif xx in ["njs", "najis"]:
        text = "NAJIS CUIHHHHHHHH"
    elif xx in ["sokap"]:
        text = "GAUSAH SOKAP ANJING"
    elif xx in ["caper"]:
        text = "[CAPER CAPER MULU BEGO, MUKA LO AJA KEK BIJI PLER DAKIAN GITU](tg://settings)"
    elif xx in ["bgst", "bangsat"]:
        text = "BANGSATTTTTTTTTTT"
    elif xx in ["aliansi", "aliangsi"]:
        text = "ALIANGSI ALIANGSI ALAYYYY"
    elif xx in ["babu"]:
        text = "NYADAR DIRI LO ITU CUMA JADI BABU"
    elif xx in ["jlk", "pinterest"]:
        text = "[PP PINTEREST AJA BELAGU NGENTOT, GUA TAU MUKA LO JELEK JANGAN BANYAK GAYA ANJING](tg://settings)"
    elif xx in ["lonte", "perek"]:
        text = "LONTE MURAHANNNNNNNN"
    elif xx in ["senggol"]:
        text = "[SENGGOL DONG, MUKA LO KEK ANJING](tg://settings)"
    elif xx in ["gc ampas"]:
        text = "GC AMPAS BUBARIN AJA SAMPAHHHHHHHH"
    elif xx in ["war"]:
        text = "WAR WAR TAI ANJING, KETRIGGER MINTA SHERLOK, UDAH SHERLOCK GA NYAMPERIN SAMPAHHHHHHHH"
    elif xx in ["limit"]:
        text = "LIMIT LIMIT TAI ANJING KEBANYAKAN ALIBI LO SEGAPUNG"
    elif xx in ["pc"]:
        text = "PC PC MATAMU, GUA TAU LO LAGI SANGE MAKANNYA MINTA PC KAN ANAK ANJING"

    if text != "":
        return await answer(e, "**{}**".format(text))


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
            "`caper`\n"
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
