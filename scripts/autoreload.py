# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

"""
https://github.com/stevekrenzel/autoreload
"""
import os
import signal
import subprocess
import sys
import time
from glob import glob
from typing import Generator

import psutil

RST = "\x1b[0m"
BOLD = "\x1b[1m"
RED = "\x1b[31m"
YELLOW = "\x1b[33m"


def file_times(path) -> Generator[int, None, None]:
    for file_name in glob(path, recursive=True):
        yield os.stat(file_name).st_mtime


def print_stdout(process) -> None:
    stdout = process.stdout
    if stdout is not None:
        print(stdout)


def kill_process_tree(process) -> None:
    # https://psutil.readthedocs.io/en/latest/#kill-process-tree
    parent = psutil.Process(process.pid)
    children = parent.children(recursive=True)
    children.append(parent)
    for p in children:
        try:
            p.send_signal(signal.SIGTERM)
        except psutil.NoSuchProcess:
            pass
    process.terminate()


# The path to watch
path = "**/*.py"

# Check the filesystem for changes (in seconds)
wait = 1


def main() -> None:
    if len(sys.argv) <= 1:
        print("python3 -m scripts.autoreload [command]")
        sys.exit(0)

    command = " ".join(sys.argv[1:])
    process = subprocess.Popen(command, shell=True)
    last_mtime = max(file_times(path))

    try:
        while True:
            max_mtime = max(file_times(path))
            print_stdout(process)
            if max_mtime > last_mtime:
                last_mtime = max_mtime
                print(f"{BOLD}{YELLOW}Kill current process [{process.pid}] and restarting [{process.args}]{RST}")
                kill_process_tree(process)
                process = subprocess.Popen(command, shell=True)
            time.sleep(wait)
    except subprocess.CalledProcessError as e:
        kill_process_tree(process)
        sys.exit(e.returncode)
    except Exception:
        print("internal error!", file=sys.stderr)
        raise  # traceback will output to stderr
    except KeyboardInterrupt:
        print(f"{BOLD}{RED}Kill current process [{process.pid}]{RST}")
        kill_process_tree(process)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    main()
