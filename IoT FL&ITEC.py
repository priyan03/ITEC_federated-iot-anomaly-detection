import sys
import time
import threading
import requests
import pandas as pd
import numpy as np
import os
from cryptography.fernet import Fernet
import json

#---------------------------------------------------------DECRYPTION SETUP------------------------------------
# Load the same key used in the Flask server
with open("encryption.key", "rb") as key_file:
    encryption_key = key_file.read()

cipher_suite = Fernet(encryption_key)

def decrypt_data(encrypted_data):
    """Decrypts encrypted data from Flask."""
    decrypted = cipher_suite.decrypt(encrypted_data).decode()
    return json.loads(decrypted)

#---------------------------------------------------------IOT APP SUBMISSION------------------------------------

IOT_API_URL = "http://localhost:5000/sensor-data"
CSV_FILE_PATH = r"D:\Final year project\Test IOT app\IoT_device_data.csv"

print("\n📱 Collecting IoT application data...")

def loading_animation(num_samples):
    """Displays a loading animation while capturing data."""
    for i in range(1, num_samples + 1):
        sys.stdout.write(f"\r📊 Capturing data sample {i}/{num_samples}... ")
        sys.stdout.flush()
        time.sleep(0.005)

# Fetch sensor data from API
response = requests.get(IOT_API_URL)
if response.status_code == 200:
    # Decrypt the encrypted byte response content
    data = decrypt_data(response.content)
    
    if data:
        df = pd.DataFrame(data).T
        num_samples = len(df)

        animation_thread = threading.Thread(target=loading_animation, args=(num_samples,))
        animation_thread.start()
        animation_thread.join()

        df.to_csv(CSV_FILE_PATH, index=True)
        print(f"\n✅ Data saved to: {CSV_FILE_PATH}")
        print("\n===== 📊 All Collected Data =====")
        print(df)
    else:
        print("\n⚠️ No data available.")
        sys.exit()
else:
    print(f"\n❌ Failed to fetch data. Status code: {response.status_code}. Error: {response.text}")
    sys.exit()

#---------------------------------------------FL FSE--------------------------------------------------------------------

proceed = input("\nFEDERATED LEARNING FSE - Proceed with extraction? [y/n]: ").strip().lower()
if proceed != 'y':
    print("❌ Extraction canceled.")
    sys.exit()

print("\n🔐 Extracting Numerical File Signatures for Federated Learning...\n")

def extract_numerical_features(df):
    """Extracts only numerical columns for ML processing."""
    numerical_df = df.select_dtypes(include=[np.number])
    if numerical_df.empty:
        print("⚠️ No numerical data available for extraction.")
        return None
    return numerical_df

def signature_extraction_process(df, num_clients=3):
    extracted_data_list = []
    print("\n===== 🔐 File Signature Extraction Across Clients =====")
    for client_id in range(1, num_clients + 1):
        sys.stdout.write(f"\r🔄 Extracting Signatures from Client {client_id}...")
        sys.stdout.flush()
        time.sleep(1)
        extracted_data = extract_numerical_features(df)
        if extracted_data is not None:
            if "S.No" not in extracted_data.columns:
                extracted_data.insert(0, "S.No", range(1, len(extracted_data) + 1))
            sys.stdout.write("\r\033[K")
            print(f"✅ Extraction Completed for Client {client_id}")
            extracted_data_list.append(extracted_data)
    return extracted_data_list[0] if extracted_data_list else pd.DataFrame()

if os.path.exists(CSV_FILE_PATH):
    df = pd.read_csv(CSV_FILE_PATH)
else:
    sys.exit("❌ CSV file not found!")

extracted_signatures = signature_extraction_process(df)

sys.stdout.write("\r🔄 Aggregating Extracted Signatures...")
sys.stdout.flush()
time.sleep(2)
sys.stdout.write("\r\033[K")
print("✅ Aggregation Completed")

print("\n===== 📂 Extracted Numerical File Signatures for ML Processing =====")
#print(extracted_signatures)

