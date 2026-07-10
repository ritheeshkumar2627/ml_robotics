import os
from ultralytics import YOLO
import cv2
import time
vision_model=YOLO('yolov8n.pt')
path="images.jpg"
if not os.path.exists(path):
    print(f"image named {path} not found")
    exit()

frame=cv2.imread(path)
print("image is loaded")
final_system_status="clear"

vision_results=vision_model(frame,verbose=False)
for result in vision_results:
    for box in result.boxes:
        class_id=int(box.cls[0])
        class_name=vision_model.names[class_id]
        coords=box.xyxy[0].tolist()
        height=coords[3]-coords[1]
        estimated_distance=500/height if height>0 else 1000
        if estimated_distance<4:
            final_system_status="critical brake"
        
        
filename = "autopilot_signal.cfg"
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"CONTROL_STATUS={final_system_status}\n")

print(f"📡 Perception complete. Live override state '{final_system_status}' dispatched to '{filename}'.")