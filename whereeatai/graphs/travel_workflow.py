"""旅行工作流图，用于多Agent协作"""
from typing import Dict, Any, List, TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
import logging

logger = logging.getLogger(__name__)


# 定义工作流状态
class TravelWorkflowState(TypedDict):
    """旅行工作流状态"""
    messages: Annotated[List[BaseMessage], add_messages]
    input_data: Dict[str, Any]
    travelogue_result: Dict[str, Any]
    itinerary_result: Dict[str, Any]
    food_result: Dict[str, Any]
    price_result: Dict[str, Any]
    xiaohongshu_result: Dict[str, Any]
    video_result: Dict[str, Any]
    topic_result: Dict[str, Any]
    final_plan: Dict[str, Any]
    errors: List[str]


class TravelWorkflow:
    """旅行工作流，用于协调多个Agent完成旅行相关任务"""
    
    def __init__(self, agent_manager):
        """
        初始化旅行工作流
        
        Args:
            agent_manager: Agent管理器实例
        """
        self.agent_manager = agent_manager
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        构建旅行工作流图
        
        Returns:
            StateGraph: 构建好的工作流图
        """
        # 创建状态图
        workflow = StateGraph(TravelWorkflowState)
        
        # 添加节点
        workflow.add_node("analyze_input", self._analyze_input)
        workflow.add_node("generate_travelogue", self._generate_travelogue)
        workflow.add_node("plan_itinerary", self._plan_itinerary)
        workflow.add_node("recommend_food", self._recommend_food)
        workflow.add_node("compare_prices", self._compare_prices)
        workflow.add_node("generate_final_plan", self._generate_final_plan)
        
        # 添加边 - 定义工作流执行顺序
        workflow.add_edge(START, "analyze_input")
        workflow.add_edge("analyze_input", "generate_travelogue")
        workflow.add_edge("analyze_input", "plan_itinerary")
        workflow.add_edge("generate_travelogue", "recommend_food")
        workflow.add_edge("plan_itinerary", "recommend_food")
        workflow.add_edge("recommend_food", "compare_prices")
        workflow.add_edge("compare_prices", "generate_final_plan")
        workflow.add_edge("generate_final_plan", END)
        
        return workflow.compile()
    
    def _analyze_input(self, state: TravelWorkflowState) -> TravelWorkflowState:
        """
        分析输入数据，验证必要字段
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        try:
            logger.info("开始分析用户输入")
            input_data = state.get("input_data", {})
            
            # 验证必要字段
            required_fields = ["destination", "duration", "interests"]
            missing_fields = [f for f in required_fields if f not in input_data]
            
            if missing_fields:
                error_msg = f"缺少必要字段: {', '.join(missing_fields)}"
                logger.error(error_msg)
                state["errors"] = state.get("errors", []) + [error_msg]
            else:
                logger.info(f"输入验证通过: {input_data.get('destination')}")
            
            return state
        except Exception as e:
            logger.error(f"分析输入失败: {str(e)}")
            state["errors"] = state.get("errors", []) + [str(e)]
            return state
    
    def _generate_travelogue(self, state: TravelWorkflowState) -> TravelWorkflowState:
        """
        生成游记
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        try:
            logger.info("开始生成游记")
            result = self.agent_manager.execute_agent("travelogue", state["input_data"])
            state["travelogue_result"] = result
            logger.info("游记生成完成")
            return state
        except Exception as e:
            logger.error(f"游记生成失败: {str(e)}")
            state["errors"] = state.get("errors", []) + [f"游记生成失败: {str(e)}"]
            state["travelogue_result"] = {"status": "error", "message": str(e)}
            return state
    
    def _plan_itinerary(self, state: TravelWorkflowState) -> TravelWorkflowState:
        """
        规划行程
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        try:
            logger.info("开始规划行程")
            result = self.agent_manager.execute_agent("itinerary", state["input_data"])
            state["itinerary_result"] = result
            logger.info("行程规划完成")
            return state
        except Exception as e:
            logger.error(f"行程规划失败: {str(e)}")
            state["errors"] = state.get("errors", []) + [f"行程规划失败: {str(e)}"]
            state["itinerary_result"] = {"status": "error", "message": str(e)}
            return state
    
    def _recommend_food(self, state: TravelWorkflowState) -> TravelWorkflowState:
        """
        推荐美食
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        try:
            logger.info("开始推荐美食")
            
            # 准备美食推荐的输入，结合之前的结果
            food_input = state["input_data"].copy()
            food_input["location"] = food_input.get("destination", "")
            food_input["cuisine_type"] = food_input.get("interests", ["中餐"])
            
            # 如果行程规划已完成，可以基于行程推荐美食
            if state.get("itinerary_result", {}).get("status") == "success":
                logger.info("基于行程规划推荐美食")
            
            result = self.agent_manager.execute_agent("food_recommendation", food_input)
            state["food_result"] = result
            logger.info("美食推荐完成")
            return state
        except Exception as e:
            logger.error(f"美食推荐失败: {str(e)}")
            state["errors"] = state.get("errors", []) + [f"美食推荐失败: {str(e)}"]
            state["food_result"] = {"status": "error", "message": str(e)}
            return state
    
    def _compare_prices(self, state: TravelWorkflowState) -> TravelWorkflowState:
        """
        比较价格
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        try:
            logger.info("开始价格比价")
            
            # 准备价格比价的输入
            price_input = {
                "product": f"{state['input_data'].get('destination', '')}旅游套餐",
                "platforms": ["携程", "美团", "飞猪", "去哪儿"],
                "location": state['input_data'].get('destination', '')
            }
            
            result = self.agent_manager.execute_agent("price_comparison", price_input)
            state["price_result"] = result
            logger.info("价格比价完成")
            return state
        except Exception as e:
            logger.error(f"价格比价失败: {str(e)}")
            state["errors"] = state.get("errors", []) + [f"价格比价失败: {str(e)}"]
            state["price_result"] = {"status": "error", "message": str(e)}
            return state
    
    def _generate_final_plan(self, state: TravelWorkflowState) -> TravelWorkflowState:
        """
        生成最终旅行计划
        
        Args:
            state: 当前工作流状态
            
        Returns:
            更新后的状态
        """
        try:
            logger.info("开始生成最终旅行计划")
            
            # 整合所有Agent的结果
            final_plan = {
                "destination": state["input_data"].get("destination", ""),
                "duration": state["input_data"].get("duration", ""),
                "interests": state["input_data"].get("interests", []),
                "travelogue": state.get("travelogue_result", {}).get("data", {}),
                "itinerary": state.get("itinerary_result", {}).get("data", {}),
                "food_recommendations": state.get("food_result", {}).get("data", {}),
                "price_comparison": state.get("price_result", {}).get("data", {}),
                "errors": state.get("errors", [])
            }
            
            state["final_plan"] = final_plan
            logger.info("最终旅行计划生成完成")
            return state
        except Exception as e:
            logger.error(f"生成最终计划失败: {str(e)}")
            state["errors"] = state.get("errors", []) + [f"生成最终计划失败: {str(e)}"]
            state["final_plan"] = {"status": "error", "message": str(e)}
            return state
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行旅行工作流
        
        Args:
            input_data: 输入数据
            
        Returns:
            工作流执行结果
        """
        try:
            logger.info(f"启动旅行工作流: {input_data.get('destination', '')}")
            
            # 初始化状态
            initial_state: TravelWorkflowState = {
                "messages": [],
                "input_data": input_data,
                "travelogue_result": {},
                "itinerary_result": {},
                "food_result": {},
                "price_result": {},
                "xiaohongshu_result": {},
                "video_result": {},
                "topic_result": {},
                "final_plan": {},
                "errors": []
            }
            
            # 执行工作流
            result = self.graph.invoke(initial_state)
            
            # 返回最终计划
            final_plan = result.get("final_plan", {})
            
            if result.get("errors"):
                logger.warning(f"工作流执行中出现错误: {result['errors']}")
                return {
                    "status": "partial_success",
                    "message": "部分功能执行失败",
                    "data": final_plan,
                    "errors": result["errors"]
                }
            
            return {
                "status": "success",
                "message": "旅行计划生成成功",
                "data": final_plan
            }
        except Exception as e:
            logger.error(f"工作流执行失败: {str(e)}")
            return {
                "status": "error",
                "message": f"工作流执行失败: {str(e)}",
                "data": {}
            }


class ContentAnalysisWorkflow:
    """内容分析工作流，用于分析小红书笔记和视频内容"""
    
    def __init__(self, agent_manager):
        """
        初始化内容分析工作流
        
        Args:
            agent_manager: Agent管理器实例
        """
        self.agent_manager = agent_manager
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        构建内容分析工作流图
        
        Returns:
            StateGraph: 构建好的工作流图
        """
        # 创建状态图
        workflow = StateGraph(TravelWorkflowState)
        
        # 添加节点
        workflow.add_node("analyze_xiaohongshu", self._analyze_xiaohongshu)
        workflow.add_node("analyze_video", self._analyze_video)
        workflow.add_node("extract_recommendations", self._extract_recommendations)
        
        # 添加边
        workflow.add_edge(START, "analyze_xiaohongshu")
        workflow.add_edge(START, "analyze_video")
        workflow.add_edge("analyze_xiaohongshu", "extract_recommendations")
        workflow.add_edge("analyze_video", "extract_recommendations")
        workflow.add_edge("extract_recommendations", END)
        
        return workflow.compile()
    
    def _analyze_xiaohongshu(self, state: TravelWorkflowState) -> TravelWorkflowState:
        """分析小红书内容"""
        try:
            if "note_content" in state["input_data"]:
                logger.info("开始分析小红书笔记")
                result = self.agent_manager.execute_agent("xiaohongshu", state["input_data"])
                state["xiaohongshu_result"] = result
                logger.info("小红书笔记分析完成")
            return state
        except Exception as e:
            logger.error(f"小红书分析失败: {str(e)}")
            state["errors"] = state.get("errors", []) + [str(e)]
            return state
    
    def _analyze_video(self, state: TravelWorkflowState) -> TravelWorkflowState:
        """分析视频内容"""
        try:
            if "video_url" in state["input_data"]:
                logger.info("开始分析视频内容")
                result = self.agent_manager.execute_agent("video", state["input_data"])
                state["video_result"] = result
                logger.info("视频内容分析完成")
            return state
        except Exception as e:
            logger.error(f"视频分析失败: {str(e)}")
            state["errors"] = state.get("errors", []) + [str(e)]
            return state
    
    def _extract_recommendations(self, state: TravelWorkflowState) -> TravelWorkflowState:
        """提取推荐信息"""
        try:
            logger.info("开始提取推荐信息")
            
            recommendations = {
                "xiaohongshu_insights": state.get("xiaohongshu_result", {}).get("data", {}),
                "video_insights": state.get("video_result", {}).get("data", {})
            }
            
            state["final_plan"] = recommendations
            logger.info("推荐信息提取完成")
            return state
        except Exception as e:
            logger.error(f"提取推荐信息失败: {str(e)}")
            state["errors"] = state.get("errors", []) + [str(e)]
            return state
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """运行内容分析工作流"""
        try:
            logger.info("启动内容分析工作流")
            
            initial_state: TravelWorkflowState = {
                "messages": [],
                "input_data": input_data,
                "travelogue_result": {},
                "itinerary_result": {},
                "food_result": {},
                "price_result": {},
                "xiaohongshu_result": {},
                "video_result": {},
                "topic_result": {},
                "final_plan": {},
                "errors": []
            }
            
            result = self.graph.invoke(initial_state)
            
            return {
                "status": "success",
                "message": "内容分析完成",
                "data": result.get("final_plan", {})
            }
        except Exception as e:
            logger.error(f"内容分析工作流失败: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "data": {}
            }
