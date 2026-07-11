import os
import cv2
import time
from ultralytics import YOLO

print("🎬 Initializing Headless Production Stream Perception Node...")

vision_model = YOLO("models/yolov8n.pt")

video_path = "videos.mp4"
if not os.path.exists(video_path):
    print(f"❌ Input Stream Error: Video file '{video_path}' not found.")
    exit(1)

cap = cv2.VideoCapture(video_path)

# Extract stream metadata properties from the video file
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define our automated export video writer using the high-performance MP4V codec
output_path = "output_stream.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

print(f"🚀 Processing frame buffers headless... Saving results directly to '{output_path}'")

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    start_time = time.perf_counter()
    vision_results = vision_model(frame, verbose=False)
    end_time = time.perf_counter()
    latency_ms = (end_time - start_time) * 1000
    
    for result in vision_results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = vision_model.names[class_id]
            
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{class_name} ({latency_ms:.1f}ms)", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write the compiled tracking frame matrix slice straight to our output file container
    out.write(frame)
    frame_count += 1
    
    if frame_count % 50 == 0:
        print(f"📥 Processed {frame_count} frames successfully...")

# Release all allocated file handlers and sync memory registers to disk completely
cap.release()
out.release()
print(f"🛑 Done! Telemetry tracking stream exported cleanly to '{output_path}'.")

