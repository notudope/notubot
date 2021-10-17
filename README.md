# `notubot`

> Another **userbot** powered by `telethon` for lazy **Telegram** user 😖

<p align="center">
    <a href="https://app.codacy.com/gh/notudope/notubot/dashboard"> <img src="https://img.shields.io/codacy/grade/a723cb464d5a4d25be3152b5d71de82d?color=blue&logo=codacy&style=flat-square" alt="Codacy" /></a><br>
    <a href="https://github.com/notudope/notubot/stargazers"> <img src="https://img.shields.io/github/stars/notudope/notubot?logo=github&style=flat-square" alt="Stars" /></a>
    <a href="https://github.com/notudope/notubot/network/members"> <img src="https://img.shields.io/github/forks/notudope/notubot?logo=github&style=flat-square" alt="Forks" /></a>
    <a href="https://github.com/notudope/notubot/watchers"> <img src="https://img.shields.io/github/watchers/notudope/notubot?logo=github&style=flat-square" alt="Watch" /></a><br>
    <a href="https://github.com/notudope/notubot/graphs/contributors"> <img src="https://img.shields.io/github/contributors/notudope/notubot?color=blue&style=flat-square" alt="Contributors" /></a>
    <a href="https://pypi.org/project/Telethon/"> <img src="https://img.shields.io/pypi/v/telethon?label=telethon&logo=pypi&logoColor=white&style=flat-square" /></a>
</p>

```
#include <std/disclaimer.h>
/*
*    Your Telegram account may get banned.
*    I am not responsible for any improper use of this bot
*    This bot is intended for the purpose of having fun with memes,
*    as well as efficiently managing groups.
*    You ended up spamming groups, getting reported left and right,
*    and you ended up in a Finale Battle with Telegram and at the end
*    Telegram Team deleted your account?
*    And after that, then you pointed your fingers at us
*    for getting your acoount deleted?
*    I will be rolling on the floor laughing at you.
*/
```

A modular Telegram Userbot running on Python3 with sqlalchemy database.

based on [WeebProject](https://github.com/BianSepang/WeebProject) Userbot

## Deploy
### Heroku
Click this button below to Deploy to Heroku
<p align="center"><a href="https://heroku.com/deploy?template=https://github.com/notudope/notubot/tree/main"> <img src="https://www.herokucdn.com/deploy/button.png" alt="Deploy to Heroku"/></a></p>

### "Bare hands", using Git and Python3 -- on (Linux, macOS, and Android [via Termux])
1. Clone this repository on your local machine and `cd` (or `chdir`, anti bloat guy) to it
2. Set up Python virtual environment named "venv" inside it (Requires `virtualenv` installed on the system)
  - `virtualenv venv`
  - Don't forget to activate the virtualenv: `. venv/bin/activate`
3. Set up database for the userbot, search Google on how to set up a local database (PostgreSQL is recommended)
4. Install the requirements: `pip3 install -r ./requirements.txt`
5. Edit `sample_config.env` and save it as `config.env`
  - Do not forget to fill in the `REQUIRED %%` values, or else the bot will not run
6. Run the bot: `bash ./exec.sh`
  - Protip: See what `bash ./exec.sh --help` tells you

### Docker
1. Clone this repository on your local machine and `cd` (or `chdir`, anti bloat guy) to it
2. Edit `sample_config.env` and save it as `config.env`
  - Set `DATABASE_URL` to `postgresql://USERNAME:PASSWORD@db:5432/notubot`
  - You should set `USERNAME` and `PASSWORD` too in `docker-compose.yml`
  - Do not forget to fill in the `REQUIRED %%` values, or else the bot will not run
3. Run docker: `docker-compose up`

##### ※ Those steps are probably possible to pull off on Windows but it's pretty much unknown (different file tree paradigm, directory conventions, PowerShell instead of BASH or ZSH) -- If you're on Windows, you'd be better off running this on WSL (or WSL2)
---
## Credits
* [BianSepang](https://github.com/BianSepang/WeebProject) - WeebProject (Original Source)
* [vckyou](https://github.com/vckyou/Geez-UserBot) - Geez-UserBot

and [everyone](https://github.com/notudope/notubot/graphs/contributors) that makes this userbot awesome!

## License
Licensed under [GNU General Public License v3.0](https://github.com/notudope/notubot/blob/main/LICENSE)
