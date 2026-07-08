import cv2
import os
from ultralytics import YOLO
import time

print("yolo multi-class object detector in installed")



vision_model= YOLO("yolov8n.pt")


image_path="images.jpg"
if not os.path.exists(image_path):
    print(" image name images.jpg  not found")
    exit()

frame=cv2.imread(image_path)
print("image is loaded into memory")
start_time=time.perf_counter()
vision_result=vision_model(frame,verbose=False)
end_time=time.perf_counter()

latency_ms = (end_time - start_time) * 1000
print(f"⏱️ Inference Latency: {latency_ms:.2f} ms")


filename="vision_profile.txt"
with open(filename, "w", encoding="utf-8") as file:
    file.write("Detected_Class,latency,confidence_score,Aspect-ratio,gain-profile,X1,Y1,X2,Y2\n")
for result in vision_result:
    for box in result.boxes:
        class_id=int(box.cls[0])
        class_name = vision_model.names[class_id]
        coords = box.xyxy[0].tolist()
        width=coords[0]-coords[2]
        height=coords[1]-coords[3]
        aspect_ratio=width/height if height != 0 else 0.0
    
        # If aspect ratio is thin (< 0.8), it's a pedestrian. If wide (>= 0.8), it's a vehicle.
        if aspect_ratio < 0.8:
            command_profile = "SMOOTH"
        else:
            command_profile = "HIGH_SPEED"

        

        confidence_score = float(box.conf[0])

        # 🛠️ FIXED STEP: Added the active data cleaning fence condition
        if confidence_score > 0.65:
            with open(filename, "a", encoding="utf-8") as f:
                # Create a string line starting with the class name, followed by the confidence and 4 coordinates
                coord_string = f"{class_name},{latency_ms:.1f},{confidence_score:.2f},{aspect_ratio:.2f},{command_profile},{coords[0]:.1f},{coords[1]:.1f},{coords[2]:.1f},{coords[3]:.1f}"
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




