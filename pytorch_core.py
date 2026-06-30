import os
import cv2
import torch
import torch.nn as nn
import torch.optim as optim
import random
from ultralytics import YOLO

print("📈 Initializing YOLO-to-PyTorch Metric Logging Engine...")

# Fix seed for reproducibility where applicable
torch.manual_seed(42)

# 1. Load your standard CPU-optimized YOLOv8 model architecture
vision_model = YOLO("yolov8n.pt")

# 2. Define the brain network architecture
model = nn.Sequential(
    nn.Linear(in_features=4, out_features=1),
    nn.LeakyReLU(negative_slope=0.1)
)

perfect_brake_target = torch.tensor([[1.0]], dtype=torch.float32)
optimizer = optim.Adam(model.parameters(), lr=0.01)
criterion = nn.MSELoss()

# 3. Data Augmentation Function 
def augment_coordinates(coords):
    # Add a random shift between -10 and +10 pixels to simulate pedestrian movement
    augmented = [
        coords[0] + random.uniform(-10, 10), # Shift X1
        coords[1] + random.uniform(-10, 10), # Shift Y1
        coords[2] + random.uniform(-10, 10), # Shift X2
        coords[3] + random.uniform(-10, 10)  # Shift Y2
    ]
    return [c / 1000.0 for c in augmented]

image_path = "images.jpg"
if not os.path.exists(image_path):
    print(f"❌ Error: '{image_path}' missing!")
    exit()

frame = cv2.imread(image_path)
vision_results = vision_model(frame, verbose=False)

base_coords = None
for result in vision_results:
    for box in result.boxes:
        if int(box.cls) == 0:  # Lock onto first pedestrian
            # FIXED: Added [0] to extract the 1D list from the nested 2D list structure
            base_coords = box.xyxy.tolist()[0] 
            break

if base_coords is None:
    print("❌ Error: No pedestrians detected.")
    exit()

print(f"🚶 Base Pedestrian Coordinates Locked: {base_coords}")

# 4. PREPARE THE METRIC FILE: Open a fresh text log file to write training metrics
log_filename = "loss_log.txt"
with open(log_filename, "w") as log_file:
    log_file.write("Epoch,Loss,Current_Braking_Output\n") # Write CSV file headers

# 5. THE RUNNING TRAINING LOOP WITH SYSTEM LOGGING
print("\n🏋️ Training over 50 epochs and exporting metrics...")
for epoch in range(1, 51):
    optimizer.zero_grad()
    
    dynamic_coords = augment_coordinates(base_coords)
    input_tensor = torch.tensor([dynamic_coords], dtype=torch.float32)
    
    current_guess = model(input_tensor)
    mistake = criterion(current_guess, perfect_brake_target)
    mistake.backward()
    optimizer.step()
    
    # 6. LOGGING STEP: Save metrics directly to the text log file
    with open(log_filename, "a") as log_file:
        log_file.write(f"{epoch},{mistake.item():.6f},{current_guess.item():.4f}\n")
        
    if epoch % 10 == 0:
        print(f"   🔹 Epoch {epoch:2d} | Loss: {mistake.item():.6f} | Logged to file cleanly.")

print(f"\n💾 Success! Training run complete. Metrics compiled inside '{log_filename}'.")
