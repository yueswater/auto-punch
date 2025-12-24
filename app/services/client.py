import requests, random
from requests import Session, Response
from dataclasses import dataclass
from app.core.config import settings
from app.utils.html_parser import extract_csrf

@dataclass
class PunchClient:
    session: Session = requests.Session()

    def login(self) -> None:
        r: Response = self.session.get(url=settings.login_url)
        csrf: str = extract_csrf(html=r.text)

        payload = {
            "csrfmiddlewaretoken": csrf,
            "username": settings.username,
            "password": settings.password,
            "language": "zh-hant",
        }

        resp = self.session.post(
            settings.login_url,
            data=payload,
            headers={"Referer": settings.login_url},
            allow_redirects=False,
        )

        if resp.status_code != 302:
            raise RuntimeError("Login failed")
        
    def clock_in(self) -> None:
        r: Response = self.session.get(url=settings.dashboard_url)
        csrf: str = extract_csrf(html=r.text)
        
        payload = {
            "csrfmiddlewaretoken": csrf,
            "lat": settings.company_lat,
            "lng": settings.company_lng,
            "accuracy": random.randint(10, 50)
        }

        resp = self.session.post(
            settings.clockin_url,
            data=payload,
            headers={"Referer": settings.dashboard_url},
            allow_redirects=False,
        )

        if resp.status_code != 302:
            raise RuntimeError("Clock-in failed")
        
    def clock_out(self) -> None:
        r: Response = self.session.get(url=settings.dashboard_url)
        csrf: str = extract_csrf(html=r.text)
        
        payload = {
            "csrfmiddlewaretoken": csrf,
            "lat": settings.company_lat,
            "lng": settings.company_lng,
        }

        resp = self.session.post(
            settings.clockout_url,
            data=payload,
            headers={"Referer": settings.dashboard_url},
            allow_redirects=False,
        )

        if resp.status_code != 302:
            raise RuntimeError("Clock-in failed")
