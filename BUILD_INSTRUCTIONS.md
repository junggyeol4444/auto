# Building Executables - Translation Automation Platform

This document explains how to build standalone executables for different platforms.

## Quick Start - Pre-built Launchers

### Windows Users
**Double-click:** `run_translation_platform.bat`

This will:
1. Check if Python is installed
2. Create a virtual environment (first time only)
3. Install dependencies automatically
4. Launch the application

### Linux/Mac Users
**Run in terminal:** `./run_translation_platform.sh`

Or:
```bash
bash run_translation_platform.sh
```

This will:
1. Check if Python is installed
2. Create a virtual environment (first time only)
3. Install dependencies automatically
4. Launch the application

## Building Standalone Executables

### Option 1: Using Build Scripts (Recommended)

#### Windows
```batch
build_executable.bat
```

This creates `dist/TranslationPlatform.exe`

#### Linux/Mac
```bash
./build_executable.sh
```

This creates `dist/TranslationPlatform` (executable binary)

### Option 2: Manual PyInstaller Build

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable:**
   ```bash
   pyinstaller build.spec --clean
   ```

3. **Find your executable in:**
   - Windows: `dist/TranslationPlatform.exe`
   - Linux/Mac: `dist/TranslationPlatform`

### Option 3: One-File Executable

For a single portable file, modify `build.spec`:

```python
# Change from:
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # <- These are separate
    a.zipfiles,
    a.datas,
    ...
)

# To:
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TranslationPlatform',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    onefile=True,  # <- Add this line
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
```

Then build again.

## Distribution

### What to Distribute

**Method 1: Launcher Scripts (Smallest)**
- Package: `run_translation_platform.bat` or `run_translation_platform.sh`
- Plus: All Python source files
- Size: ~50 KB
- Requires: Python 3.8+ installed on target system

**Method 2: PyInstaller Executable (Recommended)**
- Package: Contents of `dist/` folder after build
- Size: ~50-100 MB (includes Python runtime)
- Requires: Nothing (fully standalone)

### Platform-Specific Notes

#### Windows (.exe)
- Built on Windows: Works on Windows
- Built on Linux: Won't work on Windows
- **Recommendation:** Build on Windows for Windows users

#### Linux/Mac (binary)
- Built on Linux: Works on Linux
- Built on Mac: Works on Mac
- Built on Linux: Won't work on Mac (and vice versa)
- **Recommendation:** Build on target platform

#### Cross-Platform Solution
Use the launcher scripts (.bat/.sh) - they work on any platform with Python installed.

## Troubleshooting

### "Python not found"
Install Python 3.8 or higher from:
- Windows: https://www.python.org/downloads/
- Linux: `sudo apt install python3` or `sudo yum install python3`
- Mac: `brew install python3`

### "ModuleNotFoundError" after building
Add the missing module to `hiddenimports` in `build.spec`:
```python
hiddenimports=[
    'customtkinter',
    'your_missing_module',  # Add here
    ...
],
```

### Executable is too large
1. Use `upx=True` in build.spec (already enabled)
2. Remove unused dependencies from requirements.txt
3. Use `--onefile` option for single file (slightly larger but portable)

### Antivirus flags the executable
This is common with PyInstaller. Solutions:
1. Submit to antivirus vendor as false positive
2. Sign the executable with a code signing certificate
3. Distribute as Python source + launcher script

## File Sizes

Approximate sizes:

| Distribution Method | Size |
|---------------------|------|
| Python source only | ~50 KB |
| With dependencies | ~100 MB (in site-packages) |
| PyInstaller EXE (onedir) | ~80-120 MB |
| PyInstaller EXE (onefile) | ~90-130 MB |

## Advanced: Custom Icon

To add an icon to the executable:

1. **Get an icon file:**
   - Windows: `.ico` format
   - Mac: `.icns` format

2. **Modify build.spec:**
   ```python
   icon='path/to/icon.ico'  # or icon.icns on Mac
   ```

3. **Rebuild:**
   ```bash
   pyinstaller build.spec --clean
   ```

## Testing the Executable

After building:

1. **Test on your system:**
   ```bash
   dist/TranslationPlatform  # or TranslationPlatform.exe
   ```

2. **Test on a clean system:**
   - No Python installed
   - No dependencies installed
   - Should work standalone

3. **Verify features:**
   - GUI launches
   - Can select files
   - Translation works (with API keys)
   - Settings persist

## Support

For build issues:
1. Check PyInstaller docs: https://pyinstaller.org/
2. Check our issues: https://github.com/junggyeol4444/auto/issues
3. Ensure all dependencies are in requirements.txt

## Summary

**Easiest for end users:** Use `run_translation_platform.bat` (Windows) or `run_translation_platform.sh` (Linux/Mac)

**Most portable:** Build with PyInstaller using `build_executable.bat` or `build_executable.sh`

**Smallest size:** Distribute Python source with launcher scripts
