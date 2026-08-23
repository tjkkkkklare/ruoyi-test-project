# 被测环境配置 —— RuoYi 后端（本项目自动化测试的统一配置入口）
# 所有用例从这里取地址 / 账号 / 鉴权方式，改环境只改这一个文件
BASE_URL = "http://localhost:8080"   # RuoYi 后端地址（前端 /dev-api 代理到这里）

USERNAME = "admin"                    # 默认管理员账号
PASSWORD = "admin123"

TOKEN_HEADER = "Authorization"        # RuoYi 鉴权请求头（登录后须携带）
TOKEN_PREFIX = "Bearer "              # RuoYi token 前缀
LOGIN_PATH = "/login"                 # 登录接口路径

# 断言参考：RuoYi 返回的业务 code（HTTP 状态恒为 200）
CODE_SUCCESS = 200
CODE_ERROR = 500
