import os
import requests
from dotenv import load_dotenv
import pathlib
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("CULTURE_API_KEY")
API_URL = "https://apis.data.go.kr/B553457/cultureinfo/period2"

print(f"Testing Culture API with Key: {API_KEY}")

params = {
    "serviceKey": API_KEY,
    "from": "20250101",
    "to": "20251231",
    "cPage": 1,
    "rows": 5,
}

try:
    # Test 1: Standard params (requests will encode)
    print("\n--- Test 1: Standard params ---")
    response = requests.get(API_URL, params=params, verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    # Test 2: Manual URL construction (no encoding of key if it was already encoded, though this key looks raw)
    print("\n--- Test 2: Manual URL construction ---")
    url = f"{API_URL}?serviceKey={API_KEY}&from=20250101&to=20251231&cPage=1&rows=5"
    response = requests.get(url, verify=False)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")

except Exception as e:
    print(f"Error: {e}")
