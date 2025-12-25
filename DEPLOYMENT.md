# WhereEatAI 部署指南

本文档提供详细的部署说明，包括开发环境、测试环境和生产环境的部署方式。

## 目录

- [环境要求](#环境要求)
- [开发环境部署](#开发环境部署)
- [Docker部署](#docker部署)
- [生产环境部署](#生产环境部署)
- [配置说明](#配置说明)
- [监控与日志](#监控与日志)
- [故障排查](#故障排查)

## 环境要求

### 基础要求
- **Python**: 3.10 或更高版本
- **操作系统**: Linux/macOS/Windows
- **内存**: 最低 2GB，推荐 4GB+
- **磁盘**: 最低 5GB 可用空间

### 可选要求
- **Docker**: 20.10+ (用于容器化部署)
- **Docker Compose**: 1.29+ (用于多容器编排)
- **Nginx**: 1.20+ (用于反向代理)
- **Redis**: 7.0+ (用于缓存，可选)

## 开发环境部署

### 1. 克隆项目

```bash
git clone <repository-url>
cd whereeatai
```

### 2. 创建虚拟环境

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 配置环境变量

复制环境变量模板并编辑：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的硅基流动API密钥：

```env
API_KEY=your_siliconflow_api_key_here
MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 5. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

访问 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker部署

### 方式一：使用Docker Compose（推荐）

1. **配置环境变量**

编辑 `.env` 文件：

```env
API_KEY=your_api_key
ENVIRONMENT=production
LOG_LEVEL=INFO
```

2. **启动所有服务**

```bash
docker-compose up -d
```

这将启动以下服务：
- WhereEatAI API (端口 8000)
- Redis缓存 (端口 6379)
- Nginx反向代理 (端口 80/443)

3. **查看日志**

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看API服务日志
docker-compose logs -f whereeatai-api

# 查看Nginx日志
docker-compose logs -f nginx
```

4. **停止服务**

```bash
docker-compose down
```

5. **重启服务**

```bash
docker-compose restart whereeatai-api
```

### 方式二：仅使用Docker

1. **构建镜像**

```bash
docker build -t whereeatai:latest .
```

2. **运行容器**

```bash
docker run -d \
  --name whereeatai-api \
  -p 8000:8000 \
  -e API_KEY=your_api_key \
  -e ENVIRONMENT=production \
  -v $(pwd)/logs:/app/logs \
  whereeatai:latest
```

3. **查看日志**

```bash
docker logs -f whereeatai-api
```

## 生产环境部署

### 架构建议

```
Internet
    │
    ↓
[负载均衡器] (Nginx/HAProxy)
    │
    ├── [API实例1] (Docker)
    ├── [API实例2] (Docker)
    └── [API实例3] (Docker)
         │
         ├── [Redis缓存]
         └── [日志收集]
```

### 1. 使用Systemd管理服务（Linux）

创建服务文件 `/etc/systemd/system/whereeatai.service`：

```ini
[Unit]
Description=WhereEatAI API Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/whereeatai
Environment="PATH=/opt/whereeatai/venv/bin"
ExecStart=/opt/whereeatai/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable whereeatai
sudo systemctl start whereeatai
sudo systemctl status whereeatai
```

### 2. 使用Nginx反向代理

编辑 `/etc/nginx/sites-available/whereeatai`：

```nginx
upstream whereeatai_backend {
    server 127.0.0.1:8000;
    # 添加更多实例以实现负载均衡
    # server 127.0.0.1:8001;
    # server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://whereeatai_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/whereeatai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. HTTPS配置

使用Let's Encrypt免费证书：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 4. 多实例部署

编辑 `docker-compose.yml` 扩展实例数量：

```yaml
services:
  whereeatai-api:
    deploy:
      replicas: 3
```

或使用Docker Swarm/Kubernetes进行容器编排。

## 配置说明

### 环境变量详解

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `API_KEY` | 硅基流动API密钥 | - | ✓ |
| `BASE_URL` | 模型API基础URL | https://api.siliconflow.cn/v1 | × |
| `MODEL_NAME` | 使用的模型名称 | Qwen/Qwen2.5-7B-Instruct | × |
| `API_HOST` | 服务监听地址 | 0.0.0.0 | × |
| `API_PORT` | 服务监听端口 | 8000 | × |
| `API_WORKERS` | 工作进程数 | 4 | × |
| `LOG_LEVEL` | 日志级别 | INFO | × |
| `ENVIRONMENT` | 运行环境 | development | × |
| `RATE_LIMIT_CALLS` | 限流请求数 | 100 | × |
| `RATE_LIMIT_PERIOD` | 限流时间窗口(秒) | 60 | × |

### 性能优化配置

**生产环境推荐配置** (`.env`):

```env
# 环境
ENVIRONMENT=production

# 工作进程
API_WORKERS=4

# 日志
LOG_LEVEL=WARNING
LOG_JSON=true

# 缓存
CACHE_ENABLED=true
CACHE_TTL=3600

# 限流
RATE_LIMIT_CALLS=1000
RATE_LIMIT_PERIOD=60

# 超时
MAX_TIMEOUT=120
```

## 监控与日志

### 日志管理

**日志位置**:
- 应用日志: `logs/whereeatai.log`
- 错误日志: `logs/error.log`

**日志轮转**:
- 默认单个文件最大 10MB
- 保留最近 5 个备份文件

**查看实时日志**:

```bash
# 开发环境
tail -f logs/whereeatai.log

# Docker环境
docker-compose logs -f whereeatai-api

# 生产环境
journalctl -u whereeatai -f
```

### 健康检查

**API端点**:

```bash
# 基础健康检查
curl http://localhost:8000/status

# 详细信息
curl http://localhost:8000/
```

**Docker健康检查**:

容器自动执行健康检查，可查看状态：

```bash
docker inspect --format='{{.State.Health.Status}}' whereeatai-api
```

### 性能监控

访问以下端点获取系统信息：

```bash
# Agent列表
curl http://localhost:8000/agents

# API文档
http://localhost:8000/docs
```

## 故障排查

### 常见问题

#### 1. 服务启动失败

**检查日志**:
```bash
docker-compose logs whereeatai-api
```

**可能原因**:
- API_KEY未配置或无效
- 端口被占用
- 依赖未安装

**解决方案**:
```bash
# 检查端口
netstat -tunlp | grep 8000

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

#### 2. Agent执行失败

**检查**:
- 模型API配置是否正确
- 网络连接是否正常
- API密钥是否有效

**测试连接**:
```bash
curl -H "Authorization: Bearer $API_KEY" \
  https://api.siliconflow.cn/v1/models
```

#### 3. 内存不足

**调整配置**:
```env
# 减少工作进程数
API_WORKERS=2

# 限制并发
RATE_LIMIT_CALLS=50
```

#### 4. 响应超时

**调整超时配置**:
```env
MAX_TIMEOUT=300
```

**Nginx配置**:
```nginx
proxy_connect_timeout 300s;
proxy_send_timeout 300s;
proxy_read_timeout 300s;
```

### 性能调优

**1. 启用缓存**:
```env
CACHE_ENABLED=true
REDIS_URL=redis://localhost:6379/0
```

**2. 水平扩展**:
```bash
docker-compose up -d --scale whereeatai-api=3
```

**3. 数据库连接池** (如需要):
```env
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
```

### 获取支持

如遇到问题，请提供以下信息：

1. 错误日志
2. 环境配置
3. 复现步骤
4. 系统信息

```bash
# 导出日志
docker-compose logs whereeatai-api > debug.log

# 系统信息
uname -a
docker --version
docker-compose --version
```

## 安全建议

1. **不要在公共仓库提交 `.env` 文件**
2. **使用HTTPS加密传输**
3. **定期更新依赖包**
4. **限制API访问频率**
5. **使用防火墙限制访问**
6. **定期备份日志和数据**

## 更新部署

### 滚动更新

```bash
# 拉取最新代码
git pull

# 重新构建镜像
docker-compose build

# 滚动更新
docker-compose up -d --no-deps --build whereeatai-api
```

### 零停机部署

使用多实例 + 负载均衡器实现零停机：

1. 启动新版本实例
2. 从负载均衡器移除旧实例
3. 等待旧实例请求处理完成
4. 停止旧实例
5. 将新实例加入负载均衡器

---

更多信息请参考 [ARCHITECTURE.md](ARCHITECTURE.md)
