# Changelog

## [2.0.0] - 2024

### Added
- **Technical Test Generation Endpoint** (`POST /generate-technical-test`)
  - Generates customized technical tests based on candidate profiles
  - Returns test in Markdown format
  - Adjusts difficulty based on experience level
  - Includes theoretical questions, practical exercises, and case studies
  
- **MongoDB Prompt Management**
  - Prompts stored in MongoDB for dynamic management
  - Fallback to default prompts if MongoDB unavailable
  - New prompt: `technical_test_generation`
  
- **Coolify Deployment Support**
  - Complete Docker Compose configuration
  - MongoDB with authentication
  - Environment variable configuration for Coolify
  
- **Enhanced Documentation**
  - Usage examples in multiple languages (curl, Python, JavaScript, PowerShell)
  - Integration examples for React applications
  - Deployment guide for Coolify

### Changed
- Refactored to Object-Oriented Programming architecture
- All variables and code in English
- Consolidated documentation in README.md
- Improved MongoDB connection with authentication support
- Enhanced error handling and validation

### Technical Details
- MongoDB connection supports both authenticated and non-authenticated modes
- AI service factory pattern with automatic fallback (Groq → Gemini)
- Singleton pattern for MongoDB client
- Repository pattern for prompt management

## [1.0.0] - Initial Release

### Features
- Video upload and audio extraction
- AI-powered transcription (Groq Whisper)
- Profile information extraction
- Professional CV profile generation
- FastAPI REST API
- Docker support
