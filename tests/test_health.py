"""
Tests for the health check endpoint.
"""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test that the /ping endpoint returns 'pong'."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/ping")
        assert response.status_code == 200
        assert response.text == '"pong"'


@pytest.mark.asyncio
async def test_docs_endpoint():
    """Test that the /docs endpoint returns 200."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/docs")
        assert response.status_code == 200 