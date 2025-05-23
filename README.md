# ITEC_federated-iot-anomaly-detection
A federated learning-based IoT framework that encrypts sensor data, detects anomalies, classifies device risk levels, and visualizes blacklist data using machine learning and real-time dashboards. Intelligence trust and secure edge computing for cyber physical systems.


# 🔐 Federated IoT Anomaly Detection

A secure, federated learning-based IoT system for collecting, encrypting, analyzing, and classifying sensor data from industrial temperature sensors. It enables anomaly detection and risk classification using ML and provides real-time dashboards and blacklist reporting.


---

## 📖 About

This project simulates an IoT environment with 100 industrial temperature sensors (Siemens SITRANS series). It encrypts and transmits sensor data to a client module for federated processing and anomaly detection. Unsafe devices are identified using machine learning and visualized through dashboards. Blacklisted devices are reported to the server for monitoring.

---

## ✨ Features

- 🔒 AES-level encryption using Fernet
- 📡 Real-time temperature sensor simulation (100+ sensors)
- 📁 Federated learning signature extraction
- 🧠 Enhanced anomaly detection via Random Forest & SMOTE
- ⚠️ Risk classification: Low, Medium, High
- 📊 Interactive GUI dashboards (Tkinter + Matplotlib)
- 📤 Flask-based REST API communication
- 🧾 Auto-generated white/blacklists
- 📈 Gantt chart & risk heatmap visualization

---

## 🛠️ Tech Stack

- **Languages**: Python
- **Libraries**:
  - Flask (API & backend server)
  - Pandas, NumPy, Scikit-learn (data analysis & ML)
  - Matplotlib, Seaborn (visualization)
  - Tkinter (GUI)
  - Cryptography (Fernet encryption)
  - imbalanced-learn (SMOTE oversampling)
- **Tools**: Git, GitHub, VS Code

---
## How to run the code.

1) Open Vscode (python)  create two new files and then paste the "IoT Malware detection using FL & ML" in file 1, "DT based sample Temperature sensor" in file 2.
2) Install Required Packages
   Open your terminal and run: pip install -r requirements.txt
3) Run the Server :
    run the "DT based sample Temperature sensor"  file 2 
4) Run the Client :
    run the "IoT Malware detection using FL & ML" file 1 in new terminal.

Usage

Start the Flask server.
Authenticate with the super key.
Monitor, extract, classify, and visualize data.
View saved outputs in the LOCAL LIST and Risk classification folders.




---
## License

This project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0).

© 2025 Priyan Paul Samuel P

You are free to share and adapt this project as long as you provide proper attribution to me, link to the license, and distribute your contributions under the same license.

For more details, see the [LICENSE](LICENSE) file or visit https://creativecommons.org/licenses/by-sa/4.0/

## 🚀 Installation

### 1. Clone the Repository
```bash

git clone https://github.com/priyan03/ITEC_federated-iot-anomaly-detection.git cd ITEC_federated-iot-anomaly-detection


