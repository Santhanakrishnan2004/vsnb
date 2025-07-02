import time
import requests
from bs4 import BeautifulSoup

# Replace these with your actual values
BOT_TOKEN = "7682639011:AAHRIEumPuLtLdL73wvUQ7nL78xpuwL6rk0"
CHAT_ID = "915284943"
CHECK_INTERVAL = 60  # in seconds

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print("❌ Failed to send Telegram message:", e)

def get_slot_availability():
    try:
        url = "https://visaslots.info/details/15"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        if not table:
            return None

        rows = table.find_all("tr")[1:]
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                slots = cols[0].text.strip()
                location = cols[1].text.strip()
                visa_type = cols[2].text.strip()
                if location == "CHENNAI VAC" and visa_type.startswith("F") and slots.isdigit():
                    return int(slots)
        return None
    except Exception as e:
        print("Error fetching data:", e)
        return None

def main():
    print("🔍 Watching visa slot availability...")
    while True:
        slots = get_slot_availability()
        if slots is not None:
            print(f"Checked: {slots} slots available.")
            if slots > 0:  # For testing
                message = f"✅ <b>Visa Slots Available!</b>\n\n<b>Location:</b> Chennai VAC\n<b>Slots:</b> {slots}\n\n🔗 Check: https://visaslots.info/details/15"
                send_telegram_message(message)
                time.sleep(60)  # wait 5 minutes before checking again
            else:
                time.sleep(CHECK_INTERVAL)
        else:
            print("⚠️ Failed to fetch slot info.")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
