# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.
#
# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".
#
# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""MongoDB backed helper for storing lists of values for arbitrary keys."""

from typing import Iterable, List

from . import DB, run_sync


async def _add_to_collectionlist(key: str, contents: Iterable[str]):
    if DB is None:
        return
    await DB.global_collection.update_one(
        {"key": key}, {"$addToSet": {"contents": {"$each": list(contents)}}}, upsert=True
    )


def add_to_collectionlist(key: str, contents: Iterable[str]):
    """Add ``contents`` to the list stored for ``key``."""

    run_sync(_add_to_collectionlist(key, contents))


async def _rm_from_collectionlist(key: str, contents: Iterable[str]):
    if DB is None:
        return False
    result = await DB.global_collection.update_one(
        {"key": key}, {"$pullAll": {"contents": list(contents)}}
    )
    return result.modified_count > 0


def rm_from_collectionlist(key: str, contents: Iterable[str]) -> bool:
    """Remove ``contents`` from ``key``'s list."""

    return run_sync(_rm_from_collectionlist(key, contents))


async def _del_keyword_collectionlist(key: str):
    if DB is None:
        return
    await DB.global_collection.delete_one({"key": key})


def del_keyword_collectionlist(key: str):
    """Delete ``key`` entirely from the collection."""

    run_sync(_del_keyword_collectionlist(key))


async def _get_item_collectionlist(key: str) -> List[str]:
    if DB is None:
        return []
    doc = await DB.global_collection.find_one({"key": key})
    return doc.get("contents", []) if doc else []


def get_item_collectionlist(key: str) -> List[str]:
    """Return list stored for ``key``."""

    return run_sync(_get_item_collectionlist(key))


async def _get_collectionlist_items() -> List[str]:
    if DB is None:
        return []
    cursor = DB.global_collection.find({}, {"key": 1})
    return [doc["key"] async for doc in cursor]


def get_collectionlist_items() -> List[str]:
    """Return all keys in the collection list."""

    return run_sync(_get_collectionlist_items())
