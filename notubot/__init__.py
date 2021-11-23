# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio
import logging
import sys
from distutils.util import strtobool
from os import (
    environ,
    getenv,
    path,
    chmod,
    remove,
)
from pathlib import Path
from platform import python_version
from time import time

from dotenv import dotenv_values, load_dotenv
from heroku3 import from_key
from pySmartDL import SmartDL
from requests import get
from telethon import TelegramClient, version
from telethon.errors.rpcerrorlist import (
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
    PhoneNumberInvalidError,
    MessageIdInvalidError,
    MessageNotModifiedError,
    MessageDeleteForbiddenError,
    ChatWriteForbiddenError,
)
from telethon.sessions import StringSession
from telethon.tl.functions.channels import DeleteMessagesRequest, JoinChannelRequest  # noqa: F401
from telethon.utils import get_display_name

start_time = time()
__botversion__ = "0.1"
__botname__ = "ツNOTUBOT UserBot "

if path.exists("notubot.log"):
    remove("notubot.log")

logging.basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] : %(message)s",
    level=logging.INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[logging.FileHandler("notubot.log"), logging.StreamHandler()],
)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("Telethon").setLevel(logging.ERROR)
logging.getLogger("telethon.network.mtprotosender").setLevel(logging.ERROR)
LOGS = logging.getLogger("NOTUBOT")


if not sys.platform.startswith("linux"):
    LOGS.error("HARUS menggunakan Platform linux, saat ini {}".format(sys.platform))
    sys.exit(1)

if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    LOGS.error("HARUS menggunakan python versi minimal 3.8.")
    sys.exit(1)

dirs = ["logs", "bin"]
for dir in dirs:
    if not path.exists(dir):
        Path(dir).mkdir(parents=True, exist_ok=True)
    else:
        for file in Path(path.realpath(dir)).rglob("*.*"):
            if path.isfile(file):
                remove(file)

app_dir: Path = Path(__file__).parent.parent
dotenv_path = app_dir / "config.env"
load_dotenv(dotenv_path=dotenv_path)
config = {
    **dotenv_values("config.env"),
    **environ,
}

# Check if the config was edited by using the already used variable
CONFIG_CHECK = strtobool(getenv("_____REMOVE_____THIS_____LINE_____", default="False"))

if CONFIG_CHECK:
    LOGS.error("Hapus baris dalam hashtag pertama dari file config.env")
    sys.exit(1)

# Telegram API_ID and API_HASH
API_ID = int(getenv("API_ID", default=0))
API_HASH = getenv("API_HASH", default=None)

# Telegram Session String
STRING_SESSION = getenv("STRING_SESSION", default=None)

# notubot logging feature switch
BOTLOG = strtobool(getenv("BOTLOG", default="True"))

# Logging channel/group ID configuration
BOTLOG_CHATID = int(getenv("BOTLOG_CHATID", default=0))

# Command handler
HANDLER = getenv("HANDLER", default=".")

# Running developer command
I_DEV = strtobool(getenv("I_DEV", default="False"))

# Default .alive logo
ALIVE_LOGO = getenv("ALIVE_LOGO", default=None)

# Default .alive text
ALIVE_TEXT = getenv("ALIVE_TEXT", default="Hey, I am alive.")

# Default .alive Instagram
ALIVE_IG = getenv("ALIVE_IG", default="notudope")
ALIVE_IG = ALIVE_IG.replace("@", "") if ALIVE_IG.startswith("@") else ALIVE_IG

# Heroku Credentials for updater
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", default=None)
HEROKU_API_KEY = getenv("HEROKU_API_KEY", default=None)

# Custom (forked) repo URL for updater
UPSTREAM_REPO_URL = getenv("UPSTREAM_REPO_URL", "https://github.com/notudope/notubot.git")
# UPSTREAM_REPO_URL branch, the default is main
UPSTREAM_REPO_BRANCH = getenv("UPSTREAM_REPO_BRANCH", "main")

# SQL Database URI
DB_URI = getenv("DATABASE_URL", default="")

# Blacklist group manually
NOSPAM_GROUP = list(map(int, getenv("NOSPAM_GROUP", default="").split()))

# Auto BAN user if not approved
PM_AUTO_BAN = strtobool(getenv("PM_AUTO_BAN", default="False"))

# OpenWeatherMap API Key
OPEN_WEATHER_MAP_APPID = getenv("OPEN_WEATHER_MAP_APPID", default="")
WEATHER_DEFCITY = getenv("WEATHER_DEFCITY", default="")

# Anti Spambot Config
ANTI_SPAMBOT = strtobool(getenv("ANTI_SPAMBOT", default="False"))
ANTI_SPAMBOT_SHOUT = strtobool(getenv("ANTI_SPAMBOT_SHOUT", default="False"))

# Time & Date - Country and Time Zone
COUNTRY = getenv("COUNTRY", default="ID")
TZ_NUMBER = int(getenv("TZ_NUMBER", default=1))

# Clean Welcome
CLEAN_WELCOME = strtobool(getenv("CLEAN_WELCOME", default="True"))

# OCR API key
OCR_SPACE_API_KEY = getenv("OCR_SPACE_API_KEY", default="")

# remove.bg API key
REM_BG_API_KEY = getenv("REM_BG_API_KEY", default="")

# Chrome Driver and Headless Google Chrome Binaries
CHROME_DRIVER = getenv("CHROME_DRIVER", default="/usr/bin/chromedriver")
GOOGLE_CHROME_BIN = getenv("GOOGLE_CHROME_BIN", default="/usr/bin/google-chrome")

