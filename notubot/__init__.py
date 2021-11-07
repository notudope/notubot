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
from time import sleep, time

from dotenv import dotenv_values, load_dotenv
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from requests import get
from telethon import TelegramClient, version
from telethon.errors.rpcerrorlist import ApiIdInvalidError, AuthKeyDuplicatedError, PhoneNumberInvalidError
from telethon.sessions import StringSession

start_time = time()
__botversion__ = "0.1"
__botname__ = "⚡NOTUBOT UserBot⚡"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S", level=logging.INFO
)
logging.getLogger("asyncio").setLevel(logging.ERROR)
logging.getLogger("telethon.network.mtprotosender").setLevel(logging.WARNING)
LOGS = logging.getLogger(__name__)

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

# Check if the config was edited by using the already used variable.
CONFIG_CHECK = strtobool(getenv("_____REMOVE_____THIS_____LINE_____", default="False"))

if CONFIG_CHECK:
    LOGS.error("Hapus baris dalam hashtag pertama dari file config.env")
    sys.exit(1)

# Telegram App KEY and HASH
API_ID = int(getenv("API_ID", default=0))
API_HASH = getenv("API_HASH", default=None)

# Userbot Session String
STRING_SESSION = getenv("STRING_SESSION", default=None)

# Logging channel/group ID configuration.
BOTLOG_CHATID = int(getenv("BOTLOG_CHATID", default=0))

# Userbot logging feature switch.
BOTLOG = strtobool(getenv("BOTLOG", default="True"))

# Command handler
HANDLER = getenv("HANDLER", default="-")

# Blacklist group
BLACKLIST_GROUP = list(map(int, getenv("BLACKLIST_GROUP", default="").split()))

# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = strtobool(getenv("PM_AUTO_BAN", default="False"))

# Default .alive logo
ALIVE_LOGO = getenv("ALIVE_LOGO", default=None)

# Default .alive Instagram
IG_ALIVE = getenv("IG_ALIVE", default="https://www.instagram.com/notudope")

# Heroku Credentials for updater.
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", default=None)
HEROKU_API_KEY = getenv("HEROKU_API_KEY", default=None)

# Custom (forked) repo URL for updater.
UPSTREAM_REPO_URL = getenv("UPSTREAM_REPO_URL", "https://github.com/notudope/notubot.git")
# UPSTREAM_REPO_URL branch, the default is main
UPSTREAM_REPO_BRANCH = getenv("UPSTREAM_REPO_BRANCH", "main")

# SQL Database URI
DB_URI = getenv("DATABASE_URL", default="")

# Chrome Driver and Headless Google Chrome Binaries
CHROME_DRIVER = getenv("CHROME_DRIVER", default="/usr/bin/chromedriver")
GOOGLE_CHROME_BIN = getenv("GOOGLE_CHROME_BIN", default="/usr/bin/google-chrome")

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

# Deezload Credentials
DEEZER_ARL_TOKEN = getenv("DEEZER_ARL_TOKEN", default="")
DEEZER_EMAIL = getenv("DEEZER_EMAIL", default="")
DEEZER_PASSWORD = getenv("DEEZER_PASSWORD", default="")

# Last.fm Plugin
BIO_PREFIX = getenv("BIO_PREFIX", default="")
DEFAULT_BIO = getenv("DEFAULT_BIO", default="")

LASTFM_API = getenv("LASTFM_API", default="")
LASTFM_SECRET = getenv("LASTFM_SECRET", default="")
LASTFM_USERNAME = getenv("LASTFM_USERNAME", default="")
LASTFM_PASSWORD_PLAIN = getenv("LASTFM_PASSWORD", default="")
LASTFM_PASS = md5(LASTFM_PASSWORD_PLAIN)

lastfm = None
if LASTFM_API and LASTFM_SECRET and LASTFM_USERNAME and LASTFM_PASS:
    try:
        lastfm = LastFMNetwork(
            api_key=LASTFM_API,
            api_secret=LASTFM_SECRET,
            username=LASTFM_USERNAME,
            password_hash=LASTFM_PASS,
        )
    except Exception:
        pass

