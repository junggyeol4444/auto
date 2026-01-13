# 실행 가이드 (Execution Guide)

## 빠른 실행 방법

### Windows 사용자

1. **간단한 방법**: `run.bat` 더블클릭
   - 자동으로 의존성을 확인하고 프로그램을 실행합니다
   - Python이 설치되어 있어야 합니다

2. **명령 프롬프트에서**:
   ```cmd
   run.bat
   ```

### Linux/Mac 사용자

1. **간단한 방법**: 터미널에서
   ```bash
   ./run.sh
   ```

2. **또는**:
   ```bash
   bash run.sh
   ```

---

## Windows EXE 파일 만들기

독립 실행형 EXE 파일을 만들려면 PyInstaller를 사용합니다.

### 1단계: PyInstaller 설치

```cmd
pip install pyinstaller
```

### 2단계: EXE 파일 빌드

**단일 파일 EXE** (권장):
```cmd
pyinstaller --onefile --windowed --name="CreativeWritingAssistant" --icon=icon.ico main.py
```

**폴더 형태** (더 빠른 시작):
```cmd
pyinstaller --windowed --name="CreativeWritingAssistant" main.py
```

### 3단계: EXE 파일 찾기

- `dist/` 폴더에서 `CreativeWritingAssistant.exe` 찾기
- 이 파일을 더블클릭하면 프로그램 실행

### 옵션 설명

- `--onefile`: 모든 것을 하나의 EXE로 묶기
- `--windowed`: 콘솔 창 숨기기 (GUI만 표시)
- `--name`: 실행 파일 이름 지정
- `--icon`: 아이콘 파일 지정 (선택사항)

### 고급 옵션

더 작은 EXE 파일을 원한다면:
```cmd
pyinstaller --onefile --windowed --name="CreativeWritingAssistant" ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    main.py
```

---

## Linux AppImage 만들기

Linux에서 이식 가능한 실행 파일을 만들려면:

### 방법 1: PyInstaller 사용

```bash
pip install pyinstaller
pyinstaller --onefile --name="CreativeWritingAssistant" main.py
```

실행 파일은 `dist/CreativeWritingAssistant`에 생성됩니다.

### 방법 2: 직접 실행 가능한 Python 스크립트

`run.sh` 파일이 이미 제공되어 있습니다:
```bash
chmod +x run.sh
./run.sh
```

---

## macOS App 번들 만들기

### PyInstaller 사용

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="CreativeWritingAssistant" main.py
```

`.app` 번들이 `dist/` 폴더에 생성됩니다.

---

## 문제 해결

### "Python이 설치되지 않았습니다" 오류

**Windows**:
1. https://www.python.org/ 에서 Python 다운로드
2. 설치 시 "Add Python to PATH" 체크박스 선택
3. 설치 후 컴퓨터 재시작

**Linux**:
```bash
sudo apt-get install python3 python3-pip  # Ubuntu/Debian
sudo dnf install python3 python3-pip      # Fedora
```

**macOS**:
```bash
brew install python3
```

### "모듈을 찾을 수 없습니다" 오류

의존성을 수동으로 설치:
```bash
pip install -r requirements.txt
```

### GUI가 실행되지 않음

GUI는 디스플레이 서버가 필요합니다:
- **Windows/macOS**: 정상적으로 작동해야 함
- **Linux**: X11 또는 Wayland 필요
- **서버 환경**: Python API를 직접 사용 (EXAMPLES.md 참조)

### EXE 파일이 너무 큼

PyInstaller 최적화 옵션:
```cmd
pyinstaller --onefile --windowed ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --strip ^
    main.py
```

또는 UPX 압축 사용:
```cmd
pip install pyinstaller[upx]
pyinstaller --onefile --windowed --upx-dir=upx main.py
```

---

## 배포용 실행 파일

### Windows 배포 패키지

배포용 ZIP 파일 만들기:
```cmd
# EXE 빌드
pyinstaller --onefile --windowed --name="CreativeWritingAssistant" main.py

# 필요한 파일 복사
mkdir release
copy dist\CreativeWritingAssistant.exe release\
copy README.md release\
copy QUICKSTART.md release\

# ZIP으로 압축
powershell Compress-Archive -Path release\* -DestinationPath CreativeWritingAssistant-Windows.zip
```

### Linux 배포 패키지

```bash
# 실행 파일 빌드
pyinstaller --onefile --name="CreativeWritingAssistant" main.py

# 배포 패키지 생성
mkdir -p release
cp dist/CreativeWritingAssistant release/
cp README.md QUICKSTART.md release/
chmod +x release/CreativeWritingAssistant

# tar.gz로 압축
tar -czf CreativeWritingAssistant-Linux.tar.gz release/
```

---

## 개발자용

### 직접 Python으로 실행

```bash
python main.py
```

### 테스트 실행

```bash
python test_modules.py
```

### Python API로 사용

```python
from modules.webnovel.plot_generator import PlotGenerator

pg = PlotGenerator()
plot = pg.generate_plot("판타지")
print(plot)
```

자세한 내용은 `EXAMPLES.md` 참조.

---

## 추가 정보

- **시스템 요구사항**: Python 3.8 이상
- **권장 RAM**: 최소 2GB
- **디스크 공간**: 약 500MB (의존성 포함)

문제가 지속되면 GitHub Issues에 보고해주세요.
