# FORG  
**A quick, easy and safe file organizer for Windows**

FORG is a lightweight Windows application designed to automatically organize files by type **without putting your system at risk**.  
It was built for users who want a clean workspace but are afraid of breaking something important.

Unlike generic file organizers, FORG includes **Safe Mode**, confirmations, and system path protection by default.

---

## 🚀 Features

- 📂 Automatically organizes files by extension  
- 🛡️ Built-in **Safe Mode** to prevent dangerous operations  
- ⚠️ Protection against organizing critical system folders  
- ✅ Clear confirmation before any action  
- 🔊 Sound feedback for success, errors, and confirmations  
- 🖥️ Simple and clean Windows interface  
- ⚡ Fast and lightweight — no installation required  

---

## 🔒 Safe Mode (Core Feature)

Safe Mode is enabled by default and is the heart of FORG.

When Safe Mode is active:
- System-critical folders are blocked
- Risky operations are prevented
- The user is always warned before changes

You can manually disable Safe Mode if you know exactly what you are doing — **with an extra confirmation step**.

This ensures FORG is safe even for non-technical users.

---

## 🧠 How It Works

1. Select a folder
2. Confirm the action
3. FORG creates folders based on file extensions
4. Files are moved safely into their respective folders

**Files are never deleted.**

---

## 🖼️ Example

Downloads/
├── photo.png
├── video.mp4
├── document.pdf

After organizing:

Downloads/
├── PNG/
│ └── photo.png
├── MP4/
│ └── video.mp4
└── PDF/
└── document.pdf

---

## ❗ Important Notes

- FORG does **not** rename your files  
- Folders without files will not be processed  
- System paths (like `C:\Windows`) are automatically blocked  
- Always make a backup if organizing important data  

---

## 🧩 Requirements

- Windows 10 or newer  
- No Python installation required (standalone executable)

---

## 📦 Download

You can download the latest version from the **Releases** section:

👉 **GitHub Releases**

---

## 🛠️ Built With

- Python  
- Tkinter + ttk  
- PyInstaller  

---

## ⚠️ Antivirus Notice

Some antivirus software may show a warning for Python-based executables.  
This is a **false positive** and common with many legitimate tools.

You can inspect the source code in this repository for full transparency.

---

## 📄 License

This project is licensed under the MIT License.

---

## 💡 Feedback & Contributions

Suggestions, issues, and improvements are welcome.  
Feel free to open an issue or submit a pull request.

---

**FORG — organize your files without risking your system.**
