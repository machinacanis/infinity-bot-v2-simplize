import httpx
from httpx import Response

import infinity


class DivingFishClient:
    def __init__(self, import_token: str = ""):
        self.uri = infinity.df_api
        self.developer_token = infinity.df_token
        self.import_token = import_token
        self.is_agree = False

    async def get(self, data_type: str, endpoint: str) -> Response:
        headers = {"Developer-Token": self.developer_token}
        if self.import_token:
            headers["Import-Token"] = self.import_token
        async with httpx.AsyncClient() as c:
            print(self.uri + data_type + endpoint)
            resp = await c.get(self.uri + data_type + endpoint, headers=headers)
            return resp

    async def post(self, data_type: str, endpoint: str, data: dict) -> Response:
        headers = {"Developer-Token": self.developer_token}
        if self.import_token:
            headers["Import-Token"] = self.import_token
        async with httpx.AsyncClient() as c:
            resp = await c.post(
                self.uri + data_type + endpoint, headers=headers, json=data
            )
            return resp

    async def get_agreement(self) -> bool:
        if not self.is_agree:
            resp = await self.get("maimaidxprober", "/player/agreement")
            if resp.status_code == 200 and resp.json().get("message", "") == "success":
                self.is_agree = True
        return self.is_agree

    async def query_user_plate(
        self, qq: int | str = "", username: str = "", version: str | list[str] = ""
    ):
        # qq和username至少有一个，version可以为空，如果为空则查询全部版本
        if not qq and not username:
            return None
        data = {}
        if qq:
            data["qq"] = str(qq)
        if username:
            data["username"] = username
        if version:
            data["version"] = version if isinstance(version, list) else [version]
        resp = await self.post("maimaidxprober", "/player/plate", data)
        return resp


class LxnsClient:
    def __init__(self, user_token: str = ""):
        self.uri = infinity.lx_api
        self.developer_token = infinity.lx_token
        self.user_token = user_token

    async def get(self, endpoint: str) -> Response:
        headers = {"Authorization": self.developer_token}
        if self.user_token:
            headers["X-User-Token"] = self.user_token
        async with httpx.AsyncClient() as c:
            resp = await c.get(self.uri + endpoint, headers=headers)
            return resp

    async def post(self, endpoint: str, data: dict) -> Response:
        headers = {"Authorization": self.developer_token}
        if self.user_token:
            headers["X-User-Token"] = self.user_token
        async with httpx.AsyncClient() as c:
            resp = await c.post(self.uri + endpoint, headers=headers, json=data)
            return resp
