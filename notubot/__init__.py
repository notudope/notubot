# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import logging
import signal
import sys
from datetime import datetime
from os import (
    environ,
    getenv,
    path,
    chmod,
    remove,
)
from pathlib import Path
from platform import python_version, uname
from time import sleep

from dotenv import dotenv_values, load_dotenv
from loguru import logger as LOGS
from pylast import LastFMNetwork, md5
from pySmartDL import SmartDL
from requests import get
from telethon import TelegramClient, version
from telethon.sessions import StringSession

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

# Logging at the start to catch everything
fmtLog = "<bold><cyan>[{name}]</cyan></bold><level>[{level}]</level><bold><green>[{time:YY-MM-DD/HH:mm:ss}]</green> <cyan>{function}</cyan>:<cyan>{line}</cyan></bold> - {message}"
timeName = datetime.now().strftime("%d-%m-%Y")
fmtFile = "{name}:{function}:{line} | {time:YY-MMM-DD HH:mm:ss} - {message}"

LOGS.remove()
LOGS.configure(
    handlers=[
        {"sink": sys.stderr, "format": fmtLog, "colorize": True},
        {
            "sink": "logs/notubot-{}.log".format(timeName),
            "format": fmtFile,
            "rotation": "50 MB",
            "retention": "3 days",
            "encoding": "utf8",
            "serialize": True,
            "enqueue": True,
            "filter": lambda record: record["level"].name == "ERROR",
        },
    ],
)
LOGS.opt(lazy=True)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = LOGS.level(record.levelname).name
        except ValueError:
            level = record.levelno
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        LOGS.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.getLogger("telethon").setLevel(logging.ERROR)
logging.basicConfig(handlers=[InterceptHandler()], level="INFO")


if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    LOGS.info("You MUST have a python version of at least 3.8." "Multiple features depend on this. Bot quitting.")
    quit(1)

# Check if the config was edited by using the already used variable.
# Basically, its the 'virginity check' for the config file ;)
CONFIG_CHECK = getenv("___________PLOX_______REMOVE_____THIS_____LINE__________", default="")

if CONFIG_CHECK:
    LOGS.info("Please remove the line mentioned in the first hashtag from the config.env file")
    quit(1)

# Telegram App KEY and HASH
API_ID = int(getenv("API_ID", default=0))
API_HASH = getenv("API_HASH", default="")

# Userbot Session String
STRING_SESSION = getenv("STRING_SESSION", default="")

# Logging channel/group ID configuration.
BOTLOG_CHATID = int(getenv("BOTLOG_CHATID", default=0))

# Userbot logging feature switch.
BOTLOG = bool(getenv("BOTLOG", False))
LOGSPAMMER = bool(getenv("LOGSPAMMER", False))

# Blacklist group
BLACKLIST_GROUP = list(map(int, getenv("BLACKLIST_GROUP", default="").split()))

# Bot Project Name
BOT_NAME = getenv("BOT_NAME", default="⚡NOTUBOT UserBot⚡")

# Bot Version
BOT_VER = getenv("BOT_VER", default="0.1")

# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = bool(getenv("PM_AUTO_BAN", False))

# Default .alive name and logo
ALIVE_NAME = getenv("ALIVE_NAME", default=uname().node)
ALIVE_LOGO = getenv("ALIVE_LOGO", default="")

# Default .alive Instagram
IG_ALIVE = getenv("IG_ALIVE", default="https://www.instagram.com/notudope")

# Heroku Credentials for updater.
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", default="")
HEROKU_API_KEY = getenv("HEROKU_API_KEY", default="")

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
ANTI_SPAMBOT = bool(getenv("ANTI_SPAMBOT", False))
ANTI_SPAMBOT_SHOUT = bool(getenv("ANTI_SPAMBOT_SHOUT", False))

# Time & Date - Country and Time Zone
COUNTRY = getenv("COUNTRY", default="ID")
TZ_NUMBER = int(getenv("TZ_NUMBER", default=1))

# Clean Welcome
CLEAN_WELCOME = bool(getenv("CLEAN_WELCOME", True))

# OCR API key
OCR_SPACE_API_KEY = getenv("OCR_SPACE_API_KEY", default="")

# remove.bg API key
REM_BG_API_KEY = getenv("REM_BG_API_KEY", default="")

# Deezload Credentials
DEEZER_ARL_TOKEN = getenv("DEEZER_ARL_TOKEN", default="")
DEEZER_EMAIL = getenv("DEEZER_EMAIL", default="")
DEEZER_PASSWORD = getenv("DEEZER_PASSWORD", default="")

# Last.fm Module
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

# Google Drive Module
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
for binary, p in binaries.items():
    downloader = SmartDL(binary, p, progress_bar=False)
    downloader.start()
    chmod(p, 0o755)


def shutdown_bot(signum, frame):
    LOGS.info("Received SIGTERM.")
    bot.disconnect()
    sys.exit(143)


signal.signal(signal.SIGTERM, shutdown_bot)


def migration_workaround():
    try:
        from notubot.modules.sql_helper.globals import addgvar, delgvar, gvarstatus
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


bot = None
if STRING_SESSION:
    bot = TelegramClient(session=StringSession(STRING_SESSION), api_id=API_ID, api_hash=API_HASH)
else:
    bot = TelegramClient(session="notubot", api_id=API_ID, api_hash=API_HASH)


async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "You must set up the BOTLOG_CHATID variable in the config.env or environment variables, for the private error log storage to work."
        )
        quit(1)
    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "You must set up the BOTLOG_CHATID variable in the config.env or environment variables, for the userbot logging feature to work."
        )
        quit(1)
    elif not BOTLOG or not LOGSPAMMER:
        return
    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Your account doesn't have rights to send messages to BOTLOG_CHATID "
            "group. Check if you typed the Chat ID correctly."
        )
        quit(1)


async def check_alive():
    await bot.send_message(BOTLOG_CHATID, f"```{BOT_NAME} v{BOT_VER} Launched 🚀```")


with bot:
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
        bot.loop.run_until_complete(check_alive())
    except BaseException:
        LOGS.info(
            "BOTLOG_CHATID environment variable isn't a "
            "valid entity. Check your environment variables/config.env file."
        )
        quit(1)


async def update_restart_msg(chat_id, msg_id):
    message = (
        f"`{BOT_NAME}`\n"
        f"[REPO](https://github.com/notudope/notubot)  /  [Channel](https://t.me/notudope)  /  [Grup](https://t.me/NOTUBOTS)\n\n"
        f"😎 **Owner :** __{ALIVE_NAME}__\n"
        f"🤖 **Version :** `v{BOT_VER}`\n"
        f"🐍 **Python :** `v{python_version()}`\n"
        f"📦 **Telethon :** `v{version.__version__}`"
    )
    await bot.edit_message(chat_id, msg_id, message, link_preview=False)
    return True


try:
    from notubot.modules.sql_helper.globals import delgvar, gvarstatus

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
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
