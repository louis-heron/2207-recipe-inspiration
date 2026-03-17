"""Header component — main navigation bar."""
from pathlib import Path

import streamlit as st
import streamlit.components.v2 as components_v2

FRONTEND = Path(__file__).parent / "frontend"
JS_PATH  = FRONTEND / "dist" / "index.mjs"
CSS_PATH = FRONTEND / "style.css"

if not JS_PATH.exists():
    raise FileNotFoundError(
        f"Header non compilé. Lance : cd {FRONTEND} && npm run build"
    )

header_component = components_v2.component(
    "header",
    html="",
    css=CSS_PATH.read_text(encoding="utf-8"),
    js=JS_PATH.read_text(encoding="utf-8"),
    isolate_styles=False,
)


def header(
    logo_svg: str,
    logo_alt: str = "Recipe Inspiration - Return at home",
    logo_page: str = "app.py",
    nav_links: list[dict[str, str]] | None = None,
    active_page: str = "",
    key: str | None = None,
) -> None:
    result = header_component(
        data={
            "logo_svg": logo_svg,
            "logo_alt": logo_alt,
            "logo_page": logo_page,
            "nav_links": nav_links or [],
            "active_page": active_page,
        },
        on_page_clicked_change=lambda: None,
        key=key,
    )
    if result and result.page_clicked:
        st.switch_page(result.page_clicked)
