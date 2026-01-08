"""
SQLAlchemy models.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime
from database import Base


class Review(Base):
    """Customer review with LLM-generated analysis."""
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review(id={self.id}, rating={self.rating})>"
