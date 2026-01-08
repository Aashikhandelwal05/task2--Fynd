"""
LLM integration using OpenRouter API.
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "meta-llama/llama-3.1-8b-instruct"

client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
)

# Fallback responses for API failures
FALLBACK_USER_RESPONSE = "Thank you for your feedback! We appreciate you taking the time to share your experience with us."
FALLBACK_SUMMARY = "Customer feedback received. Manual review recommended."
FALLBACK_ACTION = "Review this feedback manually and respond appropriately."


def _call_llm(prompt: str, system_message: str) -> str:
    """Make an LLM API call and return the response content."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def generate_user_response(rating: int, review_text: str) -> str:
    """Generate a customer-facing response to their review."""
    try:
        if not review_text or not review_text.strip():
            return FALLBACK_USER_RESPONSE

        system_message = """You are a friendly customer service representative. Generate a warm, 
        personalized response to customer feedback. Be appreciative and professional.
        Keep the response under 100 words. Return ONLY the response text, no JSON."""

        prompt = f"""Customer Rating: {rating}/5
Customer Review: {review_text}

Generate a personalized thank you response for this customer."""

        response = _call_llm(prompt, system_message)
        return response if response else FALLBACK_USER_RESPONSE
        
    except Exception as e:
        print(f"LLM Error (user_response): {e}")
        return FALLBACK_USER_RESPONSE


def generate_admin_summary(rating: int, review_text: str) -> str:
    """Generate a concise summary of the review for admin dashboard."""
    try:
        if not review_text or not review_text.strip():
            return FALLBACK_SUMMARY

        # Truncate very long reviews to avoid token limits
        truncated_review = review_text[:2000] if len(review_text) > 2000 else review_text

        system_message = """You are an analyst. Summarize customer feedback in 1-2 sentences.
        Focus on key points, sentiment, and any specific issues mentioned.
        Return ONLY the summary text, no JSON or formatting."""

        prompt = f"""Rating: {rating}/5
Review: {truncated_review}

Provide a brief admin summary of this feedback."""

        response = _call_llm(prompt, system_message)
        return response if response else FALLBACK_SUMMARY
        
    except Exception as e:
        print(f"LLM Error (admin_summary): {e}")
        return FALLBACK_SUMMARY


def generate_recommended_action(rating: int, review_text: str) -> str:
    """Generate recommended action for admin based on the review."""
    try:
        if not review_text or not review_text.strip():
            return FALLBACK_ACTION

        # Truncate very long reviews
        truncated_review = review_text[:2000] if len(review_text) > 2000 else review_text

        system_message = """You are a customer success manager. Based on the feedback, 
        suggest ONE specific, actionable next step for the support team.
        Keep it under 50 words. Return ONLY the action, no JSON or formatting."""

        prompt = f"""Rating: {rating}/5
Review: {truncated_review}

What is the single most important action to take for this customer?"""

        response = _call_llm(prompt, system_message)
        return response if response else FALLBACK_ACTION
        
    except Exception as e:
        print(f"LLM Error (recommended_action): {e}")
        return FALLBACK_ACTION
