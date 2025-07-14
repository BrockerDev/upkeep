# UpKeep - Server Uptime Monitor

UpKeep is a lightweight, desktop-based server uptime monitor written in Python with Tkinter.  
It allows users to easily track the status of up to **five servers**, providing **real-time ping checks**, **logging**, **notifications**, and **dark/light themes** — all in a clean and intuitive interface.

## 📦 Features

- ✅ Real-time server status (ping)
- 💾 Saves up to 5 server IPs or domains
- 🌗 Light & Dark mode toggle
- 🔁 Adjustable ping interval (in seconds)
- 🗂️ Persistent config (servers, settings, preferences)
- 🧠 Automatic background ping loop
- 📊 Status bar & live statistics
- 📂 Log file with timestamps for offline/online history
- 🔔 System notifications (via `notify-send`) for downed servers
- ✍️ Simple GUI made with Tkinter (compatible with low-end hardware)
- ☁️ Cross-platform (tested on Linux, may work on Windows/macOS with tweaks)
- ⚙️ Easily build into executable via `PyInstaller`

## 🛠 Requirements

- Python 3.8+
- Linux Mint / Ubuntu / Debian-based system
- Packages:
  - `tkinter` (GUI)
  - `subprocess`, `threading`, `json`, `os`, `datetime`, `notify-send`

## 🚀 Getting Started

Clone the repository:

```bash
git clone https://github.com/BrockerDev/upkeep.git
cd upkeep
python3 app.py
```

## 🧪 Build as Executable (Linux)

To build a standalone binary using PyInstaller:

```bash
sudo apt install pipx
pipx ensurepath
pipx install pyinstaller
pyinstaller --onefile --windowed app.py
```

Resulting binary will be in the `dist/` folder.

## 📁 Files

- `app.py` – main application logic
- `upkeep_config.json` – stores user settings and saved servers
- `upkeep_log.txt` – stores log of uptime/downtime events

## 💡 Notes

- Make sure `notify-send` is available on your system (usually part of `libnotify-bin`)
- Your data (server IPs, preferences) is stored locally in the script's directory
- For safety, the max number of servers is limited to 5 (can be extended manually in `MAX_SERVERS`)

## 📜 License

MIT License © 2025 BrockerDev

## 🤝 Contribution

Contributions, ideas, or issues? Feel free to open a pull request or issue.

## 🌐 Author

**BrockerDev** – [https://github.com/BrockerDev](https://github.com/BrockerDev)
