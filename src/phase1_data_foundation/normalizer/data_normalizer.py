import hashlib
import re
from datetime import datetime
from typing import Dict, Any

class DataNormalizer:
    @staticmethod
    def clean_text(text: str) -> str:
        """Remove extra whitespaces, newlines, and basic HTML tags."""
        if not text:
            return ""
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', text)
        # Standardize whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean

    @staticmethod
    def is_relevant_for_discovery(content: str) -> bool:
        """
        Lightweight keyword pre-filter to immediately discard generic app reviews
        or delivery complaints that do not contain evidence of shopping behavior.
        """
        if not content:
            return False
            
        content_lower = content.lower()
        
        keywords = [
            # Explicit Intent / Wishlisting
            'wishlist', 'cart', 'waiting', 'sale', 'discount', 'buy', 'bought', 'purchased',
            
            # Implicit Intent / Saving / Shortlisting
            'save', 'shortlist', 'bookmark', 'maybe later', 'heart', 'leave it',
            
            # Choice Paralysis / Uncertainty
            'compare', 'hesitate', 'think', 'thinking', 'decide', 'sure', 'not sure', 
            'confused', 'which one', 'options', 'looking for',
            
            # Product Attributes & Cost Objections
            'size', 'fit', 'price', 'expensive', 'costly', 'budget', 'afford',
            'quality', 'material', 'color', 'look', 'style', 'fabric', 'design', 
            
            # Post-purchase actions (can still contain relevant product sizing/fit feedback)
            'return', 'returned'
        ]
        
        for kw in keywords:
            if kw in content_lower:
                return True
                
        return False

    @staticmethod
    def hash_author(author_name: str) -> str:
        """Hash the author name to anonymize PII."""
        if not author_name:
            return ""
        return hashlib.sha256(author_name.encode('utf-8')).hexdigest()

    @staticmethod
    def generate_content_hash(platform: str, author_hash: str, content: str) -> str:
        """Generate a unique hash for deduplication based on platform, author, and content."""
        unique_string = f"{platform}_{author_hash}_{content}"
        return hashlib.md5(unique_string.encode('utf-8')).hexdigest()

    @staticmethod
    def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize a raw record dictionary."""
        content_clean = DataNormalizer.clean_text(record.get('content', ''))
        author_hash = DataNormalizer.hash_author(record.get('author', ''))
        
        # Ensure date is a datetime object
        date_obj = record.get('date')
        if isinstance(date_obj, str):
            try:
                # Try parsing standard ISO format if it comes as string
                date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
            except ValueError:
                date_obj = datetime.utcnow()
        elif date_obj is None:
            date_obj = datetime.utcnow()

        content_hash = DataNormalizer.generate_content_hash(
            platform=record.get('platform', 'unknown'),
            author_hash=author_hash,
            content=content_clean
        )

        return {
            'platform': record.get('platform'),
            'source_url': record.get('source_url'),
            'author_hash': author_hash,
            'content': record.get('content', ''),
            'content_clean': content_clean,
            'language': record.get('language', 'en'),
            'date': date_obj,
            'rating': record.get('rating'),
            'metadata_json': record.get('metadata', {}),
            'content_hash': content_hash
        }
