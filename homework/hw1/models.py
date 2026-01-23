from sqlalchemy import Column, Integer, String, Text
from .database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    cook_time_minutes = Column(Integer, nullable=False)
    views = Column(Integer, nullable=False, default=0)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
