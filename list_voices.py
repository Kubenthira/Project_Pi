import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MURF_API_KEY")

url = "https://api.murf.ai/v1/speech/voices"
headers = {"api-key": api_key}

response = requests.get(url, headers=headers)
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    voices = response.json()
    with open("murf_voices.txt", "w") as f:
        for v in voices:
            line = f"ID: {v.get('voiceId')} | Lang: {v.get('displayLanguage')}\n"
            f.write(line)
    print("All voices written to murf_voices.txt")
else:
    print(f"Error: {response.text}")
