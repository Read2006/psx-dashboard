import requests
from bs4 import BeautifulSoup
import re
from database import SessionLocal, StockSnapshot  # import from your database.py

# URL and headers
URL = "https://scstrade.com/StockScreening/SS_TechSnapShot.aspx?symbol=FATIMA"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}


# --- Helper function ---
def to_float(x):
    if not x:
        return None
    try:
        return float(x.replace(",", "").strip())
    except:
        m = re.search(r"[-+]?\d*\.?\d+", str(x))
        return float(m.group(0)) if m else None


def parse_snapshot(html):
    soup = BeautifulSoup(html, "html.parser")

    def get_val(id_):
        tag = soup.select_one(f"#{id_}")
        return tag.text.strip() if tag else None

    # ✅ Using the real IDs you found
    data = {
        "symbol": "FATIMA",
        "market_price": to_float(get_val("ContentPlaceHolder1_lbl_price")),
        "ma_10": to_float(get_val("ContentPlaceHolder1_lbl_sma10")),
        "ma_30": to_float(get_val("ContentPlaceHolder1_lbl_sma30")),
        "ma_60": to_float(get_val("ContentPlaceHolder1_lbl_sma50")),   # 50-day MA
        "rsi": to_float(get_val("ContentPlaceHolder1_lbl_rsi")),
        "macd_daily": get_val("ContentPlaceHolder1_lbl_macddaily"),
        "macd_weekly": get_val("ContentPlaceHolder1_lbl_macdweekly"),
        "support1": to_float(get_val("ContentPlaceHolder1_lbl_support1")),
        "support2": to_float(get_val("ContentPlaceHolder1_lbl_support2")),
        "resistance1": to_float(get_val("ContentPlaceHolder1_lbl_resistance1")),
        "resistance2": to_float(get_val("ContentPlaceHolder1_lbl_resistance2")),
    }

    return data


# --- Main script ---
print("Fetching:", URL)
try:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    print("Status Code:", response.status_code)

    if response.status_code != 200:
        raise Exception("Failed to fetch page")

    parsed = parse_snapshot(response.text)
    print("\n📊 Extracted Data:")
    for k, v in parsed.items():
        print(f"{k}: {v}")

    # --- Save to database ---
    db = SessionLocal()
    snapshot = StockSnapshot(**parsed)
    db.add(snapshot)
    db.commit()
    db.close()
    print("\n✅ Data saved successfully to stocks.db")

except Exception as e:
    print("❌ Error:", e)
