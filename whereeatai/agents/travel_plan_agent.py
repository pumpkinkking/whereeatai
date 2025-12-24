from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.qwen_model import QwenModel


class TravelPlanAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="TravelPlanAgent",
            description="用于生成完整旅行计划的Agent，包括美食、酒店、路线等"
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
        group_size = input_data.get("group_size", "")
        
        prompt = f"""
        请为前往{destination}旅游{duration}的游客生成一份完整的旅行计划。
        旅游日期：{travel_dates}
        游客人数：{group_size}
        游客的兴趣爱好是：{', '.join(interests)}
        预算水平是：{budget}
        旅行风格是：{travel_style}
        
        旅行计划应该包括：
        1. 行程概览
        2. 每日详细行程安排（时间、地点、活动内容）
        3. 景点推荐及门票信息
        4. 美食推荐及餐厅信息
        5. 酒店推荐及住宿安排
        6. 交通安排及费用
        7. 预算明细
        8. 装备建议
        9. 安全提示
        10. 应急方案
        11. 实用小贴士
        
        请确保旅行计划全面、详细、实用，符合游客的需求和兴趣。
        """
        
        travel_plan = self.model.generate(prompt)
        
        return {
            "status": "success",
            "message": "旅行计划生成成功",
            "data": {
                "destination": destination,
                "duration": duration,
                "interests": interests,
                "travel_plan": travel_plan
            }
        }
