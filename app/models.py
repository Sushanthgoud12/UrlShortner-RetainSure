import threading
from datetime import datetime, timezone
from typing import Dict, Optional

class URLMapping:
    """Data model for storing URL mappings and analytics."""
    
    def __init__(self, original_url: str, short_code: str):
        self.original_url = original_url
        self.short_code = short_code
        self.clicks = 0
        self.created_at = datetime.now(timezone.utc)
    
    def increment_clicks(self):
        """Increment the click count for this URL."""
        self.clicks += 1
    
    def to_dict(self) -> Dict:
        """Convert the mapping to a dictionary for JSON serialization."""
        return {
            "url": self.original_url,
            "short_code": self.short_code,
            "clicks": self.clicks,
            "created_at": self.created_at.isoformat()
        }

class URLStore:
    """Thread-safe in-memory storage for URL mappings."""
    
    def __init__(self):
        self._mappings: Dict[str, URLMapping] = {}
        self._lock = threading.Lock()
    
    def add_mapping(self, short_code: str, original_url: str) -> URLMapping:
        """Add a new URL mapping."""
        with self._lock:
            mapping = URLMapping(original_url, short_code)
            self._mappings[short_code] = mapping
            return mapping
    
    def get_mapping(self, short_code: str) -> Optional[URLMapping]:
        """Get a URL mapping by short code."""
        with self._lock:
            return self._mappings.get(short_code)
    
    def increment_clicks(self, short_code: str) -> bool:
        """Increment clicks for a short code. Returns True if successful."""
        with self._lock:
            mapping = self._mappings.get(short_code)
            if mapping:
                mapping.increment_clicks()
                return True
            return False
    
    def get_stats(self, short_code: str) -> Optional[Dict]:
        """Get analytics for a short code."""
        with self._lock:
            mapping = self._mappings.get(short_code)
            return mapping.to_dict() if mapping else None

# Global instance for the application
url_store = URLStore()