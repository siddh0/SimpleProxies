import requests
from bs4 import BeautifulSoup
import re

# List of proxies
proxies = [
    {"http": "http://HOST:PORT", "https": "http://HOST:PORT"}  #You can add more proxies
]

# Target URL
url = ''   #Enter URL

def check_robots_txt(url):
    robots_url = f"{url}/robots.txt"
    try:
        response = requests.get(robots_url, timeout=5)
        if response.status_code == 200:
            print(f"robots.txt Content for {url}:")
            print(response.text)
            return response.text
        else:
            print(f"robots.txt not found or inaccessible. Status code: {response.status_code}")
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve robots.txt: {e}")
        return None

def parse_robots_txt(content):
    rules = {}
    lines = content.splitlines()
    user_agent = None

    for line in lines:
        line = line.strip()
        if line.lower().startswith('user-agent'):
            user_agent = line.split(':')[1].strip()
            rules[user_agent] = []
        elif line.lower().startswith('disallow') and user_agent:
            rules[user_agent].append(line.split(':')[1].strip())
    
    return rules

def scrape_with_proxies(url, proxies):
    # Check robots.txt
    robots_txt_content = check_robots_txt(url)
    if robots_txt_content:
        rules = parse_robots_txt(robots_txt_content)
        user_agent = '*'
        disallowed_paths = rules.get(user_agent, [])
        print(f"Disallowed paths for User-agent {user_agent}: {disallowed_paths}")

        # Ensure the target URL is not disallowed
        if any(url.endswith(path) for path in disallowed_paths):
            print(f"Scraping is disallowed for {url}")
            return

    for i, proxy in enumerate(proxies):
        try:
            response = requests.get(url, proxies=proxy, timeout=5)
            print(f"Proxy {i+1} Response Status: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')

            paragraphs = soup.find_all('p')
            print(f"Proxy {i+1} - Found {len(paragraphs)} paragraphs")
            for p in paragraphs:
                print(f"Paragraph: {p.get_text()}")

            links = soup.find_all('a', href=True)
            print(f"Proxy {i+1} - Found {len(links)} links")
            for link in links:
                print(f"Link: {link['href']} Text: {link.get_text()}")

        except requests.exceptions.Timeout:
            print(f"Proxy {i+1} failed: Timeout")
        except requests.exceptions.ConnectionError:
            print(f"Proxy {i+1} failed: Connection Error")
        except requests.exceptions.RequestException as e:
            print(f"Proxy {i+1} failed: {e}")

# Run the function
scrape_with_proxies(url, proxies)
