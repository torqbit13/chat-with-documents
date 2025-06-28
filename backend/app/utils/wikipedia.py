import requests
from bs4 import BeautifulSoup

def fetch_wikipedia_content(url: str):
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ValueError("Failed to fetch Wikipedia page")
    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.find("h1", {"id": "firstHeading"}).text.strip()
    paragraphs = soup.find_all("p")
    text = "\n".join([p.get_text() for p in paragraphs if p.get_text(strip=True)])
    return title, text
