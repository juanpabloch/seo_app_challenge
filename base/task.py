from celery import shared_task
from core import settings
import requests


@shared_task()
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
