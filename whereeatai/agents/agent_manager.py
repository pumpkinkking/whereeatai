"""Agent管理器，用于协调和管理所有Agent"""
from typing import Dict, Any, List
import logging
from .travelogue_agent import TravelogueAgent
from .itinerary_agent import ItineraryAgent
from .food_recommendation_agent import FoodRecommendationAgent
from .price_comparison_agent import PriceComparisonAgent
from .xiaohongshu_agent import XiaoHongShuAgent
from .video_agent import VideoAgent
from .topic_recommendation_agent import TopicRecommendationAgent
from .travel_plan_agent import TravelPlanAgent

logger = logging.getLogger(__name__)


class AgentManager:
    """Agent管理器，负责协调和管理所有Agent"""
    
    def __init__(self):
        """初始化Agent管理器，创建所有Agent实例"""
        logger.info("初始化Agent管理器")
        self.agents = {
            "travelogue": TravelogueAgent(),
            "itinerary": ItineraryAgent(),
            "food_recommendation": FoodRecommendationAgent(),
            "price_comparison": PriceComparisonAgent(),
            "xiaohongshu": XiaoHongShuAgent(),
            "video": VideoAgent(),
            "topic_recommendation": TopicRecommendationAgent(),
            "travel_plan": TravelPlanAgent()
        }
        
        # 延迟导入以避免循环依赖
        from whereeatai.graphs.travel_workflow import TravelWorkflow, ContentAnalysisWorkflow
        self.travel_workflow = TravelWorkflow(self)
        self.content_workflow = ContentAnalysisWorkflow(self)
        logger.info(f"Agent管理器初始化完成，共{len(self.agents)}个Agent")
    
    def get_agent(self, agent_name: str):
        """
        获取指定名称的Agent
        
        Args:
            agent_name: Agent名称
            
        Returns:
            指定的Agent实例或None
        """
        return self.agents.get(agent_name)
    
    def get_all_agents(self) -> Dict[str, Any]:
        """
        获取所有可用的Agent信息
        
        Returns:
            所有可用Agent的信息字典
        """
        agent_info = {}
        for name, agent in self.agents.items():
            agent_info[name] = agent.get_info()
        return agent_info
    
    def execute_agent(self, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行指定Agent的任务
        
        Args:
            agent_name: Agent名称
            input_data: 输入数据
            
        Returns:
            Agent执行结果
        """
        logger.info(f"执行Agent: {agent_name}")
        agent = self.get_agent(agent_name)
        if not agent:
            logger.error(f"Agent不存在: {agent_name}")
            return {
                "status": "error",
                "message": f"Agent {agent_name} not found"
            }
        
        try:
            result = agent.execute(input_data)
            logger.info(f"Agent执行成功: {agent_name}")
            return result
        except Exception as e:
            logger.error(f"Agent执行失败: {agent_name}, 错误: {str(e)}")
            return {
                "status": "error",
                "message": f"Agent执行失败: {str(e)}"
            }
    
    def execute_workflow(self, workflow_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行指定工作流
        
        Args:
            workflow_name: 工作流名称
            input_data: 输入数据
            
        Returns:
            工作流执行结果
        """
        logger.info(f"执行工作流: {workflow_name}")
        
        if workflow_name == "travel_plan":
            return self.travel_workflow.run(input_data)
        elif workflow_name == "content_analysis":
            return self.content_workflow.run(input_data)
        else:
            logger.error(f"工作流不存在: {workflow_name}")
            return {
                "status": "error",
                "message": f"Workflow {workflow_name} not found"
            }
    
    def _execute_travel_plan_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行旅行计划工作流（已废弃，使用TravelWorkflow替代）
        
        Args:
            input_data: 输入数据
            
        Returns:
            旅行计划工作流执行结果
        """
        logger.warning("使用废弃的旅行计划工作流，建议使用TravelWorkflow")
        return self.travel_workflow.run(input_data)
