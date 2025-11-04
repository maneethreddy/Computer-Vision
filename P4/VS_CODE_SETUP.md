# How to Run This Project in VS Code

## Method 1: Run Button (Easiest) 🚀

1. **Open VS Code**
   - Open Visual Studio Code
   
2. **Open the Project Folder**
   - Go to `File` → `Open Folder...`
   - Navigate to: `C:\Users\abhin\Downloads\cv1`
   - Click "Select Folder"

3. **Open `main.py`**
   - In the left sidebar (Explorer), click on `main.py`
   - The file will open in the editor

4. **Run the Project**
   - **Option A**: Click the ▶️ "Run Python File" button in the top-right corner
   - **Option B**: Press `Ctrl + F5` (Run without debugging)
   - **Option C**: Press `F5` (Run with debugging)

## Method 2: Terminal in VS Code 💻

1. **Open Terminal**
   - Press `` Ctrl + ` `` (backtick) OR
   - Go to `Terminal` → `New Terminal`

2. **Navigate to Project (if not already there)**
   ```powershell
   cd C:\Users\abhin\Downloads\cv1
   ```

3. **Run the Project**
   ```powershell
   python main.py
   ```

## Method 3: Using Python Extension Debugger 🐛

1. **Install Python Extension** (if not installed)
   - Press `Ctrl + Shift + X` to open Extensions
   - Search for "Python" by Microsoft
   - Click "Install"

2. **Create Launch Configuration** (Optional but Recommended)
   - Press `F5` OR click "Run and Debug" icon (left sidebar)
   - Click "create a launch.json file"
   - Select "Python File"
   - VS Code will create `.vscode/launch.json`

3. **Run with Debugger**
   - Press `F5` to start debugging
   - Set breakpoints by clicking left of line numbers
   - See variables, call stack, etc.

## Method 4: Command Palette 🎯

1. **Open Command Palette**
   - Press `Ctrl + Shift + P`

2. **Type and Select**
   - Type: `Python: Run Python File in Terminal`
   - Press Enter

## Quick Steps Summary ✅

**Fastest Way:**
1. Open `main.py` in VS Code
2. Press `Ctrl + F5`
3. Done! App runs! 🎉

**With Debugging:**
1. Open `main.py` in VS Code
2. Press `F5`
3. Set breakpoints if needed
4. App runs with debugging! 🐛

## Troubleshooting

### "Python interpreter not found"
- Press `Ctrl + Shift + P`
- Type: `Python: Select Interpreter`
- Choose your Python installation

### "Module not found"
- Open terminal: `Ctrl + `` `
- Run: `pip install -r requirements.txt`

### "Camera not working"
- Check Windows camera permissions
- Close other apps using camera
- See `CAMERA_SETUP.md` for details

## VS Code Shortcuts You'll Use

| Shortcut | Action |
|----------|--------|
| `Ctrl + F5` | Run without debugging |
| `F5` | Run with debugging |
| `Ctrl + `` ` | Open/Close terminal |
| `Ctrl + Shift + P` | Command Palette |
| `Ctrl + B` | Toggle sidebar |

## Recommended VS Code Extensions

1. **Python** (Microsoft) - Essential
2. **Python Indent** - Better formatting
3. **Pylance** - Better IntelliSense
4. **Error Lens** - Show errors inline

## Running Specific Files

You can also run individual files:

- `test_camera.py` - Test camera separately
- `diagnose_camera.py` - Camera diagnostics
- `main.py` - Main application

Just right-click the file → "Run Python File in Terminal"

---

**That's it! Your project is now running in VS Code!** 🎊




