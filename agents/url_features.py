from urllib.parse import urlparse
import re

def extract_features(url):
    parsed = urlparse(url)

    hostname = parsed.hostname or ""

    return {
        "url_length": len(url),
        "uses_https": parsed.scheme == "https",
        "has_ip": bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname)),
        "num_dots": hostname.count("."),
        "num_hyphens": hostname.count("-"),
        "has_at_symbol": "@" in url,
    }