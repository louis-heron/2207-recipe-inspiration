from ultralytics import YOLO
from pathlib import Path

import io
from PIL import Image

class IngredientDetector:
    def __init__(self, model_path):
        self.model_path = "Vision/best.pt"
        self.model = YOLO(model_path)

    def detect(self, image_bytes):
        # Run results
        image = Image.open(io.BytesIO(image_bytes))
        results = self.model(image)

        # Extract unique class names detected
        detected_ingredients = []
        for r in results:
            for c in r.boxes.cls:
                label = self.model.names[int(c)]
                if label not in detected_ingredients:
                    detected_ingredients.append(label)

        return detected_ingredients