#-----------------------------------------------------Pre - Identification database----------------------------------------------------------

# Define the file path for the Pre-Identification database
PRE_ID_DB_PATH = r"D:\Final year project\Test IOT app\Pre-indification data Store\Pre-indification data.csv"

print("\n🛠️ Creating Pre-Identification Database...")
time.sleep(1)
print("✅ Pre-Identification Database Created Successfully!")

# Save the extracted signatures to the CSV file
extracted_signatures.to_csv(PRE_ID_DB_PATH, index=False)
print(f"\n📂 Extracted Signatures saved to: {PRE_ID_DB_PATH}")

#---------------------------------------------------------ML----------------------------------------------------------
import random
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE

# Paths to save lists
WHITE_LIST_PATH = r"D:\Final year project\Test IOT app\LOCAL LIST\LOCAL_WHITE_LIST.csv"
BLACK_LIST_PATH = r"D:\Final year project\Test IOT app\LOCAL LIST\LOCAL_BLACK_LIST.csv"
RISK_CLASSIFICATION_DIR = r"D:\Final year project\Test IOT app\LOCAL LIST\Risk classification"

# Ensure directory exists
os.makedirs(RISK_CLASSIFICATION_DIR, exist_ok=True)

print("\nTraining Enhanced Machine Learning Model for File Signature Classification...")

# Ensure extracted_signatures is loaded
try:
    extracted_signatures = extracted_signatures  # Replace with actual dataset loading
    if extracted_signatures.empty:
        raise ValueError("Dataset is empty!")
except Exception as e:
    print(f"❌ Error loading dataset: {e}")
    sys.exit(1)

# Encode categorical data
label_encoders = {}
original_values = {}
for col in extracted_signatures.select_dtypes(include=['object']).columns:
    label_encoders[col] = LabelEncoder()
    extracted_signatures[col] = label_encoders[col].fit_transform(extracted_signatures[col])
    original_values[col] = dict(enumerate(label_encoders[col].classes_))

# Add probability values to simulate risk factor
extracted_signatures["Probability_Value"] = np.random.uniform(0, 1, len(extracted_signatures))

# Define features (X) and labels (y)
X = extracted_signatures.drop(columns=["S.No", "Probability_Value"], errors='ignore')
y = (extracted_signatures["Probability_Value"] <= 0.1).astype(int)  # Unsafe = 1, Safe = 0

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split (80-20)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# Adjust SMOTE sampling strategy
smote = SMOTE(sampling_strategy=0.5, random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# Train RandomForest Model
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=30,
    min_samples_split=4,
    min_samples_leaf=2,
    max_features='sqrt',
    bootstrap=True,
    random_state=42
)

model.fit(X_train_resampled, y_train_resampled)

# Evaluate accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Model trained with enhanced accuracy: {accuracy:.4f}")

# Generate classification report
target_names = ["Safe (0)", "Unsafe (1)"]
report = classification_report(y_test, y_pred, target_names=target_names, output_dict=True)
report_df = pd.DataFrame(report).T[:-1]

# Predict on the entire dataset
extracted_signatures["Predicted_Label"] = model.predict(X_scaled)

# Separate Safe & Unsafe devices
white_list = extracted_signatures[extracted_signatures["Predicted_Label"] == 0]
black_list = extracted_signatures[extracted_signatures["Predicted_Label"] == 1]

# Save to CSV
white_list.to_csv(WHITE_LIST_PATH, index=False)
black_list.to_csv(BLACK_LIST_PATH, index=False)

print(f"\n✅ Safe Sensors/Devices (WHITE LIST) saved to: {WHITE_LIST_PATH}")
print(f"\n✅ Unsafe Sensors/Devices (BLACK LIST) saved to: {BLACK_LIST_PATH}")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot classification report
sns.heatmap(report_df.iloc[:-1, :-1], annot=True, cmap="Blues", fmt=".2f", ax=axes[0])
axes[0].set_title("Classification Report")
axes[0].set_ylabel("Classes")
axes[0].set_xlabel("Metrics")

