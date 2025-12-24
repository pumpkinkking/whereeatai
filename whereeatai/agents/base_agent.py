"""基础Agent类，定义所有Agent的统一接口"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """所有Agent的基类"""
    
    def __init__(self, name: str, description: str):
        """
        初始化Agent
        
        Args:
            name: Agent名称
            description: Agent描述
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行Agent任务
        
        Args:
            input_data: 输入数据
            
        Returns:
            执行结果
        """
        pass
    
    def get_info(self) -> Dict[str, str]:
        """
        获取Agent基本信息
        
        Returns:
            Agent基本信息
        """
        return {
            "name": self.name,
            "description": self.description
        }
    
    def validate_input(self, input_data: Dict[str, Any], required_fields: list) -> bool:
        """
        验证输入数据是否包含所有必填字段
        
        Args:
            input_data: 输入数据
            required_fields: 必填字段列表
            
        Returns:
            验证结果
        """
        for field in required_fields:
            if field not in input_data:
                return False
        return True
