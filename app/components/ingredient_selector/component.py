"""Ingredient selector — ARIA combobox + listbox pattern (WAI-ARIA 1.2)."""
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v2 as components_v2

FRONTEND = Path(__file__).parent / "frontend"
JS_PATH  = FRONTEND / "dist" / "index.mjs"
CSS_PATH = FRONTEND / "style.css"

_PARQUET_PATH = Path(__file__).parent.parent.parent.parent / "ingredients.parquet"

if not JS_PATH.exists():
    raise FileNotFoundError(
        f"Ingredient selector not compiled. Run: cd {FRONTEND} && npm run build"
    )

_HTML = """
<label for="ri-cb-input" class="ri-cb__label" id="ri-cb-label"></label>
<search class="ri-cb__field" id="ri-cb-field">
  <ul
    class="ri-cb__chips"
    id="ri-cb-chips"
    role="list"
    aria-label="Selected ingredients"
  ></ul>
  <input
    type="text"
    id="ri-cb-input"
    class="ri-cb__input"
    role="combobox"
    aria-expanded="false"
    aria-haspopup="listbox"
    aria-autocomplete="list"
    aria-controls="ri-cb-listbox"
    aria-activedescendant=""
    autocomplete="off"
    spellcheck="false"
  />
  <ul
    role="listbox"
    id="ri-cb-listbox"
    class="ri-cb__listbox"
    aria-label="Ingredient suggestions"
    hidden
  ></ul>
</search>
"""

ingredient_selector_component = components_v2.component(
    "ingredient_selector",
    html=_HTML,
    css=CSS_PATH.read_text(encoding="utf-8"),
    js=JS_PATH.read_text(encoding="utf-8"),
    isolate_styles=False,
)


@st.cache_data
def load_ingredient_options() -> list[str]:
    """Load ingredient names from the parquet file."""
    df = pd.read_parquet(_PARQUET_PATH)
    return df["ingredient_name"].tolist()


def ingredient_selector(
    options: list[str],
    selected: list[str] | None = None,
    version: int = 0,
    label: str = "Which ingredients do you have?",
    placeholder: str = "Search for ingredients...",
    key: str = "ingredient-selector",
) -> list[str]:
    """Render an accessible combobox multiselect. Returns selected ingredients."""
    result = ingredient_selector_component(
        data={
            "options": options,
            "selected": selected or [],
            "version": version,
            "label": label,
            "placeholder": placeholder,
        },
        on_selected_change=lambda: None,
        key=key,
    )
    if not result or result.selected is None:
        return selected or []
    return result.selected
