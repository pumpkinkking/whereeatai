"""Agent管理器，用于协调和管理所有Agent"""
from typing import Dict, Any, List
from .travelogue_agent import TravelogueAgent
from .itinerary_agent import ItineraryAgent
from .food_recommendation_agent import FoodRecommendationAgent
from .price_comparison_agent import PriceComparisonAgent
from .xiaohongshu_agent import XiaoHongShuAgent
from .video_agent import VideoAgent
from .topic_recommendation_agent import TopicRecommendationAgent
from .travel_plan_agent import TravelPlanAgent


class AgentManager:
    """Agent管理器，负责协调和管理所有Agent"""
    
    def __init__(self):
        """初始化Agent管理器，创建所有Agent实例"""
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
        agent = self.get_agent(agent_name)
        if not agent:
            return {
                "status": "error",
                "message": f"Agent {agent_name} not found"
            }
        
        return agent.execute(input_data)
    
    def execute_workflow(self, workflow_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行指定工作流
        
        Args:
            workflow_name: 工作流名称
            input_data: 输入数据
            
        Returns:
            工作流执行结果
        """
        if workflow_name == "travel_plan":
            return self._execute_travel_plan_workflow(input_data)
        else:
            return {
                "status": "error",
                "message": f"Workflow {workflow_name} not found"
            }
    
    def _execute_travel_plan_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行旅行计划工作流
        
        Args:
            input_data: 输入数据
            
        Returns:
            旅行计划工作流执行结果
        """
        try:
            # 1. 生成游记
            travelogue_result = self.execute_agent("travelogue", input_data)
            
            # 2. 生成行程规划
            itinerary_result = self.execute_agent("itinerary", input_data)
            
            # 3. 整合结果
            return {
                "status": "success",
                "message": "旅行计划生成成功",
                "data": {
                    "travelogue": travelogue_result["data"]["travelogue"],
                    "itinerary": itinerary_result["data"]["itinerary"],
                    "destination": input_data["destination"],
                    "duration": input_data["duration"],
                    "interests": input_data["interests"]
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"旅行计划生成失败: {str(e)}"
            }
