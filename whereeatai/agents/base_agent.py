"""基础Agent类，定义所有Agent的统一接口"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from whereeatai.protocols.a2a_protocol import (
    A2AProtocol,
    AgentRegistration,
    AgentCapability,
    AgentStatus,
    A2AMessage,
    MessageType,
    ActionType,
    Priority,
    get_a2a_protocol
)
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """所有Agent的基类，支持A2A协议"""
    
    def __init__(self, name: str, description: str, agent_id: Optional[str] = None):
        """
        初始化Agent
        
        Args:
            name: Agent名称
            description: Agent描述
            agent_id: Agent唯一ID（可选）
        """
        self.name = name
        self.description = description
        self.agent_id = agent_id or f"{name.lower()}_agent"
        self.status = AgentStatus.ACTIVE
        self.load = 0.0
        self.a2a_protocol: A2AProtocol = get_a2a_protocol()
        
        # 注册到A2A协议
        self._register_to_a2a()
    
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
    
    def _register_to_a2a(self):
        """
        注册Agent到A2A协议
        """
        try:
            registration = AgentRegistration(
                agent_id=self.agent_id,
                agent_name=self.name,
                description=self.description,
                capabilities=self.get_capabilities(),
                status=self.status,
                load=self.load
            )
            self.a2a_protocol.register_agent(registration)
            logger.info(f"Agent注册到A2A协议: {self.agent_id}")
        except Exception as e:
            logger.error(f"Agent注册失败: {str(e)}")
    
    @abstractmethod
    def get_capabilities(self) -> List[AgentCapability]:
        """
        获取Agent能力列表
        
        Returns:
            List[AgentCapability]: 能力列表
        """
        pass
    
    def send_message(self, receiver: str, action: ActionType, data: Dict[str, Any], 
                    priority: Priority = Priority.MEDIUM) -> Dict[str, Any]:
        """
        发送消息给其他Agent
        
        Args:
            receiver: 接收者Agent ID
            action: 操作类型
            data: 消息数据
            priority: 优先级
            
        Returns:
            发送结果
        """
        message = self.a2a_protocol.create_message(
            sender=self.agent_id,
            receiver=receiver,
            message_type=MessageType.REQUEST,
            action=action,
            data=data,
            priority=priority
        )
        return self.a2a_protocol.send_message(message)
    
    def update_status(self, status: AgentStatus, load: Optional[float] = None):
        """
        更新Agent状态
        
        Args:
            status: 新状态
            load: 负载水平
        """
        self.status = status
        if load is not None:
            self.load = load
        self.a2a_protocol.update_agent_status(self.agent_id, status, load)