# Google Drive Plugin
G_DRIVE_DATA = getenv("G_DRIVE_DATA", default="")
G_DRIVE_CLIENT_ID = getenv("G_DRIVE_CLIENT_ID", default="")
G_DRIVE_CLIENT_SECRET = getenv("G_DRIVE_CLIENT_SECRET", default="")
G_DRIVE_AUTH_TOKEN_DATA = getenv("G_DRIVE_AUTH_TOKEN_DATA", default="")
G_DRIVE_FOLDER_ID = getenv("G_DRIVE_FOLDER_ID", default="")
G_DRIVE_INDEX_URL = getenv("G_DRIVE_INDEX_URL", default="")
TEMP_DOWNLOAD_DIRECTORY = getenv("TMP_DOWNLOAD_DIRECTORY", default="./downloads/")

# Terminal Alias
TERM_ALIAS = getenv("TERM_ALIAS", default="notubot")

# Genius Lyrics API
GENIUS = getenv("GENIUS_ACCESS_TOKEN", default="")

# Uptobox
USR_TOKEN = getenv("USR_TOKEN_UPTOBOX", default="")


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


def migration_workaround() -> None:
    try:
        from notubot.plugins.sql_helper.globals import addgvar, delgvar, gvarstatus
    except AttributeError:
        return None

    old_ip = gvarstatus("public_ip")
    new_ip = get("https://api.ipify.org").text
    if old_ip is None:
        delgvar("public_ip")
        addgvar("public_ip", new_ip)
        return None
    if old_ip == new_ip:
        return None

    sleep_time = 180
    LOGS.info(f"A change in IP address is detected, waiting for {sleep_time / 60} minutes before starting the bot.")
    sleep(sleep_time)
    LOGS.info("Starting bot...")
    delgvar("public_ip")
    addgvar("public_ip", new_ip)
    return None


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
        LOGS.warning("STRING_SESSION Kedaluwarsa. Silakan buat STRING_SESSION baru. Berhenti...")
        sys.exit(1)
    except ApiIdInvalidError:
        LOGS.warning("Kombinasi API_ID dan API_HASH tidak valid. Silahkan cek ulang. Berhenti...")
        sys.exit(1)
    except Exception as e:
        LOGS.exception("ERROR - {}".format(e))
        sys.exit(1)

    return client


bot = client_connection()


async def check_botlog_chatid() -> None:
    if not BOTLOG_CHATID and BOTLOG:
        LOGS.warning(
            "Wajib mengatur variabel BOTLOG_CHATID di config.env atau environment variabel, supaya fitur logging berfungsi."
        )
        sys.exit(1)
    elif not BOTLOG:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.warning(
            "Akun tidak memiliki hak/akses untuk mengirim pesan ke grup/channel BOTLOG_CHATID. Periksa apakah ID sudah benar."
        )
        sys.exit(1)


with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGS.warning(
            "Environment variable BOTLOG_CHATID tidak valid. Periksa environment variable atau file config.env."
        )
        sys.exit(1)


async def check_alive() -> None:
    await bot.send_message(BOTLOG_CHATID, "```{} v{} Launched 🚀```".format(__botname__, __botversion__))


with bot:
    try:
        bot.loop.run_until_complete(check_alive())
    except BaseException:
        LOGS.warning(
            "Environment variable BOTLOG_CHATID tidak valid. Periksa environment variable atau config.env file."
        )
        sys.exit(1)


async def update_restart_msg(chat_id: int, msg_id: int) -> bool:
    message = (
        f"`{__botname__}`\n"
        f"[REPO](https://github.com/notudope/notubot)  /  [Channel](https://t.me/notudope)  /  [Support](https://t.me/NOTUBOTS)  /  [Mutualan](https://t.me/CariTeman_Asik)\n\n"
        f"**Version** - `v{__botversion__}`\n"
        f"**Python** - `{python_version()}`\n"
        f"**Telethon** - `{version.__version__}`"
    )
    await bot.edit_message(chat_id, msg_id, message, link_preview=False)
    return True


try:
    from notubot.plugins.sql_helper.globals import delgvar, gvarstatus

    chat_id, msg_id = gvarstatus("restartstatus").split("\n")
    try:
        with bot:
            bot.loop.run_until_complete(update_restart_msg(int(chat_id), int(msg_id)))
    except BaseException:
        pass
    delgvar("restartstatus")
except AttributeError:
    pass

# Global Variables
CMD_HELP = {}
CMD_LIST = {}
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
ISAFK = False
AFKREASON = None
