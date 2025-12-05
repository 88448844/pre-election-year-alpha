
import yfinance as yf
print("yfinance version:", yf.__version__)
data = yf.download("^GSPC", start="1950-01-01", progress=False)
print("Data shape:", data.shape)
print("Columns:", data.columns)
print("Head:", data.head())
if len(data) == 0:
    print("Empty dataframe downloaded")
else:
    try:
        print("Close Head:", data['Close'].head())
    except Exception as e:
        print("Error accessing Close:", e)
