
import yfinance as yf
print("Testing various tickers...")
tickers = ["SPY", "AAPL", "^GSPC"]
for t in tickers:
    print(f"\nDownloading {t}...")
    try:
        data = yf.download(t, period="1mo", progress=False)
        print(f"Shape: {data.shape}")
        if len(data) > 0:
            print("Success")
        else:
            print("Failed (Empty)")
    except Exception as e:
        print(f"Exception: {e}")
