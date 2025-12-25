"""请求中间件"""
import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        # 生成请求ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # 记录请求开始
        start_time = time.time()
        logger.info(
            f"请求开始 - ID: {request_id}, 方法: {request.method}, 路径: {request.url.path}"
        )
        
        # 处理请求
        try:
            response = await call_next(request)
            
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 添加自定义响应头
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            
            # 记录请求完成
            logger.info(
                f"请求完成 - ID: {request_id}, 状态码: {response.status_code}, "
                f"耗时: {process_time:.3f}秒"
            )
            
            return response
        except Exception as e:
            # 记录错误
            logger.error(
                f"请求失败 - ID: {request_id}, 错误: {str(e)}",
                exc_info=True
            )
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """简单的限流中间件"""
    
    def __init__(self, app: ASGIApp, calls: int = 100, period: int = 60):
        """
        初始化限流中间件
        
        Args:
            app: ASGI应用
            calls: 时间窗口内允许的请求数
            period: 时间窗口(秒)
        """
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.requests = {}  # {ip: [(timestamp, ...)]}
    
    async def dispatch(self, request: Request, call_next):
        # 获取客户端IP
        client_ip = request.client.host
        current_time = time.time()
        
        # 清理过期记录
        if client_ip in self.requests:
            self.requests[client_ip] = [
                t for t in self.requests[client_ip]
                if current_time - t < self.period
            ]
        
        # 检查是否超过限制
        if client_ip in self.requests and len(self.requests[client_ip]) >= self.calls:
            logger.warning(f"限流触发 - IP: {client_ip}")
            return Response(
                content="Too many requests",
                status_code=429,
                headers={"Retry-After": str(self.period)}
            )
        
        # 记录请求
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip].append(current_time)
        
        # 继续处理
        response = await call_next(request)
        return response
