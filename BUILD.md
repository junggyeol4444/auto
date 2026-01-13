# Building Executable Files

This document explains how to build executable files for the Social Media Automation Suite.

## Quick Start Scripts

### Windows Users
Simply double-click `run.bat` to launch the application. The script will:
- Check if Python is installed
- Create a virtual environment (first time only)
- Install dependencies (first time only)
- Launch the application

### Linux/Mac Users
Run the shell script:
```bash
./run.sh
```

The script will:
- Check if Python 3 is installed
- Create a virtual environment (first time only)
- Install dependencies (first time only)
- Launch the application

## Building Windows EXE

### Prerequisites
- Python 3.8 or higher
- PyInstaller

### Steps

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build the executable**
   ```bash
   pyinstaller social_media_suite.spec
   ```

3. **Find the executable**
   The executable will be created in the `dist` folder:
   ```
   dist/Social_Media_Automation_Suite.exe
   ```

4. **Distribute**
   You can distribute the entire `dist` folder or just the `.exe` file.
   Note: The exe includes all dependencies, so users don't need Python installed.

### Build Options

#### One-file vs One-folder
The current spec creates a **one-file** executable (all dependencies packed into one .exe).

To create a **one-folder** distribution (faster startup):
1. Open `social_media_suite.spec`
2. Change the `EXE` section to use `onefile=False`

#### Adding an Icon
1. Create or download a `.ico` file (Windows icon)
2. Place it in the project root
3. In `social_media_suite.spec`, change:
   ```python
   icon=None,
   ```
   to:
   ```python
   icon='your_icon.ico',
   ```

#### Console vs Windowed
Current setting: `console=False` (no console window)

To show console for debugging:
- Change `console=False` to `console=True` in the spec file

## Building for Other Platforms

### macOS App Bundle
```bash
pyinstaller --windowed --onefile --name "Social Media Suite" main.py
```

This creates a `.app` bundle in the `dist` folder.

### Linux Binary
```bash
pyinstaller --onefile main.py
```

This creates a Linux binary in the `dist` folder.

## Troubleshooting

### "Module not found" errors
Add missing modules to `hiddenimports` in `social_media_suite.spec`:
```python
hiddenimports=[
    'your_missing_module',
],
```

### Large file size
The exe includes all dependencies. To reduce size:
1. Remove unused dependencies from `requirements.txt`
2. Use `--exclude-module` for large unused modules
3. Enable UPX compression (already enabled in spec)

### Antivirus false positives
PyInstaller executables sometimes trigger antivirus warnings. This is normal.
To avoid:
1. Sign your executable with a code signing certificate
2. Submit to antivirus vendors as false positive
3. Build on a clean VM

## Advanced Configuration

### Custom spec file
The provided `social_media_suite.spec` includes:
- Template files bundled
- Config file bundled
- All required hidden imports
- UPX compression enabled
- Windowed mode (no console)

You can customize this file for your needs.

### Environment Variables
To include environment variables in the build:
1. Create a `hook-mymodule.py` file
2. Add to `hookspath` in the spec file

### Multiple executables
To create multiple executables (e.g., GUI and CLI versions):
1. Create separate spec files
2. Run PyInstaller with each spec

## Distribution

### Windows
Distribute the `dist` folder or just the `.exe` file.

Recommended: Create an installer using:
- Inno Setup (free)
- NSIS (free)
- Advanced Installer

### macOS
Create a `.dmg` disk image:
```bash
hdiutil create -volname "Social Media Suite" -srcfolder dist/Social\ Media\ Suite.app -ov -format UDZO SocialMediaSuite.dmg
```

### Linux
Create a `.deb` or `.rpm` package, or distribute as AppImage.

## File Structure After Build

```
dist/
└── Social_Media_Automation_Suite.exe (or .app on macOS)

build/
└── (temporary build files - can be deleted)
```

## Notes

- The build process may take 2-5 minutes
- First launch may be slower as files are extracted
- The executable is portable - copy to any Windows PC
- No Python installation required on target machines
- Config and cache files are created on first run

## Support

For build issues:
1. Check PyInstaller documentation: https://pyinstaller.org/
2. Review the spec file for configuration
3. Test in a clean Python environment

---

**Last Updated**: January 13, 2024
