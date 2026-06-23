import numpy as np
from PIL import Image, ImageDraw
from ultralytics import YOLO

# 1. Create a fake image entirely through code (No internet download needed!)
print("🎨 Generating a custom test image...")
img = Image.new("RGB", (640, 480), color=(200, 200, 200))
draw = ImageDraw.Draw(img)

# Draw a blue rectangle to mimic an object box
draw.rectangle([200, 150, 400, 350], fill=(0, 0, 255))
img.save("test_shape.jpg")

# 2. Load the lightweight YOLO model
print("🔄 Loading YOLOv8 architecture...")
model = YOLO("yolov8n.pt")

# 3. Run object detection inference on the generated file
print("🧠 Running object detection inference...")
results = model("test_shape.jpg")

# 4. Save the visual bounding box output to your workspace
for result in results:
    result.save(filename="detected_output.jpg")

print("✅ Success! Open 'detected_output.jpg' from the left sidebar to see the results.")
