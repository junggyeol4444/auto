#!/usr/bin/env python3
"""
Validation script for Smart Video Editor Pro
Checks project structure and code quality without requiring dependencies
"""
import os
import sys
import ast
import re

class ProjectValidator:
    """Validates project structure and code"""
    
    def __init__(self, project_root):
        self.project_root = project_root
        self.errors = []
        self.warnings = []
        self.passed = []
    
    def validate_all(self):
        """Run all validation checks"""
        print("=" * 60)
        print("Smart Video Editor Pro - Project Validation")
        print("=" * 60)
        print()
        
        self.check_directory_structure()
        self.check_required_files()
        self.check_python_syntax()
        self.check_docstrings()
        self.check_imports()
        
        self.print_results()
    
    def check_directory_structure(self):
        """Verify directory structure"""
        print("Checking directory structure...")
        
        required_dirs = [
            'src',
            'src/core',
            'src/database',
            'src/gui',
            'data',
            'data/profiles',
            'data/temp'
        ]
        
        for dir_path in required_dirs:
            full_path = os.path.join(self.project_root, dir_path)
            if os.path.isdir(full_path):
                self.passed.append(f"✓ Directory: {dir_path}")
            else:
                self.errors.append(f"✗ Missing directory: {dir_path}")
    
    def check_required_files(self):
        """Check for required files"""
        print("Checking required files...")
        
        required_files = [
            'main.py',
            'requirements.txt',
            'README.md',
            'LICENSE',
            'build.spec',
            'src/__init__.py',
            'src/core/__init__.py',
            'src/core/video_downloader.py',
            'src/core/scene_detector.py',
            'src/core/audio_analyzer.py',
            'src/core/style_learner.py',
            'src/core/video_editor.py',
            'src/database/__init__.py',
            'src/database/models.py',
            'src/gui/__init__.py',
            'src/gui/main_window.py'
        ]
        
        for file_path in required_files:
            full_path = os.path.join(self.project_root, file_path)
            if os.path.isfile(full_path):
                self.passed.append(f"✓ File: {file_path}")
            else:
                self.errors.append(f"✗ Missing file: {file_path}")
    
    def check_python_syntax(self):
        """Check Python files for syntax errors"""
        print("Checking Python syntax...")
        
        python_files = []
        for root, dirs, files in os.walk(os.path.join(self.project_root, 'src')):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        # Add main.py
        python_files.append(os.path.join(self.project_root, 'main.py'))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    ast.parse(code)
                rel_path = os.path.relpath(file_path, self.project_root)
                self.passed.append(f"✓ Syntax OK: {rel_path}")
            except SyntaxError as e:
                rel_path = os.path.relpath(file_path, self.project_root)
                self.errors.append(f"✗ Syntax error in {rel_path}: {e}")
    
    def check_docstrings(self):
        """Check for module and function docstrings"""
        print("Checking docstrings...")
        
        python_files = []
        for root, dirs, files in os.walk(os.path.join(self.project_root, 'src')):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    python_files.append(os.path.join(root, file))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    tree = ast.parse(code)
                
                rel_path = os.path.relpath(file_path, self.project_root)
                
                # Check module docstring
                if ast.get_docstring(tree):
                    self.passed.append(f"✓ Module docstring: {rel_path}")
                else:
                    self.warnings.append(f"⚠ Missing module docstring: {rel_path}")
                
                # Check class/function docstrings
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        if not ast.get_docstring(node):
                            self.warnings.append(
                                f"⚠ Missing docstring: {rel_path}::{node.name}"
                            )
            except Exception as e:
                self.warnings.append(f"⚠ Could not check docstrings in {rel_path}: {e}")
    
    def check_imports(self):
        """Check import statements"""
        print("Checking imports...")
        
        required_imports = {
            'src/core/video_downloader.py': ['yt_dlp'],
            'src/core/scene_detector.py': ['cv2', 'numpy'],
            'src/core/audio_analyzer.py': ['pydub', 'numpy'],
            'src/core/style_learner.py': ['scene_detector', 'audio_analyzer'],
            'src/core/video_editor.py': ['moviepy'],
            'src/database/models.py': ['sqlalchemy'],
            'src/gui/main_window.py': ['PyQt5']
        }
        
        for file_path, expected_imports in required_imports.items():
            full_path = os.path.join(self.project_root, file_path)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for expected in expected_imports:
                    if expected in content:
                        self.passed.append(f"✓ Import found: {expected} in {file_path}")
                    else:
                        self.warnings.append(f"⚠ Import not found: {expected} in {file_path}")
            except Exception as e:
                self.errors.append(f"✗ Could not check imports in {file_path}: {e}")
    
    def print_results(self):
        """Print validation results"""
        print()
        print("=" * 60)
        print("Validation Results")
        print("=" * 60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"  {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more warnings")
        
        print(f"\n✅ PASSED ({len(self.passed)}):")
        print(f"  {len(self.passed)} checks passed successfully")
        
        print()
        print("=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"Total Checks: {len(self.passed) + len(self.warnings) + len(self.errors)}")
        print(f"✅ Passed: {len(self.passed)}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.errors:
            print("\n❌ VALIDATION FAILED - Please fix errors")
            return False
        else:
            print("\n✅ VALIDATION PASSED - Project structure is valid!")
            if self.warnings:
                print("   (Some warnings present - consider addressing them)")
            return True


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.abspath(__file__))
    validator = ProjectValidator(project_root)
    success = validator.validate_all()
    sys.exit(0 if success else 1)
