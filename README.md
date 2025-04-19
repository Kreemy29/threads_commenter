# Threads Comment Generator

A FastAPI service that generates contextual comments for Threads posts using DeepSeek AI.

## Features

- Generate contextual comments based on text content
- Analyze images to provide relevant responses
- Clean, modular codebase structure
- Environment-based configuration
- Docker support for easy deployment

## Development Setup

```bash
# Clone & run locally
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # add your DeepSeek key here
```

## Environment Variables

Set the following in `.env` file:

- `DEEPSEEK_API_KEY` - Your DeepSeek API key

## Running Locally

```bash
# Start the service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker Deployment

```bash
# Build Docker image
docker build -t comment-service .

# Run container
docker run -d -p 8000:8000 --name comment-service \
  -e DEEPSEEK_API_KEY=your_api_key_here \
  comment-service
```

## API Usage

### Generate Comment Endpoint

`POST /generate-comment`

Sample request:
```json
{
  "postId": "post123",
  "username": "user_account",
  "text": "Just hiked to the top of Mount Rainier today!",
  "mediaType": "image",
  "imageUrls": ["https://example.com/mountain.jpg"],
  "hashtags": ["hiking", "nature"],
  "language": "en",
  "isReply": false
}
```

Sample response:
```json
{
  "comment": "Amazing view from the summit! 🏔️"
}
```

## Testing

```bash
# Run tests
pytest -q
```

## Project Structure

```
.
├─ app/
│  ├─ main.py             # FastAPI entrypoint
│  ├─ api.py              # FastAPI router with endpoints
│  ├─ models.py           # Pydantic models
│  ├─ services/
│  │   ├─ comment.py      # Comment generation logic
│  │   ├─ vision.py       # Image description helper
│  │   └─ __init__.py
│  └─ config.py           # Environment configuration
├─ tests/
│  ├─ test_health.py      # Test health endpoint
│  └─ test_comment.py     # Test comment generation
└─ ...
``` 