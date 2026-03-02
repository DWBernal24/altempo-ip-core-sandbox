import re

from rest_framework import serializers

def check_for_url(value):
    """
    Detects URL patterns and raises an error in case that it founds one or more
    """
    patterns = [
        r'https?://[^\s<>"{}|\\^`\[\]]+',  # http/https URLs
        r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # www domains
        r'\b[a-zA-Z0-9.-]+\.(?:com|org|net|edu|gov|co\.uk|io|ly)\b'  # Common TLDs only
    ]

    matches = []

    for pattern in patterns:
        found = re.findall(pattern, value, re.IGNORECASE)
        matches.extend(found)

    if matches:
        raise serializers.ValidationError("URL found in the provided text")

    # preserve order for better DX
    return list(dict.fromkeys(matches))
