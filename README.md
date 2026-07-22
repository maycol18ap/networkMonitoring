🌐 Language: **English** | [Español](README.es.md)

# 📡 Network Traffic Monitor

> Lightweight network traffic monitoring tool built with Python, Scapy and Npcap.

Network Traffic Monitor is a lightweight command-line application that captures network packets in real time to monitor total bandwidth usage and detect DNS requests made by your computer.

The project was created as a proof of concept to explore packet capture, network analysis, concurrent programming, and desktop application distribution using Python.

---

# ✨ Features

- 📊 Real-time network traffic monitoring.
- 🌐 DNS request detection.
- ⚡ Multithreaded architecture for smooth packet processing.
- 💻 Lightweight terminal interface.
- 📦 Standalone Windows executable (.exe).
- 🔓 Open Source.

---

# 🏗 Architecture

```text
                     +--------------------+
                     |      main.py       |
                     +----------+---------+
                                |
         +----------------------+----------------------+
         |                      |                      |
         |                      |                      |
+--------v-------+     +--------v-------+     +--------v-------+
| Packet Capture |     |  ARP Scanner   |     |   Database     |
| Scapy + DNS    |     | Device Detect  |     | SQLite         |
+--------+-------+     +--------+-------+     +--------+-------+
         |                      |                      |
         +----------------------+----------------------+
                                |
                     +----------v----------+
                     |     Console UI      |
                     +---------------------+
```

Packet capturing runs in a dedicated thread while the main thread continuously updates the console and displays statistics, preventing UI blocking during high network traffic.

---

# 📸 Screenshots



<img width="617" height="266" alt="image" src="https://github.com/user-attachments/assets/182dcd0e-7122-4784-bd54-edb631dca25a" />


<img width="831" height="371" alt="image" src="https://github.com/user-attachments/assets/1f377fe1-744f-406c-a276-df89f5419c13" />

<img width="641" height="351" alt="image" src="https://github.com/user-attachments/assets/ad960e08-2967-4878-9e85-d954d1ab3906" />



---

# 🚀 Installation

There are two ways to use this application.

## Option 1 — Download the Executable

Recommended if you only want to use the application.

1. Download the latest release from the **Releases** section.
2. Install **Npcap**.
3. Run `main.exe` as Administrator.
4. Select your active network interface.
5. Start monitoring.

---

## Option 2 — Run from Source Code

Clone the repository

```bash
git clone https://github.com/maycol18ap/networkMonitoring.git

cd networkMonitoring
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python main.py
```

---

# ⚠ Requirements

This application requires:

- Windows
- Npcap installed
- Administrator privileges

Without these requirements, Scapy cannot capture packets from the selected network interface.

---

# ▶ Usage

1. Launch the application.
2. Select your active network interface.
3. Packet capture starts immediately.
4. Watch the real-time bandwidth usage.
5. Stop the application to display the session report.

Example report

```text
Total bandwidth: 245.8 MB

Detected domains

google.com
github.com
youtube.com
stackoverflow.com
```

---

# 🛠 Technologies

| Technology | Purpose |
|------------|----------|
| Python 3.12 | Main programming language |
| Scapy | Packet capture and analysis |
| Npcap | Windows packet capture driver |
| Threading | Concurrent packet processing |
| PyInstaller | Executable generation |
| uv | Dependency management |

---

# 📂 Project Structure

```text
networkMonitoring/

├── main.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── README.es.md
├── main.spec
└── dist/
```

The current version focuses on validating the project's core idea. Future versions will introduce a modular architecture to improve maintainability and scalability.

---

# 🗺 Roadmap

## 🗺 Roadmap

### v1.0

- ✅ Packet capture
- ✅ DNS monitoring
- ✅ Multithreading
- ✅ Windows executable

### v1.2

- ✅ SQLite persistence
- ✅ ARP device discovery
- ✅ Modular architecture

### Upcoming

- [ ] Session statistics
- [ ] Device manufacturer detection (OUI lookup)
- [ ] CSV export
- [ ] Rich interactive interface
- [ ] Historical charts
- [ ] GUI

# 🤝 Contributing

Contributions, suggestions and bug reports are welcome.

Feel free to open an Issue or submit a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.
