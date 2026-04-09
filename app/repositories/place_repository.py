from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func
from typing import List, Optional, Tuple
from uuid import UUID
from decimal import Decimal

from app.models.place import Place, PlaceCategory
from app.models.place_tag import PlaceTag
from app.models.visited_place import VisitedPlace
from app.models.user import ExperienceLevel
from app.utils.geo import get_bounding_box, haversine_distance


class PlaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, place_data: dict, tags: List[str] = None) -> Place:
        place = Place(**place_data)
        self.db.add(place)
        self.db.flush()

        if tags:
            for tag in tags:
                place_tag = PlaceTag(place_id=place.id, tag=tag.lower().strip())
                self.db.add(place_tag)

        self.db.commit()
        self.db.refresh(place)
        return place

    def get_by_id(self, place_id: UUID) -> Optional[Place]:
        return self.db.query(Place).options(
            joinedload(Place.tags)
        ).filter(Place.id == place_id).first()

    def get_by_google_place_id(self, google_place_id: str) -> Optional[Place]:
        return self.db.query(Place).filter(Place.google_place_id == google_place_id).first()

    def search(
            self,
            experience_level: Optional[ExperienceLevel] = None,
            category: Optional[str] = None,
            tags: Optional[List[str]] = None,
            user_id: Optional[UUID] = None,
            exclude_visited: bool = True,
            latitude: Optional[float] = None,
            longitude: Optional[float] = None,
            radius_km: Optional[float] = None,
            limit: int = 20,
            offset: int = 0
    ) -> Tuple[List[Place], int]:
        query = self.db.query(Place).options(joinedload(Place.tags))

        if experience_level == ExperienceLevel.FIRST_TIMER:
            query = query.filter(Place.popularity_score >= 60)
        elif experience_level == ExperienceLevel.ADVANCED:
            query = query.filter(Place.popularity_score <= 40)
        if category:
            query = query.filter(Place.category == category)
        if tags:
            tag_filters = [PlaceTag.tag == tag.lower() for tag in tags]
            query = query.join(Place.tags).filter(or_(*tag_filters))
        if exclude_visited and user_id:
            visited_subquery = self.db.query(VisitedPlace.place_id).filter(
                VisitedPlace.user_id == user_id
            ).subquery()
            query = query.filter(~Place.id.in_(visited_subquery))
        if latitude is not None and longitude is not None and radius_km is not None:
            min_lat, max_lat, min_lon, max_lon = get_bounding_box(latitude, longitude, radius_km)
            query = query.filter(
                and_(
                    Place.latitude >= min_lat,
                    Place.latitude <= max_lat,
                    Place.longitude >= min_lon,
                    Place.longitude <= max_lon
                )
            )
        total = query.count()

        places = query.limit(limit).offset(offset).all()

        if latitude is not None and longitude is not None:
            for place in places:
                distance = haversine_distance(
                    latitude, longitude,
                    float(place.latitude), float(place.longitude)
                )
                place.distance_km = distance

            if radius_km is not None:
                places = [p for p in places if p.distance_km <= radius_km]
                total = len(places)
                places.sort(key=lambda p: p.distance_km)
        return places, total

    def get_all(self, limit: int = 100, offset: int = 0) -> Tuple[List[Place], int]:
        query = self.db.query(Place).options(joinedload(Place.tags))
        total = query.count()
        places = query.limit(limit).offset(offset).all()
        return places, total

    def update(self, place: Place, **kwargs) -> Place:
        for key, value in kwargs.items():
            if hasattr(place, key) and value is not None:
                setattr(place, key, value)

        self.db.commit()
        self.db.refresh(place)
        return place

    def delete(self, place: Place) -> None:
        self.db.delete(place)
        self.db.commit()

    def add_tag(self, place_id: UUID, tag: str) -> PlaceTag:
        place_tag = PlaceTag(place_id=place_id, tag=tag.lower().strip())
        self.db.add(place_tag)
        self.db.commit()
        self.db.refresh(place_tag)
        return place_tag

    def remove_tag(self, place_id: UUID, tag: str) -> bool:
        deleted = self.db.query(PlaceTag).filter(
            and_(PlaceTag.place_id == place_id, PlaceTag.tag == tag.lower())
        ).delete()
        self.db.commit()
        return deleted > 0

    def get_visit_statistics(self, place_id: UUID) -> dict:
        stats = self.db.query(
            func.count(VisitedPlace.id).label('visit_count'),
            func.avg(VisitedPlace.rating).label('average_rating')
        ).filter(VisitedPlace.place_id == place_id).first()

        return {
            'visit_count': stats.visit_count or 0,
            'average_rating': float(stats.average_rating) if stats.average_rating else None
        }