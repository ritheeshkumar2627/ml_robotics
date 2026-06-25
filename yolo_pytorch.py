import os
import cv2
import torch
import torch.nn as nn
from ultralytics import YOLO

print("🔗 Activating Connected YOLO-to-PyTorch Core Pipeline...")

# 1. Load your YOLO vision architecture
vision_model = YOLO("yolov8n.pt")

# 2. Define a PyTorch Brain Layer (Takes 4 box numbers -> Outputs 1 Steering Command)
brain_layer = nn.Linear(in_features=4, out_features=1)

# Verify our downloaded photo is sitting in the folder
image_path = "images.jpg"
if not os.path.exists(image_path):
    print("❌ Error: 'images.jpg' missing! Drag and drop it into your folder first.")
    exit()

# 3. Read the real photo using OpenCV
frame = cv2.imread(image_path)
print("📥 Real image layer loaded into the pipeline successfully.")

# 4. Pass the frame through YOLO to detect objects
vision_results = vision_model(frame, verbose=False)

# 5. Extract bounding box coordinates from the first real object found (the bus or person!)
for result in vision_results:
    if len(result.boxes) > 0:
        # Grab coordinates of the very first detected box: [X1, Y1, X2, Y2]
        first_box = result.boxes.xyxy[0].tolist()
        print(f"\n👁️ YOLO Successfully Detected a Real Object! Box Coordinates: {first_box}")
        
        # LINKING STEP: Convert the raw python coordinate list into a PyTorch Tensor matrix
        yolo_input_tensor = torch.tensor([first_box], dtype=torch.float32)
        print(f"🧠 Converted Input Tensor Matrix for Brain: {yolo_input_tensor}")
        
        # 6. Pass YOLO's output numbers straight into PyTorch's math layer! and it guess with random weights without training
        steering_decision = brain_layer(yolo_input_tensor)
        
        print("\n🏎️ Final Autopilot Output Decision:")
        print(f"   └── Calculated Steering Adjustment Force: {steering_decision.item():.4f}")
        print("\n✅ Success! Real visual metrics are driving your deep learning model layer.")
        break
    else:
        print("❓ YOLO ran, but couldn't identify any known objects in this image layer.")
