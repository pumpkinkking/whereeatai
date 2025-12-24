"""API服务入口文件"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from src.graphs.travel_workflow import TravelWorkflow
from src.agents.agent_manager import AgentManager

# 创建FastAPI应用
app = FastAPI(
    title="WhereEatAI API",
    description="智能旅行规划与美食推荐API",
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

# 创建工作流和agent管理器实例
travel_workflow = TravelWorkflow()
agent_manager = AgentManager()


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


@app.get("/agents")
async def get_agents():
    """获取可用的agent列表"""
    agents = agent_manager.get_all_agents()
    return {
        "status": "success",
        "message": "Available agents retrieved successfully",
        "data": agents
    }


@app.post("/travel-plan", response_model=TravelResponse)
async def generate_travel_plan(request: TravelRequest):
    """生成完整旅行计划"""
    try:
        # 转换请求为字典
        input_data = request.model_dump()
        
        # 运行旅行工作流
        result = travel_workflow.run(input_data)
        
        return TravelResponse(
            status="success",
            message="Travel plan generated successfully",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/{agent_name}", response_model=TravelResponse)
async def call_agent(agent_name: str, request: TravelRequest):
    """调用指定的agent"""
    try:
        # 转换请求为字典
        input_data = request.model_dump()
        
        # 调用指定的agent
        result = agent_manager.execute_agent(agent_name, input_data)
        
        return TravelResponse(
            status="success",
            message=f"Agent {agent_name} called successfully",
            data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
