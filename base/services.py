import requests

from core import settings
from base.models import UrlData


def get_url_data(url, strategy):
    base_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?category=performance'

    params = {
        "url": url,
        "strategy": strategy,
    }

    if settings.API_KEY:
        params["key"] = settings.API_KEY

    try:
        response = requests.get(base_url, params=params)
        result = response.json()

        data = {
            "url": url,
            "strategy": strategy,
            "index": round(result['lighthouseResult']['audits']['speed-index']["numericValue"], 3),
            "interactive": round(result['lighthouseResult']['audits']['interactive']["numericValue"], 3),
        }
    except Exception as err:
        print("ERROR fetching url data: ", err)
        return False
    
    return data


def save_urls_comparison(data):
    try:
        UrlData.objects.create(
            strategy = data["url_1"]["strategy"],
            url_1 = data["url_1"]["url"], 
            index_1 = data["url_1"]["index"], 
            interactive_1 = data["url_1"]["interactive"],
            url_2 = data["url_2"]["url"], 
            index_2 = data["url_2"]["index"], 
            interactive_2 = data["url_2"]["interactive"],
        )
    except Exception as err:
        print("ERROR saving urls comparison: ", err)

