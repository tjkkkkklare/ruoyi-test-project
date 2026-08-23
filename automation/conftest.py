"""pytest 全局 fixtures：整个测试会话复用一次登录，避免重复登录与 token 泄漏。"""
import pytest
from api_client import RuoYiClient


@pytest.fixture(scope="session")
def client():
    """已登录的接口客户端（session 级：整个测试过程只登录一次）。"""
    c = RuoYiClient()
    resp = c.login()
    body = resp.json()
    assert body.get("code") == 200 and c.token, f"登录失败，请检查后端是否启动/账号是否正确: {resp.text}"
    return c


@pytest.fixture(scope="session")
def admin_token(client):
    """当前登录 token，供需要手工拼请求头的用例使用。"""
    return client.token
