"""
Basic Verification Script
Checks project structure and basic Python syntax without requiring dependencies
"""

import os
import ast
import sys

print("=" * 60)
print("Social Media Automation Suite - Structure Verification")
print("=" * 60)
print()

# Check directory structure
print("Verifying directory structure...")
required_dirs = [
    'modules',
    'modules/converter',
    'modules/generator',
    'modules/publisher',
    'gui',
    'templates',
    'database',
]

all_dirs_exist = True
for dir_path in required_dirs:
    exists = os.path.isdir(dir_path)
    status = "✓" if exists else "✗"
    print(f"  {status} {dir_path}")
    if not exists:
        all_dirs_exist = False

if all_dirs_exist:
    print("✓ All required directories exist")
else:
    print("✗ Some directories are missing")
    sys.exit(1)

# Check required files
print("\nVerifying required files...")
required_files = [
    'main.py',
    'config.json',
    'requirements.txt',
    'README.md',
    'QUICKSTART.md',
    'LICENSE',
    '.gitignore',
    'templates/caption_templates.json',
    'templates/emoji_library.json',
    'modules/converter/video_converter.py',
    'modules/converter/image_processor.py',
    'modules/generator/hashtag_generator.py',
    'modules/generator/caption_generator.py',
    'modules/generator/trend_analyzer.py',
    'modules/publisher/instagram_publisher.py',
    'modules/publisher/tiktok_publisher.py',
    'modules/publisher/youtube_publisher.py',
    'modules/publisher/twitter_publisher.py',
    'modules/publisher/facebook_publisher.py',
    'modules/publisher/pinterest_publisher.py',
    'modules/publisher/discord_publisher.py',
    'modules/publishing_coordinator.py',
    'gui/main_window.py',
    'gui/preview_window.py',
    'gui/settings_window.py',
    'database/database.py',
]

all_files_exist = True
for file_path in required_files:
    exists = os.path.isfile(file_path)
    status = "✓" if exists else "✗"
    print(f"  {status} {file_path}")
    if not exists:
        all_files_exist = False

if all_files_exist:
    print("✓ All required files exist")
else:
    print("✗ Some files are missing")
    sys.exit(1)

# Check Python syntax
print("\nVerifying Python syntax...")
python_files = []
for root, dirs, files in os.walk('.'):
    # Skip cache and other directories
    if '__pycache__' in root or '.git' in root or 'cache' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            python_files.append(os.path.join(root, file))

syntax_errors = []
for py_file in python_files:
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        print(f"  ✓ {py_file}")
    except SyntaxError as e:
        print(f"  ✗ {py_file}: {e}")
        syntax_errors.append((py_file, str(e)))

if not syntax_errors:
    print(f"✓ All {len(python_files)} Python files have valid syntax")
else:
    print(f"✗ {len(syntax_errors)} files have syntax errors")
    sys.exit(1)

# Check JSON files
print("\nVerifying JSON files...")
import json

json_files = [
    'config.json',
    'templates/caption_templates.json',
    'templates/emoji_library.json',
]

json_errors = []
for json_file in json_files:
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"  ✓ {json_file}")
    except json.JSONDecodeError as e:
        print(f"  ✗ {json_file}: {e}")
        json_errors.append((json_file, str(e)))

if not json_errors:
    print("✓ All JSON files are valid")
else:
    print("✗ Some JSON files have errors")
    sys.exit(1)

# Count lines of code
print("\nCounting lines of code...")
total_lines = 0
for py_file in python_files:
    with open(py_file, 'r', encoding='utf-8') as f:
        lines = len(f.readlines())
        total_lines += lines

print(f"Total Python files: {len(python_files)}")
print(f"Total lines of code: {total_lines:,}")

# Summary
print("\n" + "=" * 60)
print("✅ VERIFICATION PASSED!")
print("=" * 60)
print("\nProject Structure Summary:")
print(f"  • {len(required_dirs)} core directories")
print(f"  • {len(required_files)} essential files")
print(f"  • {len(python_files)} Python modules")
print(f"  • {total_lines:,} lines of code")
print(f"  • 7 platform publishers")
print(f"  • 3 GUI windows")
print(f"  • 5 caption templates")
print("\nNext Steps:")
print("  1. Install dependencies: pip install -r requirements.txt")
print("  2. Run full tests: python test_suite.py")
print("  3. Launch application: python main.py")
print("=" * 60)
