import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def create_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    })
    return session

def clean_url(url):
    url = url.strip().lower()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def get_google_favicon(domain):
    return f"https://www.google.com/s2/favicons?domain={domain}&sz=64"

def extract_favicon(url):
    session = create_session()
    url = clean_url(url)
    domain = urlparse(url).netloc

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        favicon_candidates = []

        icon_rels = ['icon', 'shortcut icon', 'apple-touch-icon', 'apple-touch-icon-precomposed', 'mask-icon', 'fluid-icon']

        for link in soup.find_all('link'):
            rel = link.get('rel', [])
            if not isinstance(rel, list):
                rel = [rel]
            rel = [r.lower() for r in rel]

            if any(icon_type in rel for icon_type in icon_rels):
                href = link.get('href')
                if href:
                    sizes = link.get('sizes', '')
                    if '32x32' in sizes or '64x64' in sizes:
                        favicon_candidates.insert(0, urljoin(url, href))
                    else:
                        favicon_candidates.append(urljoin(url, href))

        default_favicon = urljoin(url, '/favicon.ico')
        if default_favicon not in favicon_candidates:
            favicon_candidates.append(default_favicon)

        for favicon_url in favicon_candidates:
            try:
                response = session.head(favicon_url, timeout=5)
                if response.status_code == 200 and 'image' in response.headers.get('content-type', '').lower():
                    return {'status': 'success', 'favicon_url': favicon_url, }
            except:
                continue
            time.sleep(0.1)

        return {'status': 'success', 'favicon_url': get_google_favicon(domain)}

    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'message': str(e), 'favicon_url': get_google_favicon(domain),}

def main():
    url = input("Enter a website URL: ").strip()
    result = extract_favicon(url)

    if result['status'] == 'success':
        print(f"\nFavicon found!")
        print(f"URL: {result['favicon_url']}")
    else:
        print(f"\nError: {result['message']}")
        if result['favicon_url']:
            print(f"favicon URL: {result['favicon_url']}")

if __name__ == "__main__":
    main()
