import requests

try:
    print("Testing Flask app...")
    r = requests.get('http://127.0.0.1:5000')
    print(f"Status: {r.status_code}")
    print(f"Content length: {len(r.text)}")
    if r.status_code == 200:
        print("✅ Flask app is working correctly!")
    else:
        print("❌ Flask app returned error status")
except Exception as e:
    print(f"❌ Error testing Flask app: {e}")
