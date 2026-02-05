import urllib.request
import urllib.parse

try:
    print("Testing analyze endpoint...")
    
    # Test with a simple POST request (no file)
    data = urllib.parse.urlencode({}).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:5000/analyze', data=data)
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print(f"Status: {response.status}")
        print(f"Response: {result}")
        
        if response.status == 400:
            print("Expected error (no file provided) - this is correct!")
        else:
            print("Unexpected response")
            
except Exception as e:
    print(f"Error testing analyze endpoint: {e}")
