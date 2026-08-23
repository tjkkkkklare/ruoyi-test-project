"""基于 requests 的 RuoYi 接口客户端。

职责：登录、token 缓存、鉴权头注入，提供 get/post/put/delete 便捷方法。
所有用例通过 conftest 里的 session 级 fixtures 拿到已登录的 client，无需重复登录。
"""
import requests
import config


class RuoYiClient:
    def __init__(self, base_url=None):
        self.base_url = base_url or config.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.token = None

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        return self.session.request(method, url, **kwargs)

    def login(self, username=None, password=None):
        """登录并缓存 token。RuoYi 成功返回 code=200 + token；失败 code=500。"""
        data = {
            "username": config.USERNAME if username is None else username,
            "password": config.PASSWORD if password is None else password,
        }
        resp = self.request("POST", config.LOGIN_PATH, json=data)
        body = resp.json()
        if body.get("code") == config.CODE_SUCCESS and body.get("token"):
            self.token = body["token"]
            self.session.headers[config.TOKEN_HEADER] = config.TOKEN_PREFIX + self.token
        return resp

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, json=None, **kwargs):
        return self.request("POST", path, json=json, **kwargs)

    def put(self, path, json=None, **kwargs):
        return self.request("PUT", path, json=json, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)
