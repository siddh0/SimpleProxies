import requests

# Example list of free proxies
proxies = [
    {"http": "http://184.168.124.233:5402", "https": "http://184.168.124.233:5402"}

]

# Target URL
url = 'https://dnsleaktest.com'

def request_through_proxies(url, proxies):
    for i, proxy in enumerate(proxies):
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            print(f"Proxy {i+1} Response Status: {response.status_code}")
            print(response.text)  # Print the first 100 characters of the response
        except Exception as e:
            print(f"Proxy {i+1} failed: {e}")

request_through_proxies(url, proxies)
