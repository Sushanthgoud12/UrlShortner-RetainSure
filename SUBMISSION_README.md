# URL Shortener Service - Submission

## Overview
A complete URL shortening service built with Flask, featuring URL validation, click tracking, and analytics.

## Features Implemented
- ✅ URL shortening with 6-character alphanumeric codes
- ✅ URL validation and normalization
- ✅ Redirect functionality with click tracking
- ✅ Analytics endpoint with creation time and click count
- ✅ Thread-safe concurrent request handling
- ✅ Comprehensive error handling
- ✅ 15+ test cases covering all functionality

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Tests
```bash
python -m pytest tests/ -v
```

### 3. Start the Application
```bash
python -m flask --app app.main run
```

### 4. Test the API

#### Create a Short URL:
```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'
```

#### Use the Short URL (redirects):
```bash
curl -L http://localhost:5000/{short_code}
```

#### Get Analytics:
```bash
curl http://localhost:5000/api/stats/{short_code}
```

## API Endpoints

### POST /api/shorten
Creates a short URL from a long URL.

**Request:**
```json
{
    "url": "https://www.example.com/very/long/url"
}
```

**Response:**
```json
{
    "short_code": "abc123",
    "short_url": "http://localhost:5000/abc123"
}
```

### GET /{short_code}
Redirects to the original URL and tracks the click.

**Response:** 302 redirect to original URL

### GET /api/stats/{short_code}
Returns analytics for a short code.

**Response:**
```json
{
    "url": "https://www.example.com/very/long/url",
    "short_code": "abc123",
    "clicks": 5,
    "created_at": "2024-01-01T10:00:00"
}
```

## Architecture

### Components:
- **`app/models.py`**: Thread-safe in-memory storage with URL mappings
- **`app/utils.py`**: URL validation and short code generation utilities
- **`app/main.py`**: Flask application with RESTful API endpoints
- **`tests/test_basic.py`**: Comprehensive test suite

### Key Design Decisions:
- **Thread-safe storage**: Uses `threading.Lock()` for concurrent requests
- **URL validation**: Comprehensive validation using `urllib.parse`
- **Error handling**: Proper HTTP status codes and descriptive error messages
- **Clean architecture**: Separation of concerns between models, utils, and API

## Testing

The test suite includes:
- Unit tests for utility functions
- Integration tests for API endpoints
- Error case testing
- Thread safety testing
- Edge case validation

Run tests with: `python -m pytest tests/ -v`

## Technical Requirements Met

- ✅ URLs validated before shortening
- ✅ 6-character alphanumeric short codes
- ✅ Concurrent request handling
- ✅ Basic error handling
- ✅ 5+ tests covering core functionality

## Future Enhancements

- Database persistence (SQLite, PostgreSQL)
- Custom short codes
- URL expiration
- Rate limiting
- User authentication
- Web UI

## AI Usage Disclosure

This implementation was developed with assistance from AI tools:
- **Used for**: Code structure suggestions, error handling patterns, and test organization
- **Modified**: All AI-generated code was reviewed and customized for specific requirements
- **Rejected**: Initial suggestions that didn't meet the thread-safety requirements 