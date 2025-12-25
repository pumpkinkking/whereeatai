"""A2A (Agent-to-Agent) 协议实现"""
from typing import Dict, Any, Optional, List, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import uuid
import logging

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """消息类型枚举"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"


class Priority(str, Enum):
    """优先级枚举"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ActionType(str, Enum):
    """操作类型枚举"""
    EXECUTE = "execute"
    QUERY = "query"
    UPDATE = "update"
    CANCEL = "cancel"


class AgentStatus(str, Enum):
    """Agent状态枚举"""
    ACTIVE = "active"
    BUSY = "busy"
    IDLE = "idle"
    ERROR = "error"
    OFFLINE = "offline"


class A2AMessageMetadata(BaseModel):
    """A2A消息元数据"""
    priority: Priority = Priority.MEDIUM
    timeout: int = Field(default=30, ge=1, le=300, description="超时时间(秒)")
    retry_count: int = Field(default=3, ge=0, le=10, description="重试次数")
    correlation_id: Optional[str] = Field(default=None, description="关联ID，用于追踪相关消息")
    tags: List[str] = Field(default_factory=list, description="消息标签")


class A2AMessagePayload(BaseModel):
    """A2A消息负载"""
    action: ActionType
    data: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict, description="上下文信息")


class A2AMessage(BaseModel):
    """A2A消息标准格式"""
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = Field(..., description="发送者Agent ID")
    receiver: str = Field(..., description="接收者Agent ID")
    timestamp: datetime = Field(default_factory=datetime.now)
    message_type: MessageType
    payload: A2AMessagePayload
    metadata: A2AMessageMetadata = Field(default_factory=A2AMessageMetadata)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AgentCapability(BaseModel):
    """Agent能力定义"""
    name: str = Field(..., description="能力名称")
    description: str = Field(..., description="能力描述")
    input_schema: Dict[str, Any] = Field(default_factory=dict, description="输入数据结构")
    output_schema: Dict[str, Any] = Field(default_factory=dict, description="输出数据结构")
    estimated_duration: int = Field(default=10, description="预估执行时间(秒)")


