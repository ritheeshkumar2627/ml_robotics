import os
import cv2
from ultralytics import YOLO

print("✂️ Initializing YOLO-to-OpenCV Object Cropper Pipeline...")

# 1. Load your lightweight YOLO vision model architecture
vision_model = YOLO("yolov8n.pt")

# 2. Check if your downloaded photo exists in the folder workspace
image_path = "images.jpg"
if not os.path.exists(image_path):
    print("❌ Error: 'images.jpg' missing! Drag and drop it into your folder first.")
    exit()

# 3. Read the image layer using OpenCV
frame = cv2.imread(image_path)
print("📥 Real image layer loaded into memory successfully.")

# 4. Pass the frame through YOLO to detect objects
vision_results = vision_model(frame, verbose=False)

# 5. Extract bounding box coordinates and slice the pixel matrix arrays
for result in vision_results:
    if len(result.boxes) > 0:
        # Get the first bounding box detected
        box = result.boxes[0]
        coords = box.xyxy[0].tolist() # Extract pixel boundaries: [X1, Y1, X2, Y2]
        
        # Convert coordinate floats to integers for pixel indices
        x1, y1, x2, y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])
        print(f"\n👁️ YOLO Target Locked! Box Coordinates: [X1={x1}, Y1={y1}, X2={x2}, Y2={y2}]")
        
        # SLICING STEP: Extract the object pixels using standard matrix slicing [height, width]
        cropped_object = frame[y1:y2, x1:x2]
        
        # 6. Save the cropped slice as a brand new image file locally
        output_filename = "cropped_target.jpg"
        cv2.imwrite(output_filename, cropped_object)
        
        print(f"💾 Success! Object sliced and saved cleanly as '{output_filename}'.")
        break
    else:
        print("❓ YOLO ran, but couldn't identify any known objects in this image.")
