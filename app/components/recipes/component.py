"""Recipe cards component."""
from pathlib import Path

import streamlit.components.v2 as components_v2

FRONTEND = Path(__file__).parent / "frontend"
JS_PATH  = FRONTEND / "dist" / "index.mjs"
CSS_PATH = FRONTEND / "style.css"

if not JS_PATH.exists():
    raise FileNotFoundError(
        f"Recipes component not compiled. Run: cd {FRONTEND} && npm run build"
    )

recipes_component = components_v2.component(
    "recipes",
    html="",
    css=CSS_PATH.read_text(encoding="utf-8"),
    js=JS_PATH.read_text(encoding="utf-8"),
    isolate_styles=False,
)


def recipes_section(
    recipes: list[dict],
    ingredients_used: list[str],
    key: str | None = None,
) -> None:
    """Render the recipes page: title, summary, and recipe cards grid."""
    recipes_component(
        data={"recipes": recipes, "ingredients_used": ingredients_used},
        key=key,
    )
