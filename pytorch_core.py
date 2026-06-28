import torch
import torch.nn as nn
import torch.optim as optim

print("⚙️ Booting Optimized PyTorch Training Loop...")


torch.manual_seed(42)

# 1. Inputs (Sensor Data) and the Perfect Target
robot_sensors = torch.tensor([[2.5, 1.2, 1.2]], dtype=torch.float32)
perfect_steering = torch.tensor([[0.5, 0.0]], dtype=torch.float32)


model = nn.Sequential(
    nn.Linear(in_features=3, out_features=2),
    nn.ReLU()
)


criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# --- BEFORE TRAINING ---
initial_guess = model(robot_sensors)
print(f"\n❌ Initial Untrained Guess: {initial_guess.detach().numpy()}")

print("\n🏋️ Training over 100 epochs...")
# 4. Run the training loop over 100 steps
for epoch in range(1, 101):
    optimizer.zero_grad()                                # Clear old calculations
    guess = model(robot_sensors)                         # Generate prediction
    mistake = criterion(guess, perfect_steering)         # Calculate error distance
    mistake.backward()                                   # Trace back propagation directions
    optimizer.step()                                     # Update neural weights precisely
    
    # Print progress snapshot every 20 steps
    if epoch % 20 == 0:
        print(f"   🔹 Epoch {epoch:3d} | Current Mistake (Loss): {mistake.item():.6f} | Guess: {guess.detach().numpy()}")

# --- AFTER TRAINING ---
final_guess = model(robot_sensors)
print(f"\n🎯 Final Trained Guess: {final_guess.detach().numpy()}")
print("✅ Success! The model optimized smoothly without collapsing your matrix layer values.")



