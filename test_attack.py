import requests
import time

url = "http://ddos-lab-alb-1222108909.ap-northeast-1.elb.amazonaws.com"

print(f"Starting connection-isolated rate test against {url}...")
print("Forcing new TCP connections to trigger WAF. Press Ctrl+C to cancel.")

request_count = 0

# Explicitly use a session and disable keep-alive headers
with requests.Session() as session:
    while True:
        request_count += 1
        try:
            # Adding 'Connection: close' forces a clean TCP handshake every time
            response = session.get(url, headers={"Connection": "close"}, timeout=5)
            print(f"Request {request_count}: Status {response.status_code}")
            
            if response.status_code == 403:
                print("\n🛑 SUCCESS! AWS WAF has officially blocked your IP with a 403 Forbidden!")
                break
                
            time.sleep(0.1) 
            
        except Exception as e:
            print(f"Request {request_count}: Failed - {e}")
