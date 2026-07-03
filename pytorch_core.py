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
    file.write("Detected_Class,X1,Y1,X2,Y2\n")
for result in vision_result:
    for box in result.boxes:
        class_id=int(box.cls[0])
        class_name = vision_model.names[class_id]
        coords = box.xyxy[0].tolist()
       
        with open(filename, "a", encoding="utf-8") as f:
            # Create a string line starting with the class name, followed by the 4 coordinates
            coord_string = f"{class_name},{coords[0]:.1f},{coords[1]:.1f},{coords[2]:.1f},{coords[3]:.1f}"
            f.write(coord_string + "\n")


print(f"💾 Success! object coordinates saved cleanly into '{filename}'.")




