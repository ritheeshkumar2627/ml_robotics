import os
import matplotlib.pyplot as plt

print("📊 Initializing AI Performance Visualisation Engine...")

log_filename = "loss_log.txt"

# 1. Error boundary check: Verify if the loss log exists in the folder
if not os.path.exists(log_filename):
    print(f"❌ Error: '{log_filename}' not found! Run your 'pytorch_core.py' script first to generate metrics.")
    exit()

epochs = []
losses = []

# 2. Parse the text data log rows step-by-step
with open(log_filename, "r") as log_file:
    lines = log_file.readlines()
    # Skip the first line layer because it contains the text column headers (Epoch, Loss...)
    for line in lines[1:]:
        if line.strip():
            parts = line.split(",")
            epochs.append(int(parts[0]))
            losses.append(float(parts[1]))

print(f"📥 Successfully extracted {len(epochs)} historical metrics data rows.")

# 3. CONSTRUCT THE VISUAL PLOT: Layout lines, labels, and grid boundaries
plt.figure(figsize=(10, 6))
plt.plot(epochs, losses, label="Training Error (MSE Loss)", color="red", linewidth=2.5)

# Add titles and labels so human recruiters can read it instantly
plt.title("YOLO-to-PyTorch Brain Learning Convergence Curve", fontsize=14, fontweight="bold")
plt.xlabel("Training Steps (Epochs)", fontsize=12)
plt.ylabel("Error Margin (Mean Squared Error Loss)", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=11)

# 4. EXPORT THE GRAPH: Save the final plotted rendering layer as an image
output_graph_name = "learning_curve.png"
plt.savefig(output_graph_name, dpi=300)
plt.close()

print(f"🖼️ Success! Your learning graph has been drawn and saved as '{output_graph_name}'.")
