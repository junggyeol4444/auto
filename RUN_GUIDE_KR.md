# 실행 가이드 - Smart Video Editor Pro

## 빠른 실행 방법

### Windows 사용자

1. **간단한 방법** (권장):
   - `run.bat` 파일을 더블클릭
   - 첫 실행 시 자동으로 환경 설정 및 패키지 설치
   - 이후 실행 시 바로 프로그램 시작

2. **수동 실행**:
   ```cmd
   python main.py
   ```

### macOS/Linux 사용자

1. **간단한 방법** (권장):
   - 터미널에서 실행:
     ```bash
     ./run.sh
     ```
   - 또는 파일 관리자에서 `run.sh` 더블클릭 (실행 권한 필요)
   - 첫 실행 시 자동으로 환경 설정 및 패키지 설치
   - 이후 실행 시 바로 프로그램 시작

2. **수동 실행**:
   ```bash
   python3 main.py
   ```

---

## 독립 실행 파일 만들기 (Standalone Executable)

사용자에게 배포하거나 Python 설치 없이 실행하고 싶은 경우:

### Windows (.exe 파일 생성)

1. **자동 빌드** (권장):
   ```cmd
   build.bat
   ```

2. **수동 빌드**:
   ```cmd
   # 가상 환경 활성화
   venv\Scripts\activate
   
   # PyInstaller로 빌드
   pyinstaller build.spec
   ```

3. **결과**:
   - 실행 파일 위치: `dist\SmartVideoEditorPro.exe`
   - 이 파일을 다른 컴퓨터에 복사하여 Python 없이 실행 가능

### macOS/Linux (앱 번들 생성)

1. **빌드**:
   ```bash
   # 가상 환경 활성화
   source venv/bin/activate
   
   # PyInstaller로 빌드
   pyinstaller build.spec
   ```

2. **결과**:
   - 실행 파일 위치: `dist/SmartVideoEditorPro`
   - macOS: `dist/SmartVideoEditorPro.app` (앱 번들)
   - Linux: `dist/SmartVideoEditorPro` (실행 파일)

---

## 실행 파일 종류 및 용도

### 런처 스크립트 (간편 실행)

| 파일 | 플랫폼 | 용도 |
|------|--------|------|
| `run.bat` | Windows | 더블클릭으로 즉시 실행 |
| `run.sh` | macOS/Linux | 터미널 또는 더블클릭 실행 |
| `main.py` | 모든 플랫폼 | Python으로 직접 실행 |

### 빌드 스크립트 (.exe 생성용)

| 파일 | 플랫폼 | 용도 |
|------|--------|------|
| `build.bat` | Windows | .exe 파일 자동 생성 |
| `build.spec` | 모든 플랫폼 | PyInstaller 설정 파일 |
| `setup.sh` | macOS/Linux | 개발 환경 설정 |

---

## 첫 실행 시 자동 설정

`run.bat` 또는 `run.sh`를 처음 실행하면 자동으로:

1. ✅ Python 버전 확인
2. ✅ 가상 환경 생성 (`venv` 폴더)
3. ✅ 필요한 패키지 설치 (`requirements.txt`)
4. ✅ 프로그램 시작

이후 실행부터는 바로 프로그램이 시작됩니다.

---

## 문제 해결

### Windows: "Python을 찾을 수 없습니다"

**해결 방법**:
1. Python 설치: https://www.python.org/downloads/
2. 설치 시 "Add Python to PATH" 체크 필수
3. 재부팅 후 다시 시도

### macOS/Linux: "Permission denied"

**해결 방법**:
```bash
chmod +x run.sh
./run.sh
```

### "FFmpeg를 찾을 수 없습니다"

**해결 방법**:
- **Windows**: 
  1. https://ffmpeg.org/download.html 에서 다운로드
  2. `C:\ffmpeg`에 압축 해제
  3. 시스템 PATH에 `C:\ffmpeg\bin` 추가

- **macOS**:
  ```bash
  brew install ffmpeg
  ```

- **Linux**:
  ```bash
  sudo apt-get install ffmpeg
  ```

### 모듈 설치 오류

**해결 방법**:
```bash
# 가상 환경 삭제 후 재생성
rm -rf venv          # Linux/macOS
rmdir /s venv        # Windows

# 다시 실행
./run.sh             # Linux/macOS
run.bat              # Windows
```

---

## 고급 사용자를 위한 옵션

### 개발 모드로 실행

```bash
# 가상 환경 활성화
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 디버그 모드로 실행
python main.py
```

### 커스텀 Python 경로 사용

```bash
# 특정 Python 버전으로 실행
/usr/bin/python3.9 main.py
```

### 로그 파일 생성

```bash
# 출력을 파일로 저장
python main.py > output.log 2>&1
```

---

## 배포용 패키징

### Windows 배포 패키지 만들기

1. `build.bat` 실행
2. `dist\SmartVideoEditorPro.exe` 파일 확인
3. (선택) Inno Setup 등으로 인스톨러 생성

### 휴대용 버전 만들기

1. 실행 파일 빌드
2. 필요한 파일들 복사:
   ```
   SmartVideoEditorPro/
   ├── SmartVideoEditorPro.exe
   ├── data/
   └── README.txt
   ```
3. ZIP으로 압축하여 배포

---

## 요약

**가장 쉬운 방법**:
- Windows: `run.bat` 더블클릭
- macOS/Linux: `./run.sh` 실행

**배포용 실행 파일 만들기**:
- Windows: `build.bat` 실행 → `dist\SmartVideoEditorPro.exe`
- macOS/Linux: `pyinstaller build.spec` → `dist/SmartVideoEditorPro`

**직접 실행**:
- `python main.py` (또는 `python3 main.py`)
