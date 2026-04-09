from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime

from app.models.visited_place import VisitedPlace
from app.models.place import Place


class VisitedPlaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
            self,
            user_id: UUID,
            place_id: UUID,
            rating: Optional[int] = None,
            notes: Optional[str] = None
    ) -> VisitedPlace:
        visited = VisitedPlace(
            user_id=user_id,
            place_id=place_id,
            rating=rating,
            notes=notes,
            visited_at=datetime.utcnow()
        )
        self.db.add(visited)
        self.db.commit()
        self.db.refresh(visited)
        return visited

    def get_by_id(self, visited_id: UUID) -> Optional[VisitedPlace]:
        return self.db.query(VisitedPlace).filter(VisitedPlace.id == visited_id).first()

    def get_by_user_and_place(self, user_id: UUID, place_id: UUID) -> Optional[VisitedPlace]:
        return self.db.query(VisitedPlace).filter(
            VisitedPlace.user_id == user_id,
            VisitedPlace.place_id == place_id
        ).first()

    def get_user_visited_places(
            self,
            user_id: UUID,
            limit: int = 50,
            offset: int = 0
    ) -> Tuple[List[VisitedPlace], int]:
        query = self.db.query(VisitedPlace).options(
            joinedload(VisitedPlace.place).joinedload(Place.tags)
        ).filter(VisitedPlace.user_id == user_id).order_by(
            desc(VisitedPlace.visited_at)
        )

        total = query.count()
        visited_places = query.limit(limit).offset(offset).all()

        return visited_places, total

    def update(
            self,
            visited: VisitedPlace,
            rating: Optional[int] = None,
            notes: Optional[str] = None
    ) -> VisitedPlace:
        if rating is not None:
            visited.rating = rating
        if notes is not None:
            visited.notes = notes

        self.db.commit()
        self.db.refresh(visited)
        return visited

    def delete(self, visited: VisitedPlace) -> None:
        self.db.delete(visited)
        self.db.commit()

    def delete_by_user_and_place(self, user_id: UUID, place_id: UUID) -> bool:
        deleted = self.db.query(VisitedPlace).filter(
            VisitedPlace.user_id == user_id,
            VisitedPlace.place_id == place_id
        ).delete()
        self.db.commit()
        return deleted > 0

    def get_user_statistics(self, user_id: UUID) -> dict:
        stats = self.db.query(
            func.count(VisitedPlace.id).label('total_visited'),
            func.avg(VisitedPlace.rating).label('average_rating')
        ).filter(VisitedPlace.user_id == user_id).first()

        most_common_category = self.db.query(
            Place.category,
            func.count(Place.category).label('count')
        ).join(VisitedPlace).filter(
            VisitedPlace.user_id == user_id,
            Place.category.isnot(None)
        ).group_by(Place.category).order_by(desc('count')).first()

        from app.models.place_tag import PlaceTag
        most_common_tags = self.db.query(
            PlaceTag.tag,
            func.count(PlaceTag.tag).label('count')
        ).join(Place).join(VisitedPlace).filter(
            VisitedPlace.user_id == user_id
        ).group_by(PlaceTag.tag).order_by(desc('count')).limit(5).all()

        return {
            'total_visited': stats.total_visited or 0,
            'average_rating': float(stats.average_rating) if stats.average_rating else None,
            'most_common_category': most_common_category.category if most_common_category else None,
            'most_common_tags': [tag.tag for tag in most_common_tags]
        }

    def is_place_visited(self, user_id: UUID, place_id: UUID) -> bool:
        return self.db.query(VisitedPlace).filter(
            VisitedPlace.user_id == user_id,
            VisitedPlace.place_id == place_id
        ).count() > 0

    def get_visited_place_ids(self, user_id: UUID) -> List[UUID]:
        visited = self.db.query(VisitedPlace.place_id).filter(
            VisitedPlace.user_id == user_id
        ).all()
        return [v.place_id for v in visited]