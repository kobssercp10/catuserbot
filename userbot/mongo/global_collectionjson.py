# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.
#
# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".
#
# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""Store arbitrary JSON blobs keyed by string."""

from typing import Any, Dict

from . import DB, run_sync


async def _add_collection(key: str, json: Dict[str, Any], njson: Dict[str, Any] | None = None):
    if DB is None:
        return
    payload = {"json": json, "njson": njson or {}}
    await DB.global_collectionjson.update_one({"key": key}, {"$set": payload}, upsert=True)


def add_collection(key: str, json: Dict[str, Any], njson: Dict[str, Any] | None = None):
    """Store ``json`` (and optional ``njson``) for ``key``."""

    run_sync(_add_collection(key, json, njson))


async def _get_collection(key: str) -> Dict[str, Any] | None:
    if DB is None:
        return None
    return await DB.global_collectionjson.find_one({"key": key})


def get_collection(key: str) -> Dict[str, Any] | None:
    """Fetch stored document for ``key``."""

    return run_sync(_get_collection(key))


async def _del_collection(key: str) -> bool:
    if DB is None:
        return False
    result = await DB.global_collectionjson.delete_one({"key": key})
    return result.deleted_count > 0


def del_collection(key: str) -> bool:
    """Remove ``key`` from the database."""

    return run_sync(_del_collection(key))


async def _get_collections():
    if DB is None:
        return []
    cursor = DB.global_collectionjson.find({})
    return [doc async for doc in cursor]


def get_collections():
    """Return all stored collections."""

    return run_sync(_get_collections())
