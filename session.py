#!/usr/bin/env python3
# python3 -m pip install --upgrade https://github.com/LonamiWebs/Telethon/archive/master.zip
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import ApiIdInvalidError, PhoneNumberInvalidError
from telethon.sessions import StringSession

print("Get your API ID and API HASH from my.telegram.org or @ScrapperRoBot to proceed.\n\n")

try:
    API_ID = int(input("Please enter your API ID: "))
except ValueError:
    print("APP ID must be an integer.\nQuitting...")
    exit(0)
API_HASH = input("Please enter your API HASH: ")

client = TelegramClient(StringSession(), API_ID, API_HASH)


async def main() -> None:
    try:
        print("Generating a user STRING_SESSION...")
        string_session = client.session.save()

        print(string_session)
        await client.send_message(
            "me", f"<code>STRING_SESSION</code>: <code>{string_session}</code>", parse_mode="html"
        )

        print(
            'Your SESSION has been generated. Check your Telegram "Saved Messages" to copy STRING_SESSION or copy from above.'
        )
        exit(0)
    except ApiIdInvalidError:
        print("Your API ID/API HASH combination is invalid. Kindly recheck.\nQuitting...")
        exit(0)
    except ValueError:
        print("API HASH must not be empty!\nQuitting...")
        exit(0)
    except PhoneNumberInvalidError:
        print("The phone number is invalid!\nQuitting...")
        exit(0)


with client:
    client.loop.run_until_complete(main())
