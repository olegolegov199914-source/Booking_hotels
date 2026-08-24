from sqlalchemy import Column, Integer, ForeignKey, Date, Computed, String, JSON
from app.database import Base
from sqlalchemy.orm import relationship

class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key = True, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    servisces = Column(JSON, nullable=True)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    booking = relationship("Bookings", back_populates="room")
    hotel = relationship("Hotels", back_populates="rooms")

    def __str__(self):
        return f"Номер {self.name}"
