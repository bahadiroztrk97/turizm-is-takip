import requests
import json
import os
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SEARCH_URLS = [
    "https://www.kariyer.net/is-ilanlari?kw=turizm%20kontrat"
]

KEYWORDS = [
    "kontrat",
    "contract",
    "contracting",
    "operasyon",
    "operation",
    "vip",
    "product",
    "incoming",
    "destination"
]

COMPANIES = [
    "setur",
    "ets",
    "jolly",
    "tatilbudur",
    "prontotour",
    "tatilsepeti",
    "coral",
    "odeon"
]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )


def load_jobs():
    if not os.path.exists("jobs.json"):
        return []

    with open("jobs.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_jobs(data):
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_relevant(title):
    title = title.lower()

    if any(keyword in title for keyword in KEYWORDS):
        return True

    if any(company in title for company in COMPANIES):
        return True

    return False


def scrape():
    known_jobs = load_jobs()
    new_jobs = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
for url in SEARCH_URLS:
    response = requests.get(url, headers=headers, timeout=30)

    print(response.status_code)
    print(response.text[:5000])

    soup = BeautifulSoup(response.text, "lxml")

    links = soup.find_all("a")

    print("Bulunan link sayısı:", len(links))

    for link in links[:20]:
        print(link.get("href"))

    for link in links:
        href = link.get("href")

        if not href:
            continue

        if "/is-ilani/" not in href:
            continue

        title = link.get_text(strip=True)

        if not title:
            continue

        if not is_relevant(title):
            continue

        full_url = "https://www.kariyer.net" + href

        if full_url in known_jobs:
            continue

        known_jobs.append(full_url)
        new_jobs.append((title, full_url))


def main():
    jobs = scrape()

    if not jobs:
        return

    for title, url in jobs:
        send_telegram(
            f"Yeni ilan bulundu\n\n{title}\n{url}"
        )


if __name__ == "__main__":
    main()



