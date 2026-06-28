import os
import cv2
from ultralytics import YOLO

print("🔍 Initializing YOLO Multi-Object Class Filter Engine...")

# 1. Load your standard, CPU-optimized YOLOv8 model architecture [1.1]
vision_model = YOLO("yolov8n.pt")

# 2. Check if your downloaded photo exists in the folder workspace
image_path = "images.jpg"
if not os.path.exists(image_path):
    print("❌ Error: 'images.jpg' missing! Make sure it is in your directory.")
    exit()

# 3. Read the image layer using OpenCV [1.1]
frame = cv2.imread(image_path)
print("📥 Real image layer loaded into memory successfully.")

# 4. Pass the frame through YOLO to detect all objects
vision_results = vision_model(frame, verbose=False)

print("\n🕵️ Parsing detection array parameters...")
person_counter = 0

# 5. Loop through all detected objects in the results layout
for result in vision_results:
    for box in result.boxes:
        # Extract the numeric Class ID (YOLO codes '0' for person, '5' for bus, etc.)
        class_id = int(box.cls[0])
        
        # FILTER LAYER: Focus ONLY if the detected object is a person (Class ID 0)
        if class_id == 0:
            person_counter += 1
            
            # Extract coordinates for this specific person: [X1, Y1, X2, Y2]
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])
            
            print(f"🚶 Person #{person_counter} Isolated! Bounding Box: [X1={x1}, Y1={y1}, X2={x2}, Y2={y2}]")
            
            # Draw a visual green rectangle box over the person on our image matrix array
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 6. Save the final filtered image showing highlighted targets
if person_counter > 0:
    output_filename = "filtered_targets.jpg"
    cv2.imwrite(output_filename, frame)
    print(f"\n💾 Success! Saved highlighted tracking layout as '{output_filename}'.")
else:
    print("\n❓ YOLO ran, but did not find any pedestrians in this frame image layer.")
