import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]

print("TOKEN UZUNLUGU:", len(TOKEN))

url = f"https://api.telegram.org/bot{TOKEN}/getMe"

response = requests.get(url)

print(response.text)
