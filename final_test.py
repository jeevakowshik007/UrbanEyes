import urllib.request

try:
    print("Testing Flask app...")
    with urllib.request.urlopen('http://127.0.0.1:5000') as response:
        html = response.read().decode('utf-8')
        print(f"Status: {response.status}")
        print(f"Content length: {len(html)}")
        if response.status == 200:
            print("Flask app is working correctly!")
            if "UrbanEyes24" in html:
                print("HTML content loaded correctly!")
            else:
                print("HTML content might be different than expected")
        else:
            print("Flask app returned error status")
except Exception as e:
    print(f"Error testing Flask app: {e}")
