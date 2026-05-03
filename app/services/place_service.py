from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID

from app.models import Place
from app.models.user import ExperienceLevel
from app.repositories.place_repository import PlaceRepository
from app.repositories.visited_repository import VisitedPlaceRepository
from app.schemas.place import (
    PlaceCreate,
    PlaceUpdate,
    PlaceSearchFilters,
    PlaceResponse,
    PlaceDetailResponse,
    PlaceListResponse
)


class PlaceService:

    def __init__(self, db: Session):
        self.db = db
        self.place_repo = PlaceRepository(db)
        self.visited_repo = VisitedPlaceRepository(db)

    def create_place(self, place_data: PlaceCreate) -> PlaceResponse:
        if place_data.google_place_id:
            existing = self.place_repo.get_by_google_place_id(place_data.google_place_id)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Place with Google Place ID {place_data.google_place_id} already exists"
                )
        tags = place_data.tags or []
        place_dict = place_data.model_dump(exclude={'tags'})
        place = self.place_repo.create(place_dict, tags=tags)
        return PlaceResponse.model_validate(place)

    def get_place_by_id(self, place_id: UUID, user_id: Optional[UUID] = None) -> PlaceDetailResponse:
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found"
            )
        stats = self.place_repo.get_visit_statistics(place_id)

        place_response = PlaceDetailResponse.model_validate(place)
        place_response.visit_count = stats['visit_count']
        place_response.average_rating = stats['average_rating']
        if user_id:
            place_response.is_visited = self.visited_repo.is_place_visited(user_id, place_id)

        return place_response

    def search_places(self, filters: PlaceSearchFilters, user_id: Optional[UUID] = None):
        query = self.db.query(Place)

        if filters.category:
            query = query.filter(Place.category == filters.category)

        if filters.experience_level:
            if filters.experience_level == "first_timer" or filters.experience_level == ExperienceLevel.FIRST_TIMER:
                query = query.filter(Place.popularity_score >= 60)
            elif filters.experience_level == "advanced" or filters.experience_level == ExperienceLevel.ADVANCED:
                query = query.filter(Place.popularity_score <= 40)

        if filters.tags:
            pass

        total = query.count()
        places = query.offset(filters.offset).limit(filters.limit).all()

        visited_ids = set()
        if user_id:
            visited_ids = set(self.visited_repo.get_visited_place_ids(user_id))

        results = []
        for p in places:
            res = PlaceResponse.model_validate(p)
            res.is_visited = p.id in visited_ids
            results.append(res)

        return PlaceListResponse(
            places=results,
            total=total,
            limit=filters.limit,
            offset=filters.offset,
            has_more=total > (filters.offset + filters.limit)
        )

    def update_place(self, place_id: UUID, place_data: PlaceUpdate) -> PlaceResponse:
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found"
            )
        update_dict = place_data.model_dump(exclude_unset=True, exclude={'tags'})
        updated_place = self.place_repo.update(place, **update_dict)
        if place_data.tags is not None:
            pass

        return PlaceResponse.model_validate(updated_place)

    def delete_place(self, place_id: UUID) -> None:
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")
        self.place_repo.delete(place)