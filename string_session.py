#!/usr/bin/env python3
# python3 -m pip install --upgrade https://github.com/LonamiWebs/Telethon/archive/master.zip
from telethon import TelegramClient
from telethon.sessions import StringSession

print("my.telegram.org")

API_KEY = int(input("Enter API_KEY here: "))
API_HASH = input("Enter API_HASH here: ")

client = TelegramClient(StringSession(), API_KEY, API_HASH)


async def main():
    print('Check Telegram "Saved Messages" to copy STRING_SESSION ')
    session_string = client.session.save()

    print(session_string)
    await client.send_message("me", f"<code>STRING_SESSION</code>: <code>{session_string}</code>", parse_mode="html")


with client:
    client.loop.run_until_complete(main())
