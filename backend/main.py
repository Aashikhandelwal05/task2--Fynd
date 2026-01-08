"""
FastAPI application with review endpoints.
"""
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db, init_db
from models import Review
from schemas import (
    ReviewSubmitRequest,
    ReviewSubmitResponse,
    ReviewListItem,
    ErrorResponse
)
from llm import (
    generate_user_response,
    generate_admin_summary,
    generate_recommended_action
)

app = FastAPI(
    title="Feedback API",
    description="API for customer feedback analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/", tags=["Health"])
async def root():
    return {"status": "healthy", "message": "Feedback API is running"}


@app.post(
    "/submit-review",
    response_model=ReviewSubmitResponse,
    responses={400: {"model": ErrorResponse}},
    tags=["Reviews"]
)
async def submit_review(
    request: ReviewSubmitRequest,
    db: Session = Depends(get_db)
):
    """Submit a customer review and receive a generated response."""
    try:
        review_text = request.review.strip()
        if not review_text:
            raise HTTPException(status_code=400, detail="Review cannot be empty")

        # Generate responses server-side
        ai_response = generate_user_response(request.rating, review_text)
        ai_summary = generate_admin_summary(request.rating, review_text)
        recommended_action = generate_recommended_action(request.rating, review_text)

        db_review = Review(
            rating=request.rating,
            review_text=review_text,
            ai_response=ai_response,
            ai_summary=ai_summary,
            recommended_action=recommended_action
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)

        return ReviewSubmitResponse(status="success", ai_response=ai_response)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error submitting review: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your review. Please try again."
        )


@app.get(
    "/reviews",
    response_model=List[ReviewListItem],
    tags=["Reviews"]
)
async def get_reviews(db: Session = Depends(get_db)):
    """Retrieve all reviews for the admin dashboard."""
    try:
        reviews = db.query(Review).order_by(Review.created_at.desc()).all()
        
        return [
            ReviewListItem(
                id=review.id,
                rating=review.rating,
                review=review.review_text,
                ai_summary=review.ai_summary,
                recommended_action=review.recommended_action,
                created_at=review.created_at
            )
            for review in reviews
        ]

    except Exception as e:
        print(f"Error retrieving reviews: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving reviews.")
