"""
Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class ReviewSubmitRequest(BaseModel):
    """Request body for submitting a review."""
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    review: str = Field(..., min_length=1, max_length=5000, description="Review text")

    @field_validator("review")
    @classmethod
    def validate_review(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Review cannot be empty or contain only whitespace")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"rating": 5, "review": "Excellent product! Fast shipping and great quality."}
            ]
        }
    }


class ReviewSubmitResponse(BaseModel):
    """Response body after submitting a review."""
    status: str = Field(..., description="Status of the submission")
    ai_response: str = Field(..., description="Generated response to the customer")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"status": "success", "ai_response": "Thank you for your wonderful feedback!"}
            ]
        }
    }


class ReviewListItem(BaseModel):
    """Single review item for admin dashboard."""
    id: int
    rating: int
    review: str
    ai_summary: Optional[str] = None
    recommended_action: Optional[str] = None
    created_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "rating": 4,
                    "review": "Good product overall.",
                    "ai_summary": "Positive feedback with minor suggestions.",
                    "recommended_action": "Send thank you email.",
                    "created_at": "2024-01-15T10:30:00"
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Error response body."""
    status: str = "error"
    message: str
