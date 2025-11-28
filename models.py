from sqlalchemy.orm import Mapped, mapped_column
from db import Base



class Photos(Base):
    __tablename__="photos"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column(nullable=True)





