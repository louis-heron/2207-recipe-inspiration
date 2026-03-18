"""Home section — hero content."""
import base64
from pathlib import Path

import streamlit.components.v2 as components_v2

FRONTEND = Path(__file__).parent / "frontend"
_IMG_DIR = Path(__file__).parent.parent.parent / "static" / "img"

home_component = components_v2.component(
    "home",
    html="""
        <main id="home">
          <h1>Find your next recipe</h1>
          <p>
            Is your fridge overflowing with food, just like your cupboards,
            but you're lacking inspiration for what to cook?
          </p>
          <p>
            Don't panic—we have the solution. Take a photo of what you have
            on hand, or of what you'd like to eat, and we'll select the most
            suitable recipes.
          </p>
          <p>
            You don't always have to go out to restock; most of the time,
            we'll find a recipe that perfectly matches your ingredients.
          </p>
          <a href="/inspiration" class="cta-link">Get inspired</a>
        </main>
    """,
    css=(FRONTEND / "style.css").read_text(encoding="utf-8"),
    js="""
const renderer = ({ data, parentElement }) => {
  if (data.head_chef_url) {
    const el = parentElement.querySelector('main#home');
    if (el) el.style.setProperty('--head-chef-photo', 'url("' + data.head_chef_url + '")');
  }
};
export default renderer;
""",
)


def home_section(key: str | None = None) -> None:
    b64 = base64.b64encode((_IMG_DIR / "head_chef.png").read_bytes()).decode()
    head_chef_url = "data:image/png;base64," + b64
    home_component(data={"head_chef_url": head_chef_url}, key=key, isolate_styles=False)
