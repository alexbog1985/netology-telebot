import requests
import json
import settings

TRANSLATE_URL = "https://ftapi.pythonanywhere.com/translate"


def translate(text):
    params = {
        "sl": "ru",
        "dl": 'en',
        "text": text,
    }

    response = requests.get(TRANSLATE_URL, params=params)
    if response.status_code == 200 and response.json().get("translations").get('possible-translations'):
        result = response.json().get("translations").get('possible-translations')[0].lower()
    else:
        result = None
    return result


if __name__ == "__main__":
    print(translate("привет"))