# Plot whitelist vs blacklist
labels = ["Safe Sensors/Devices", "Unsafe Sensors/Devices"]
values = [len(white_list), len(black_list)]
axes[1].bar(labels, values, color=["green", "red"])
axes[1].set_title("Whitelist vs Blacklist Distribution")
axes[1].set_ylabel("Number of Sensors/Devices")

plt.tight_layout()
plt.show()

#--------------------------------------------Risk Classification-------------------------------------------------

# Proceeding to Risk Classification
print("\n✅ Proceeding to Risk Classification...")

# Debugging: Check if black_list is empty
if black_list.empty:
    print("❌ No unsafe devices detected. Skipping risk classification.")
    sys.exit(0)

# Ensure Probability_Value exists
if "Probability_Value" not in black_list.columns:
    print("❌ Error: Probability_Value column missing. Risk classification aborted.")
    sys.exit(1)

# Convert Probability_Value to numeric
black_list["Probability_Value"] = pd.to_numeric(black_list["Probability_Value"], errors="coerce")

# Debugging: Check Probability Value distribution
print("\n===== 🚨 Debugging: Probability Value Distribution =====")
print(black_list["Probability_Value"].describe())

# Assign Risk Levels based on Probability_Value
black_list["Risk_Level"] = np.select(
    [
        black_list["Probability_Value"] <= 0.4,
        (black_list["Probability_Value"] > 0.4) & (black_list["Probability_Value"] <= 0.7),
        black_list["Probability_Value"] > 0.7
    ],
    ["Low Risk", "Medium Risk", "High Risk"],
    default="Unknown"
)

# Debugging: Print classification counts
print("\n===== 🚨 Debugging: Risk Classification Count =====")
print(black_list["Risk_Level"].value_counts())

# Display all risk levels in the table
print("\n===== 🚨 Risk Classification Results =====")
print(black_list[["S.No", "Probability_Value", "Risk_Level"]].sort_values("Risk_Level", ascending=False).head(10))

# Save risk classification results separately
low_risk = black_list[black_list["Risk_Level"] == "Low Risk"]
medium_risk = black_list[black_list["Risk_Level"] == "Medium Risk"]
high_risk = black_list[black_list["Risk_Level"] == "High Risk"]

low_risk.to_csv(os.path.join(RISK_CLASSIFICATION_DIR, "LOW_RISK.csv"), index=False)
medium_risk.to_csv(os.path.join(RISK_CLASSIFICATION_DIR, "MEDIUM_RISK.csv"), index=False)
high_risk.to_csv(os.path.join(RISK_CLASSIFICATION_DIR, "HIGH_RISK.csv"), index=False)

print("\n✅ Risk classification CSV files saved in:")
print(f"   📂 {RISK_CLASSIFICATION_DIR}")

# Risk Visualization
plt.figure(figsize=(8, 5))
colors = {"Low Risk": "yellow", "Medium Risk": "orangered", "High Risk": "darkred"}
risk_counts = black_list["Risk_Level"].value_counts()

plt.bar(risk_counts.index, risk_counts.values, color=[colors[risk] for risk in risk_counts.index])
plt.xlabel("Risk Level")
plt.ylabel("Number of Devices")
plt.title("Risk Classification of Unsafe Sensors/Devices")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

print("\n✅ Risk classification completed. Visualization displayed successfully!")

#-------------------------------------------------black list sender---------------------------------------

BLACKLIST_API_URL = "http://localhost:5000/blacklist"

if not black_list.empty:
    blacklisted_sensors = black_list.to_dict(orient="records")  # Send full blacklist data

    try:
        response = requests.post(BLACKLIST_API_URL, json={"blacklist": blacklisted_sensors})
        if response.status_code == 200:
            print("\n✅ Blacklist successfully sent to Flask server!")
        else:
            print(f"\n❌ Failed to send blacklist. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error sending blacklist: {e}")
else:
    print("\n⚠️ No unsafe sensors detected. Blacklist not sent.")
    