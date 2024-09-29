from database.db import db
from sqlalchemy import String, Boolean, UUID
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class User(db.Model):
    id: Mapped[str] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(
        String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def __init__(self, email=None, password=None, is_admin=None):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
