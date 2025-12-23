from bs4 import BeautifulSoup

def extract_csrf(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("input", {"name": "csrfmiddlewaretoken"})
    if not tag:
        raise RuntimeError("CSRF token not found")
    return tag["value"]