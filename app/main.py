from flask import Flask, jsonify, request, redirect, abort
from app.models import url_store
from app.utils import is_valid_url, generate_short_code, normalize_url
import random

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """
    Shorten a URL endpoint.
    
    Expected JSON payload:
    {
        "url": "https://www.example.com/very/long/url"
    }
    
    Returns:
    {
        "short_code": "abc123",
        "short_url": "http://localhost:5000/abc123"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                "error": "Missing 'url' field in request body"
            }), 400
        
        original_url = data['url'].strip()
        
        if not original_url:
            return jsonify({
                "error": "URL cannot be empty"
            }), 400
        
        # Normalize the URL
        normalized_url = normalize_url(original_url)
        
        # Validate the URL
        if not is_valid_url(normalized_url):
            return jsonify({
                "error": "Invalid URL format"
            }), 400
        
        # Generate a unique short code
        short_code = generate_short_code()
        
        # Store the mapping
        url_store.add_mapping(short_code, normalized_url)
        
        # Build the short URL
        short_url = f"{request.host_url.rstrip('/')}/{short_code}"
        
        return jsonify({
            "short_code": short_code,
            "short_url": short_url
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": "Internal server error"
        }), 500

@app.route('/<short_code>')
def redirect_to_original(short_code):
    """
    Redirect endpoint for short codes.
    
    Args:
        short_code: The short code to redirect
        
    Returns:
        Redirect to original URL or 404 if not found
    """
    # Skip if this is an API route
    if short_code.startswith('api'):
        abort(404)
    
    # Validate short code format
    if not short_code or len(short_code) != 6 or not short_code.isalnum():
        abort(404)
    
    # Get the mapping
    mapping = url_store.get_mapping(short_code)
    
    if not mapping:
        abort(404)
    
    # Increment click count
    url_store.increment_clicks(short_code)
    
    # Redirect to original URL
    return redirect(mapping.original_url, code=302)

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    """
    Analytics endpoint for a short code.
    
    Args:
        short_code: The short code to get stats for
        
    Returns:
        JSON with URL stats or 404 if not found
    """
    # Validate short code format
    if not short_code or len(short_code) != 6 or not short_code.isalnum():
        return jsonify({
            "error": "Invalid short code format"
        }), 400
    
    # Get the stats
    stats = url_store.get_stats(short_code)
    
    if not stats:
        return jsonify({
            "error": "Short code not found"
        }), 404
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)