
try:
    with open('results.txt', 'r', encoding='utf-16') as f:
        print(f.read())
except Exception as e:
    print(f"UTF-16 failed: {e}")
    try:
        with open('results.txt', 'r', encoding='cp1252') as f:
            print(f.read())
    except Exception as e2:
        print(f"CP1252 failed: {e2}")
