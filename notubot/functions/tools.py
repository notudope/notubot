from telegraph import Telegraph

from notubot import LOGS, bot

TELEGRAPH = []


def telegraph_client():
    if TELEGRAPH:
        return TELEGRAPH[0]

    try:
        from notubot.database.globals import addgv, getgv
    except AttributeError:
        return None

    token = getgv("_TELEGRAPH_TOKEN")
    TelegraphClient = Telegraph(token)
    if token:
        TELEGRAPH.append(TelegraphClient)
        return TelegraphClient

    short_name = bot.name if len(bot.name) < 32 else "notubot"
    profile_url = f"https://t.me/{bot.me.username}" if bot.me.username else None

    try:
        TelegraphClient.create_account(short_name=short_name, author_name=bot.name, author_url=profile_url)
    except Exception as er:
        LOGS.exception(er)
        return

    addgv("_TELEGRAPH_TOKEN", TelegraphClient.get_access_token())
    TELEGRAPH.append(TelegraphClient)
    return TelegraphClient
