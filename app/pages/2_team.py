from components.team import TeamMember, team_section

TEAM: list[TeamMember] = [
    {
        "name": "Louis Héron",
        "photo_url": "/app/static/img/louis_heron.png",
        "quote": "A short quote from this person.",
        "cite": "Unknown",
        "linkedin": "#",
    },
    {
        "name": "Pauline Le\u00a0Biez",
        "photo_url": "/app/static/img/pauline_le-biez.png",
        "quote": "A short quote from this person.",
        "cite": "Unknown",
        "linkedin": "#",
    },
    {
        "name": "Yoann Fortin",
        "photo_url": "/app/static/img/yoann_fortin.png",
        "quote": "Choose a job you love, and you’ll never have to work a day in your life.",
        "cite": "Confucius",
        "linkedin": "https://www.linkedin.com/in/yoann-fortin/",
    },
]

team_section(TEAM)
