
print("Start Debug")
try:
    import yfinance
    print("Imported yfinance")
    import scipy
    print("Imported scipy")
    import pandas
    print("Imported pandas")
    
    with open("debug_output.txt", "w") as f:
        f.write("File write successful")
    print("File write successful")
except Exception as e:
    print(f"Error: {e}")
print("End Debug")
