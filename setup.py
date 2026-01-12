"""
Setup and validation script
"""
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'requests',
        'beautifulsoup4',
        'lxml',
        'gtts',
        'pyttsx3',
        'moviepy',
        'google-api-python-client',
        'google-auth-oauthlib',
        'customtkinter',
        'pillow'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').split('[')[0])
            logger.info(f"✓ {package} is installed")
        except ImportError:
            logger.warning(f"✗ {package} is not installed")
            missing.append(package)
    
    return missing


def install_dependencies():
    """Install missing dependencies"""
    logger.info("Installing dependencies from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        logger.info("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ Failed to install dependencies: {e}")
        return False


def check_directory_structure():
    """Check if required directories exist"""
    import os
    
    required_dirs = [
        'src/crawler',
        'src/content',
        'src/tts',
        'src/video',
        'src/youtube',
        'src/gui',
        'config',
        'templates'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            logger.info(f"✓ Directory exists: {dir_path}")
        else:
            logger.warning(f"✗ Directory missing: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
            logger.info(f"  Created: {dir_path}")
    
    # Create output directory
    if not os.path.exists('output'):
        os.makedirs('output')
        logger.info("✓ Created output directory")


def check_youtube_credentials():
    """Check if YouTube credentials are configured"""
    import os
    
    if os.path.exists('credentials.json'):
        logger.info("✓ YouTube credentials.json found")
        return True
    else:
        logger.warning("✗ YouTube credentials.json not found")
        logger.info("  To enable YouTube upload:")
        logger.info("  1. Go to https://console.cloud.google.com/")
        logger.info("  2. Create a project and enable YouTube Data API v3")
        logger.info("  3. Create OAuth 2.0 credentials")
        logger.info("  4. Download credentials.json to project root")
        return False


def run_basic_tests():
    """Run basic import tests"""
    logger.info("\nRunning basic tests...")
    
    try:
        from src.crawler import ContentCrawler
        logger.info("✓ ContentCrawler import successful")
    except Exception as e:
        logger.error(f"✗ ContentCrawler import failed: {e}")
    
    try:
        from src.content import ContentRestructurer
        logger.info("✓ ContentRestructurer import successful")
    except Exception as e:
        logger.error(f"✗ ContentRestructurer import failed: {e}")
    
    try:
        from src.tts import TTSManager
        logger.info("✓ TTSManager import successful")
    except Exception as e:
        logger.error(f"✗ TTSManager import failed: {e}")
    
    try:
        from src.video import VideoCreator
        logger.info("✓ VideoCreator import successful")
    except Exception as e:
        logger.error(f"✗ VideoCreator import failed: {e}")
    
    try:
        from src.youtube import YouTubeUploader
        logger.info("✓ YouTubeUploader import successful")
    except Exception as e:
        logger.error(f"✗ YouTubeUploader import failed: {e}")
    
    try:
        from src.gui import AutoContentGeneratorGUI
        logger.info("✓ AutoContentGeneratorGUI import successful")
    except Exception as e:
        logger.error(f"✗ AutoContentGeneratorGUI import failed: {e}")


def main():
    """Main setup function"""
    print("\n" + "=" * 60)
    print("YouTube Auto Content Generator - Setup")
    print("=" * 60 + "\n")
    
    # Check Python version
    if not check_python_version():
        return
    
    print()
    
    # Check directory structure
    check_directory_structure()
    
    print()
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print()
        response = input(f"\n{len(missing)} packages are missing. Install now? (y/n): ")
        if response.lower() == 'y':
            install_dependencies()
        else:
            logger.info("You can install dependencies later with: pip install -r requirements.txt")
    
    print()
    
    # Check YouTube credentials
    check_youtube_credentials()
    
    print()
    
    # Run basic tests
    run_basic_tests()
    
    print("\n" + "=" * 60)
    print("Setup completed!")
    print("=" * 60)
    print("\nTo start the application, run:")
    print("  python main.py")
    print("\nFor examples, run:")
    print("  python examples.py")
    print()


if __name__ == "__main__":
    main()
