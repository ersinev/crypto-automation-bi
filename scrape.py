import os
import yfinance as yf
import pandas as pd
from datetime import datetime
from supabase import create_client

# GitHub Secrets'tan bilgileri çekiyoruz
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

def run_scraper():
    symbols = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'XRP-USD', 'ADA-USD', 'DOGE-USD', 'AVAX-USD', 'LINK-USD']
    rows = []
    scrape_time = datetime.now().isoformat()

    for ticker in symbols:
        try:
            hist = yf.Ticker(ticker).history(period="2d")
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                curr_price = hist['Close'].iloc[-1]
                volume = hist['Volume'].iloc[-1]
                change = ((curr_price - prev_close) / prev_close) * 100
                
                rows.append({
                    "symbol": ticker.replace('-USD', ''),
                    "name": ticker,
                    "price_usd": round(float(curr_price), 4),
                    "volume_24h": float(volume),
                    "change_pct": round(float(change), 2),
                    "scraped_at": scrape_time
                })
        except Exception as e:
            print(f"Hata: {ticker} çekilemedi -> {e}")

    if rows:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        supabase.table("crypto_tracker").insert(rows).execute()
        print(f"✅ {len(rows)} satır başarıyla eklendi!")

if __name__ == "__main__":
    run_scraper()
