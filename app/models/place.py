from sqlalchemy import Column, String, Text, Integer, Numeric, DateTime, Index, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.database import Base


class PlaceCategory(str, enum.Enum):
    MUST_SEE = "must_see"
    STUDENT_FRIENDLY = "student_friendly"
    LOCAL_SECRET = "local_secret"


class Place(Base):
    __tablename__ = "places"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    google_place_id = Column(String(255), unique=True, nullable=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=True, index=True)
    place_type = Column(String(50), nullable=True, index=True, default="other")
    rating = Column(Float, default=4.5)
    latitude = Column(Numeric(10, 8), nullable=False)
    longitude = Column(Numeric(11, 8), nullable=False)
    address = Column(Text, nullable=True)
    popularity_score = Column(Integer, default=50, nullable=False)  # 0-100
    image_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tags = relationship("PlaceTag", back_populates="place", cascade="all, delete-orphan")
    visited_by = relationship("VisitedPlace", back_populates="place", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Place {self.name} (pop: {self.popularity_score})>"

    @property
    def is_for_first_timer(self) -> bool:
        return self.popularity_score >= 60

    @property
    def is_for_advanced(self) -> bool:
        return self.popularity_score <= 40

Index('idx_place_location', Place.latitude, Place.longitude)