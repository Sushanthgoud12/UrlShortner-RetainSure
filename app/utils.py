import re
import random
import string
from urllib.parse import urlparse
from typing import Optional

def is_valid_url(url: str) -> bool:
    """
    Validate if the given string is a valid URL.
    
    Args:
        url: The URL string to validate
        
    Returns:
        True if the URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        # Check if scheme and netloc are present
        # Also ensure the URL has a valid format with a domain
        return all([result.scheme, result.netloc]) and '.' in result.netloc and len(result.netloc) > 3
    except:
        return False

def generate_short_code(length: int = 6) -> str:
    """
    Generate a random alphanumeric short code.
    
    Args:
        length: The length of the short code (default: 6)
        
    Returns:
        A random alphanumeric string of the specified length
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def normalize_url(url: str) -> str:
    """
    Normalize a URL by ensuring it has a scheme.
    
    Args:
        url: The URL to normalize
        
    Returns:
        The normalized URL with a scheme
    """
    if not url.startswith(('http://', 'https://')):
        return f'https://{url}'
    return url