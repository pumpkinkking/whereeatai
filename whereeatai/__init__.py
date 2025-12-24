"""智能旅行规划与美食推荐系统"""

__version__ = "1.0.0"
__author__ = "WhereEatAI Team"
__description__ = "智能旅行规划与美食推荐系统，基于多Agent协作"

from .config import *
from .models.qwen_model import QwenModel

__all__ = [
    "QwenModel",
    "API_KEY",
    "BASE_URL",
    "MODEL_NAME",
    "API_HOST",
    "API_PORT",
    "LOG_LEVEL",
    "PROJECT_NAME",
    "VERSION"
]
