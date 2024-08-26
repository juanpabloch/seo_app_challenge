import requests
from django.core.exceptions import ObjectDoesNotExist

from core import settings
from base.models import UrlData, UrlCompareHistory
import json


def get_url_db(url, strategy):
    data = {}
    try:
        data_url = UrlData.objects.get(url=url, strategy=strategy)

        data["find"] = True
        data["url"] = {
            "id": data_url.id,
            "url": data_url.url,
            "strategy": data_url.strategy,
            "index": data_url.index,
            "interactive": data_url.interactive,
        }
        
    except ObjectDoesNotExist:
        data["find"] = False
        data["url"] = url
        data["strategy"] = strategy

    return data


def get_url_data(url, strategy):
    base_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?category=performance'

    params = {
        "url": url,
        "strategy": strategy,
    }

    if settings.API_KEY:
        params["key"] = settings.API_KEY

    response = requests.get(base_url, params=params)
    result = response.json()

    data = {
        "url": url,
        "strategy": strategy,
        "index": round(result['lighthouseResult']['audits']['speed-index']["numericValue"], 3),
        "interactive": round(result['lighthouseResult']['audits']['interactive']["numericValue"], 3),
    }

    return data


def process_data(data):
    if not data["find"]:
        try:
            url_data = get_url_data(data["url"], data["strategy"])
            url = UrlData.objects.create(**url_data)
            return {
                "id": url.id,
                "url": url.url,
                "strategy": url.strategy,
                "index": url.index,
                "interactive": url.interactive,
            }
            
        except Exception as err:
            print("ERROR: ", err)
    else:
        return data["url"]


def save_compare(data):
    id_1 = data["url_1"]["id"]
    id_2 = data["url_2"]["id"]
    UrlCompareHistory.objects.get_or_create(url_1_id=id_1, url_2_id=id_2)
