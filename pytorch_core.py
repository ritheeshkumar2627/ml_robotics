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
for result in vision_result:
    for box in result.boxes:
        if int(box.cls) == 0:  # Lock onto first pedestrian
            base_coords = box.xyxy[0].tolist()
            break

if base_coords is None:
    print("❌ Error: No pedestrians detected.")
    exit()

# 6. FILE WRITING DATA GENERATOR STEP
output_filename = "dataset_inputs.txt"
with open(output_filename, "a") as f:
    # Convert our list of numbers into a clean comma-separated text line string
    coord_string = ",".join([str(c) for c in base_coords])
    f.write(coord_string + "\n")

print(f"💾 Success! Pedestrian coordinates saved cleanly into '{output_filename}'.")




