from typing import Dict, Any
from .base_agent import BaseAgent
from ..models.qwen_model import QwenModel


class TopicRecommendationAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="TopicRecommendationAgent",
            description="用于生成专题推荐的Agent"
        )
        self.model = QwenModel()
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["topic", "interests"]
        if not self.validate_input(input_data, required_fields):
            return {
                "status": "error",
                "message": f"缺少必填字段：{required_fields}"
            }
        
        topic = input_data["topic"]
        interests = input_data["interests"]
        target_audience = input_data.get("target_audience", "")
        budget = input_data.get("budget", "")
        season = input_data.get("season", "")
        
        prompt = f"""
        请为{target_audience}生成关于{topic}的专题推荐。
        兴趣爱好：{', '.join(interests) if isinstance(interests, list) else interests}
        预算水平：{budget}
        季节：{season}
        
        专题推荐应该包括：
        1. 专题主题和核心内容
        2. 推荐的目的地或产品
        3. 每个推荐项的特色和亮点
        4. 适合的人群
        5. 预算参考
        6. 最佳时间
        7. 推荐理由
        8. 实用小贴士
        
        请确保推荐内容丰富，结构清晰，适合目标用户群体。
        """
        
        recommendation_result = self.model.generate(prompt)
        
        return {
            "status": "success",
            "message": "专题推荐生成成功",
            "data": {
                "topic": topic,
                "recommendation_result": recommendation_result
            }
        }
