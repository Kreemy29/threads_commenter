"""
Tests for the comment generation endpoint.
"""

import pytest
from httpx import AsyncClient
from app.main import app
from app.config import DEEPSEEK_API_KEY


@pytest.mark.asyncio
async def test_minimal_post():
    """Test generating a comment with minimal post data."""
    payload = {
        "postId": "test123",
        "username": "testuser",
        "mediaType": "text"
    }
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/generate-comment", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "comment" in data
        assert data["comment"] == "Hey @testuser! 👋"


@pytest.mark.asyncio
async def test_post_with_image():
    """Test generating a comment with an image URL."""
    # Skip if no API key is configured
    if not DEEPSEEK_API_KEY:
        pytest.skip("DEEPSEEK_API_KEY not configured")
        
    payload = {
        "postId": "img456",
        "username": "imageuser",
        "mediaType": "image",
        "imageUrls": ["https://example.com/sample-image.jpg"]
    }
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/generate-comment", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "comment" in data 