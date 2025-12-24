"""应用主入口，用于启动API服务"""
import uvicorn
from whereeatai.config import API_HOST, API_PORT, PROJECT_NAME, VERSION
from whereeatai.api.main import app


if __name__ == "__main__":
    """启动API服务"""
    print(f"Starting {PROJECT_NAME} API Server...")
    print(f"Version: {VERSION}")
    print(f"Host: {API_HOST}")
    print(f"Port: {API_PORT}")
    print(f"Docs: http://{API_HOST}:{API_PORT}/docs")
    print("\nPress Ctrl+C to stop the server.")
    
    uvicorn.run(
        "whereeatai.api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True
    )
