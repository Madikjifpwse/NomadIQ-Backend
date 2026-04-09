from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.models.user import User, ExperienceLevel
from app.repositories.place_repository import PlaceRepository
from app.repositories.visited_repository import VisitedPlaceRepository
from app.schemas.place import PlaceResponse, PlaceListResponse


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        self.place_repo = PlaceRepository(db)
        self.visited_repo = VisitedPlaceRepository(db)

    def get_recommendations(
            self,
            user: User,
            experience_level: Optional[ExperienceLevel] = None,
            category: Optional[str] = None,
            tags: Optional[List[str]] = None,
            latitude: Optional[float] = None,
            longitude: Optional[float] = None,
            radius_km: Optional[float] = None,
            limit: int = 10
    ) -> PlaceListResponse:
        exp_level = experience_level or user.experience_level
        stats = self.visited_repo.get_user_statistics(user.id)
        preferred_tags = stats['most_common_tags'][:3] if not tags else tags
        places, total = self.place_repo.search(
            experience_level=exp_level,
            category=category,
            tags=preferred_tags if preferred_tags else None,
            user_id=user.id,
            exclude_visited=True,
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            limit=limit * 2,
            offset=0
        )
        visited_ids = set(self.visited_repo.get_visited_place_ids(user.id))
        scored_places = []
        for place in places:
            score = self._score_place(
                place=place,
                user_experience_level=exp_level,
                user_preferred_tags=preferred_tags,
                has_location=latitude is not None and longitude is not None
            )
            scored_places.append((place, score))
        scored_places.sort(key=lambda x: x[1], reverse=True)
        top_places = [place for place, score in scored_places[:limit]]
        place_responses = []
        for place in top_places:
            place_response = PlaceResponse.model_validate(place)
            place_response.is_visited = False
            if hasattr(place, 'distance_km'):
                place_response.distance_km = place.distance_km
            place_responses.append(place_response)
        has_more = len(scored_places) > limit

        return PlaceListResponse(
            places=place_responses,
            total=len(top_places),
            limit=limit,
            offset=0,
            has_more=has_more
        )

    def _score_place(
            self,
            place,
            user_experience_level: ExperienceLevel,
            user_preferred_tags: List[str],
            has_location: bool
    ) -> float:
        score = 0.0
        if user_experience_level == ExperienceLevel.FIRST_TIMER:
            score += (place.popularity_score / 100.0) * 40
        else:
            score += ((100 - place.popularity_score) / 100.0) * 40
        if user_preferred_tags and place.tags:
            place_tag_set = set(tag.tag for tag in place.tags)
            matching_tags = len(set(user_preferred_tags) & place_tag_set)
            max_possible_matches = min(len(user_preferred_tags), len(place_tag_set))
            if max_possible_matches > 0:
                tag_match_ratio = matching_tags / max_possible_matches
                score += tag_match_ratio * 30

        normalized_popularity = place.popularity_score / 100.0
        score += normalized_popularity * 20
        if has_location and hasattr(place, 'distance_km'):
            if place.distance_km <= 1:
                score += 10
            elif place.distance_km <= 5:
                score += 5 * (1 - (place.distance_km - 1) / 4)
            elif place.distance_km <= 10:
                score += 2.5 * (1 - (place.distance_km - 5) / 5)
        return score

    def get_nearby_recommendations(
            self,
            user: User,
            latitude: float,
            longitude: float,
            radius_km: float = 5.0,
            limit: int = 10
    ) -> PlaceListResponse:
        return self.get_recommendations(
            user=user,
            latitude=latitude,
            longitude=longitude,
            radius_km=radius_km,
            limit=limit
        )