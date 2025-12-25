from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..models.qwen_model import QwenModel
from ..protocols.a2a_protocol import AgentCapability


class FoodRecommendationAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="FoodRecommendationAgent",
            description="用于推荐附近美食的Agent",
            agent_id="food_recommendation_agent"
        )
        self.model = QwenModel()
    
    def get_capabilities(self) -> List[AgentCapability]:
        """获取Agent能力列表"""
        return [
            AgentCapability(
                name="recommend_restaurants",
                description="根据位置、菜系和预算推荐附近餐厅",
                input_schema={
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"},
                        "cuisine_type": {"type": "string"},
                        "budget": {"type": "string"}
                    },
                    "required": ["location", "cuisine_type"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "recommendations": {"type": "string"}
                    }
                },
                estimated_duration=15
            )
        ]
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["location", "cuisine_type"]
        if not self.validate_input(input_data, required_fields):
            return {
                "status": "error",
                "message": f"缺少必填字段：{required_fields}"
            }
        
        location = input_data["location"]
        cuisine_type = input_data["cuisine_type"]
        budget = input_data.get("budget", "")
        dietary_restrictions = input_data.get("dietary_restrictions", [])
        
        prompt = f"""
        请为位于{location}的用户推荐附近的{', '.join(cuisine_type) if isinstance(cuisine_type, list) else cuisine_type}美食。
        预算水平：{budget}
        饮食限制：{', '.join(dietary_restrictions) if isinstance(dietary_restrictions, list) else dietary_restrictions}
        
        美食推荐应该包括：
        1. 餐厅名称和地址
        2. 菜系类型
        3. 推荐菜品
        4. 人均消费
        5. 餐厅特色
        6. 评分和评价
        7. 营业时间
        8. 交通指南
        
        请确保推荐的餐厅符合用户的要求，信息准确实用。
        """
        
        recommendations = self.model.generate(prompt)
        
        return {
            "status": "success",
            "message": "美食推荐生成成功",
            "data": {
                "location": location,
                "cuisine_type": cuisine_type,
                "recommendations": recommendations
            }
        }
