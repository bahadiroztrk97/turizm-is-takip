import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

message = """
🎉 Turizm İş Takip Sistemi Aktif

GitHub Actions başarılı şekilde çalışıyor.

Bir sonraki aşamada gerçek iş ilanlarını taramaya başlayacağız.
"""

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(response.text)
