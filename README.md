# Video Profile Extractor API

API for extracting professional profiles from video presentations using AI transcription and analysis.

## Features

- Video upload and audio extraction
- AI-powered audio transcription (Groq Whisper / Gemini)
- Automatic profile information extraction
- Professional CV profile generation
- Automatic fallback between AI services

## Architecture

The application follows Object-Oriented Programming principles with clear separation of concerns:

```
├── main.py                    # FastAPI application and endpoints
├── config.py                  # Configuration management
├── services/
│   ├── __init__.py           # Service exports
│   ├── ai_service.py         # AI service implementations (Groq, Gemini)
│   ├── ai_factory.py         # Factory pattern for AI service creation
│   └── video_processor.py    # Video processing and audio extraction
├── database/
│   ├── __init__.py           # Database exports
│   ├── mongodb.py            # MongoDB client singleton
│   └── prompt_repository.py  # Prompt management repository
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Docker image definition
└── COOLIFY_DEPLOYMENT.md      # Complete Coolify deployment guide
```

## Quick Start

### Local Development with Docker Compose

```bash
# Clone repository
git clone https://github.com/ferrosero91/micoservicioProcesarVideo.git
cd micoservicioProcesarVideo

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose up -d

# Access API
open http://localhost:9000
```

### Local Development without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Configure .env (leave MongoDB credentials empty for local)
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USERNAME=
MONGODB_PASSWORD=

# Start MongoDB
net start MongoDB  # Windows
# or
sudo systemctl start mongod  # Linux/Mac

# Run application
python main.py
```

## API Endpoints

### `GET /`
Returns HTML upload form

### `POST /upload-video`
Process video and extract profile

**Request:** multipart/form-data with video file

**Response:**
```json
{
  "cv_profile": "Professional profile text...",
  "profile_data": {
    "name": "John Doe",
    "profession": "Software Engineer",
    "experience": "5 years in web development",
    "education": "Computer Science degree",
    "technologies": "Python, JavaScript, React",
    "languages": "English, Spanish",
    "achievements": "Led team of 5 developers",
    "soft_skills": "Leadership, communication"
  }
}
```

### `GET /health`
Health check endpoint

### `GET /prompts`
List all available prompts

### `GET /prompts/{prompt_name}`
Get a specific prompt template

### `PUT /prompts/{prompt_name}`
Update a prompt template

**Request:**
```json
{
  "template": "Your new prompt template with {variables}"
}
```

### `POST /generate-technical-test`
Generate technical test for selected candidates (Company use)

**Use Case:** After reviewing candidate profiles, companies use this endpoint to generate customized technical tests based on job requirements.

**Request:**
```json
{
  "profession": "Software Engineer",
  "technologies": "Python, FastAPI, PostgreSQL",
  "experience": "3 years in backend development",
  "education": "Computer Science degree"
}
```

**Response:**
```json
{
  "technical_test_markdown": "# Prueba Técnica - Software Engineer\n\n...",
  "profile_summary": {
    "profession": "Software Engineer",
    "technologies": "Python, FastAPI, PostgreSQL",
    "experience": "3 years in backend development"
  }
}
```

**Note:** The test is generated based on job requirements, not candidate profile. This allows companies to create standardized tests for specific positions.

## Environment Variables

```env
# AI Service Keys (At least one required)
# Fallback order: Groq → Gemini → Z.AI
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
ZAI_API_KEY=your_zai_key

# MongoDB Configuration
MONGODB_HOST=localhost              # or Coolify internal host
MONGODB_PORT=27017
MONGODB_USERNAME=videoprofile       # empty for local without auth
MONGODB_PASSWORD=videoprofile       # empty for local without auth
MONGODB_DATABASE=video_profile_extractor
MONGODB_AUTH_DATABASE=admin

# Server
PORT=9000
```

**AI Service Fallback:**
- The system tries services in order: Groq → Gemini → Z.AI
- If one fails, it automatically uses the next available service
- At least one API key must be configured

## Deployment to Coolify

### 1. Create MongoDB Database
- In Coolify: **+ New Resource** → **Database** → **MongoDB**
- Username: `videoprofile`, Password: `videoprofile`, Database: `video_profile_extractor`
- Copy the internal host (e.g., `pwsggksos88cokc40s04088w`)

### 2. Create API Resource
- **+ New Resource** → **Docker Compose**
- Repository: `https://github.com/ferrosero91/micoservicioProcesarVideo.git`
- Branch: `master`

### 3. Set Environment Variables
```env
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
ZAI_API_KEY=your_key
MONGODB_HOST=pwsggksos88cokc40s04088w  # from step 1
MONGODB_PORT=27017
MONGODB_USERNAME=videoprofile
MONGODB_PASSWORD=videoprofile
MONGODB_DATABASE=video_profile_extractor
MONGODB_AUTH_DATABASE=admin
PORT=9000
```

**Note:** At least one AI service key is required. The system will use them in order: Groq → Gemini → Z.AI

### 4. Deploy
Click **Deploy** and wait 5-10 minutes.

## Workflow

### Complete Recruitment Process

```
1. Candidate → Uploads video presentation
   ↓
2. API → Extracts profile + Generates CV
   ↓
3. Company → Reviews profiles
   ↓
4. Company → Selects candidates
   ↓
5. Company → Generates technical test (this API)
   ↓
6. Candidate → Completes technical test
   ↓
7. Company → Evaluates and makes hiring decision
```

### Use Cases

#### 1. Candidate: Upload Video Presentation
```bash
curl -X POST http://localhost:9000/upload-video \
  -F "file=@presentation.mp4"
```

**Response:** CV profile + Extracted data

#### 2. Company: Generate Technical Test for Selected Candidates
After reviewing profiles, companies generate customized tests:

```bash
curl -X POST http://localhost:9000/generate-technical-test \
  -H "Content-Type: application/json" \
  -d '{
    "profession": "Software Engineer",
    "technologies": "Python, FastAPI, PostgreSQL",
    "experience": "3 years in backend development",
    "education": "Computer Science degree"
  }'
```

**Response:** Technical test in Markdown format

#### 3. Admin: Manage Prompts
```bash
# List prompts
curl http://localhost:9000/prompts

# Update prompt
curl -X PUT http://localhost:9000/prompts/technical_test_generation \
  -H "Content-Type: application/json" \
  -d '{"template": "Your new prompt with {variables}"}'
```
