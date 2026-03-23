import csv
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib


# --------------------------------------------------
# 1. Load Data
# --------------------------------------------------
def load_data(filename="dataset.csv"):
    """Reads CSV, returns numpy arrays for features and target."""
    X, y = [], []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            X.append([
                float(row["thickness"]),
                float(row["camber"]),
                float(row["camber_position"])
            ])
            y.append(float(row["fitness"]))
    return np.array(X), np.array(y).reshape(-1, 1)


# --------------------------------------------------
# 2. Neural Network Definition
# --------------------------------------------------
class FitnessNet(nn.Module):
    """
    Fully connected network: 3 → 64 → 64 → 32 → 1
    ReLU activations with Dropout for regularization.
    """
    def __init__(self):
        super(FitnessNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 64),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.net(x)


# --------------------------------------------------
# 3. Training with Early Stopping
# --------------------------------------------------
def train_model():

    # --- Load and Split ---
    X, y = load_data("dataset.csv")
    print(f"Loaded {len(X)} samples from dataset.csv\n")

    # Split: 70% train, 15% validation, 15% test
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=42
    )

    print(f"Train: {len(X_train)}  |  Val: {len(X_val)}  |  Test: {len(X_test)}\n")

    # --- Scale Inputs and Outputs ---
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()

    X_train = scaler_X.fit_transform(X_train)
    X_val   = scaler_X.transform(X_val)
    X_test  = scaler_X.transform(X_test)

    y_train = scaler_y.fit_transform(y_train)
    y_val   = scaler_y.transform(y_val)
    y_test_scaled = scaler_y.transform(y_test)

    # --- Convert to Tensors ---
    X_train_t = torch.tensor(X_train, dtype=torch.float32)
    y_train_t = torch.tensor(y_train, dtype=torch.float32)
    X_val_t   = torch.tensor(X_val,   dtype=torch.float32)
    y_val_t   = torch.tensor(y_val,   dtype=torch.float32)
    X_test_t  = torch.tensor(X_test,  dtype=torch.float32)

    # --- Model, Loss, Optimizer ---
    model = FitnessNet()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)

    # --- Early Stopping Setup ---
    max_epochs = 2000
    patience = 50
    best_val_loss = float("inf")
    patience_counter = 0
    best_model_state = None

    # --- Training Loop ---
    print("Training started...")
    for epoch in range(max_epochs):

        # Train
        model.train()
        optimizer.zero_grad()
        train_pred = model(X_train_t)
        train_loss = criterion(train_pred, y_train_t)
        train_loss.backward()
        optimizer.step()

        # Validate
        model.eval()
        with torch.no_grad():
            val_pred = model(X_val_t)
            val_loss = criterion(val_pred, y_val_t).item()

        # Print every 100 epochs
        if (epoch + 1) % 100 == 0:
            print(f"  Epoch {epoch+1:4d}/{max_epochs}"
                  f"  |  Train Loss: {train_loss.item():.6f}"
                  f"  |  Val Loss: {val_loss:.6f}")

        # Early stopping check
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            best_model_state = model.state_dict().copy()
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"\nEarly stopping at epoch {epoch+1} (no improvement for {patience} epochs)")
                break

    # --- Load Best Model ---
    if best_model_state is not None:
        model.load_state_dict(best_model_state)

    # --- Evaluate on Test Set ---
    model.eval()
    with torch.no_grad():
        y_pred_scaled = model(X_test_t).numpy()

    # Inverse-transform predictions back to original scale
    y_pred = scaler_y.inverse_transform(y_pred_scaled)

    mse = mean_squared_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)

    print("\n========== Test Results ==========")
    print(f"  MSE:  {mse:.6f}")
    print(f"  R²:   {r2:.6f}")
    print("==================================")

    # --- Save Model and Scalers ---
    torch.save(model.state_dict(), "fitness_model.pth")
    joblib.dump(scaler_X, "scaler_X.pkl")
    joblib.dump(scaler_y, "scaler_y.pkl")

    print("\nSaved:")
    print("  Model   → fitness_model.pth")
    print("  Scalers → scaler_X.pkl, scaler_y.pkl")

    return model, scaler_X, scaler_y


if __name__ == "__main__":
    train_model()
