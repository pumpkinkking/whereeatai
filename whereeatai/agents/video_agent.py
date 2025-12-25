from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..models.qwen_model import QwenModel
from ..protocols.a2a_protocol import AgentCapability


class VideoAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="VideoAgent",
            description="用于识别和分析视频内容的Agent",
            agent_id="video_agent"
        )
        self.model = QwenModel()
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="analyze_video",
                description="分析旅游视频内容",
                input_schema={
                    "type": "object",
                    "properties": {
                        "video_url": {"type": "string"}
                    },
                    "required": ["video_url"]
                },
                output_schema={"type": "object"},
                estimated_duration=15
            )
        ]
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["video_url"]
        if not self.validate_input(input_data, required_fields):
            return {
                "status": "error",
                "message": f"缺少必填字段：{required_fields}"
            }
        
        video_url = input_data["video_url"]
        video_summary = input_data.get("video_summary", "")
        video_frames = input_data.get("video_frames", [])
        
        prompt = f"""
        请分析以下视频内容：
        视频URL：{video_url}
        视频摘要：{video_summary}
        视频帧：{video_frames}
        
        分析内容应该包括：
        1. 视频主题和核心内容
        2. 推荐的地点或产品
        3. 推荐理由
        4. 价格信息（如果有）
        5. 适合人群
        6. 视频真实性评估
        7. 有用的旅行或美食建议
        8. 相关标签和关键词
        
        请使用清晰的结构和语言，提取有用的信息。
        """
        
        analysis_result = self.model.generate(prompt)
        
        return {
            "status": "success",
            "message": "视频分析成功",
            "data": {
                "video_url": video_url,
                "analysis_result": analysis_result
            }
        }
