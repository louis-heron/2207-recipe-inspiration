from pathlib import Path

import streamlit as st

from components.footer import footer
from components.header import header

st.set_page_config(
    page_title="Recipe Inspiration",
    layout="wide",
)

st.markdown("""
<style>
[data-testid="stMain"] {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}
[data-testid="stMain"] .block-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding-bottom: 0 !important;
}
[data-testid="stVerticalBlock"] {
    flex: 1;
    display: flex;
    flex-direction: column;
}
[data-testid="stVerticalBlock"] > *:last-child {
    margin-top: auto;
}
</style>
""", unsafe_allow_html=True)

_NAV_LINKS = [
    {"label": "Home", "page": "pages/0_home.py"},
    {"label": "Inspiration", "page": "pages/1_inspiration.py"},
    {"label": "Team", "page": "pages/2_team.py"},
]

home = st.Page("pages/0_home.py", title="Home")
inspiration = st.Page("pages/1_inspiration.py", title="Inspiration")
team = st.Page("pages/2_team.py", title="Team")
recipes = st.Page("pages/3_recipes.py", title="Recipes")

pages = st.navigation([home, inspiration, team, recipes], position="hidden")

_LOGO_SVG = (Path(__file__).parent / "static" / "img" / "logo.svg").read_text(encoding="utf-8")

header(
    logo_svg=_LOGO_SVG,
    logo_alt="Recipe Inspiration",
    logo_page="pages/0_home.py",
    nav_links=_NAV_LINKS,
    active_page=pages.title,
    key="main-header",
)

pages.run()

footer(
    copyright="2026 Recipe Inspiration — A Le Wagon project",
    key="main-footer",
)
