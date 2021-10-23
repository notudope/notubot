# NOTUBOT - UserBot
# Copyright (C) 2021 notudope
#
# This file is a part of < https://github.com/notudope/notubot/ >
# PLease read the GNU General Public License v3.0 in
# <https://www.github.com/notudope/notubot/blob/main/LICENSE/>.

from time import time

from notubot import LOGS


def __list_all_plugins():
    from glob import glob
    from os.path import dirname, basename, isfile

    paths = glob("{}/*.py".format(dirname(__file__)))
    plugins = [
        basename(plugin)[:-3]
        for plugin in paths
        if isfile(plugin) and plugin.endswith(".py") and not plugin.endswith("__init__.py")
    ]
    return plugins


start = time()
ALL_PLUGINS = sorted(__list_all_plugins())
took = time() - start
LOGS.info(f"Loaded Plugins {len(ALL_PLUGINS)} (took {took:.2f}s) : %s", str(ALL_PLUGINS))
__all__ = ALL_PLUGINS + ["ALL_PLUGINS"]
