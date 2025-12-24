from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.qwen_model import QwenModel


class ItineraryAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="ItineraryAgent",
            description="用于生成动态行程的Agent"
        )
        self.model = QwenModel()
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["destination", "duration", "interests"]
        if not self.validate_input(input_data, required_fields):
            return {
                "status": "error",
                "message": f"缺少必填字段：{required_fields}"
            }
        
        destination = input_data["destination"]
        duration = input_data["duration"]
        interests = input_data["interests"]
        budget = input_data.get("budget", "")
        travel_dates = input_data.get("travel_dates", "")
        travel_style = input_data.get("travel_style", "")
        
        prompt = f"""
        请为前往{destination}旅游{duration}的游客生成一份详细的动态行程规划。
        旅游日期：{travel_dates}
        游客的兴趣爱好是：{', '.join(interests)}
        预算水平是：{budget}
        旅行风格是：{travel_style}
        
        行程规划应该包括：
        1. 每日行程安排（时间、地点、活动内容）
        2. 景点推荐及游览时间
        3. 美食推荐及餐厅信息
        4. 住宿建议
        5. 交通安排
        6. 预算分配
        7. 备选方案
        8. 实用小贴士
        
        请确保行程安排合理，时间充裕，活动内容符合游客兴趣。
        """
        
        itinerary = self.model.generate(prompt)
        
        return {
            "status": "success",
            "message": "行程规划生成成功",
            "data": {
                "destination": destination,
                "duration": duration,
                "interests": interests,
                "itinerary": itinerary
            }
        }
