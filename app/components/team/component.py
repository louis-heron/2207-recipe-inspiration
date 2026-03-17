"""Team section — hexagonal orbit with flip effect."""
from pathlib import Path
from typing import TypedDict

import streamlit.components.v2 as components_v2

class TeamMember(TypedDict):
    name: str
    photo_url: str
    quote: str
    cite: str
    linkedin: str


FRONTEND = Path(__file__).parent / "frontend"
JS_PATH = FRONTEND / "dist" / "index.mjs"
CSS_PATH = FRONTEND / "style.css"
_LOGO_SVG = (Path(__file__).parent.parent.parent / "static" / "img" / "logo.svg").read_text(encoding="utf-8")

if not JS_PATH.exists():
    raise FileNotFoundError(
        f"Team component not compiled. Run : cd {FRONTEND} && npm run build"
    )

team_component = components_v2.component(
    "team",
    html=f"""
        <section id="team-orbit">
          <figure class="hex-central">
            <figcaption>
              {_LOGO_SVG}
              <p>Recipe Inspiration</p>
            </figcaption>
          </figure>
          <ul class="hex-list"></ul>
        </section>
    """,
    css=CSS_PATH.read_text(encoding="utf-8"),
    js=JS_PATH.read_text(encoding="utf-8"),
)


def team_section(members: list[TeamMember], key: str | None = None) -> None:
    team_component(data={"members": members}, key=key, isolate_styles=False, height=700)
