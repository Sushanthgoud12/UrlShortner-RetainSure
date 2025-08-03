# URL Shortener Service

## Overview
A complete URL shortening service built with Flask, featuring URL validation, click tracking, and analytics. This implementation provides a production-ready URL shortener similar to bit.ly or tinyurl.

## Features Implemented

### Core Functionality
- ✅ **URL Shortening**: Create 6-character alphanumeric short codes
- ✅ **URL Validation**: Comprehensive validation and normalization
- ✅ **Redirect System**: Automatic redirects with click tracking
- ✅ **Analytics**: Track clicks, creation time, and original URLs
- ✅ **Thread Safety**: Handle concurrent requests properly
- ✅ **Error Handling**: Comprehensive error handling with proper HTTP status codes

### Technical Features
- **RESTful API Design**: Clean, intuitive endpoints
- **In-Memory Storage**: Thread-safe storage with locking mechanisms
- **URL Normalization**: Automatic scheme addition (https://)
- **Comprehensive Testing**: 15+ test cases covering all functionality
- **Production Ready**: Proper error handling and edge case management

## Quick Start

### Prerequisites
- Python 3.8+ installed
- pip package manager

### Setup (Takes < 2 minutes)
```bash
# Navigate to the project directory
cd url-shortener

# Install dependencies
pip install -r requirements.txt

# Run tests to verify everything works
python -m pytest tests/ -v

# Start the application
python -m flask --app app.main run

# The API will be available at http://localhost:5000
```

## API Endpoints

### 1. Health Check
```bash
GET /api/health
```
**Response:**
```json
{
    "status": "ok",
    "message": "URL Shortener API is running"
}
```

### 2. Create Short URL
```bash
POST /api/shorten
Content-Type: application/json

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

### 3. Redirect to Original URL
```bash
GET /{short_code}
```
**Response:** 302 redirect to original URL (tracks click)

### 4. Get Analytics
```bash
GET /api/stats/{short_code}
```
**Response:**
```json
{
    "url": "https://www.example.com/very/long/url",
    "short_code": "abc123",
    "clicks": 5,
    "created_at": "2024-01-01T10:00:00"
}
```

## Example Usage

### Using curl:
```bash
# Create a short URL
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# Use the short URL (redirects to Google)
curl -L http://localhost:5000/abc123

# Check analytics
curl http://localhost:5000/api/stats/abc123
```

### Using Postman:
1. **POST** `http://localhost:5000/api/shorten`
   - Body: `{"url": "https://www.google.com"}`
   - Headers: `Content-Type: application/json`

2. **GET** `http://localhost:5000/{short_code}` (replace with actual short code)

3. **GET** `http://localhost:5000/api/stats/{short_code}`

## Architecture

### Project Structure
```
url-shortener/
├── app/
│   ├── __init__.py
│   ├── main.py          # Flask application with API endpoints
│   ├── models.py        # Thread-safe data models and storage
│   └── utils.py         # URL validation and utility functions
├── tests/
│   └── test_basic.py    # Comprehensive test suite
├── requirements.txt      # Python dependencies
├── CHANGES.md          # Implementation notes and approach
└── README.md           # This file
```

### Key Components

#### 1. Data Models (`app/models.py`)
- `URLMapping`: Stores URL mappings with metadata (clicks, creation time)
- `URLStore`: Thread-safe in-memory storage with atomic operations
- Global `url_store` instance for application-wide access

#### 2. Utility Functions (`app/utils.py`)
- `is_valid_url()`: Comprehensive URL validation
- `generate_short_code()`: Random 6-character alphanumeric generation
- `normalize_url()`: Automatic URL scheme normalization

#### 3. API Endpoints (`app/main.py`)
- `POST /api/shorten`: URL shortening with validation
- `GET /{short_code}`: Redirect with click tracking
- `GET /api/stats/{short_code}`: Analytics endpoint
- Health check endpoints for monitoring

## Technical Implementation

### Thread Safety
- Uses `threading.Lock()` for all storage operations
- Atomic read/write operations prevent race conditions
- Tested with concurrent requests

### URL Validation
- Comprehensive validation using `urllib.parse`
- Automatic scheme addition (adds https:// if missing)
- Domain validation with proper format checking

### Error Handling
- Proper HTTP status codes (200, 201, 400, 404, 500)
- Descriptive error messages for debugging
- Graceful handling of edge cases

### Testing
- **15+ comprehensive tests** covering all functionality
- Unit tests for utility functions
- Integration tests for API endpoints
- Error case testing and edge case validation
- Thread safety testing

## Testing

Run the complete test suite:
```bash
python -m pytest tests/ -v
```

Test coverage includes:
- ✅ URL shortening functionality
- ✅ Redirect and click tracking
- ✅ Analytics endpoint
- ✅ Error handling (invalid URLs, missing fields)
- ✅ Thread safety and concurrent requests
- ✅ Utility function validation
- ✅ Edge cases and boundary conditions

## Technical Requirements Met

- ✅ **URL Validation**: Comprehensive validation before shortening
- ✅ **6-Character Codes**: Alphanumeric short codes (62^6 combinations)
- ✅ **Concurrent Handling**: Thread-safe implementation
- ✅ **Error Handling**: Proper HTTP status codes and messages
- ✅ **Testing**: 15+ tests covering core functionality

## Future Enhancements

- Database persistence (SQLite, PostgreSQL)
- Custom short codes
- URL expiration
- Rate limiting
- User authentication
- Web UI
- API rate limiting
- URL analytics dashboard

## AI Usage Disclosure

This implementation was developed with assistance from AI tools:
- **Used for**: Code structure suggestions, error handling patterns, and test organization
- **Modified**: All AI-generated code was reviewed and customized for specific requirements
- **Rejected**: Initial suggestions that didn't meet the thread-safety requirements

## License

This project is part of a coding assignment and is provided as-is for educational purposes.