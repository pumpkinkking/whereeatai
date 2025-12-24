"""API服务主入口"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from whereeatai.agents.agent_manager import AgentManager

# 创建Agent管理器实例
agent_manager = AgentManager()

# 创建FastAPI应用
app = FastAPI(
    title="WhereEatAI API",
    description="智能旅行规划与美食推荐API，基于多Agent协作",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 请求模型
class TravelRequest(BaseModel):
    """旅行请求模型"""
    destination: str
    duration: str
    interests: List[str]
    budget: str
    location: str = ""
    travel_dates: str = ""
    travel_style: str = ""
    cuisine_type: str = ""


# 响应模型
class TravelResponse(BaseModel):
    """旅行响应模型"""
    status: str
    message: str
    data: Dict[str, Any]


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to WhereEatAI API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/status")
async def status():
    """获取服务状态"""
    return {
        "status": "running",
        "message": "WhereEatAI API is running normally"
    }


@app.post("/travel-plan")
async def generate_travel_plan(request: TravelRequest):
    """生成旅行计划"""
    try:
        # 转换请求模型为字典
        input_data = request.model_dump()
        
        # 使用AgentManager执行旅行计划工作流
        result = agent_manager.execute_workflow("travel_plan", input_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成旅行计划失败: {str(e)}")


@app.post("/food-recommendation")
async def recommend_food(request: TravelRequest):
    """推荐美食"""
    try:
        # 转换请求模型为字典
        input_data = request.model_dump()
        
        # 使用AgentManager执行美食推荐
        result = agent_manager.execute_agent("food_recommendation", input_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐美食失败: {str(e)}")


@app.post("/itinerary")
async def generate_itinerary(request: TravelRequest):
    """生成行程安排"""
    try:
        # 转换请求模型为字典
        input_data = request.model_dump()
        
        # 使用AgentManager执行行程规划
        result = agent_manager.execute_agent("itinerary", input_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成行程安排失败: {str(e)}")


@app.post("/travelogue")
async def generate_travelogue(request: TravelRequest):
    """生成游记"""
    try:
        # 转换请求模型为字典
        input_data = request.model_dump()
        
        # 使用AgentManager执行游记生成
        result = agent_manager.execute_agent("travelogue", input_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成游记失败: {str(e)}")


@app.post("/price-comparison")
async def compare_prices(request: TravelRequest):
    """多平台价格比价"""
    try:
        # 转换请求模型为字典
        input_data = request.model_dump()
        
        # 使用AgentManager执行价格比价
        result = agent_manager.execute_agent("price_comparison", input_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"价格比价失败: {str(e)}")


@app.post("/xiaohongshu-analysis")
async def analyze_xiaohongshu(request: TravelRequest):
    """分析小红书笔记"""
    try:
        # 转换请求模型为字典
        input_data = request.model_dump()
        
        # 使用AgentManager执行小红书笔记分析
        result = agent_manager.execute_agent("xiaohongshu", input_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"小红书笔记分析失败: {str(e)}")


@app.post("/video-analysis")
async def analyze_video(request: TravelRequest):
    """分析视频内容"""
    try:
        # 转换请求模型为字典
        input_data = request.model_dump()
        
        # 使用AgentManager执行视频分析
        result = agent_manager.execute_agent("video", input_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"视频分析失败: {str(e)}")


@app.post("/topic-recommendation")
async def recommend_topic(request: TravelRequest):
    """生成专题推荐"""
    try:
        # 转换请求模型为字典
        input_data = request.model_dump()
        
        # 使用AgentManager执行专题推荐
        result = agent_manager.execute_agent("topic_recommendation", input_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"专题推荐生成失败: {str(e)}")


@app.get("/agents")
async def get_agents():
    """获取可用的Agent列表"""
    try:
        # 使用AgentManager获取可用Agent列表
        agents = agent_manager.get_all_agents()
        
        return {
            "status": "success",
            "message": "可用Agent列表获取成功",
            "data": agents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取可用Agent列表失败: {str(e)}")


@app.post("/execute-agent/{agent_name}")
async def execute_agent(agent_name: str, request: TravelRequest):
    """执行指定Agent"""
    try:
        # 转换请求模型为字典
        input_data = request.model_dump()
        
        # 使用AgentManager执行指定Agent
        result = agent_manager.execute_agent(agent_name, input_data)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"执行Agent失败: {str(e)}")
