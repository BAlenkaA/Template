from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.databases.database import Base


class Role(Base):
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="role",
        lazy="selectin"
    )

    def __repr__(self):
        return self.name


class User(Base):
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="selectin")


    def __repr__(self):
        return self.username
