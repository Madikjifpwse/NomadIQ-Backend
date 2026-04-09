from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional
from uuid import UUID

from app.repositories.visited_repository import VisitedPlaceRepository
from app.repositories.place_repository import PlaceRepository
from app.schemas.visited import (
    VisitedPlaceCreate,
    VisitedPlaceUpdate,
    VisitedPlaceResponse,
    VisitedPlaceWithDetails,
    VisitedPlaceListResponse,
    VisitedPlaceStats
)
from app.schemas.place import PlaceResponse

class VisitedPlaceService:
    def __init__(self, db: Session):
        self.db = db
        self.visited_repo = VisitedPlaceRepository(db)
        self.place_repo = PlaceRepository(db)

    def mark_as_visited(self, user_id: UUID, visit_data: VisitedPlaceCreate) -> VisitedPlaceResponse:
        place = self.place_repo.get_by_id(visit_data.place_id)
        if not place:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Place not found"
            )

        existing_visit = self.visited_repo.get_by_user_and_place(user_id, visit_data.place_id)
        if existing_visit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Place already marked as visited. Use update endpoint to modify."
            )

        try:
            visited = self.visited_repo.create(
                user_id=user_id,
                place_id=visit_data.place_id,
                rating=visit_data.rating,
                notes=visit_data.notes
            )
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to mark place as visited"
            )
        return VisitedPlaceResponse.model_validate(visited)

    def update_visited(
            self,
            user_id: UUID,
            place_id: UUID,
            update_data: VisitedPlaceUpdate
    ) -> VisitedPlaceResponse:
        visited = self.visited_repo.get_by_user_and_place(user_id, place_id)
        if not visited:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visit record not found"
            )

        updated_visit = self.visited_repo.update(
            visited,
            rating=update_data.rating,
            notes=update_data.notes
        )

        return VisitedPlaceResponse.model_validate(updated_visit)

    def remove_visited(self, user_id: UUID, place_id: UUID) -> None:
        deleted = self.visited_repo.delete_by_user_and_place(user_id, place_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visit record not found"
            )

    def get_user_visited_places(
            self,
            user_id: UUID,
            limit: int = 50,
            offset: int = 0
    ) -> VisitedPlaceListResponse:
        visited_places, total = self.visited_repo.get_user_visited_places(
            user_id=user_id,
            limit=limit,
            offset=offset
        )

        visited_responses = []
        for visited in visited_places:
            visited_response = VisitedPlaceWithDetails.model_validate(visited)
            if visited.place:
                visited_response.place = PlaceResponse.model_validate(visited.place)
                visited_response.place.is_visited = True
            visited_responses.append(visited_response)
        has_more = (offset + limit) < total

        return VisitedPlaceListResponse(
            visited_places=visited_responses,
            total=total,
            limit=limit,
            offset=offset,
            has_more=has_more
        )

    def get_user_statistics(self, user_id: UUID) -> VisitedPlaceStats:
        stats = self.visited_repo.get_user_statistics(user_id)

        return VisitedPlaceStats(
            total_visited=stats['total_visited'],
            average_rating=stats['average_rating'],
            most_common_category=stats['most_common_category'],
            most_common_tags=stats['most_common_tags']
        )

    def check_if_visited(self, user_id: UUID, place_id: UUID) -> bool:
        return self.visited_repo.is_place_visited(user_id, place_id)