# 🦷 Plastl Mesh Converter

Plastl is a lightweight and user-friendly mesh format converter for dental applications. Built with **PyQt5** and powered by **Trimesh**, it allows you to convert mesh files between .PLY, .STL, and .OBJ formats — efficiently and effortlessly.

<p align="center">
  <img src="./assets/readme.png" alt="Plastl" width="600"/>
</p>

## 🚀 Features

- ✅ Batch Conversion: Select multiple files or drag-and-drop them into the app.
- ⚡ Parallel Processing: Converts meshes using multiple CPU cores for blazing-fast performance.
- 🔁 Bidirectional Format Support: Convert between PLY ↔ STL, OBJ ↔ STL, etc.
- 🧾 Intuitive UI: Clean, minimal interface with logging for quick feedback.
- 💾 Compression Insight: Displays space savings after conversion (for PLY output).
- 📂 Integrated Folder Handling: Quickly open the output directory directly from the app.

## 📦 Supported Formats

| Input Format | Supported Output Formats |
| ------------ | ------------------------ |
| `.stl`       | `.ply`, `.stl`           |
| `.ply`       | `.stl`, `.ply`           |
| `.obj`       | `.stl`, `.ply`           |

## 📦 Download Prebuilt App

[👉 Download Plastl Latest Release](https://github.com/thangngoc89/plastl/releases/latest)

Available Platforms:

| Platform              | File                       |
| --------------------- | -------------------------- |
| macOS (Apple Silicon) | plastl-macos-arm64.app.zip |
| Windows               | plastl-windows-x64.zip     |
| Linux                 | plastl-linux-x64.zip       |

🗂 Unzip the downloaded file and run the app directly. No installation needed.

### ⚠️ Security Notice

Plastl is currently not code-signed or notarized. Depending on your operating system, you may need to:

macOS:

- Right-click the .app → Open → Click “Open” again in the dialog.
- Alternatively, allow it via System Settings → Privacy & Security.

Windows:

- You may see a Windows Defender SmartScreen warning. Click “More info” → “Run anyway” if you trust the source.

## Build from source

### 🛠 Requirements

- Python ≥ 3.8
- PyQt5
- Trimesh

### Install dependencies

```bash
pip install trimesh PyQt5
```

### ▶️ How to Use

```bash
python plastl.py
```

1. Launch the application.
2. Drag & drop or select mesh files (.stl, .ply, .obj).
3. Choose an output format.
4. Pick an output folder.
5. Click Run – and watch the magic happen!

## 💡 Why “Plastl”?

Inspired by **Plaster + STL**, Plastl pays homage to the physical dental casts now transformed into clean digital meshes.

## 📸 Screenshots

_Coming soon..._

## 🧪 Known Limitations

- No preview or mesh inspection (yet).
- May not support some malformed mesh files.

## 📜 License

MIT License