class AgentRegistration(BaseModel):
    """Agent注册信息"""
    agent_id: str = Field(..., description="Agent唯一标识")
    agent_name: str = Field(..., description="Agent名称")
    description: str = Field(..., description="Agent描述")
    capabilities: List[AgentCapability] = Field(default_factory=list)
    status: AgentStatus = AgentStatus.ACTIVE
    load: float = Field(default=0.0, ge=0.0, le=1.0, description="负载水平 0-1")
    last_heartbeat: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class A2AProtocol:
    """A2A协议处理器"""
    
    def __init__(self):
        """初始化A2A协议处理器"""
        self.registered_agents: Dict[str, AgentRegistration] = {}
        self.message_history: List[A2AMessage] = []
        logger.info("A2A协议处理器初始化完成")
    
    def register_agent(self, registration: AgentRegistration) -> bool:
        """
        注册Agent
        
        Args:
            registration: Agent注册信息
            
        Returns:
            bool: 注册是否成功
        """
        try:
            agent_id = registration.agent_id
            self.registered_agents[agent_id] = registration
            logger.info(f"Agent注册成功: {agent_id} - {registration.agent_name}")
            return True
        except Exception as e:
            logger.error(f"Agent注册失败: {str(e)}")
            return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        注销Agent
        
        Args:
            agent_id: Agent ID
            
        Returns:
            bool: 注销是否成功
        """
        try:
            if agent_id in self.registered_agents:
                del self.registered_agents[agent_id]
                logger.info(f"Agent注销成功: {agent_id}")
                return True
            else:
                logger.warning(f"Agent不存在: {agent_id}")
                return False
        except Exception as e:
            logger.error(f"Agent注销失败: {str(e)}")
            return False
    
    def get_agent_info(self, agent_id: str) -> Optional[AgentRegistration]:
        """
        获取Agent信息
        
        Args:
            agent_id: Agent ID
            
        Returns:
            AgentRegistration: Agent注册信息
        """
        return self.registered_agents.get(agent_id)
    
    def list_agents(self, status: Optional[AgentStatus] = None) -> List[AgentRegistration]:
        """
        列出所有Agent
        
        Args:
            status: 过滤状态
            
        Returns:
            List[AgentRegistration]: Agent列表
        """
        agents = list(self.registered_agents.values())
        if status:
            agents = [a for a in agents if a.status == status]
        return agents
    
    def find_agent_by_capability(self, capability_name: str) -> List[AgentRegistration]:
        """
        根据能力查找Agent
        
        Args:
            capability_name: 能力名称
            
        Returns:
            List[AgentRegistration]: 具有该能力的Agent列表
        """
        result = []
        for agent in self.registered_agents.values():
            for capability in agent.capabilities:
                if capability.name == capability_name:
                    result.append(agent)
                    break
        return result
    
    def create_message(
        self,
        sender: str,
        receiver: str,
        message_type: MessageType,
        action: ActionType,
        data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
        priority: Priority = Priority.MEDIUM,
        timeout: int = 30
    ) -> A2AMessage:
        """
        创建A2A消息
        
        Args:
            sender: 发送者Agent ID
            receiver: 接收者Agent ID
            message_type: 消息类型
            action: 操作类型
            data: 消息数据
            context: 上下文信息
            priority: 优先级
            timeout: 超时时间
            
        Returns:
            A2AMessage: 创建的消息
        """
        message = A2AMessage(
            sender=sender,
            receiver=receiver,
            message_type=message_type,
            payload=A2AMessagePayload(
                action=action,
                data=data,
                context=context or {}
            ),
            metadata=A2AMessageMetadata(
                priority=priority,
                timeout=timeout
            )
        )
        
        # 保存到历史记录
        self.message_history.append(message)
        
        logger.debug(f"创建消息: {sender} -> {receiver}, 类型: {message_type}")
        return message
    
    def send_message(self, message: A2AMessage) -> Dict[str, Any]:
        """
        发送消息（模拟发送过程）
        
        Args:
            message: A2A消息
            
        Returns:
            Dict: 发送结果
        """
        try:
            # 验证接收者是否存在
            receiver_info = self.get_agent_info(message.receiver)
            if not receiver_info:
                logger.error(f"接收者Agent不存在: {message.receiver}")
                return {
                    "status": "error",
                    "message": f"接收者Agent不存在: {message.receiver}"
                }
            
            # 检查接收者状态
            if receiver_info.status == AgentStatus.OFFLINE:
                logger.error(f"接收者Agent离线: {message.receiver}")
                return {
                    "status": "error",
                    "message": f"接收者Agent离线: {message.receiver}"
                }
            
            logger.info(f"消息发送成功: {message.message_id}")
            return {
                "status": "success",
                "message_id": message.message_id,
                "timestamp": message.timestamp.isoformat()
            }
        except Exception as e:
            logger.error(f"消息发送失败: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def update_agent_status(self, agent_id: str, status: AgentStatus, load: Optional[float] = None):
        """
        更新Agent状态
        
        Args:
            agent_id: Agent ID
            status: 新状态
            load: 负载水平
        """
        if agent_id in self.registered_agents:
            self.registered_agents[agent_id].status = status
            self.registered_agents[agent_id].last_heartbeat = datetime.now()
            if load is not None:
                self.registered_agents[agent_id].load = load
            logger.debug(f"Agent状态更新: {agent_id} -> {status}")
    
    def get_message_history(self, agent_id: Optional[str] = None, limit: int = 100) -> List[A2AMessage]:
        """
        获取消息历史
        
        Args:
            agent_id: Agent ID（可选，用于过滤）
            limit: 返回数量限制
            
        Returns:
            List[A2AMessage]: 消息历史列表
        """
        messages = self.message_history
        if agent_id:
            messages = [m for m in messages if m.sender == agent_id or m.receiver == agent_id]
        return messages[-limit:]


# 全局A2A协议实例
a2a_protocol = A2AProtocol()


def get_a2a_protocol() -> A2AProtocol:
    """获取全局A2A协议实例"""
    return a2a_protocol
