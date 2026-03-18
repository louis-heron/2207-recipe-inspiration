import base64
from pathlib import Path

from components.team import TeamMember, team_section

_IMG_DIR = Path(__file__).parent.parent / "static" / "img"


def _b64_png(filename: str) -> str:
    data = (_IMG_DIR / filename).read_bytes()
    return "data:image/png;base64," + base64.b64encode(data).decode()


TEAM: list[TeamMember] = [
    {
        "name": "Louis Héron",
        "photo_url": _b64_png("louis_heron.png"),
        "quote": "A short quote from this person.",
        "cite": "Unknown",
        "linkedin": "#",
    },
    {
        "name": "Pauline Le\u00a0Biez",
        "photo_url": _b64_png("pauline_le-biez.png"),
        "quote": "A short quote from this person.",
        "cite": "Unknown",
        "linkedin": "#",
    },
    {
        "name": "Yoann Fortin",
        "photo_url": _b64_png("yoann_fortin.png"),
        "quote": "Choose a job you love, and you'll never have to work a day in your life.",
        "cite": "Confucius",
        "linkedin": "https://www.linkedin.com/in/yoann-fortin/",
    },
]

team_section(TEAM)
