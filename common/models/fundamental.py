import datetime
import uuid
from sqlalchemy.ext.declarative import declared_attr

from user import db
from sqlalchemy.dialects.postgresql import UUID


class Auditable(db.Model):
    __abstract__ = True

    deleted = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime,default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow )
    modified_on = db.Column(db.DateTime,default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    deleted_on = db.Column(db.DateTime, nullable=True, onupdate=datetime.datetime.utcnow)

    @declared_attr
    def created_by(cls):
        return db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

    @declared_attr
    def modified_by(cls):
        return db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

    @declared_attr
    def deleted_by(cls):
        return db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

    def save(self, current_user):
        if not self.created_by:  # check if it's an insert via pk does not work
            self.created_by = current_user.id

        self.modified_by = current_user.id


class BaseModel(Auditable):
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
