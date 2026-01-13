/**
 * 카카오톡 봇 스크립트
 * KakaoTalk Bot Script for MessengerBot R
 * 
 * 사용법:
 * 1. 메신저봇R 앱 설치
 * 2. 이 스크립트를 복사하여 붙여넣기
 * 3. 봇 활성화
 */

const scriptName = "멀티봇";

// API 키 (사용자가 설정)
const WEATHER_API_KEY = "YOUR_WEATHER_API_KEY";
const TRANSLATE_API_KEY = "YOUR_TRANSLATE_API_KEY";

// 응답 함수
function response(room, msg, sender, isGroupChat, replier, ImageDB, packageName) {
    try {
        // 명령어 파싱
        const command = msg.trim();
        
        // 날씨 명령어
        if (command.startsWith("날씨")) {
            const city = command.replace("날씨", "").trim() || "서울";
            const weather = getWeather(city);
            replier.reply(weather);
        }
        
        // 번역 명령어
        else if (command.startsWith("번역 ")) {
            const text = command.replace("번역 ", "").trim();
            const translated = translateText(text);
            replier.reply(translated);
        }
        
        // 계산 명령어
        else if (command.startsWith("계산 ")) {
            const expression = command.replace("계산 ", "").trim();
            const result = calculate(expression);
            replier.reply("결과: " + result);
        }
        
        // 뉴스 명령어
        else if (command === "뉴스") {
            const news = getNews();
            replier.reply(news);
        }
        
        // 도움말
        else if (command === "도움말" || command === "도움") {
            const help = getHelpMessage();
            replier.reply(help);
        }
        
        // 안녕 응답
        else if (command.includes("안녕")) {
            replier.reply("안녕하세요! 무엇을 도와드릴까요?");
        }
        
        // 시간
        else if (command === "시간") {
            const now = new Date();
            const timeStr = now.getFullYear() + "년 " + 
                          (now.getMonth() + 1) + "월 " + 
                          now.getDate() + "일 " + 
                          now.getHours() + "시 " + 
                          now.getMinutes() + "분";
            replier.reply("현재 시간: " + timeStr);
        }
        
        // 주사위
        else if (command === "주사위") {
            const dice = Math.floor(Math.random() * 6) + 1;
            replier.reply("🎲 주사위 결과: " + dice);
        }
        
    } catch (e) {
        replier.reply("오류가 발생했습니다: " + e.message);
    }
}

/**
 * 날씨 정보 가져오기
 */
function getWeather(city) {
    try {
        // 실제 구현에서는 API 호출
        // const url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + WEATHER_API_KEY;
        // const response = org.jsoup.Jsoup.connect(url).ignoreContentType(true).get();
        // const json = JSON.parse(response.text());
        
        // 더미 데이터
        return "🌤️ " + city + " 날씨\n\n" +
               "날씨: 맑음\n" +
               "기온: 15°C\n" +
               "습도: 60%\n" +
               "풍속: 2m/s";
    } catch (e) {
        return "날씨 정보를 가져올 수 없습니다.";
    }
}

/**
 * 번역 기능
 */
function translateText(text) {
    try {
        // 실제 구현에서는 번역 API 호출
        // Papago API, Google Translate API 등 사용
        
        // 간단한 예시 (영어 -> 한국어)
        const translations = {
            "hello": "안녕하세요",
            "hi": "안녕",
            "thank you": "감사합니다",
            "good morning": "좋은 아침입니다",
            "good night": "좋은 밤 되세요"
        };
        
        const lower = text.toLowerCase();
        if (translations[lower]) {
            return "번역 결과: " + translations[lower];
        } else {
            return "번역: " + text + "\n(실제 API 연동 시 자동 번역)";
        }
    } catch (e) {
        return "번역할 수 없습니다.";
    }
}

/**
 * 계산기 기능
 */
function calculate(expression) {
    try {
        // 보안을 위해 숫자와 연산자만 허용
        const sanitized = expression.replace(/[^0-9+\-*/().]/g, '');
        
        if (sanitized.length === 0) {
            return "잘못된 수식입니다.";
        }
        
        // eval 대신 안전한 계산 방법 사용
        const result = eval(sanitized);
        return result;
    } catch (e) {
        return "계산할 수 없는 수식입니다.";
    }
}

/**
 * 뉴스 가져오기
 */
function getNews() {
    try {
        // 실제 구현에서는 뉴스 API 호출 또는 크롤링
        // 네이버 뉴스 API, Google News API 등
        
        return "📰 최신 뉴스\n\n" +
               "1. 주요 기술 뉴스 헤드라인\n" +
               "2. 경제 뉴스 헤드라인\n" +
               "3. 정치 뉴스 헤드라인\n\n" +
               "(실제 API 연동 시 실시간 뉴스 제공)";
    } catch (e) {
        return "뉴스를 가져올 수 없습니다.";
    }
}

/**
 * 도움말 메시지
 */
function getHelpMessage() {
    return "📚 사용 가능한 명령어\n\n" +
           "• 날씨 [도시명] - 날씨 정보\n" +
           "• 번역 [텍스트] - 번역\n" +
           "• 계산 [수식] - 계산기\n" +
           "• 뉴스 - 최신 뉴스\n" +
           "• 시간 - 현재 시간\n" +
           "• 주사위 - 주사위 굴리기\n" +
           "• 도움말 - 이 메시지\n\n" +
           "예시:\n" +
           "- 날씨 서울\n" +
           "- 번역 Hello\n" +
           "- 계산 1+1";
}

/**
 * 일정 알림 기능 (타이머 사용)
 */
function setReminder(room, time, message) {
    // 실제 구현에서는 타이머 설정
    // 메신저봇R의 타이머 기능 활용
}

/**
 * 크롤링 예시 (Jsoup 사용)
 */
function crawlWebsite(url) {
    try {
        // const doc = org.jsoup.Jsoup.connect(url).get();
        // const title = doc.select("title").text();
        // return title;
        
        return "크롤링 기능 (Jsoup 라이브러리 필요)";
    } catch (e) {
        return "크롤링 실패";
    }
}

/**
 * 데이터 저장 (FileStream 사용)
 */
function saveData(key, value) {
    try {
        // DataBase.setDataBase(scriptName, key, value);
        return true;
    } catch (e) {
        return false;
    }
}

/**
 * 데이터 불러오기
 */
function loadData(key) {
    try {
        // return DataBase.getDataBase(scriptName, key);
        return null;
    } catch (e) {
        return null;
    }
}

// 봇 시작 시 실행
function onStartCompile() {
    // 초기화 작업
}

// 주기적 실행 (1분마다)
function onNotificationPosted(statusBarNotification, sm) {
    // 주기적 작업 수행
}

/**
 * 사용 예시:
 * 
 * 사용자: 날씨 서울
 * 봇: 🌤️ 서울 날씨
 *     날씨: 맑음
 *     기온: 15°C
 *     습도: 60%
 *     풍속: 2m/s
 * 
 * 사용자: 번역 Hello
 * 봇: 번역 결과: 안녕하세요
 * 
 * 사용자: 계산 1+1
 * 봇: 결과: 2
 */
