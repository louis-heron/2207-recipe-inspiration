"""Footer component — page footer."""
from pathlib import Path

import streamlit.components.v2 as components_v2

FRONTEND = Path(__file__).parent / "frontend"
JS_PATH  = FRONTEND / "dist" / "index.mjs"
CSS_PATH = FRONTEND / "style.css"

if not JS_PATH.exists():
    raise FileNotFoundError(
        f"Footer non compilé. Lance : cd {FRONTEND} && npm run build"
    )

footer_component = components_v2.component(
    "footer",
    html="",
    css=CSS_PATH.read_text(encoding="utf-8"),
    js=JS_PATH.read_text(encoding="utf-8"),
    isolate_styles=False,
)


def footer(
    copyright: str = "Recipe Inspiration — Un projet Le Wagon",
    links: list[dict] | None = None,
    key: str | None = None,
) -> None:
    footer_component(
        data={
            "copyright": copyright,
            "links": links or [{"label": "Le Wagon", "url": "https://www.lewagon.com"}],
        },
        key=key,
    )
