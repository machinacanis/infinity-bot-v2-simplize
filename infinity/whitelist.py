import json
import os

import infinity

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
            # noinspection PyTypeChecker
            json.dump([], f)
    with open("whitelist_qq_groups.json", "r") as f:
        whitelisted_qq_groups = json.load(f)

def read_banned_qq_users_from_json():
    global banned_qq_users
    if not os.path.exists("banned_qq_users.json"):
        with open("banned_qq_users.json", "w") as f:
            # noinspection PyTypeChecker
            json.dump([], f)
    with open("banned_qq_users.json", "r") as f:
        banned_qq_users = json.load(f)

def add_whitelist_qq_group(qq_group: int):
    if qq_group not in whitelisted_qq_groups:
        whitelisted_qq_groups.append(qq_group)
        write_whitelist_qq_groups_into_json()

def remove_whitelist_qq_group(qq_group: int):
    if qq_group in whitelisted_qq_groups:
        whitelisted_qq_groups.remove(qq_group)
        write_whitelist_qq_groups_into_json()

def add_banned_qq_user(qq_user: int):
    if qq_user not in banned_qq_users:
        banned_qq_users.append(qq_user)
        write_banned_qq_users_into_json()

def remove_banned_qq_user(qq_user: int):
    if qq_user in banned_qq_users:
        banned_qq_users.remove(qq_user)
        write_banned_qq_users_into_json()

def update_whitelist_and_banned_list():
    """需要在初始化时调用"""
    read_whitelist_qq_groups_from_json()
    read_banned_qq_users_from_json()
    for supergroup in infinity.supergroups:
        add_whitelist_qq_group(int(supergroup))