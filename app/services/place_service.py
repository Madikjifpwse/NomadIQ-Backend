from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from uuid import UUID

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

    def search_places(self, filters: PlaceSearchFilters, user_id: Optional[UUID] = None) -> PlaceListResponse:
        exclude_visited = filters.exclude_visited and user_id is not None
        places, total = self.place_repo.search(
            experience_level=filters.experience_level,
            category=filters.category,
            tags=filters.tags,
            user_id=user_id,
            exclude_visited=exclude_visited,
            latitude=filters.latitude,
            longitude=filters.longitude,
            radius_km=filters.radius_km,
            limit=filters.limit,
            offset=filters.offset
        )

        visited_ids = set()
        if user_id:
            visited_ids = set(self.visited_repo.get_visited_place_ids(user_id))

        place_responses = []
        for place in places:
            place_response = PlaceResponse.model_validate(place)
            place_response.is_visited = place.id in visited_ids
            if hasattr(place, 'distance_km'):
                place_response.distance_km = place.distance_km
            place_responses.append(place_response)
        has_more = (filters.offset + filters.limit) < total

        return PlaceListResponse(
            places=place_responses,
            total=total,
            limit=filters.limit,
            offset=filters.offset,
            has_more=has_more
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
            for tag in place.tags:
                self.place_repo.remove_tag(place_id, tag.tag)
            for tag in place_data.tags:
                self.place_repo.add_tag(place_id, tag)

        return PlaceResponse.model_validate(updated_place)

    def delete_place(self, place_id: UUID) -> None:
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found"
            )
        self.place_repo.delete(place)

    def get_all_places(self, limit: int = 100, offset: int = 0, user_id: Optional[UUID] = None) -> PlaceListResponse:
        places, total = self.place_repo.get_all(limit=limit, offset=offset)
        visited_ids = set()
        if user_id:
            visited_ids = set(self.visited_repo.get_visited_place_ids(user_id))

        place_responses = []
        for place in places:
            place_response = PlaceResponse.model_validate(place)
            place_response.is_visited = place.id in visited_ids
            place_responses.append(place_response)
        has_more = (offset + limit) < total

        return PlaceListResponse(
            places=place_responses,
            total=total,
            limit=limit,
            offset=offset,
            has_more=has_more
        )