"""旅行工作流图，用于多agent协作"""
from typing import Dict, Any, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from src.agents.agent_manager import AgentManager


# 定义工作流状态
class TravelWorkflowState:
    """旅行工作流状态"""
    def __init__(self):
        """初始化状态"""
        self.messages = []
        self.input_data = {}
        self.results = {}


class TravelWorkflow:
    """旅行工作流，用于协调多个agent完成旅行相关任务"""
    
    def __init__(self):
        """初始化旅行工作流"""
        self.agent_manager = AgentManager()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        构建旅行工作流图
        
        Returns:
            StateGraph: 构建好的工作流图
        """
        # 创建状态图
        graph = StateGraph(TravelWorkflowState)
        
        # 添加节点
        graph.add_node("travel_guide", self._call_travel_guide)
        graph.add_node("itinerary_planning", self._call_itinerary_planning)
        graph.add_node("food_recommendation", self._call_food_recommendation)
        graph.add_node("price_comparison", self._call_price_comparison)
        graph.add_node("final_plan", self._generate_final_plan)
        
        # 添加边
        graph.add_edge(START, "travel_guide")
        graph.add_edge("travel_guide", "itinerary_planning")
        graph.add_edge("itinerary_planning", "food_recommendation")
        graph.add_edge("food_recommendation", "price_comparison")
        graph.add_edge("price_comparison", "final_plan")
        graph.add_edge("final_plan", END)
        
        return graph.compile()
    
    def _call_travel_guide(self, state: TravelWorkflowState) -> Dict[str, Any]:
        """
        调用旅行向导agent
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        result = self.agent_manager.execute_agent("travel_guide", state.input_data)
        state.results["travel_guide"] = result
        return state
    
    def _call_itinerary_planning(self, state: TravelWorkflowState) -> Dict[str, Any]:
        """
        调用行程规划agent
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        result = self.agent_manager.execute_agent("itinerary_planning", state.input_data)
        state.results["itinerary_planning"] = result
        return state
    
    def _call_food_recommendation(self, state: TravelWorkflowState) -> Dict[str, Any]:
        """
        调用美食推荐agent
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        # 合并旅行向导和行程规划的结果，作为美食推荐的输入
        food_input = state.input_data.copy()
        if "travel_guide" in state.results:
            food_input["attractions"] = state.results["travel_guide"].get("attractions", [])
        
        result = self.agent_manager.execute_agent("food_recommendation", food_input)
        state.results["food_recommendation"] = result
        return state
    
    def _call_price_comparison(self, state: TravelWorkflowState) -> Dict[str, Any]:
        """
        调用价格比价agent
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        # 合并之前的结果，作为价格比价的输入
        price_input = state.input_data.copy()
        
        # 从美食推荐结果中提取餐厅名称
        if "food_recommendation" in state.results:
            food_recommendations = state.results["food_recommendation"].get("food_recommendations", [])
            if food_recommendations:
                price_input["product_name"] = food_recommendations[0].get("name", "")
        
        result = self.agent_manager.execute_agent("price_comparison", price_input)
        state.results["price_comparison"] = result
        return state
    
    def _generate_final_plan(self, state: TravelWorkflowState) -> Dict[str, Any]:
        """
        生成最终旅行计划
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        # 整合所有agent的结果，生成最终旅行计划
        final_plan = {
            "destination": state.input_data.get("destination", ""),
            "duration": state.input_data.get("duration", ""),
            "travel_notes": state.results.get("travel_guide", {}).get("travel_notes", ""),
            "itinerary": state.results.get("itinerary_planning", {}).get("daily_itinerary", []),
            "attractions": state.results.get("travel_guide", {}).get("attractions", []),
            "food_recommendations": state.results.get("food_recommendation", {}).get("food_recommendations", []),
            "price_comparison": state.results.get("price_comparison", {}).get("price_comparison", {})
        }
        
        state.results["final_plan"] = final_plan
        return state
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行旅行工作流
        
        Args:
            input_data: 输入数据
            
        Returns:
            工作流执行结果
        """
        initial_state = TravelWorkflowState()
        initial_state.input_data = input_data
        
        result = self.graph.invoke(initial_state)
        return result.results
