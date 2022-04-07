from common.models.fundamental import BaseModel
from user import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Product(BaseModel):
    __tablename__ = 'product'

    name = db.Column(db.String(), nullable=False)
    brand = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

class Inventory(BaseModel):
    product = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'))
    stock = db.Column(db.Integer)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))
    #status = db.Column(db.String())
    #status = EnumField(enum=StockStatus, max_length=20, default=None, null=True)
    #_objects = BaseManager()