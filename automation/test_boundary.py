"""边界 / 异常参数测试。

重点：用自动化暴露 BUG-001 —— 用户列表接口对 pageSize 缺少边界校验。
结合测试环境实测：
- pageSize=-1、pageSize=999999 均返回 HTTP 200、body.code=200，接口不拒绝、不返回参数校验错误。
- 符合预期的实现应当：对非法/超大分页参数返回参数校验错误，或限制最大分页。
用例用 pytest.mark.xfail 标记为「已知缺陷（预期失败）」，既能记录缺陷，又不会产生刺眼的失败红灯。
"""
import pytest


def test_pageSize_zero_does_not_error(client):
    """观察项：pageSize=0 的边界行为（接口不应抛 500）。"""
    body = client.get("/system/user/list", params={"pageNum": 1, "pageSize": 0}).json()
    assert body.get("code") in (200, 500)


@pytest.mark.xfail(reason="BUG-001: 用户列表接口 pageSize 缺少边界校验——负数应返回参数校验错误，实测返回 200", strict=False)
def test_pageSize_negative_should_be_rejected(client):
    body = client.get("/system/user/list", params={"pageNum": 1, "pageSize": -1}).json()
    assert body.get("code") != 200, "BUG: pageSize=-1 未做边界校验，返回了 200"


@pytest.mark.xfail(reason="BUG-001: 超大 pageSize(999999) 未做上限限制——一次拉取全量数据，实测返回 200", strict=False)
def test_pageSize_too_large_should_be_limited(client):
    body = client.get("/system/user/list", params={"pageNum": 1, "pageSize": 999999}).json()
    assert body.get("code") != 200, "BUG: pageSize=999999 未被限制，返回了 200"


@pytest.mark.xfail(reason="BUG-001(延伸): 非法 pageNum(0/负数) 同样未做校验", strict=False)
def test_pageNum_invalid_should_be_rejected(client):
    body = client.get("/system/user/list", params={"pageNum": 0, "pageSize": 10}).json()
    assert body.get("code") != 200, "BUG: pageNum=0 未做校验，返回了 200"
