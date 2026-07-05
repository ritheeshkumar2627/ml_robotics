import cv2
import os
from ultralytics import YOLO

print("yolo multi-class object detector in installed")

vision_model= YOLO("yolov8n.pt")

image_path="images.jpg"
if not os.path.exists(image_path):
    print(" image name images.jpg  not found")
    exit()

frame=cv2.imread(image_path)
print("image is loaded into memory")

vision_result=vision_model(frame,verbose=False)
filename="vision_profile.txt"
with open(filename, "w", encoding="utf-8") as file:
    file.write("Detected_Class,confidence_score,X1,Y1,X2,Y2\n")
for result in vision_result:
    for box in result.boxes:
        class_id=int(box.cls[0])
        class_name = vision_model.names[class_id]
        coords = box.xyxy[0].tolist()
        confidence_score = float(box.conf[0])

        # 🛠️ FIXED STEP: Added the active data cleaning fence condition
        if confidence_score > 0.65:
            with open(filename, "a", encoding="utf-8") as f:
                # Create a string line starting with the class name, followed by the confidence and 4 coordinates
                coord_string = f"{class_name},{confidence_score:.2f},{coords[0]:.1f},{coords[1]:.1f},{coords[2]:.1f},{coords[3]:.1f}"
                f.write(coord_string + "\n")


print(f"💾 Success! object coordinates saved cleanly into '{filename}'.")

# 🚨 RIGHT HERE IS WHERE YOU TYPE YOUR SUMMARY GENERATOR (OUTSIDE THE LOOPS)
print("\n📊 Initializing Vision Metric Summary Generator...")

class_counts = {}

# Open and parse the log file rows
with open(filename, "r", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines[1:]:
        if line.strip():
            parts = line.split(",")
            detected_label = parts[0] # Grab the string name from the first column slot
            class_counts[detected_label] = class_counts.get(detected_label, 0) + 1

# Open a fresh file to write out your analytics report totals
summary_filename = "vision_summary.txt"
with open(summary_filename, "w", encoding="utf-8") as summary_file:
    summary_file.write("=== OBJECT DETECTION SUMMARY REPORT ===\n")
    for category_name, total_count in class_counts.items():
        summary_file.write(f"Total {category_name} objects identified: {total_count}\n")

print(f"📝 Success! Analytics summary report compiled inside '{summary_filename}'.")




