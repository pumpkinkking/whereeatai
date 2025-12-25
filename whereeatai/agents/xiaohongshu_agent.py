from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..models.qwen_model import QwenModel
from ..protocols.a2a_protocol import AgentCapability


class XiaoHongShuAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="XiaoHongShuAgent",
            description="用于识别和分析小红书笔记内容的Agent",
            agent_id="xiaohongshu_agent"
        )
        self.model = QwenModel()
    
    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability(
                name="analyze_xiaohongshu",
                description="分析小红书笔记内容提取旅游信息",
                input_schema={
                    "type": "object",
                    "properties": {
                        "note_content": {"type": "string"}
                    },
                    "required": ["note_content"]
                },
                output_schema={"type": "object"},
                estimated_duration=10
            )
        ]
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["note_content"]
        if not self.validate_input(input_data, required_fields):
            return {
                "status": "error",
                "message": f"缺少必填字段：{required_fields}"
            }
        
        note_content = input_data["note_content"]
        note_images = input_data.get("note_images", [])
        note_tags = input_data.get("note_tags", [])
        
        prompt = f"""
        请分析以下小红书笔记内容：
        笔记内容：{note_content}
        笔记图片：{note_images}
        笔记标签：{note_tags}
        
        分析内容应该包括：
        1. 笔记主题和核心内容
        2. 推荐的地点或产品
        3. 推荐理由
        4. 价格信息（如果有）
        5. 适合人群
        6. 笔记真实性评估
        7. 有用的旅行或美食建议
        8. 相关标签和关键词
        
        请使用清晰的结构和语言，提取有用的信息。
        """
        
        analysis_result = self.model.generate(prompt)
        
        return {
            "status": "success",
            "message": "小红书笔记分析成功",
            "data": {
                "note_content": note_content,
                "analysis_result": analysis_result
            }
        }