# Google Drive Plugin
G_DRIVE_DATA = getenv("G_DRIVE_DATA", default="")
G_DRIVE_CLIENT_ID = getenv("G_DRIVE_CLIENT_ID", default="")
G_DRIVE_CLIENT_SECRET = getenv("G_DRIVE_CLIENT_SECRET", default="")
G_DRIVE_AUTH_TOKEN_DATA = getenv("G_DRIVE_AUTH_TOKEN_DATA", default="")
G_DRIVE_FOLDER_ID = getenv("G_DRIVE_FOLDER_ID", default="")
G_DRIVE_INDEX_URL = getenv("G_DRIVE_INDEX_URL", default="")
TEMP_DOWNLOAD_DIRECTORY = getenv("TMP_DOWNLOAD_DIRECTORY", default="./downloads/")

# Genius Lyrics API
GENIUS = getenv("GENIUS_ACCESS_TOKEN", default="")

# Setting Up CloudMail.ru and MEGA.nz extractor binaries,
# and giving them correct perms to work properly.
binaries = {
    "https://raw.githubusercontent.com/adekmaulana/megadown/master/megadown": "bin/megadown",
    "https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py": "bin/cmrudl",
}
for file, bin in binaries.items():
    if not path.exists(bin):
        downloader = SmartDL(file, bin, progress_bar=False)
        downloader.start()
        chmod(bin, 0o755)

try:
    if HEROKU_API_KEY or HEROKU_APP_NAME:
        HEROKU_APP = from_key(HEROKU_API_KEY).apps()[HEROKU_APP_NAME]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None

LOOP = asyncio.get_event_loop()


def client_connection() -> TelegramClient:
    client = None
    try:
        if STRING_SESSION:
            client = TelegramClient(StringSession(STRING_SESSION), api_id=API_ID, api_hash=API_HASH, loop=LOOP)
        else:
            client = TelegramClient("notubot", api_id=API_ID, api_hash=API_HASH, loop=LOOP)

        client.parse_mode = "markdown"
    except (AuthKeyDuplicatedError, PhoneNumberInvalidError, EOFError):
        LOGS.warning("STRING_SESSION kedaluwarsa, silakan buat STRING_SESSION baru.")
        sys.exit(1)
    except ApiIdInvalidError:
        LOGS.warning("Kombinasi API_ID dan API_HASH tidak valid. Silahkan cek ulang.")
        sys.exit(1)
    except Exception as e:
        LOGS.exception("ERROR - {}".format(e))
        sys.exit(1)

    return client


bot = client_connection()


async def prepare_botlog() -> None:
    if not BOTLOG_CHATID and BOTLOG:
        LOGS.warning(
            "Jika nilai BOTLOG = True maka wajib mengatur variabel BOTLOG_CHATID di config.env atau environment variabel!"
        )
        sys.exit(1)

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.warning(
            "Akun tidak memiliki hak/akses untuk mengirim pesan ke grup/channel BOTLOG_CHATID. Periksa apakah ID sudah benar."
        )
        sys.exit(1)


with bot:
    try:
        bot.loop.run_until_complete(prepare_botlog())
    except Exception as e:
        LOGS.exception(f"[PREPARE_BOTLOG] - {e}")
        sys.exit(1)


async def launched() -> None:
    bot.me = await bot.get_me()
    bot.uid = bot.me.id
    bot.name = get_display_name(bot.me)

    await bot.send_message(
        BOTLOG_CHATID,
        "<code>{} v{} Launched 🚀 as {} [{}]</code>".format(__botname__, __botversion__, bot.name, bot.uid),
        parse_mode="html",
    )

    await bot(JoinChannelRequest("@NOTUBOTS"))
    await bot(JoinChannelRequest("@notudope"))


with bot:
    try:
        bot.loop.run_until_complete(launched())
    except ChatWriteForbiddenError:
        pass
    except Exception as e:
        LOGS.exception(f"[LAUNCHED] - {e}")
        sys.exit(1)


async def updated_message(chatid, mid) -> None:
    text = (
        f"`{__botname__}`\n"
        f"[Repo](https://github.com/notudope/notubot)  •  [Channel](https://t.me/notudope)  •  [Support](https://t.me/NOTUBOTS)  •  [Mutualan](https://t.me/CariTemanOK)\n\n"
        f"**Version:** `v{__botversion__}`\n"
        f"**Python:** `{python_version()}`\n"
        f"**Telethon:** `{version.__version__}`"
    )
    await bot.edit_message(chatid, mid, text, link_preview=False)
    # await bot(DeleteMessagesRequest(int(chatid), [int(mid)]))
    return True


try:
    from notubot.database.globals import delgv, getgv

    chatid, mid = getgv("restartstatus").split("\n")

    try:
        with bot:
            bot.loop.run_until_complete(updated_message(int(chatid), int(mid)))
    except (
        MessageIdInvalidError,
        MessageNotModifiedError,
        MessageDeleteForbiddenError,
        ChatWriteForbiddenError,
        ValueError,
    ):
        pass
    except Exception as e:
        LOGS.exception(f"[UPDATED_MESSAGE] - {e}")
        pass

    delgv("restartstatus")
except AttributeError:
    pass


# Global Variables
CMD_HELP = {}
CMD_LIST = {}
COUNT_MSG = 0
COUNT_PM = {}
LASTMSG = {}
ISAFK = False
AFKREASON = None
GROUP_CALLS = {}
