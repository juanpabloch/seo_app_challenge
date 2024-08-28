from base.models import UrlData

def save_urls_comparison(data):
    try:
        UrlData.objects.get_or_create(
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
