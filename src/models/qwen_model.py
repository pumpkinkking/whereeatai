"""硅基流动千问模型集成"""
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from src.config.config import API_KEY, BASE_URL, MODEL_NAME


class QwenModel:
    """硅基流动千问模型封装类"""
    
    def __init__(self):
        """初始化千问模型"""
        if not API_KEY:
            raise ValueError("API_KEY未配置，请在.env文件中设置")
        
        self.model = ChatOpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
            model=MODEL_NAME,
            temperature=0.7,
            max_tokens=2048
        )
        self.output_parser = StrOutputParser()
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        生成文本
        
        Args:
            prompt: 用户提示
            system_prompt: 系统提示
            
        Returns:
            生成的文本
        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))
        
        response = self.model.invoke(messages)
        return self.output_parser.invoke(response)
    
    async def agenerate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        异步生成文本
        
        Args:
            prompt: 用户提示
            system_prompt: 系统提示
            
        Returns:
            生成的文本
        """
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))
        
        response = await self.model.ainvoke(messages)
        return self.output_parser.invoke(response)
    
    def generate_structured(self, prompt: str, system_prompt: Optional[str] = None, schema: Optional[Dict[str, Any]] = None) -> Any:
        """
        生成结构化数据
        
        Args:
            prompt: 用户提示
            system_prompt: 系统提示
            schema: 输出数据模式
            
        Returns:
            生成的结构化数据
        """
        # 这里可以添加结构化输出的实现
        # 例如，使用JSON模式或Pydantic模型
        return self.generate(prompt, system_prompt)
