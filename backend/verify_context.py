from public_data import fetch_public_data

print("Fetching data with new format...")
data = fetch_public_data(rows=5)
for i, item in enumerate(data):
    print(f"[{i+1}] {item}")
