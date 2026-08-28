from pydantic import BaseModel, Field
from typing import List, Dict, Any


class TripRequest(BaseModel):
    origin: str = Field(description="Starting location")
    destination: str = Field(description="Travel destination")
    days: int = Field(
        description="Number of travel days",
        ge=1,
        le=30
    )
    budget: float = Field(
        description="Total trip budget in PKR",
        gt=0
    )
    travelers: int = Field(
        description="Number of travelers",
        ge=1,
        le=20
    )
    interests: List[str] = Field(
        default_factory=list,
        description="User's travel interests"
    )
    transport_preference: str = Field(
        default="any",
        description="Preferred transport type"
    )


class ResearchResult(BaseModel):
    location: Dict[str, Any]
    weather: Dict[str, Any]
    places: List[Dict[str, Any]]