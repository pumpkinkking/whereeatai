"""配置文件，用于管理硅基流动模型的API密钥等配置信息"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 硅基流动模型配置
API_KEY = os.getenv("API_KEY", "")
BASE_URL = os.getenv("BASE_URL", "https://api.siliconflow.cn/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen3-8B")

# API服务配置
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# 项目信息
PROJECT_NAME = "WhereEatAI"
VERSION = "1.0.0"
