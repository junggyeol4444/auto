# 실행 프로그램 사용 가이드 (Launcher Guide)

## 📋 개요

이 프로젝트는 이제 **더블클릭만으로 실행 가능한** 편리한 실행 프로그램을 제공합니다!

## 🚀 실행 프로그램 (Launcher Scripts)

### Windows 사용자

#### 1. 프로그램 바로 실행
**파일**: `run.bat`  
**사용법**: 파일을 더블클릭  

**자동 수행 기능**:
- ✅ Python 설치 확인
- ✅ 필요한 패키지 자동 설치
- ✅ 프로그램 자동 실행
- ✅ 오류 발생 시 안내 메시지 표시

#### 2. 독립 실행 EXE 생성
**파일**: `build_exe.bat`  
**사용법**: 파일을 더블클릭  

**생성 결과**: `dist\금융분석시스템.exe`
- Python 설치 없이 실행 가능한 EXE 파일
- 다른 컴퓨터에 배포 가능

### Mac/Linux 사용자

#### 1. 프로그램 바로 실행
**파일**: `run.sh`  
**사용법**: 
```bash
cd Financial_Analysis
./run.sh
```

**자동 수행 기능**:
- ✅ Python 설치 확인
- ✅ 필요한 패키지 자동 설치
- ✅ 프로그램 자동 실행
- ✅ Python 3/Python 자동 감지

#### 2. 독립 실행 파일 생성
**파일**: `build_exe.sh`  
**사용법**:
```bash
cd Financial_Analysis
./build_exe.sh
```

**생성 결과**: `dist/금융분석시스템`

## 📁 파일 목록

```
Financial_Analysis/
├── run.bat              ⭐ Windows 실행 프로그램
├── run.sh               ⭐ Mac/Linux 실행 프로그램
├── build_exe.bat        🔧 Windows EXE 빌드
├── build_exe.sh         🔧 Unix 빌드
├── main.py              💻 메인 프로그램
└── ...
```

## ✨ 특징

### run.bat / run.sh
- Python 미설치 시 오류 메시지와 함께 설치 링크 제공
- customtkinter 등 필수 패키지 미설치 시 자동 설치
- 프로그램 종료 후 자동으로 pause (Windows)
- 사용자 친화적인 한글 안내 메시지

### build_exe.bat / build_exe.sh
- PyInstaller를 사용한 독립 실행 파일 생성
- 의존성 자동 번들링
- config.example.json 자동 포함
- 빌드 진행 상황 표시

## 🎯 사용 시나리오

### 시나리오 1: 처음 사용하는 경우
1. Python 3.8+ 설치
2. `Financial_Analysis` 폴더로 이동
3. **Windows**: `run.bat` 더블클릭
4. **Mac/Linux**: 터미널에서 `./run.sh`
5. 자동으로 패키지 설치 및 프로그램 실행!

### 시나리오 2: 다른 컴퓨터에 배포
1. `build_exe.bat` (Windows) 또는 `build_exe.sh` (Mac/Linux) 실행
2. `dist` 폴더에 생성된 실행 파일 복사
3. `config.json` 파일도 함께 복사
4. Python 설치 없이도 실행 가능!

### 시나리오 3: 빠른 테스트
1. `run.bat` / `run.sh` 실행
2. 프로그램이 자동으로 시작됨
3. 종료 후 창이 자동으로 닫힘 (또는 pause)

## 🔧 문제 해결

### "Python을 찾을 수 없습니다"
- Python 3.8 이상을 설치하세요
- Windows: https://www.python.org/downloads/
- Mac: `brew install python3`
- Linux: `sudo apt install python3`

### "패키지 설치 실패"
- 인터넷 연결 확인
- 수동 설치: `pip install -r requirements.txt`

### "실행 권한 없음" (Mac/Linux)
```bash
chmod +x run.sh
chmod +x build_exe.sh
```

## 📚 추가 문서

- **README.md**: 전체 프로젝트 설명
- **QUICKSTART.md**: 5분 빠른 시작 가이드
- **IMPLEMENTATION_SUMMARY.md**: 구현 상세 내역

## ⚙️ 고급 사용

### 수동 실행 (디버깅 시)
```bash
cd Financial_Analysis
python main.py
```

### 사용자 정의 빌드
```bash
pyinstaller --onefile --windowed --name "사용자정의이름" main.py
```

---

**버전**: 1.0.2  
**업데이트**: 2024-01-13  
**Commit**: 1ce97c4
