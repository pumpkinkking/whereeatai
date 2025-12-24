"""游记生成Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.qwen_model import QwenModel


class TravelogueAgent(BaseAgent):
    """游记生成Agent，用于生成智能游记"""
    
    def __init__(self):
        """初始化游记生成Agent"""
        super().__init__(
            name="TravelogueAgent",
            description="用于生成智能游记的Agent"
        )
        self.model = QwenModel()
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行游记生成任务
        
        Args:
            input_data: 输入数据，包含destination、duration、interests等字段
            
        Returns:
            包含生成的游记的字典
        """
        # 验证输入数据
        required_fields = ["destination", "duration", "interests"]
        if not self.validate_input(input_data, required_fields):
            return {
                "status": "error",
                "message": f"缺少必填字段：{required_fields}"
            }
        
        destination = input_data["destination"]
        duration = input_data["duration"]
        interests = input_data["interests"]
        travel_style = input_data.get("travel_style", "")
        
        # 生成游记
        prompt = f"""
        请为前往{destination}旅行{duration}的游客生成一篇精彩的游记。
        游客的兴趣爱好是：{', '.join(interests)}
        旅行风格是：{travel_style}
        
        游记应该包括：
        1. 行程安排和每日亮点
        2. 景点推荐及游览体验
        3. 美食推荐
        4. 住宿建议
        5. 交通指南
        6. 实用小贴士
        7. 个人感受和建议
        
        请使用生动有趣的语言，让读者有身临其境的感觉。
        """
        
        travelogue = self.model.generate(prompt)
        
        return {
            "status": "success",
            "message": "游记生成成功",
            "data": {
                "destination": destination,
                "duration": duration,
                "interests": interests,
                "travel_style": travel_style,
                "travelogue": travelogue
            }
        }
