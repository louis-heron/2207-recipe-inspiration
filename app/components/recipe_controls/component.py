"""Recipe controls component — slider + get recipes button."""
from pathlib import Path

import streamlit.components.v2 as components_v2

FRONTEND = Path(__file__).parent / "frontend"
JS_PATH  = FRONTEND / "dist" / "index.mjs"
CSS_PATH = FRONTEND / "style.css"

if not JS_PATH.exists():
    raise FileNotFoundError(
        f"Recipe controls not compiled. Run: cd {FRONTEND} && npm run build"
    )

_HTML = """
<form class="ri-controls__form" aria-label="Recipe options" onsubmit="return false">
  <label for="ri-num-recipes" class="ri-controls__label">
    How many recipes?
    <output id="ri-num-output" class="ri-controls__output" for="ri-num-recipes">5</output>
  </label>
  <input
    type="range"
    id="ri-num-recipes"
    class="ri-controls__slider"
    min="1"
    max="10"
    value="5"
    aria-valuemin="1"
    aria-valuemax="10"
    aria-valuenow="5"
  />
  <button type="button" id="ri-get-recipes-btn" class="ri-controls__submit">
    Get Recipes
  </button>
</form>
"""

recipe_controls_component = components_v2.component(
    "recipe_controls",
    html=_HTML,
    css=CSS_PATH.read_text(encoding="utf-8"),
    js=JS_PATH.read_text(encoding="utf-8"),
    isolate_styles=False,
)


def recipe_controls(*, key: str = "recipe-controls"):
    """Render slider + get recipes button. Returns (num_recipes, get_recipes_clicked)."""
    result = recipe_controls_component(
        on_num_recipes_change=lambda: None,
        on_get_recipes_clicked_change=lambda: None,
        key=key,
    )
    if not result:
        return 5, False
    num = result.num_recipes if result.num_recipes is not None else 5
    return num, bool(result.get_recipes_clicked)
