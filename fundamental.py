import enum
from sqlalchemy import Integer, Enum

class BusinessType(enum.Enum):
    CLIENT = 'client'
    SUPPLIER = 'supplier'


class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    NONE = "none"
    ALL = "all"


class TaskPriority(enum.Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class Language(enum.Enum):
    ENGLISH = 'en'

class OrderStatus(enum.Enum):
    PLACED = "order has been placed"
    PROCEED = "seller has processed order"
    SHIPPED = "item has been shipped"
    DELIVERED = "item has delivered"
    REJECTED = "request has rejected"
    RETURN_REQUEST = "order return request has sent"
    RETURNED = "order has return successfully"
    CANCELED = "order has canceled"
    PENDING = "return request is pending"


class StockStatus(enum.Enum):
    AVAILABLE = "Available"
    STOCK_OUT = "out of stock"

class OrderType(enum.Enum):
    BUY = "buy order"
    RETURN = "return order"

class ReturnReason(enum.Enum):
    PACKAGING = 'bad packing'
    INFERIORITY = 'quality is not good'

