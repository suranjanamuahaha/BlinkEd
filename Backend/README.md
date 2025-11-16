# BlinkEd Backend - AI Video Generation API

A FastAPI-based backend for BlinkEd, an AI-powered video generation platform that converts text prompts into engaging video presentations.

## 🎯 Features

- **Authentication**: JWT-based user authentication with refresh tokens
- **Video Generation**: AI-powered video creation pipeline
  - Text-to-Slides using Google Gemini API
  - AI Voice-Over using Google Cloud Text-to-Speech
  - Video Stitching with OpenCV
- **Caching**: Redis-based caching to optimize performance
- **Database**: PostgreSQL for persistent data storage
- **API-First Design**: RESTful API with comprehensive documentation
- **Async Processing**: Background tasks for long-running operations

## 📋 Project Structure

```
Backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py          # Authentication endpoints
│   │       └── videos.py        # Video generation endpoints
│   ├── core/
│   │   ├── config.py            # Configuration management
│   │   ├── database.py          # Database setup
│   │   └── security.py          # JWT & password hashing
│   ├── models/
│   │   └── __init__.py          # SQLAlchemy models
│   ├── schemas/
│   │   └── __init__.py          # Pydantic schemas
│   ├── services/
│   │   └── video_service.py     # Video generation orchestration
│   └── utils/
│       ├── gemini_client.py     # Gemini API client
│       ├── tts_client.py        # Text-to-Speech client
│       ├── video_processor.py   # Video creation
│       └── cache_manager.py     # Redis cache management
├── main.py                       # FastAPI app entry point
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Docker services
├── Dockerfile                    # Container definition
└── .env.example                  # Environment variables template
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Google Cloud credentials (for Gemini & TTS APIs)

### Installation

1. **Clone and navigate to backend**:
```bash
cd Backend
```

2. **Create virtual environment**:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Create databases** (ensure PostgreSQL & Redis are running):
```bash
# The database tables will be created automatically on first run
```

6. **Run the server**:
```bash
python -m uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Set environment variables
export GOOGLE_GEMINI_API_KEY=your_key_here
export SECRET_KEY=your_secret_key_here

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
docker build -t blinked-backend .
docker run -p 8000:8000 --env-file .env blinked-backend
```

## 📚 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login and get tokens |
| POST | `/api/v1/auth/refresh` | Refresh access token |
| GET | `/api/v1/auth/me` | Get current user |

### Videos

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/videos/generate` | Generate video from prompt |
| GET | `/api/v1/videos` | List user's videos |
| GET | `/api/v1/videos/{id}` | Get video details |
| PUT | `/api/v1/videos/{id}` | Update video metadata |
| DELETE | `/api/v1/videos/{id}` | Delete video |

## 🔐 Security

- **Password Hashing**: bcrypt with salt
- **JWT Tokens**: HS256 algorithm
- **CORS**: Configured for frontend domains
- **Rate Limiting**: Implement in production
- **Input Validation**: Pydantic schemas
- **SQL Injection Prevention**: SQLAlchemy ORM

## 📦 Database Schema

### Users
- Store user accounts and authentication info
- Fields: email, username, password_hash, avatar_url, etc.

### Prompts
- Cache user prompts to avoid re-generation
- Fields: user_id, title, content, is_cached

### Slides
- Generated slide content from prompts
- Fields: prompt_id, text, image_url, slide_number

### Voiceovers
- AI-generated audio for slides
- Fields: slide_id, audio_url, duration, text

### Videos
- Final generated videos
- Fields: user_id, prompt_id, video_url, status, duration

### GenerationCache
- Cache for generated content (Gemini outputs, TTS audio)
- Prevents redundant API calls

## ⚙️ Configuration

Create `.env` file with:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/blinked

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google APIs
GOOGLE_GEMINI_API_KEY=your-gemini-key
GOOGLE_TTS_CREDENTIALS_PATH=/path/to/credentials.json

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

## 🔄 Video Generation Pipeline

```
User Prompt
    ↓
[1. Generate Slides] → Gemini API → Cached
    ↓
[2. Generate Voice Overs] → TTS API → Cached
    ↓
[3. Generate Images] → Image API (optional)
    ↓
[4. Stitch Video] → OpenCV → Final Video
    ↓
[5. Update DB] → Video Record Created
```

## 📝 Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Quality
```bash
# Lint
flake8 app/

# Format
black app/

# Type checking
mypy app/
```

### Database Migrations

```bash
# Initialize Alembic
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head
```

## 🚦 Status Codes

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## 📄 License

This project is proprietary. All rights reserved.

## 📞 Support

For issues and questions, please contact the development team.

---

**Built with ❤️ using FastAPI, SQLAlchemy, and Google Cloud APIs**
