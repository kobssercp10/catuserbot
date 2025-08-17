# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.
#
# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".
#
# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

"""MongoDB helper utilities using Motor."""

import asyncio
from urllib.parse import urlsplit

from motor.motor_asyncio import AsyncIOMotorClient

from ..Config import Config
from ..core.logger import logging

LOGS = logging.getLogger(__name__)

_MONGO_LOOP = asyncio.new_event_loop()


def _get_db_name(uri: str) -> str:
    """Extract database name from a Mongo URI."""

    path = urlsplit(uri).path
    return path[1:] if path and len(path) > 1 else "catuserbot"


def start():
    """Initialise Motor client and return database handle."""

    database_url = Config.MONGO_DB_URI
    client = AsyncIOMotorClient(database_url, io_loop=_MONGO_LOOP)
    db_name = _get_db_name(database_url)
    return client[db_name]


def run_sync(coro):
    """Run an async coroutine on the dedicated Mongo loop."""

    return _MONGO_LOOP.run_until_complete(coro)


try:
    DB = start()
except Exception as e:
    LOGS.error(
        "MongoDB is not configured correctly. Features depending on the database might have issues."
    )
    LOGS.error(str(e))
    DB = None

