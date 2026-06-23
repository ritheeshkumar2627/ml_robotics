import os
import cv2
import numpy as np
from ultralytics import YOLO

# 1. Generate a synthetic moving video entirely via code (No internet required!)
video_path = "traffic_input.mp4"
output_path = "output_tracked.mp4"

if not os.path.exists(video_path):
    print("🎨 Generating a custom moving test video locally...")
    # Create a video writer (640x480 resolution, 30 frames per second)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_gen = cv2.VideoWriter(video_path, fourcc, 30.0, (640, 480))
    
    # Create 90 frames (3 seconds of video) where a shape moves across the screen
    for frame_idx in range(90):
        # Create a blank gray canvas frame
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 200
        
        # Make a box move horizontally across frames
        x_start = 50 + (frame_idx * 5)
        y_start = 200
        
        # Draw a solid blue square block onto the frame
        cv2.rectangle(frame, (x_start, y_start), (x_start + 100, y_start + 100), (255, 0, 0), -1)
        out_gen.write(frame)
        
    out_gen.release()
    print("✅ Local video creation complete.")

# 2. Load the lightweight YOLOv8 model
print("🔄 Loading YOLOv8 architecture...")
model = YOLO("yolov8n.pt")

# 3. Initialize OpenCV video handlers to read our newly created video
cap = cv2.VideoCapture(video_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Set up video writer output configurations
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

print("🧠 Running object tracking on video layers...")
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    # Run YOLO detection tracking model frame-by-frame
    results = model(frame, verbose=False)
    
    # Extract the annotated canvas frame showing tracking boxes
    annotated_frame = results[0].plot()
    
    # Save the processed image layer frame to output video file
    out.write(annotated_frame)
    frame_count += 1
    if frame_count % 30 == 0:
        print(f"   Processed {frame_count} frames...")

cap.release()
out.release()
print("✅ Success! Open 'output_tracked.mp4' from the left sidebar to see the results.")
