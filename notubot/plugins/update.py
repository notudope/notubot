# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import asyncio
import os
import sys
from io import BytesIO
from pathlib import Path

import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from notubot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    UPSTREAM_REPO_BRANCH,
    UPSTREAM_REPO_URL,
    __botname__,
    HANDLER,
)
from notubot.events import bot_cmd

app_dir: Path = Path(__file__).parent.parent
requirements_path = app_dir / "requirements.txt"


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-U", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f"•[{c.committed_datetime.strftime(d_form)}]: " f"{c.summary} <{c.author}>\n"
    return ch_log


async def print_changelogs(event, ac_br, changelog):
    chat_id = event.chat_id or event.from_id
    changelog_str = f"`{__botname__}` **Pembaruan Tersedia Untuk [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`"

    if len(changelog_str) > 4096:
        await event.edit("`Data CHANGELOG terlalu besar, buka file untuk melihatnya.`")
        try:
            with BytesIO(str.encode(changelog_str)) as file:
                file.name = "changelog.txt"
                await event.client.send_file(
                    chat_id,
                    file,
                    force_document=True,
                    allow_cache=False,
                    reply_to=event.id,
                )
        except Exception:
            pass
    else:
        await event.client.send_message(
            chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def deploy(event, repo, ups_rem, ac_br, txt):
    chat_id = event.chat_id or event.from_id
    if not HEROKU_API_KEY:
        await event.edit("Harap **tentukan variabel** `HEROKU_API_KEY`.")
        return

    heroku = heroku3.from_key(HEROKU_API_KEY)
    heroku_app = None
    heroku_applications = heroku.apps()

    if not HEROKU_APP_NAME:
        await event.edit(
            f"Harap **tentukan variabel** `HEROKU_APP_NAME` untuk Deploy perubahan terbaru dari `{__botname__}`."
        )
        repo.__del__()
        return

    for app in heroku_applications:
        if app.name == HEROKU_APP_NAME:
            heroku_app = app
            break

    if not heroku_app:
        await event.edit(f"{txt}\n" "`Variabel Heroku tidak valid untuk deploy notubot Dyno.`")
        return repo.__del__()

    await event.edit(f"`{__botname__} Dyno sedang memperbarui, perkiraan waktu sampai 5 menit...`")

    try:
        from notubot.database.globals import addgv, delgv

        delgv("restartstatus")
        addgv("restartstatus", f"{chat_id}\n{event.id}")
    except AttributeError:
        pass

    ups_rem.fetch(ac_br)
    repo.git.reset("--hard", "FETCH_HEAD")
    heroku_git_url = heroku_app.git_url.replace("https://", "https://api:" + HEROKU_API_KEY + "@")

    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(heroku_git_url)
    else:
        remote = repo.create_remote("heroku", heroku_git_url)

    try:
        remote.push(refspec="HEAD:refs/heads/main", force=True)
    except Exception as e:
        await event.edit(f"{txt}\n`Disini catatan kesalahan:\n{e}`")
        return repo.__del__()

    build = heroku_app.builds(order_by="created_at", sort="desc")[0]

    if build.status == "failed":
        await event.edit("`Build gagal!\n" "Dibatalkan atau ada beberapa kesalahan...`")
        await asyncio.sleep(5)
        return await event.delete()
    else:
        await event.edit(f"`{__botname__} Berhasil Diperbarui, Dimuat Ulang...`")
        if BOTLOG:
            await event.client.send_message(BOTLOG_CHATID, "#bot #push \n" f"**{__botname__} Berhasil Diperbarui ツ**")
    return


async def update(event, repo, ups_rem, ac_br):
    chat_id = event.chat_id or event.from_id
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")

    await update_requirements()
    await event.edit(f"**{__botname__}** `Berhasil Diperbarui!`")
    await asyncio.sleep(1)
    await event.edit(f"**{__botname__}** `Dimuat Ulang...`")
    await asyncio.sleep(1)
    await event.edit(f"**{__botname__}** `Updated !!`")

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#bot #pull \n" f"**{__botname__} Telah Diperbarui**")

    try:
        from notubot.database.globals import addgv, delgv

        delgv("restartstatus")
        addgv("restartstatus", f"{chat_id}\n{event.id}")
    except AttributeError:
        pass

    os.execl(sys.executable, sys.executable, "-m", "notubot")
    return


@bot_cmd(pattern="update(?: |$)(now|deploy|pull|push|one|all)?")
async def upstream(event):
    opts = event.pattern_match.group(1)
    force_update = False

    await event.edit("`...`")
    try:
        txt = "`Oops.. Pembaruan tidak dapat dilanjutkan karena "
        txt += "Beberapa masalah terjadi`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as e:
        await event.edit(f"{txt}\n`Direktori {e} tidak ditemukan.`")
        return repo.__del__()
    except GitCommandError as e:
        await event.edit(f"{txt}\n`Kesalahan diawal! {e}`")
        return repo.__del__()
    except InvalidGitRepositoryError as e:
        if not opts:
            return await event.edit(
                f"`Direktori {e} "
                "sepertinya bukan repositori git.\n"
                "Tapi bisa memperbaiki dengan memperbarui paksa notubot menggunakan "
                "{HANDLER}update now|pull|one.`"
            )

        repo = Repo.init()
        origin = repo.create_remote("upstream", UPSTREAM_REPO_URL)
        origin.fetch()
        force_update = True
        repo.create_head("main", origin.refs.main)
        repo.heads.main.set_tracking_branch(origin.refs.main)
        repo.heads.main.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`Sepertinya menggunakan custom branch ({ac_br}). "
            "Ini tidak dapat mengidentifikasi "
            "branch mana yang akan digabung. "
            "Silakan gunakan official branch.`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", UPSTREAM_REPO_URL)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")

    if opts in ["deploy", "push", "all"]:
        await event.edit(f"`{__botname__} Proses Deploy, Harap Tunggu...`")
        await deploy(event, repo, ups_rem, ac_br, txt)
        return

    if changelog == "" and not force_update:
        await event.edit(f"\n`{__botname__}`  **up-to-date** branch " f"`{UPSTREAM_REPO_BRANCH}`\n")
        return repo.__del__()

    if not opts and not force_update:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        await event.respond(f"Jalankan `{HANDLER}update now|pull|one` untuk __memperbarui sementara__.")
        await event.respond(f"Jalankan `{HANDLER}update deploy|push|all` untuk __memperbarui permanen__.")
        return

    if force_update:
        await event.edit("`Memaksa sinkronisasi ke kode notubot stabil terbaru, harap tunggu...`")
    else:
        await event.edit(f"`{__botname__} Proses Update, Loading....1%`")
        await event.edit(f"`{__botname__} Proses Update, Loading....20%`")
        await event.edit(f"`{__botname__} Proses Update, Loading....35%`")
        await event.edit(f"`{__botname__} Proses Update, Loading....77%`")
        await event.edit(f"`{__botname__} Proses Update, Updating...90%`")
        await event.edit(f"`{__botname__} Proses Update, Mohon Tunggu Sebentar...100%`")

    if opts in ["now", "pull", "one"]:
        await event.edit(f"`{__botname__} Memperbarui, Harap Tunggu...`")
        await update(event, repo, ups_rem, ac_br)
    return


@bot_cmd(pattern="repo$")
async def repo(event):
    await event.edit(
        f"""**{__botname__}**
[📦 Repo](https://github.com/notudope/notubot)  [🚀 Deploy](https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2Fnotudope%2Fnotubot&template=https%3A%2F%2Fgithub.com%2Fnotudope%2Fnotubot)""",
        link_preview=False,
    )


CMD_HELP.update(
    {
        "update": [
            "Update",
            "`.update`\n"
            "↳ : Mengecek apakah ada pembaruan pada repo notubot termasuk menampilkan changelog.\n\n"
            "`.update <now|pull|one>`\n"
            "↳ : Memperbarui sistem notubot jika ada pembaruan pada repo notubot.\n\n"
            "`.update <deploy|push|all>`\n"
            "↳ : Deploy notubot (heroku), ini akan memaksa deploy meskipun tidak ada pembaruan pada notubot.\n\n"
            "`.repo`\n"
            "↳ : Github Repository notubot.\n\n",
        ]
    }
)
