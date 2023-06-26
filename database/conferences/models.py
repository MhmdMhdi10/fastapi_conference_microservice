from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship
from database.database import Base


class Conferences(Base):
    __tablename__ = "conferences"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    Capacity = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="conference")

    def __repr__(self):
        return f"Order : {self.id}"
