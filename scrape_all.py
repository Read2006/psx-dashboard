import os
import requests
from bs4 import BeautifulSoup
import re
import time
from database import SessionLocal, StockSnapshot

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}

def to_float(x):
    if not x:
        return None
    try:
        return float(x.replace(",", "").strip())
    except:
        m = re.search(r"[-+]?\d*\.?\d+", str(x))
        return float(m.group(0)) if m else None

def get_all_symbols():
    try:
        symbols_path = os.path.join(os.path.dirname(__file__), "symbols.txt")
        with open(symbols_path) as f:
            symbols = [line.strip().upper() for line in f if line.strip()]
        print(f"✅ Loaded {len(symbols)} symbols from symbols.txt")
        return symbols
    except FileNotFoundError:
        print("❌ symbols.txt file not found! Please create it in the project folder.")
        return []

def parse_snapshot(html, symbol):
    soup = BeautifulSoup(html, "html.parser")

    def get_val(id_):
        tag = soup.select_one(f"#{id_}")
        return tag.text.strip() if tag else None

    data = {
        "symbol": symbol,
        "market_price": to_float(get_val("ContentPlaceHolder1_lbl_price")),
        "ma_10": to_float(get_val("ContentPlaceHolder1_lbl_sma10")),
        "ma_30": to_float(get_val("ContentPlaceHolder1_lbl_sma30")),
        "ma_60": to_float(get_val("ContentPlaceHolder1_lbl_sma50")),
        "rsi": to_float(get_val("ContentPlaceHolder1_lbl_rsi")),
        "macd_daily": get_val("ContentPlaceHolder1_lbl_macddaily"),
        "macd_weekly": get_val("ContentPlaceHolder1_lbl_macdweekly"),
        "support1": to_float(get_val("ContentPlaceHolder1_lbl_support1")),
        "support2": to_float(get_val("ContentPlaceHolder1_lbl_support2")),
        "resistance1": to_float(get_val("ContentPlaceHolder1_lbl_resistance1")),
        "resistance2": to_float(get_val("ContentPlaceHolder1_lbl_resistance2")),
    }
    return data

def main():
    symbols = get_all_symbols()
    db = SessionLocal()

    for i, symbol in enumerate(symbols, start=1):
        url = f"https://scstrade.com/StockScreening/SS_TechSnapShot.aspx?symbol={symbol}"
        print(f"\n[{i}/{len(symbols)}] Fetching {symbol} ...")

        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code != 200:
                print(f"❌ Skipping {symbol} (Bad status {r.status_code})")
                continue

            parsed = parse_snapshot(r.text, symbol)
            existing = db.query(StockSnapshot).filter_by(symbol=symbol).first()
            if existing:
                for key, value in parsed.items():
                    setattr(existing, key, value)
                print(f"🔁 Updated {symbol}")
            else:
                db.add(StockSnapshot(**parsed))
                print(f"✅ Added new {symbol}")

            db.commit()

        except Exception as e:
            print(f"⚠️ Error fetching {symbol}: {e}")

        time.sleep(1.5)

    db.close()
    print("\n🏁 Done scraping all companies!")

if __name__ == "__main__":
    main()


