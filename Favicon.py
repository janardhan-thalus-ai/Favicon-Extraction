import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_favicon_and_save(url, output_file="favicon.ico"):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        
        icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
        if icon_link and icon_link.get('href'):
            favicon_url = urljoin(url, icon_link['href'])
        else:
            favicon_url = urljoin(url, '/favicon.ico')
        
        favicon_response = requests.get(favicon_url, timeout=10)
        if favicon_response.status_code == 200:
            with open(output_file, 'wb') as file:
                file.write(favicon_response.content)
            return f"Favicon saved as {output_file}"
        else:
            return "Favicon not found at the expected location."
    except Exception as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    website_url = input("Enter the website URL: ")
    output_file = "favicon.ico"  
    result = get_favicon_and_save(website_url, output_file)
    print(result)
