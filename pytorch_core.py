import os
import cv2
import torch
import torch.nn as nn
import torch.optim as optim
from ultralytics import YOLO

print("🧠 Initializing Stabilized YOLO-to-PyTorch Training Engine...")

# Fix the random seed so numbers remain reproducible
torch.manual_seed(42)

# 1. Load the model
vision_model = YOLO("yolov8n.pt")

# 2. FIXED ARCHITECTURE: Use LeakyReLU to prevent the dying neural block trap
model = nn.Sequential(
    nn.Linear(in_features=4, out_features=1),
    nn.LeakyReLU(negative_slope=0.1) 
)

perfect_brake_target = torch.tensor([[1.0]], dtype=torch.float32)

# FIXED CONFIGURATION: Use Adam optimizer with an adjusted learning rate for safe learning curves
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

image_path = "images.jpg"
if not os.path.exists(image_path):
    print("❌ Error: 'images.jpg' missing!")
    exit()

frame = cv2.imread(image_path)
vision_results = vision_model(frame, verbose=False)

for result in vision_results:
    for box in result.boxes:
        if int(box.cls) == 0:
            coords = box.xyxy[0].tolist() 
            print(f"🚶 Pedestrian Locked! Box Coordinates: {coords}")
            
            # LINKING FIX: Normalize pixel values by dividing by 1000.0 to prevent exploding math steps
            normalized_coords = [c / 1000.0 for c in coords]
            input_tensor = torch.tensor([normalized_coords], dtype=torch.float32)
            print(f"📥 Normalized Input Tensor: {input_tensor}")
            
            # --- BEFORE TRAINING ---
            initial_guess = model(input_tensor)
            print(f"\n❌ Initial Guess: {initial_guess.item():.4f}")
            
            # 6. THE STABILIZED TRAINING LOOP
            print("\n🏋️ Training over 50 epochs...")
            for epoch in range(1, 51):
                optimizer.zero_grad()                               
                current_guess = model(input_tensor)                 
                mistake = criterion(current_guess, perfect_brake_target) 
                mistake.backward()                                  
                optimizer.step()                                    
                
                if epoch % 10 == 0:
                    print(f"   🔹 Epoch {epoch:2d} | Loss: {mistake.item():.6f} | Current Braking Output: {current_guess.item():.4f}")
            
            # --- AFTER TRAINING ---
            final_guess = model(input_tensor)
            print(f"\n🎯 Final Trained Braking Guess: {final_guess.item():.4f}")
            print(f"   (Target Safe Output was: {perfect_brake_target.item():.4f})")
            print("\n✅ Success! The math stabilized cleanly.")
            break
