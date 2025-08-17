# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.
#
# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".
#
# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

"""MongoDB backed key-value storage used throughout the bot."""

from . import DB, run_sync


async def _gvarstatus(variable: str):
    if DB is None:
        return None
    doc = await DB.globals.find_one({"variable": str(variable)})
    return doc["value"] if doc else None


def gvarstatus(variable: str):
    """Return the value for ``variable`` or ``None`` if not set."""

    return run_sync(_gvarstatus(variable))


async def _addgvar(variable: str, value: str):
    if DB is None:
        return
    await DB.globals.update_one(
        {"variable": str(variable)}, {"$set": {"value": value}}, upsert=True
    )


def addgvar(variable: str, value: str):
    """Store ``value`` for ``variable``."""

    return run_sync(_addgvar(variable, value))


async def _delgvar(variable: str):
    if DB is None:
        return
    await DB.globals.delete_one({"variable": str(variable)})


def delgvar(variable: str):
    """Remove ``variable`` from the database."""

    return run_sync(_delgvar(variable))

