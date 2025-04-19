# threads_# Threads Comment Generator

A FastAPI microservice that generates contextual comments for Threads posts using DeepSeek AI.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-green)

## 🚀 Features

- ✨ Contextual comment generation based on post text
- 🖼️ Image analysis for visual context
- 🔄 Support for replies to existing posts
- 🌐 Docker containerization
- 🧪 Automated testing

## 📋 Requirements

- Python 3.9+
- DeepSeek API key
- Docker (for containerized deployment)

## 🛠️ Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/threads-comment-service.git
cd threads-comment-service

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your DeepSeek API key

# Run the service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 🐳 Docker Deployment

```bash
# Build the Docker image
docker build -t comment-service .

# Run the container
docker run -d -p 8000:8000 --name comment-service \
  -e DEEPSEEK_API_KEY=your_api_key_here \
  comment-service

# Check logs
docker logs comment-service
```

## 🌐 API Usage

### Generate Comment

**Endpoint:** `POST /generate-comment`

**Request Example:**
```json
{
  "postId": "post123",
  "username": "traveler_jake",
  "text": "Just summited Mount Kilimanjaro! The view from the top is absolutely breathtaking.",
  "mediaType": "image",
  "imageUrls": ["https://example.com/kilimanjaro-summit.jpg"],
  "hashtags": ["adventure", "hiking", "mountains"],
  "language": "en",
  "isReply": false
}
```

**Response Example:**
```json
{
  "comment": "Epic achievement! That view is worth every step 🏔️"
}
```

### Health Check

**Endpoint:** `GET /ping`

**Response:**commenter
