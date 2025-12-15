import os
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

import pathlib

env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
API_KEY = os.getenv("CULTURE_API_KEY")
API_URL = "https://apis.data.go.kr/B553457/cultureinfo/period2"

def fetch_public_data(from_date="20250101", to_date="20251231", rows=20):
    params = {
        "serviceKey": API_KEY,
        "from": from_date,
        "to": to_date,
        "cPage": 1,
        "rows": rows,
    }
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(API_URL, params=params, verify=False)
    response.raise_for_status()
    root = ET.fromstring(response.content)
    items = root.findall(".//item")
    texts = []
    for item in items:
        title = item.findtext("title")
        place = item.findtext("place")
        start_date = item.findtext("startDate")
        end_date = item.findtext("endDate")
        
        if title:
            info = f"행사명: {title}"
            if place:
                info += f", 장소: {place}"
            if start_date and end_date:
                info += f", 기간: {start_date}~{end_date}"
            texts.append(info)
    return texts
