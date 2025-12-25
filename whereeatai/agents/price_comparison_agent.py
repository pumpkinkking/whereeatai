from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..models.qwen_model import QwenModel
from ..protocols.a2a_protocol import AgentCapability


class PriceComparisonAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="PriceComparisonAgent",
            description="用于多平台价格比价的Agent",
            agent_id="price_comparison_agent"
        )
        self.model = QwenModel()
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="compare_prices",
                description="跨平台比较产品价格",
                input_schema={
                    "type": "object",
                    "properties": {
                        "product": {"type": "string"},
                        "platforms": {"type": "array"}
                    },
                    "required": ["product", "platforms"]
                },
                output_schema={"type": "object"},
                estimated_duration=12
            )
        ]
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["product", "platforms"]
        if not self.validate_input(input_data, required_fields):
            return {
                "status": "error",
                "message": f"缺少必填字段：{required_fields}"
            }
        
        product = input_data["product"]
        platforms = input_data["platforms"]
        location = input_data.get("location", "")
        
        prompt = f"""
        请为{product}在以下平台进行价格比价：{', '.join(platforms) if isinstance(platforms, list) else platforms}。
        位置：{location}
        
        价格比价应该包括：
        1. 各个平台的产品信息
        2. 价格对比
        3. 优惠活动和折扣信息
        4. 配送信息
        5. 售后服务
        6. 推荐购买平台
        7. 购买建议
        
        请确保价格信息准确，比较全面，推荐合理。
        """
        
        comparison_result = self.model.generate(prompt)
        
        return {
            "status": "success",
            "message": "价格比价生成成功",
            "data": {
                "product": product,
                "platforms": platforms,
                "comparison_result": comparison_result
            }
        }
