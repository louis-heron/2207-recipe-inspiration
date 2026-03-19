"""Accessible file uploader component."""
from pathlib import Path

import streamlit.components.v2 as components_v2

FRONTEND = Path(__file__).parent / "frontend"
JS_PATH  = FRONTEND / "dist" / "index.mjs"
CSS_PATH = FRONTEND / "style.css"

if not JS_PATH.exists():
    raise FileNotFoundError(
        f"File uploader not compiled. Run: cd {FRONTEND} && npm run build"
    )

_HTML = """
<section class="ri-upload__wrapper" aria-labelledby="ri-upload-heading">
  <h2 id="ri-upload-heading" class="ri-upload__heading">Upload a photo of your fridge</h2>
  <form class="ri-upload__form">
    <label for="ri-file-input" class="ri-upload__label">
      Drag and drop file here
      <small>JPG, JPEG or PNG</small>
      <input
        type="file"
        id="ri-file-input"
        class="ri-upload__input"
        accept=".jpg,.jpeg,.png,image/jpeg,image/png"
        aria-describedby="ri-upload-status"
      />
    </label>
    <p id="ri-upload-status" role="status" class="ri-upload__status">No file selected</p>
    <button type="button" id="ri-detect-btn" class="ri-upload__detect" hidden>
        Detect Ingredients
    </button>
  </form>
  <figure class="ri-upload__preview" hidden>
    <img id="ri-preview-img" alt="" />
    <figcaption id="ri-preview-caption"></figcaption>
  </figure>
</section>
"""

file_uploader = components_v2.component(
    "accessible_file_uploader",
    html=_HTML,
    css=CSS_PATH.read_text(encoding="utf-8"),
    js=JS_PATH.read_text(encoding="utf-8"),
    isolate_styles=False,
)


def accessible_file_uploader(*, key: str = "file-uploader"):
    """Render an accessible file uploader. Returns (file_info, detect_clicked)."""
    result = file_uploader(
        on_file_change=lambda: None,
        on_detect_clicked_change=lambda: None,
        key=key,
    )
    if not result:
        return None, False
    return result.file, bool(result.detect_clicked)
