from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from werkzeug.security import generate_password_hash, check_password_hash

from .base import *


class User(Base):
    __tablename__ = "user"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    full_name = Column(String(250), nullable=False)
    login = Column(String(250), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    token = Column(UUID(as_uuid=True), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if check_password_hash(self.password_hash, password):
            return True


