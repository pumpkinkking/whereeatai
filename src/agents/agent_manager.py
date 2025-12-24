"""Agent管理器，用于协调和管理所有agent"""
from typing import Dict, Any, List
from .travel_agent import TravelGuideAgent
from .itinerary_agent import ItineraryPlanningAgent
from .food_recommendation_agent import FoodRecommendationAgent
from .price_comparison_agent import PriceComparisonAgent
from .xiaohongshu_agent import XiaoHongShuNoteAgent
from .video_agent import VideoRecognitionAgent
from .topic_recommendation_agent import TopicRecommendationAgent


class AgentManager:
    """Agent管理器，负责协调和管理所有agent"""
    
    def __init__(self):
        """初始化Agent管理器"""
        self.agents = {
            "travel_guide": TravelGuideAgent(),
            "itinerary_planning": ItineraryPlanningAgent(),
            "food_recommendation": FoodRecommendationAgent(),
            "price_comparison": PriceComparisonAgent(),
            "xiaohongshu_note": XiaoHongShuNoteAgent(),
            "video_recognition": VideoRecognitionAgent(),
            "topic_recommendation": TopicRecommendationAgent()
        }
    
    def get_agent(self, agent_name: str):
        """
        获取指定名称的agent
        
        Args:
            agent_name: agent名称
            
        Returns:
            指定的agent实例
        """
        return self.agents.get(agent_name)
    
    def execute_agent(self, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行指定agent的任务
        
        Args:
            agent_name: agent名称
            input_data: 输入数据
            
        Returns:
            agent执行结果
        """
        agent = self.get_agent(agent_name)
        if not agent:
            return {"error": f"Agent {agent_name} not found"}
        
        return agent.execute(input_data)
    
    def execute_multiple_agents(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        执行多个agent任务
        
        Args:
            tasks: 任务列表，每个任务包含agent_name和input_data
            
        Returns:
            所有agent执行结果的字典
        """
        results = {}
        
        for task in tasks:
            agent_name = task.get("agent_name")
            input_data = task.get("input_data", {})
            
            if agent_name:
                result = self.execute_agent(agent_name, input_data)
                results[agent_name] = result
        
        return results
    
    def get_all_agents(self) -> Dict[str, Any]:
        """
        获取所有agent信息
        
        Returns:
            包含所有agent名称和描述的字典
        """
        agent_info = {}
        
        for agent_name, agent in self.agents.items():
            agent_info[agent_name] = {
                "name": agent.name,
                "description": agent.description
            }
        
        return agent_info