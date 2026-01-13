# 실행 방법 (How to Run) / 실행 프로그램 (Executables)

## 🚀 가장 쉬운 방법 (Easiest Way)

### Windows 사용자
**`run_translation_platform.bat` 파일을 더블클릭하세요**

자동으로:
- Python 확인
- 가상환경 생성
- 필요한 패키지 설치
- 프로그램 실행

### Linux/Mac 사용자
**터미널에서 실행:**
```bash
./run_translation_platform.sh
```

또는:
```bash
bash run_translation_platform.sh
```

---

## 📦 독립 실행 파일 만들기 (Build Standalone Executable)

Python 없이 실행 가능한 EXE/실행 파일을 만들 수 있습니다:

### Windows
```batch
build_executable.bat
```
→ `dist/TranslationPlatform.exe` 생성

### Linux/Mac
```bash
./build_executable.sh
```
→ `dist/TranslationPlatform` 생성

---

## 📋 상세 설명 (Details)

### 제공되는 실행 파일 (Available Launchers)

| 파일 | 플랫폼 | 설명 |
|-----|-------|-----|
| `run_translation_platform.bat` | Windows | Windows용 실행 스크립트 |
| `run_translation_platform.sh` | Linux/Mac | Linux/Mac용 실행 스크립트 |
| `build_executable.bat` | Windows | EXE 파일 빌드 스크립트 |
| `build_executable.sh` | Linux/Mac | 실행 파일 빌드 스크립트 |

### 실행 방법 비교 (Comparison)

**방법 1: 런처 스크립트 (Launcher Scripts)**
- ✅ 가장 쉬움 (Easiest)
- ✅ 작은 크기 (~50 KB)
- ⚠️ Python 3.8+ 필요

**방법 2: 독립 실행 파일 (Standalone Executable)**
- ✅ Python 설치 불필요
- ✅ 한 번만 빌드
- ⚠️ 큰 크기 (~100 MB)

---

## 🔧 문제 해결 (Troubleshooting)

### "Python을 찾을 수 없습니다" / "Python not found"
Python 3.8 이상을 설치하세요:
- Windows: https://www.python.org/downloads/
- Linux: `sudo apt install python3`
- Mac: `brew install python3`

### 실행이 안 됩니다 / "Won't run"
1. 런처 스크립트를 먼저 시도해보세요
2. `python main.py`로 직접 실행해보세요
3. [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) 참고

---

## 📚 더 자세한 정보 (More Information)

- **빌드 가이드**: [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
- **사용 설명서**: [README.md](README.md)
- **빠른 시작**: [QUICKSTART.md](QUICKSTART.md)

---

## ⚡ 요약 (Quick Summary)

**Windows 사용자:** `run_translation_platform.bat` 더블클릭
**Linux/Mac 사용자:** `./run_translation_platform.sh` 실행
**EXE 파일 필요:** `build_executable.bat` 또는 `build_executable.sh` 실행
