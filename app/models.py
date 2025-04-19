"""
Pydantic models for API request and response data structures.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Parent(BaseModel):
    """Parent post content for replies."""
    username: str
    text: str


class PostIn(BaseModel):
    """Input model for post data to generate a comment."""
    postId: str
    username: str
    text: Optional[str] = None
    mediaType: str = Field("text", pattern="^(text|image|video)$")
    mediaDesc: Optional[str] = None
    imageUrls: List[str] = Field(default_factory=list)
    hashtags: List[str] = Field(default_factory=list)
    language: str = "en"
    isReply: bool = False
    parentContent: Optional[Parent] = None
    hasQuestion: bool = False 