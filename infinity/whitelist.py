import json
import os

import infinity
from infinity import connection

whitelisted_qq_groups: list[int] = []
banned_qq_users: list[int] = []


def write_whitelist_qq_groups_into_json():
    with open("whitelist_qq_groups.json", "w+") as f:
        j = json.dumps(whitelisted_qq_groups, ensure_ascii=False, indent=4)
        f.write(j)


def write_banned_qq_users_into_json():
    with open("banned_qq_users.json", "w+") as f:
        j = json.dumps(banned_qq_users, ensure_ascii=False, indent=4)
        f.write(j)


def read_whitelist_qq_groups_from_json():
    global whitelisted_qq_groups
    if not os.path.exists("whitelist_qq_groups.json"):
        with open("whitelist_qq_groups.json", "w") as f:
            json.dump([], f)
    with open("whitelist_qq_groups.json", "r") as f:
        whitelisted_qq_groups = json.load(f)


def read_banned_qq_users_from_json():
    global banned_qq_users
    if not os.path.exists("banned_qq_users.json"):
        with open("banned_qq_users.json", "w") as f:
            json.dump([], f)
    with open("banned_qq_users.json", "r") as f:
        banned_qq_users = json.load(f)


async def add_whitelist_qq_group(qq_group: int):
    print(whitelisted_qq_groups)
    if qq_group not in whitelisted_qq_groups:
        whitelisted_qq_groups.append(qq_group)
        await connection.add_group_to_whitelist(qq_group)


async def remove_whitelist_qq_group(qq_group: int):
    print(whitelisted_qq_groups)
    if qq_group in whitelisted_qq_groups:
        await connection.remove_group_from_whitelist(qq_group)
        await read_whitelist_from_mongo()


async def add_banned_qq_user(qq_user: int):
    print(banned_qq_users)
    if qq_user not in banned_qq_users:
        banned_qq_users.append(qq_user)
        await connection.add_user_to_blacklist(qq_user)


async def remove_banned_qq_user(qq_user: int):
    print(banned_qq_users)
    if qq_user in banned_qq_users:
        await connection.remove_user_from_blacklist(qq_user)
        await read_banned_from_mongo()


async def read_whitelist_from_mongo():
    global whitelisted_qq_groups
    whitelisted_qq_groups = await connection.get_whitelist()
    for supergroup in infinity.supergroups:
        await add_whitelist_qq_group(int(supergroup))


async def read_banned_from_mongo():
    global banned_qq_users
    banned_qq_users = await connection.get_blacklist()


async def update_whitelist_and_banned_list():
    """需要在初始化时调用"""
    await read_whitelist_from_mongo()
    await read_banned_from_mongo()
    for supergroup in infinity.supergroups:
        await add_whitelist_qq_group(int(supergroup))
