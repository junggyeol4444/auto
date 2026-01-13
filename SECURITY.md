# Security Policy

## Security Updates

This document tracks security vulnerability fixes in the Voice Service Integrated Suite.

### Recent Security Updates (2026-01-13)

#### Fixed Vulnerabilities

1. **aiohttp 3.9.1 → 3.13.3**
   - ❌ CVE: HTTP Parser auto_decompress zip bomb vulnerability (Affected: ≤ 3.13.2)
   - ❌ CVE: Denial of Service when parsing malformed POST requests (Affected: < 3.9.4)
   - ❌ CVE: Directory traversal vulnerability (Affected: ≥ 1.0.5, < 3.9.2)
   - ✅ Fixed: Updated to version 3.13.3

2. **pillow 10.1.0 → 10.3.0**
   - ❌ CVE: Buffer overflow vulnerability (Affected: < 10.3.0)
   - ✅ Fixed: Updated to version 10.3.0

3. **torch 2.1.0 → 2.6.0**
   - ❌ CVE: Heap buffer overflow vulnerability (Affected: < 2.2.0)
   - ❌ CVE: Use-after-free vulnerability (Affected: < 2.2.0)
   - ❌ CVE: `torch.load` with `weights_only=True` RCE vulnerability (Affected: < 2.6.0)
   - ⚠️  Note: Withdrawn advisory for deserialization vulnerability (≤ 2.3.1) - no patch available
   - ✅ Fixed: Updated to version 2.6.0 (addresses all patchable vulnerabilities)

## Security Best Practices

### For Users

1. **Always use the latest version** of dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **API Keys**: Never commit API keys to version control
   - Store in `config.json` (excluded from git)
   - Or use environment variables
   - Rotate keys regularly

3. **File Uploads**: Be cautious with user-uploaded files
   - The application processes audio/video files
   - Only process files from trusted sources
   - Keep antivirus software updated

4. **Network Security**: When using cloud APIs
   - Use HTTPS for all API communications (default)
   - Verify SSL certificates
   - Monitor API usage for anomalies

### For Developers

1. **Dependency Updates**:
   - Regularly check for security updates
   - Use `pip list --outdated` to check for updates
   - Review changelogs before updating major versions

2. **Input Validation**:
   - All user inputs are validated before processing
   - File types are checked before loading
   - Text inputs are sanitized for TTS engines

3. **Logging**:
   - Sensitive information (API keys) is never logged
   - Error logs are stored locally in `logs/` directory
   - Review logs regularly for suspicious activity

4. **Code Security**:
   - No use of `eval()` or `exec()` with user input
   - All file operations use absolute paths
   - Temporary files are cleaned up after use

## Reporting Vulnerabilities

If you discover a security vulnerability in this project:

1. **Do NOT** open a public issue
2. Email the maintainers with details
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Dependency Security Scanning

We recommend using the following tools to scan for vulnerabilities:

```bash
# Safety - checks Python dependencies
pip install safety
safety check -r requirements.txt

# Bandit - analyzes Python code
pip install bandit
bandit -r modules/ gui/ utils/

# pip-audit - audits Python packages
pip install pip-audit
pip-audit
```

## Security Update History

| Date | Package | Old Version | New Version | Severity | Fixed |
|------|---------|-------------|-------------|----------|-------|
| 2026-01-13 | aiohttp | 3.9.1 | 3.13.3 | High | ✅ |
| 2026-01-13 | pillow | 10.1.0 | 10.3.0 | Medium | ✅ |
| 2026-01-13 | torch | 2.1.0 | 2.6.0 | High | ✅ |

## Safe Usage Guidelines

### torch.load Usage

For models that use `torch.load()`, we recommend:

```python
# Safe usage - always use weights_only=True for untrusted sources
model = torch.load('model.pth', weights_only=True)

# For trusted local models only
model = torch.load('model.pth')
```

### File Processing

When processing user-uploaded files:

```python
# Always validate file types
from utils.file_handler import FileHandler

if FileHandler.is_audio_file(filepath):
    # Process audio
    pass
else:
    # Reject invalid file
    logger.warning(f"Invalid file type: {filepath}")
```

### API Key Management

```python
# ✅ Good - use config manager
from utils.config_manager import get_config_manager
config = get_config_manager()
api_key = config.get_api_key('azure_speech_key')

# ❌ Bad - hardcoded API keys
api_key = "hardcoded-key-here"  # NEVER DO THIS
```

## Known Limitations

1. **torch deserialization** (≤ 2.3.1): Withdrawn advisory with no patch available
   - Mitigation: Only load models from trusted sources
   - Use `weights_only=True` when possible
   - Keep torch updated to latest version (2.6.0)

2. **Third-party models**: RVC voice cloning uses community models
   - Only use models from trusted sources
   - Scan models before use
   - Keep models in isolated directory

## Compliance

This application:
- ✅ Does not store user data without consent
- ✅ Processes audio/video locally by default
- ✅ Cloud APIs are optional and user-configured
- ✅ Logs contain no personal information
- ✅ Temporary files are cleaned up

## Contact

For security concerns, please contact the repository maintainers through GitHub.

---

**Last Updated**: 2026-01-13  
**Next Review**: 2026-04-13 (quarterly)
