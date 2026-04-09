from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base


class VisitedPlace(Base):
    __tablename__ = "visited_places"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    place_id = Column(UUID(as_uuid=True), ForeignKey("places.id", ondelete="CASCADE"), nullable=False, index=True)
    visited_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 stars
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="visited_places")
    place = relationship("Place", back_populates="visited_by")

    __table_args__ = (
        UniqueConstraint('user_id', 'place_id', name='uq_user_place_visit'),
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

    def __repr__(self):
        return f"<VisitedPlace user={self.user_id} place={self.place_id}>"