# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.
#
# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".
#
# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
"""Store string lists keyed by a name."""

from typing import Iterable, List, Set

from . import DB, run_sync


async def _add_to_list(key: str, group_id: str):
    if DB is None:
        return
    await DB.global_list.update_one(
        {"key": key}, {"$addToSet": {"ids": str(group_id)}}, upsert=True
    )


def add_to_list(key: str, group_id: str):
    run_sync(_add_to_list(key, group_id))


async def _rm_from_list(key: str, group_id: str) -> bool:
    if DB is None:
        return False
    result = await DB.global_list.update_one(
        {"key": key}, {"$pull": {"ids": str(group_id)}}
    )
    return result.modified_count > 0


def rm_from_list(key: str, group_id: str) -> bool:
    return run_sync(_rm_from_list(key, group_id))


async def _is_in_list(key: str, group_id: str) -> bool:
    if DB is None:
        return False
    doc = await DB.global_list.find_one({"key": key, "ids": str(group_id)})
    return bool(doc)


def is_in_list(key: str, group_id: str) -> bool:
    return run_sync(_is_in_list(key, group_id))


async def _del_keyword_list(key: str):
    if DB is None:
        return
    await DB.global_list.delete_one({"key": key})


def del_keyword_list(key: str):
    run_sync(_del_keyword_list(key))


async def _get_collection_list(key: str) -> Set[str]:
    if DB is None:
        return set()
    doc = await DB.global_list.find_one({"key": key})
    return set(doc.get("ids", [])) if doc else set()


def get_collection_list(key: str) -> Set[str]:
    return run_sync(_get_collection_list(key))


async def _get_list_keywords() -> List[str]:
    if DB is None:
        return []
    cursor = DB.global_list.find({}, {"key": 1})
    return [doc["key"] async for doc in cursor]


def get_list_keywords() -> List[str]:
    return run_sync(_get_list_keywords())
