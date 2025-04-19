"""
FastAPI router with endpoint for generating comments.
"""

from fastapi import APIRouter, HTTPException
from app.models import PostIn
from app.services.vision import describe_image
from app.services.comment import make_comment

router = APIRouter()


@router.get("/ping")
async def health_check():
    """Health check endpoint."""
    return "pong"


@router.post("/generate-comment")
async def generate_comment(post: PostIn):
    """
    Accepts a single post payload and returns {"comment": "..."}.
    """
    try:
        data = post.dict()

        # If caller didn't caption image, try here (only first URL)
        if not data["mediaDesc"] and data["imageUrls"]:
            data["mediaDesc"] = await describe_image(data["imageUrls"][0])

        # Generate comment based on post data
        comment = await make_comment(data)

        return {"comment": comment}
    except Exception as e:
        raise HTTPException(500, str(e)) 