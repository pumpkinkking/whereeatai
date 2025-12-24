"""千问模型集成，用于连接硅基流动的千问模型"""
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from whereeatai.config import API_KEY, BASE_URL, MODEL_NAME


class QwenModel:
    """千问模型封装，用于连接硅基流动的千问模型"""
    
    def __init__(self):
        """初始化千问模型"""
        self.model = ChatOpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
            model=MODEL_NAME,
            temperature=0.7,
            max_tokens=4096
        )
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        生成模型响应
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            
        Returns:
            str: 模型生成的响应
        """
        from langchain_core.messages import HumanMessage, SystemMessage
        
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))
        
        response = self.model.invoke(messages)
        return response.content
    
    def generate_with_template(self, template: str, variables: Dict[str, Any], system_prompt: Optional[str] = None) -> str:
        """
        使用模板生成模型响应
        
        Args:
            template: 提示词模板
            variables: 模板变量
            system_prompt: 系统提示词
            
        Returns:
            str: 模型生成的响应
        """
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.messages import SystemMessage
        
        prompt_template = ChatPromptTemplate.from_template(template)
        prompt = prompt_template.format(**variables)
        
        return self.generate(prompt, system_prompt)
