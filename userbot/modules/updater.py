import asyncio
import sys
from os import (
    environ,
    execle,
    remove,
    path,
)

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import (
    BOTLOG,
    BOTLOG_CHATID,
    CMD_HELP,
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    UPSTREAM_REPO_BRANCH,
    UPSTREAM_REPO_URL,
)
from userbot.events import register

requirements_path = path.join(path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt")


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
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
    changelog_str = f"`⚡NOTUBOT UserBot⚡` **Pembaruan tersedia untuk [{ac_br}]:\n\nCHANGELOG:**\n`{changelog}`"

    if len(changelog_str) > 4096:
        await event.edit("`Data CHANGELOG terlalu besar, buka file untuk melihatnya.`")
        file = open("output.txt", "w+")
        file.write(changelog_str)
        file.close()

        await event.client.send_file(
            event.chat_id,
            "output.txt",
            reply_to=event.id,
        )
        remove("output.txt")
    else:
        await event.client.send_message(
            event.chat_id,
            changelog_str,
            reply_to=event.id,
        )
    return True


async def deploy(event, repo, ups_rem, ac_br, txt):
    if HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()

        if HEROKU_APP_NAME is None:
            await event.edit(
                "Harap **tentukan variabel** `HEROKU_APP_NAME` untuk dapat Deploy perubahan terbaru dari `⚡NOTUBOT UserBot⚡`."
            )
            repo.__del__()
            return

        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break

        if heroku_app is None:
            await event.edit(f"{txt}\n" "`Kredensial Heroku tidak valid untuk deploy UserBot dyno.`")
            return repo.__del__()

        await event.edit("`UserBot dyno sedang memperbarui, harap tunggu, perkiraan waktu 5-7 menit...`")

        try:
            from userbot.modules.sql_helper.globals import addgvar, delgvar

            delgvar("restartstatus")
            addgvar("restartstatus", f"{event.chat_id}\n{event.id}")
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
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except Exception as error:
            await event.edit(f"{txt}\n`Disini catatan kesalahan:\n{error}`")
            return repo.__del__()

        build = heroku_app.builds(order_by="created_at", sort="desc")[0]

        if build.status == "failed":
            await event.edit("`Build gagal!\n" "Dibatalkan atau ada beberapa kesalahan...`")
            await asyncio.sleep(5)
            return await event.delete()
        else:
            await event.edit("`⚡NOTUBOT UserBot⚡ berhasil diperbarui, dimuat ulang...`")
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID, "#bot #deploy \n" "`⚡NOTUBOT UserBot⚡ Berhasil Diperbarui.`"
                )

    else:
        await event.edit("Harap **tentukan variabel** `HEROKU_API_KEY`.")
    return


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")

    await update_requirements()
    await event.edit("**⚡NOTUBOT UserBot⚡** `Berhasil Diperbarui!`")
    await asyncio.sleep(1)
    await event.edit("**⚡NOTUBOT UserBot⚡** `Dimuat ulang...`")
    await asyncio.sleep(1)
    await event.edit("**⚡NOTUBOT UserBot⚡** `Tunggu beberapa detik!`")

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#bot #now \n" "`⚡NOTUBOT UserBot⚡ Telah Diperbarui.`")

    try:
        from userbot.modules.sql_helper.globals import addgvar, delgvar

        delgvar("restartstatus")
        addgvar("restartstatus", f"{event.chat_id}\n{event.id}")
    except AttributeError:
        pass

    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)


@register(outgoing=True, pattern=r"^.update(?: |$)(now|deploy|pull|push)?")
async def upstream(event):
    "For .update command, check if the bot is up to date, update if specified"
    conf = event.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_update = False

    await event.edit("`...`")
    try:
        txt = "`Oops.. Pembaruan tidak dapat dilanjutkan karena "
        txt += "Beberapa masalah terjadi`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await event.edit(f"{txt}\n`Direktori {error} tidak ditemukan.`")
        return repo.__del__()
    except GitCommandError as error:
        await event.edit(f"{txt}\n`Kesalahan diawal! {error}`")
        return repo.__del__()
    except InvalidGitRepositoryError as error:
        if conf is None:
            return await event.edit(
                f"`Sayangnya, direktori {error} "
                "sepertinya bukan repositori git.\n"
                "Tapi bisa memperbaiki dengan memperbarui paksa UserBot menggunakan "
                ".update now atau update pull.`"
            )
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        force_update = True
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != UPSTREAM_REPO_BRANCH:
        await event.edit(
            "**[UPDATER]:**\n"
            f"`Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "please checkout to any official branch`"
        )
        return repo.__del__()
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")

    if changelog == "" and force_update is False:
        await event.edit("\n`⚡NOTUBOT UserBot⚡`  **up-to-date** branch " f"`{UPSTREAM_REPO_BRANCH}`\n")
        return repo.__del__()

    if conf == "" and force_update is False:
        await print_changelogs(event, ac_br, changelog)
        await event.delete()
        await event.respond("Jalankan `.update now` atau `.update pull` untuk __memperbarui sementara__.")
        await event.respond("Jalankan `.update deploy` atau `.update push` untuk __memperbarui permanen__.")
        return

    if force_update:
        await event.edit("`Memaksa sinkronisasi ke kode UserBot stabil terbaru, harap tunggu...`")
    else:
        await event.edit("`Proses Update ⚡NOTUBOT UserBot⚡, Loading....1%`")
        await event.edit("`Proses Update ⚡NOTUBOT UserBot⚡, Loading....20%`")
        await event.edit("`Proses Update ⚡NOTUBOT UserBot⚡, Loading....35%`")
        await event.edit("`Proses Update ⚡NOTUBOT UserBot⚡, Loading....77%`")
        await event.edit("`Proses Update ⚡NOTUBOT UserBot⚡, Updating...90%`")
        await event.edit("`Proses Update ⚡NOTUBOT UserBot⚡, mohon tunggu sebentar...100%`")

    if conf == "now" or conf == "pull":
        await event.edit("`Memperbarui ⚡NOTUBOT UserBot⚡, harap tunggu...`")
        await update(event, repo, ups_rem, ac_br)
    elif conf == "deploy" or conf == "push":
        await event.edit("`Proses Deploy ⚡NOTUBOT UserBot⚡, harap tunggu...`")
        await deploy(event, repo, ups_rem, ac_br, txt)

    return


CMD_HELP.update(
    {
        "update": ">`.update`"
        "\nUsage: Mengecek apakah ada pembaruan pada repo UserBot "
        "dan termasuk menampilkan changelog."
        "\n\n>`.update now|pull`"
        "\nUsage: Memperbarui sistem UserBot, "
        "jika ada pembaruan pada repo UserBot."
        "\n\n>`.update deploy|push`"
        "\nUsage: Deploy UserBot (heroku)"
        "\nIni akan memaksa deploy meskipun tidak ada pembaruan pada UserBot."
    }
)
