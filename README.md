# WhereEatAI - 智能旅游推荐系统

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**基于多Agent协作的智能旅游规划与美食推荐系统**

[快速开始](#快速开始) • [功能特性](#功能特性) • [技术架构](#技术架构) • [API文档](#api文档) • [部署指南](#部署指南)

</div>

---

## 📖 项目简介

WhereEatAI 是一个创新的智能旅游推荐系统，采用多Agent协作架构，结合LangChain和LangGraph技术，基于硅基流动的千问大模型，为用户提供智能化、个性化的旅游规划服务。

### 核心优势

- 🤖 **多Agent协作**: 8个专业Agent分工协作，提供全方位旅游服务
- 🔄 **动态编排**: 基于LangGraph的工作流引擎，智能调度Agent执行
- 🌐 **A2A协议**: 标准化Agent间通信，支持能力发现和注册
- 🚀 **生产就绪**: 完善的日志、监控、限流机制，支持Docker部署
- 📱 **RESTful API**: 标准化API接口，易于集成到移动应用

## ✨ 功能特性

### 智能服务

| 功能 | 描述 | Agent |
|------|------|-------|
| 🎯 **智能游记生成** | 基于目的地和兴趣生成个性化游记 | TravelogueAgent |
| 📅 **动态行程规划** | 实时调整的智能行程安排 | ItineraryAgent |
| 🍽️ **美食推荐** | 基于位置和偏好的餐厅推荐 | FoodRecommendationAgent |
| 💰 **价格比价** | 跨平台酒店、门票价格对比 | PriceComparisonAgent |
| 📝 **小红书识别** | 提取小红书旅游笔记信息 | XiaoHongShuAgent |
| 🎬 **视频分析** | 分析旅游视频内容 | VideoAgent |
| 🏷️ **专题推荐** | 主题化旅游推荐 | TopicRecommendationAgent |
| 🗺️ **完整旅行计划** | 包含美食、酒店、路线的综合方案 | TravelPlanAgent |

### 技术特性

- ✅ **LangGraph工作流**: 复杂任务自动编排
- ✅ **A2A Agent协议**: 标准化通信与能力注册
- ✅ **请求日志**: 完整的请求追踪
- ✅ **智能限流**: 防止API滥用
- ✅ **健康检查**: 服务状态监控
- ✅ **Docker支持**: 容器化部署
- ✅ **CORS配置**: 跨域请求支持

## 🏗️ 技术架构

### 技术栈

```
┌─────────────────────────────────────┐
│          应用层 (FastAPI)            │
├─────────────────────────────────────┤
│      编排层 (LangGraph)              │
│  ┌──────────┐  ┌──────────┐        │
│  │ Workflow │  │ Workflow │  ...   │
│  └──────────┘  └──────────┘        │
├─────────────────────────────────────┤
│       Agent层 (A2A Protocol)        │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐      │
│  │游记│ │行程│ │美食│ │价格│ ...  │
│  └────┘ └────┘ └────┘ └────┘      │
├─────────────────────────────────────┤
│      模型层 (Qwen via 硅基流动)      │
└─────────────────────────────────────┘
```

### 核心组件

- **LangChain**: Agent基础能力构建
- **LangGraph**: 工作流图编排
- **FastAPI**: 高性能Web框架
- **Pydantic**: 数据验证
- **Qwen模型**: 硅基流动提供的大语言模型

详细架构请参考 [ARCHITECTURE.md](ARCHITECTURE.md)

## 🚀 快速开始

### 前置要求

- Python 3.10+
- pip
- 硅基流动API密钥 ([获取地址](https://siliconflow.cn))

### 安装步骤

1. **克隆项目**

```bash
git clone <repository-url>
cd whereeatai
```

2. **创建虚拟环境**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置环境变量**

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API密钥：

```env
API_KEY=your_siliconflow_api_key_here
```

5. **启动服务**

```bash
python main.py
```

6. **访问API文档**

打开浏览器访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📚 API文档

### 基础端点

#### 健康检查

```http
GET /status
```

**响应示例**:
```json
{
  "status": "running",
  "message": "WhereEatAI API is running normally",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2024-01-01T00:00:00"
}
```

#### 获取Agent列表

```http
GET /agents
```

### 核心功能端点

#### 1. 生成旅行计划

```http
POST /travel-plan
```

**请求体**:
```json
{
  "destination": "北京",
  "duration": "3天2夜",
  "interests": ["历史文化", "美食", "摄影"],
  "budget": "中等",
  "travel_dates": "2024-05-01",
  "travel_style": "休闲"
}
```

#### 2. 美食推荐

```http
POST /food-recommendation
```

**请求体**:
```json
{
  "location": "北京",
  "cuisine_type": "北京菜",
  "budget": "中等"
}
```

#### 3. 生成游记

```http
POST /travelogue
```

#### 4. 行程规划

```http
POST /itinerary
```

#### 5. 价格比价

```http
POST /price-comparison
```

#### 6. 小红书分析

```http
POST /xiaohongshu-analysis
```

#### 7. 视频分析

```http
POST /video-analysis
```

#### 8. 专题推荐

```http
POST /topic-recommendation
```

完整API文档请访问 `/docs` 端点。

## 🐳 Docker部署

### 快速启动

```bash
# 使用Docker Compose
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 仅使用Docker

```bash
# 构建镜像
docker build -t whereeatai:latest .

# 运行容器
docker run -d \
  --name whereeatai-api \
  -p 8000:8000 \
  -e API_KEY=your_api_key \
  whereeatai:latest
```

详细部署指南请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

## 📁 项目结构

```
whereeatai/
├── whereeatai/              # 主应用包
│   ├── agents/             # Agent实现
│   │   ├── base_agent.py
│   │   ├── travelogue_agent.py
│   │   ├── itinerary_agent.py
│   │   └── ...
│   ├── api/                # API接口
│   │   └── main.py
│   ├── graphs/             # LangGraph工作流
│   │   └── travel_workflow.py
│   ├── protocols/          # A2A协议
│   │   └── a2a_protocol.py
│   ├── middleware/         # 中间件
│   │   └── request_middleware.py
│   ├── models/             # 模型集成
│   │   └── qwen_model.py
│   ├── utils/              # 工具函数
│   │   └── logger.py
│   └── config.py           # 配置管理
├── logs/                   # 日志目录
├── Dockerfile              # Docker配置
├── docker-compose.yml      # Docker Compose配置
├── nginx.conf              # Nginx配置
├── requirements.txt        # Python依赖
├── .env.example            # 环境变量模板
├── main.py                 # 应用入口
├── ARCHITECTURE.md         # 架构文档
├── DEPLOYMENT.md           # 部署文档
└── README.md               # 项目说明
```

## 🔧 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `API_KEY` | 硅基流动API密钥 | 必填 |
| `MODEL_NAME` | 模型名称 | Qwen/Qwen2.5-7B-Instruct |
| `API_PORT` | 服务端口 | 8000 |
| `LOG_LEVEL` | 日志级别 | INFO |
| `ENVIRONMENT` | 运行环境 | development |

完整配置请参考 `.env.example`

## 🧪 开发指南

### 添加新Agent

1. 在 `whereeatai/agents/` 创建新Agent文件
2. 继承 `BaseAgent` 类
3. 实现 `execute()` 和 `get_capabilities()` 方法
4. 在 `AgentManager` 中注册

示例:

```python
from whereeatai.agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MyAgent",
            description="我的Agent",
            agent_id="my_agent"
        )
    
    def get_capabilities(self):
        return [...]
    
    def execute(self, input_data):
        # 实现业务逻辑
        pass
```

### 运行测试

```bash
pytest tests/ -v
```

### 代码格式化

```bash
black whereeatai/
isort whereeatai/
```

## 📊 性能优化

- **并发处理**: 支持多Worker模式
- **请求限流**: 防止API滥用
- **缓存机制**: Redis缓存支持(可选)
- **连接池**: 模型API连接复用

## 🔒 安全性

- ✅ HTTPS传输加密
- ✅ API密钥认证
- ✅ 请求限流保护
- ✅ CORS配置
- ✅ 输入验证

## 📝 更新日志

### v1.0.0 (2024-12-24)

- ✨ 初始版本发布
- ✨ 8个核心Agent实现
- ✨ LangGraph工作流编排
- ✨ A2A协议支持
- ✨ Docker部署支持
- ✨ 完整的日志和监控

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - Agent框架
- [LangGraph](https://github.com/langchain-ai/langgraph) - 工作流编排
- [FastAPI](https://github.com/tiangolo/fastapi) - Web框架
- [硅基流动](https://siliconflow.cn) - AI模型服务

## 📞 联系方式

- 项目主页: [GitHub](https://github.com/your-username/whereeatai)
- 问题反馈: [Issues](https://github.com/your-username/whereeatai/issues)
- 邮箱: your-email@example.com

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个星标支持！⭐**

Made with ❤️ by WhereEatAI Team

</div>
