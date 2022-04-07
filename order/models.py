from fundamental import OrderType, ReturnReason,OrderStatus
from user import db
from sqlalchemy.types import Enum
from sqlalchemy.dialects.postgresql import UUID
from common.models.fundamental import BaseModel
import uuid



class Order(BaseModel):
    __tablename__ = 'order'
    name = db.Column(db.String(), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    product = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'))
    qty = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String())
    payment_method = db.Column(db.String())
    price = db.Column(db.Float, default=0.0)
    status = db.Column(db.Enum(OrderStatus))
    order_type = db.Column(db.Enum(OrderType))
    reason = db.Column(db.Enum(ReturnReason))

