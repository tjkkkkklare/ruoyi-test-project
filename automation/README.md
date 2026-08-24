# RuoYi-Vue 接口自动化测试（Python + pytest + requests）

## 项目简介

基于 **Python + pytest + requests** 搭建的 RuoYi-Vue 后台接口自动化测试框架。
覆盖登录、用户管理、边界/异常参数等核心接口，实现**一次登录复用（session 级 token 管理）、参数化数据驱动、异常自动捕获、Allure可视化报告**。
用于沉淀 RuoYi 项目的接口测试能力，也作为接口自动化实战的作品。

## 技术栈

- Python 3.14（含虚拟环境 `.venv`）
- pytest（测试框架）
- requests（HTTP 请求）
- allure 2.45.0

## 目录结构

```
automation/
├── config.py            # 环境/账号/鉴权配置（改环境只改这里）
├── api_client.py        # requests 封装：登录、token 缓存、鉴权头注入
├── conftest.py          # session 级 fixture：整个测试过程只登录一次
├── test_login.py        # 登录模块（含参数化：正常/密码错误/空用户名/空密码）
├── test_user.py         # 用户管理（列表/模糊查询/分页/数据一致性/增删改查）
├── test_boundary.py     # 边界/异常参数（记录 BUG-001：pageSize 无边界校验）
├── pytest.ini           # pytest 配置（报告输出、收集规则）
├── requirements.txt     # 依赖
└── allure-report        # allure报告
```

## 如何运行

前置：后端 RuoYi 已启动（`http://localhost:8080`），并已关闭验证码（`sys_config.sys.account.captchaEnabled=false`）。

安装依赖

```bash
pip install -r requirements.txt

执行测试
cd automation
pytest --alluredir=allure-results --clean-alluredir

生成allure报告
allure generate allure-results -o allure-report --clean

## 结果示例

```
14 passed, 3 xfailed  in 1.52s
```

- `passed`：正常功能用例（登录、用户管理、增删改查、数据一致性）
- `xfailed`：**已记录的真实缺陷（预期失败）** —— BUG-001 用户列表接口 `pageSize` 缺少边界校验（`-1` / `999999` 均返回 200，未做参数校验；超大值一次拉取全量数据）。用 `xfail` 标记，既保留缺陷证据，又不会产生失败红灯。

## 测试点说明

| 模块 | 用例 | 说明 |
|---|---|---|
| 登录 | 正常 / 密码错误 / 空用户名 / 空密码 / 参数化 | 验证 `code=200` 与 token 返回、`code=500` 异常拦截 |
| 用户 | 列表 / 模糊查询 / 分页 / 数据一致性 / 增删改查 | 校验分页、数据唯一性、完整 CRUD 闭环 |
| 边界 | pageSize=0/-1/999999、pageNum=0/负数 | 发现并记录 BUG-001：分页参数缺少边界校验 |

## 数据一致性与数据库校验

本自动化聚焦**接口层**校验；更深层的**数据库一致性校验**（MySQL 多表联查 + 聚合，比对页面值 vs 库表）见项目 `05_测试报告` 与 `03_缺陷管理` 文档。
