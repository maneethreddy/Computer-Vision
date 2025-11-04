# How to Run This Project in Cursor

## Method 1: Quick Run Button (Easiest) 🚀

1. **Open Cursor**
   - Launch Cursor IDE

2. **Open the Project Folder**
   - Go to `File` → `Open Folder...` (or `Ctrl + K, Ctrl + O`)
   - Navigate to: `C:\Users\abhin\Downloads\cv1`
   - Click "Select Folder"

3. **Open `main.py`**
   - In the left sidebar (Explorer), click on `main.py`
   - The file will open in the editor

4. **Run the Project**
   - **Option A**: Click the ▶️ "Run Python File" button in the top-right corner
   - **Option B**: Press `Ctrl + F5` (Run without debugging)
   - **Option C**: Press `F5` (Run with debugging)
   - **Option D**: Right-click `main.py` → "Run Python File in Terminal"

## Method 2: Integrated Terminal 💻

1. **Open Terminal in Cursor**
   - Press `` Ctrl + ` `` (backtick key) OR
   - Go to `Terminal` → `New Terminal`
   - Or use: `View` → `Terminal`

2. **Navigate to Project** (if not already there)
   ```powershell
   cd C:\Users\abhin\Downloads\cv1
   ```

3. **Run the Project**
   ```powershell
   python main.py
   ```

## Method 3: Command Palette 🎯

1. **Open Command Palette**
   - Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on Mac)

2. **Type and Select**
   - Type: `Python: Run Python File in Terminal`
   - Press `Enter`

## Method 4: Using Cursor's AI Terminal

Cursor has an AI-powered terminal feature:

1. **Open AI Terminal**
   - Press `Ctrl + ` ` (backtick)
   - Or use the terminal panel

2. **Type Command**
   - Type: `python main.py`
   - Or ask Cursor: "Run the main.py file"

## Quick Steps Summary ✅

**Fastest Way:**
1. Open `main.py` in Cursor
2. Press `Ctrl + F5`
3. Done! App runs! 🎉

**With AI Help:**
1. Select `main.py`
2. Press `Ctrl + L` (Cursor Chat)
3. Type: "Run this Python file"
4. Cursor will run it for you!

## Cursor-Specific Features

### Using Cursor Chat to Run
1. Press `Ctrl + L` to open Cursor Chat
2. Type: "Run python main.py"
3. Cursor will execute the command

### Using Cursor Composer
1. Select `main.py`
2. Press `Ctrl + I` (Composer)
3. Ask: "Run this application"

## Troubleshooting

### "Python interpreter not found"
1. Press `Ctrl + Shift + P`
2. Type: `Python: Select Interpreter`
3. Choose your Python installation (usually `Python 3.13.x`)

### "Module not found"
1. Open terminal: `` Ctrl + ` ``
2. Run: `pip install -r requirements.txt`

### "Camera not working"
- Check Windows camera permissions
- Close other apps using camera
- See `CAMERA_SETUP.md` for details

### "Command not recognized: python"
Try:
```powershell
py main.py
```
Or:
```powershell
python3 main.py
```

## Cursor Shortcuts You'll Use

| Shortcut | Action |
|----------|--------|
| `Ctrl + F5` | Run without debugging |
| `F5` | Run with debugging |
| `Ctrl + ` ` | Open/Close terminal |
| `Ctrl + Shift + P` | Command Palette |
| `Ctrl + L` | Open Cursor Chat |
| `Ctrl + I` | Open Cursor Composer |
| `Ctrl + B` | Toggle sidebar |
| `Ctrl + K, Ctrl + O` | Open folder |

## Recommended Cursor Extensions

1. **Python** (Microsoft) - Essential for Python support
2. **Pylance** - Better code completion and IntelliSense
3. **Python Indent** - Better code formatting
4. **Error Lens** - Show errors inline

## Running Specific Files

You can run any Python file:

- **Right-click method**: Right-click file → "Run Python File in Terminal"
- **Terminal method**: `` Ctrl + ` ``, then type `python filename.py`

Files you can run:
- `main.py` - Main application
- `test_camera.py` - Test camera separately
- `diagnose_camera.py` - Camera diagnostics

## Using Cursor's AI Features

### Ask Cursor to Run It
1. Press `Ctrl + L` (Cursor Chat)
2. Type: "How do I run main.py?"
3. Cursor will guide you or run it directly

### Debug with AI Help
1. Press `F5` to start debugging
2. If you get errors, press `Ctrl + L`
3. Paste the error and ask: "How do I fix this?"
4. Cursor will help troubleshoot

## Project Status Check

After running, you should see:
- ✅ GUI window opens
- ✅ Camera initializes
- ✅ "Camera initialized successfully" in terminal
- ✅ Click START to begin detection

## Advanced: Debugging Setup

1. **Create launch.json** (Optional)
   - Press `F5`
   - Select "Python File"
   - Cursor creates `.vscode/launch.json`

2. **Set Breakpoints**
   - Click left of line numbers
   - Red dot appears = breakpoint set

3. **Debug**
   - Press `F5`
   - Execution pauses at breakpoints
   - Inspect variables, step through code

## Tips for Cursor Users

- **AI Chat**: Use `Ctrl + L` for quick questions
- **Composer**: Use `Ctrl + I` for code generation/modification
- **Terminal**: Integrated terminal is very powerful
- **Multi-cursor**: `Alt + Click` for multiple cursors

---

## Summary

**Easiest way to run:**
```powershell
1. Open Cursor
2. Open folder: C:\Users\abhin\Downloads\cv1
3. Open main.py
4. Press Ctrl + F5
```

**Using AI:**
```powershell
1. Press Ctrl + L
2. Type: "Run python main.py"
3. Done!
```

**Your Hand Gesture Recognition project is ready to run in Cursor!** 🎊




