from pydantic import BaseModel


class MsRequest(BaseModel):
    """Валидация сообщения"""
    dt_from: str
    dt_upto: str
    group_type: str
