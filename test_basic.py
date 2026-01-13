#!/usr/bin/env python3
"""
Simple test script to verify core functionality
This script tests the application without installing all dependencies
"""
import json
import os
import sys

def test_templates():
    """Test template loading"""
    print("=" * 50)
    print("Testing Template System")
    print("=" * 50)
    
    template_dir = 'templates/webnovel'
    genres = ['fantasy', 'romance', 'martial_arts', 'modern']
    
    for genre in genres:
        template_path = os.path.join(template_dir, f'{genre}.json')
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
                print(f"✓ {template['name']} template loaded")
                print(f"  - Plot templates: {len(template.get('plot_templates', {}))}")
                print(f"  - Character archetypes: {len(template.get('character_archetypes', {}))}")
        else:
            print(f"✗ {genre} template not found")
    
    print()

def test_manual_templates():
    """Test manual templates"""
    print("=" * 50)
    print("Testing Manual Templates")
    print("=" * 50)
    
    template_dir = 'templates/manual'
    types = ['product', 'software']
    
    for manual_type in types:
        template_path = os.path.join(template_dir, f'{manual_type}.json')
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                template = json.load(f)
                print(f"✓ {template['name']} template loaded")
                print(f"  - Sections: {len(template.get('sections', []))}")
        else:
            print(f"✗ {manual_type} template not found")
    
    print()

def test_config():
    """Test configuration"""
    print("=" * 50)
    print("Testing Configuration")
    print("=" * 50)
    
    config_path = 'config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            print("✓ Configuration loaded")
            print(f"  - AI API enabled: {config['api']['use_ai']}")
            print(f"  - Default format: {config['output']['default_format']}")
            print(f"  - Default chapter length: {config['webnovel']['default_chapter_length']}")
    else:
        print("✗ Configuration file not found")
    
    print()

def test_directory_structure():
    """Test directory structure"""
    print("=" * 50)
    print("Testing Directory Structure")
    print("=" * 50)
    
    required_dirs = [
        'modules/webnovel',
        'modules/proofreading',
        'modules/manual',
        'templates/webnovel',
        'templates/manual',
        'gui',
        'utils',
        'output'
    ]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ {directory} exists")
        else:
            print(f"✗ {directory} not found")
    
    print()

def test_core_files():
    """Test core files"""
    print("=" * 50)
    print("Testing Core Files")
    print("=" * 50)
    
    required_files = [
        'main.py',
        'config.json',
        'requirements.txt',
        'README.md',
        'modules/webnovel/generator.py',
        'modules/proofreading/grammar_check.py',
        'modules/manual/structure_generator.py',
        'gui/main_window.py',
        'utils/file_handler.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} not found")
    
    print()

def main():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("AI Writing Assistant Suite - Basic Tests")
    print("=" * 50 + "\n")
    
    test_directory_structure()
    test_core_files()
    test_templates()
    test_manual_templates()
    test_config()
    
    print("=" * 50)
    print("All basic tests completed!")
    print("=" * 50)
    print("\nTo install dependencies and run the full application:")
    print("  1. pip install -r requirements.txt")
    print("  2. python main.py")
    print()

if __name__ == "__main__":
    main()
