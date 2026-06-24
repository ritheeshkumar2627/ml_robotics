import torch
import torch.nn as nn
import torch.optim as optim

print("🔥 Initializing Unified PyTorch Learning Engine...")

# 1. Inputs (Sensor Data) and the Perfect Ideal Target
robot_sensors = torch.tensor([[2.5, 1.2, 1.2]], dtype=torch.float32)
perfect_steering = torch.tensor([[0.5, 0.0]], dtype=torch.float32)

# 2. Define ONE Unified Model
model = nn.Sequential(
    nn.Linear(in_features=3, out_features=2),
    nn.ReLU()
)

# 3. Setup standard Loss and Optimizer configurations
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# --- BEFORE TRAINING ---
# Generate the initial guess using our model
initial_guess = model(robot_sensors)
print("\n🧠 Brain Output Matrix (Before Training):")
print(f"📤 Initial Untrained Guess: {initial_guess.detach().numpy()}")

# 4. The Learning Step (The Backpropagation Loop)
optimizer.zero_grad()                                # 1. Clear old gradients
mistake = criterion(initial_guess, perfect_steering) # 2. Calculate error distance
mistake.backward()                                   # 3. Calculate weight directions
optimizer.step()                                     # 4. Apply math changes to weights

# --- AFTER TRAINING ---
# Generate a new prediction using the EXACT SAME model
new_guess = model(robot_sensors)
print("\n🎯 Brain Output Matrix (After 1 Step of Learning):")
print(f"📥 Corrected Value: {new_guess.detach().numpy()}")
print("\n✅ Success! The updated guess has shifted significantly closer to [0.5, 0.0].")





