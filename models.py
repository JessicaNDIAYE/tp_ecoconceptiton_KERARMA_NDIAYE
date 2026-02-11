from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(100), nullable=False)
    species_id = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    base_experience = Column(Integer)
    order = Column(Integer)
    is_default = Column(Boolean)