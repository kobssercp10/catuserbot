# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from motor.motor_asyncio import AsyncIOMotorClient

# the secret configuration specific things
from ..Config import Config
from ..core.logger import logging

LOGS = logging.getLogger(__name__)


MONGO_DB_URI = getattr(Config, "MONGO_DB_URI", None) or Config.DB_URI
MONGO_DB_NAME = getattr(Config, "MONGO_DB_NAME", "catuserbot")

try:
    MONGO_CLIENT = AsyncIOMotorClient(MONGO_DB_URI)
    MONGO_DB = MONGO_CLIENT[MONGO_DB_NAME]
except Exception as e:  # pragma: no cover - connection errors handled at runtime
    LOGS.error(
        "MongoDB connection failed. Features depending on the database might have issues."
    )
    LOGS.error(str(e))
    MONGO_CLIENT = None
    MONGO_DB = None
