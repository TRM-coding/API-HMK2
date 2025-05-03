from datetime import datetime, date
import enum, decimal, uuid

def to_dict(model):
    d = {}
    for col in model.__table__.columns:
        val = getattr(model, col.name)
        # 新增：Enum 转基础值
        if isinstance(val, enum.Enum):
            val = val.value
        # 新增：Decimal/UUID 转字符串
        elif isinstance(val, (decimal.Decimal, uuid.UUID)):
            val = str(val)
        # 同时对 datetime 和 date 类型做 ISO 序列化
        if isinstance(val, (datetime, date)):
            val = val.isoformat()
        d[col.name] = val
    return d
