"""登录模块接口自动化用例。

RuoYi 登录约定：
- 成功 -> HTTP 200，body.code=200，body.token 非空
- 失败（密码错误/账号不存在/空参数）-> HTTP 200，body.code=500，无 token
"""
import pytest


def test_login_success_returns_token(client):
    body = client.login("admin", "admin123").json()
    assert body.get("code") == 200, f"登录应成功: {body}"
    assert body.get("token"), "登录成功但未返回 token"


def test_login_wrong_password(client):
    body = client.login("admin", "wrong_password").json()
    assert body.get("code") == 500, "错误密码应被拦截"
    assert not body.get("token"), "错误密码不应返回 token"


def test_login_empty_username(client):
    body = client.login("", "admin123").json()
    assert body.get("code") == 500


def test_login_empty_password(client):
    body = client.login("admin", "").json()
    assert body.get("code") == 500


@pytest.mark.parametrize("username,password,expect_code", [
    ("admin", "admin123", 200),      # 正常登录
    ("admin", "wrongpwd", 500),      # 密码错误
    ("", "admin123", 500),           # 空用户名
    ("admin", "", 500),              # 空密码
])
def test_login_parametrized(client, username, password, expect_code):
    """数据驱动：一组参数一次覆盖四类场景。"""
    body = client.login(username, password).json()
    assert body.get("code") == expect_code, f"{username}/{password} 应返回 code={expect_code}，实际 {body.get('code')}"
    if expect_code == 200:
        assert body.get("token")
