
# Lukus - Sober FFlags Modifier

<div align="center">
  <img src="LUKUS/LukusLogo.png" alt="Lukus Logo" width="120" />
  <h3>Roblox Sober FastFlags Editor for Linux</h3>
</div>

---

## 📝 Overview

**Lukus** is a user-friendly GUI tool for Linux that lets you view and modify Roblox Sober port FastFlags. Easily tweak advanced graphics, performance, and experimental options—no need to manually edit JSON files!

---

## ✨ Features

- **Easy Access Tab:** Quick toggles for FPS, graphics, lighting, and more.
- **FFlags Tab:** Manual FFlag editing with live preview and automatic backup.
- **Credits Tab:** Info about the author and project.
- **Safe Editing:** Only the `fflags` field in the config file is modified; all other settings remain untouched.
- **Automatic Backup:** Creates a backup of the original config file before saving changes.

---

## ⚙️ How It Works

Lukus reads and edits the Sober `config.json` file located at:

```bash
~/.var/app/org.vinegarhq.Sober/config/sober/config.json
```

---

## 📦 Requirements

- Python 3.8+
- GTK4 and PyGObject
- Sober (must have been started at least once to create the config file)

### Install Dependencies (Ubuntu/Debian)

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 libadwaita-1-dev
```

---

## 🚀 Installation & Usage

1. **Download or clone this repository.**
2. **Save `lukus.py` in a folder.**
3. **Run the program:**
   - Open a terminal, navigate to the folder, and run:

   ```bash
   python3 lukus.py
   ```

---

## 📸 Screenshots

<div align="center">
  <img src="https://i.ibb.co/yBM2GKZ2/Captura-de-tela-de-2025-05-31-18-23-09.png" alt="Screenshot 1" width="400" />
  <img src="https://i.ibb.co/Cp6fCPkm/Captura-de-tela-de-2025-05-31-18-23-15.png" alt="Screenshot 2" width="400" />
</div>

---

## 🆕 What's New (2025-06-13)

- **Added:** Importing FFlags from JSON now auto-saves them.
- **Improved:** All Easy Access options start unchecked by default.
- **Improved:** FFlags preview window now uses a fixed size and scroll bar to prevent overflow.
- **Improved:** Thread options (HyperThreading, Minimum/Maximum Threads) are only available when enabled by a dedicated switch.
- **Improved:** Trailing commas in FFlag names or values are automatically fixed and the user is notified.
- **Improved:** The logo is loaded directly from the local `LUKUS/LukusLogo.png` file.
- **Fixed:** Various bugs for better stability and reliability.

---

## 👤 Credits

Developed by **Nhet/Kosurs**


