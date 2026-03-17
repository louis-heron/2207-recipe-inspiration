from ultralytics import YOLO
from pathlib import Path

model_path = "Vision/best.pt"

class IngredientDetector:
    def __init__(self):
        self.model = YOLO(model_path)

    def detect(self, image_bytes):
        # Run results
        results = self.model(image_bytes)

        # Extract unique class names detected
        detected_ingredients = []
        for r in results:
            for c in r.boxes.cls:
                label = self.model.names[int(c)]
                if label not in detected_ingredients:
                    detected_ingredients.append(label)

        return detected_ingredients
