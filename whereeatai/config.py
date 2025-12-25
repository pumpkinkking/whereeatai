"""配置文件，用于管理硅基流动模型的API密钥等配置信息"""
import os
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
load_dotenv()

# 硅基流动模型配置
API_KEY = os.getenv("API_KEY", "")
BASE_URL = os.getenv("BASE_URL", "https://api.siliconflow.cn/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")

# API服务配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_WORKERS = int(os.getenv("API_WORKERS", "4"))

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.getenv("LOG_FILE", "whereeatai.log")
LOG_JSON = os.getenv("LOG_JSON", "false").lower() == "true"

# 限流配置
RATE_LIMIT_CALLS = int(os.getenv("RATE_LIMIT_CALLS", "100"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))

# 性能配置
MAX_TIMEOUT = int(os.getenv("MAX_TIMEOUT", "120"))  # 最大超时时间(秒)
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "false").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 缓存过期时间(秒)

# 安全配置
API_KEY_HEADER = os.getenv("API_KEY_HEADER", "X-API-Key")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# 项目信息
PROJECT_NAME = "WhereEatAI"
VERSION = "1.0.0"
DESCRIPTION = "智能旅行规划与美食推荐API，基于多Agent协作"

# 环境
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, staging, production

# 数据库配置(预留)
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Redis配置(预留)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 监控配置
MONITORING_ENABLED = os.getenv("MONITORING_ENABLED", "false").lower() == "true"
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9090"))
