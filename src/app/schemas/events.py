from pydantic import BaseModel
from typing import Any, Dict

class SystemEvent(BaseModel):
    """
    系统事件的基础模型。
    """
    event_type: str
    payload: Dict[str, Any]
