import httpx
import wmill
import requests
from urllib.parse import urlencode

def main():
    """
    Calls the Spliiit API to check marketplace services and verifies 
    if there's at least one element in the data.service field.
    """
    
    # API endpoint URL
    url = "https://core.spliiit.com/api/v1/marketplace/services/the-new-york-times/offers"
    params = {
        "page": 1,
        "plan[]": "8c2278cb-c965-4ce4-adb3-df582b641a88"
    }
    
    # Headers to bypass Cloudflare protection
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "Referer": "https://core.spliiit.com/"
    }
    
    # Make the HTTP request with browser-like headers
    with httpx.Client(headers=headers, timeout=30.0, follow_redirects=True) as client:
        response = client.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
    # Parse the JSON response
    data = response.json()
    
    # Check if data.service exists and has at least one element
    offers_data = data.get("data", {}).get("offers", [])
    has_offers_data = len(offers_data) > 0
    
    if has_offers_data:
        _notify_free("Available spliiit for NYT: https://app.spliiit.com/marketplace/list/the-new-york-times")
        

def _notify_free(message):
    f = {"user": wmill.get_variable("u/alex/free_mobile_id"), "pass": wmill.get_variable("u/alex/free_mobile_api_key"), "msg": message}
    url = "https://smsapi.free-mobile.fr/sendmsg?"
    goto = url + urlencode(f)
    requests.get(goto)