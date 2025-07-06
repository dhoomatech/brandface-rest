import requests
from datetime import datetime
from cards.models import BusinessProfile


def fetch_google_reviews(profile: BusinessProfile):
    config = getattr(profile, 'google_config', None)
    if not config or not config.place_id or not config.api_key:
        return None, "Google Review configuration missing."

    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": config.place_id,
        "fields": "reviews",
        "key": config.api_key,
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None, f"API error: {response.status_code}"

    data = response.json()
    if data.get("status") != "OK":
        return None, data.get("error_message", "Unknown error")

    return data["result"].get("reviews", []), None


def fetch_instagram_posts(instagram_user_id, access_token):
    url = f"https://graph.instagram.com/{instagram_user_id}/media"
    params = {
        "fields": "id,caption,media_url,permalink,timestamp",
        "access_token": access_token
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    return []
