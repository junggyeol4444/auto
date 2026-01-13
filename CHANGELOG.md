# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-12

### Added
- Initial release of YouTube Auto Content Generator
- Web crawler module for news sites (Naver, Daum) and wikis (Wikipedia, NamuWiki)
- Content restructuring with three template types:
  - News Report
  - Informational/Educational
  - Storytelling
- TTS support with multiple engines:
  - gTTS (Google Text-to-Speech)
  - pyttsx3 (offline TTS)
  - Custom TTS support (Coqui TTS framework)
- Video creation using MoviePy:
  - Simple video with static background
  - Support for image backgrounds
  - Automatic audio-video synchronization
- YouTube API integration:
  - Automatic video upload
  - SEO-optimized metadata generation
  - Thumbnail support
  - Privacy settings
- GUI application using CustomTkinter:
  - Topic input
  - Channel type selection
  - TTS engine selection
  - Progress tracking
  - Real-time status updates
- Configuration management:
  - JSON-based configuration
  - Default settings for all modules
- Comprehensive documentation:
  - README with installation and usage
  - User Guide with detailed instructions
  - API documentation for developers
  - Quick Start guide
  - Contributing guidelines
- Example scripts demonstrating all features
- Setup validation script
- Logging system for debugging
- Error handling throughout

### Technical Details
- Python 3.8+ support
- Modular architecture with clear separation of concerns
- Type hints for better code clarity
- Comprehensive error handling and logging
- Support for both GUI and programmatic usage

### Known Limitations
- Text overlay requires ImageMagick (optional feature)
- Video concatenation simplified for stability
- Audio merging uses first file only
- Network dependency for gTTS and web crawling
- YouTube API daily quota limits apply

## [Unreleased]

### Planned
- Video thumbnail generation
- Multiple language support
- Advanced video editing features
- Custom background music
- Automated scheduling
- Batch processing improvements
- More TTS engines
- Additional crawler sources
- Template customization UI
- Video preview in GUI
- Draft saving/loading

---

[1.0.0]: https://github.com/junggyeol4444/auto/releases/tag/v1.0.0
