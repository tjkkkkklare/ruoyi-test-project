"""用户管理模块接口自动化用例：列表 / 模糊查询 / 分页 / 数据一致性 / 增删改查。"""
import random
import string

from api_client import RuoYiClient

USER_LIST = "/system/user/list"


def test_user_list_returns_data(client):
    body = client.get(USER_LIST, params={"pageNum": 1, "pageSize": 10}).json()
    assert body.get("code") == 200
    assert body.get("total", 0) >= 1
    assert isinstance(body.get("rows"), list) and len(body["rows"]) > 0


def test_user_list_filter_by_keyword(client):
    """按用户名模糊查询，返回结果应都包含关键字。"""
    body = client.get(USER_LIST, params={"pageNum": 1, "pageSize": 10, "userName": "admin"}).json()
    assert body.get("code") == 200
    rows = body.get("rows", [])
    assert rows, "按 admin 模糊查询应返回数据"
    for row in rows:
        assert "admin" in (row.get("userName") or "").lower()


def test_user_pagination_respected(client):
    """pageSize=3 时，单页最多返回 3 条。"""
    body = client.get(USER_LIST, params={"pageNum": 1, "pageSize": 3}).json()
    assert body.get("code") == 200
    assert len(body.get("rows", [])) <= 3


def test_user_data_consistency(client):
    """数据一致性（接口层）：rows 内 userId 不允许重复。"""
    body = client.get(USER_LIST, params={"pageNum": 1, "pageSize": 50}).json()
    assert body.get("code") == 200
    ids = [r.get("userId") for r in body.get("rows", [])]
    assert len(ids) == len(set(ids)), "用户列表存在重复 userId"


def test_create_update_delete_user(client):
    """核心增删改查：创建 -> 校验存在 -> 修改状态 -> 删除 -> 校验不存在。"""
    username = "auto_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    # 1. 创建
    create_body = client.post("/system/user", json={
        "userName": username,
        "nickName": "自动化测试用户",
        "password": "123456",
        "deptId": 103,
        "status": "0",
        "roleIds": [2],
    }).json()
    assert create_body.get("code") == 200, f"创建用户失败: {create_body}"

    # 2. 查询确认存在
    q = client.get(USER_LIST, params={"pageNum": 1, "pageSize": 10, "userName": username}).json()
    match = [r for r in q.get("rows", []) if r.get("userName") == username]
    assert match, "创建后未查询到该用户"
    uid = match[0]["userId"]

    # 3. 修改状态
    update_body = client.put("/system/user", json={
        "userId": uid, "userName": username, "nickName": "自动化测试用户", "status": "1", "deptId": 103,
    }).json()
    assert update_body.get("code") == 200, f"修改用户失败: {update_body}"

    # 4. 删除（逻辑删除）
    delete_body = client.delete(f"/system/user/{uid}").json()
    assert delete_body.get("code") == 200, f"删除用户失败: {delete_body}"

    # 5. 删除后查询不存在
    q2 = client.get(USER_LIST, params={"pageNum": 1, "pageSize": 10, "userName": username}).json()
    assert not any(r.get("userName") == username for r in q2.get("rows", [])), "删除后仍能查到该用户"
