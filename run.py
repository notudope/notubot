#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

import argparse
import shlex
import subprocess
import sys
from pathlib import Path
from shutil import rmtree

RST = "\x1b[0m"
BOLD = "\x1b[1m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE = "\x1b[34m"
CYAN = "\x1b[36m"

python = "python3"
app = f"{python} -m notubot"
app_watch = f"{python} -m scripts.autoreload {app}"

black = "brunette --config=setup.cfg ."
isort = "isort --settings-file=setup.cfg ."
flake8 = "flake8 --config=setup.cfg ."
mypy = "mypy --config-file=setup.cfg ."
prettyjson = f"{python} -m scripts.prettyjson"


def run_command(cmd) -> None:
    try:
        proc = subprocess.run(shlex.split(cmd), shell=False)
        if proc.returncode != 0:
            print(f"Exit code {proc.returncode}")
            sys.exit(1)
    except Exception:
        sys.exit(1)


def clean() -> None:
    for file_name in Path(".").rglob("*.py[co]"):
        file_name.unlink()
    for dir_name in Path(".").rglob("__pycache__"):
        dir_name.rmdir()
    rmtree(".mypy_cache", ignore_errors=True)


def lint() -> None:
    print(f"{CYAN}> {black}{RST}")
    run_command(black)
    print(f"{CYAN}> {isort}{RST}")
    run_command(isort)
    print(f"{CYAN}> {flake8}{RST}")
    run_command(flake8)
    # print(f"{CYAN}> {mypy}{RST}")
    # run_command(mypy)
    print(f"{CYAN}> {prettyjson}{RST}")
    run_command(prettyjson)


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = "Usage: "

        return super(CapitalisedHelpFormatter, self).add_usage(usage, actions, groups, prefix)


parser = argparse.ArgumentParser(
    formatter_class=CapitalisedHelpFormatter,
    prog=f"{GREEN}{python} -m run{RST}",
    usage="%(prog)s [options]",
    epilog="Source code https://github.com/notudope/notubot",
    add_help=False,
)
parser._optionals.title = "Options"
parser.add_argument("-p", "--prod", help="run in production mode", action="store_true")
parser.add_argument("-d", "--dev", help="run in development mode", action="store_true")
parser.add_argument("-w", "--watch", help="run and watch in development mode", action="store_true")
parser.add_argument("-l", "--lint", help="run linting and format code", action="store_true")
parser.add_argument("-c", "--clean", help="remove __pycache__ and .mypy_cache", action="store_true")
parser.add_argument("-v", "--version", help="show this program version", action="version", version="0.0.1")
parser.add_argument("-h", "--help", help="show this help information", default=argparse.SUPPRESS, action="help")


def main() -> None:
    args = parser.parse_args()
    if args.prod:
        print(f"{BOLD}{GREEN}[ PRODUCTION MODE ]{RST}")
        clean()

        print(f"{BOLD}{BLUE}> {app}{RST}")
        run_command(app)

    elif args.dev:
        print(f"{BOLD}{GREEN}[ DEVELOPMENT MODE ]{RST}")
        clean()

        lint()
        print(f"{BOLD}{BLUE}> {app}{RST}")
        run_command(app)

    elif args.watch:
        print(f"{BOLD}{GREEN}[ WATCHED DEVELOPMENT MODE ]{RST}")
        clean()

        print(f"{BOLD}{BLUE}> {app_watch}{RST}")
        run_command(app_watch)

    elif args.lint:
        print(f"{BOLD}{YELLOW}Run linting and format code...{RST}")
        lint()
        sys.exit(0)

    elif args.clean:
        clean()
        sys.exit(0)

    else:
        print(f"{python} -m run --help")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
