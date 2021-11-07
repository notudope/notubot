import asyncio
import os
import sys

import heroku3

from notubot import HEROKU_API_KEY, HEROKU_APP_NAME


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


async def restart(event):
    if HEROKU_APP_NAME and HEROKU_API_KEY:
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            app = Heroku.apps()[HEROKU_APP_NAME]
            await event.edit("`Restarting... Tunggu beberapa menit.`")
            app.restart()
        except BaseException:
            return await event.edit(
                "`HEROKU_API_KEY` atau `HEROKU_APP_NAME` salah! Cek ulang config var.",
            )
    else:
        os.execl(sys.executable, sys.executable, "-m", "notubot")
