"""应用主入口，用于启动API服务"""
import uvicorn
from whereeatai.config import (
    API_HOST, 
    API_PORT, 
    API_WORKERS,
    PROJECT_NAME, 
    VERSION,
    LOG_LEVEL,
    LOG_DIR,
    LOG_FILE,
    LOG_JSON,
    ENVIRONMENT
)
from whereeatai.utils.logger import setup_logging
import logging

# 配置日志
setup_logging(
    log_level=LOG_LEVEL,
    log_file=LOG_FILE,
    log_dir=LOG_DIR,
    use_json=LOG_JSON
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    """启动API服务"""
    logger.info(f"Starting {PROJECT_NAME} API Server...")
    logger.info(f"Version: {VERSION}")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Host: {API_HOST}")
    logger.info(f"Port: {API_PORT}")
    logger.info(f"Workers: {API_WORKERS}")
    logger.info(f"Log Level: {LOG_LEVEL}")
    logger.info(f"Docs: http://{API_HOST}:{API_PORT}/docs")
    logger.info("Press Ctrl+C to stop the server.")
    
    try:
        uvicorn.run(
            "whereeatai.api.main:app",
            host=API_HOST,
            port=API_PORT,
            reload=(ENVIRONMENT == "development"),
            workers=1 if ENVIRONMENT == "development" else API_WORKERS,
            log_level=LOG_LEVEL.lower(),
            access_log=True
        )
    except Exception as e:
        logger.error(f"服务启动失败: {str(e)}", exc_info=True)
        raise
