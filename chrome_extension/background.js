/**
 * 크롬 확장 프로그램 - 백그라운드 스크립트
 * Background Service Worker
 */

// 확장 프로그램 설치 시
chrome.runtime.onInstalled.addListener(() => {
  console.log('확장 프로그램이 설치되었습니다.');
  
  // 기본 설정 저장
  chrome.storage.sync.set({
    autoTranslate: false,
    priceTracking: true,
    adBlock: false,
    notifications: true
  });
});

// 메시지 리스너
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('메시지 수신:', request);
  
  if (request.action === 'scrapeData') {
    handleScrapeData(request.data, sendResponse);
    return true; // 비동기 응답
  }
  
  if (request.action === 'checkPrice') {
    handlePriceCheck(request.url, sendResponse);
    return true;
  }
  
  if (request.action === 'translate') {
    handleTranslate(request.text, request.targetLang, sendResponse);
    return true;
  }
  
  if (request.action === 'notify') {
    showNotification(request.title, request.message);
    sendResponse({ success: true });
  }
  
  if (request.action === 'blockAd') {
    // 광고 차단 로직
    sendResponse({ success: true });
  }
});

/**
 * 데이터 스크래핑 처리
 */
function handleScrapeData(data, sendResponse) {
  try {
    // 스크래핑된 데이터 저장
    chrome.storage.local.get(['scrapedData'], (result) => {
      const scrapedData = result.scrapedData || [];
      scrapedData.push({
        data: data,
        timestamp: new Date().toISOString(),
        url: data.url
      });
      
      chrome.storage.local.set({ scrapedData: scrapedData }, () => {
        sendResponse({ success: true, count: scrapedData.length });
      });
    });
  } catch (error) {
    sendResponse({ success: false, error: error.message });
  }
}

/**
 * 가격 체크 처리
 */
function handlePriceCheck(url, sendResponse) {
  try {
    chrome.storage.local.get(['priceHistory'], (result) => {
      const priceHistory = result.priceHistory || {};
      
      if (priceHistory[url]) {
        sendResponse({ 
          success: true, 
          history: priceHistory[url] 
        });
      } else {
        sendResponse({ 
          success: false, 
          message: '가격 기록이 없습니다.' 
        });
      }
    });
  } catch (error) {
    sendResponse({ success: false, error: error.message });
  }
}

/**
 * 번역 처리
 */
function handleTranslate(text, targetLang, sendResponse) {
  // 실제 구현에서는 Google Translate API 사용
  // 여기서는 더미 응답
  sendResponse({
    success: true,
    translatedText: `[번역됨: ${targetLang}] ${text}`,
    sourceLang: 'auto',
    targetLang: targetLang
  });
}

/**
 * 알림 표시
 */
function showNotification(title, message) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icon48.png',
    title: title,
    message: message,
    priority: 2
  });
}

/**
 * 탭 관리 자동화
 */
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete') {
    // 페이지 로드 완료 시 자동화 작업 수행
    chrome.storage.sync.get(['autoTranslate', 'priceTracking'], (settings) => {
      if (settings.autoTranslate) {
        chrome.tabs.sendMessage(tabId, { 
          action: 'autoTranslate' 
        });
      }
      
      if (settings.priceTracking && isShoppingUrl(tab.url)) {
        chrome.tabs.sendMessage(tabId, { 
          action: 'trackPrice' 
        });
      }
    });
  }
});

/**
 * 쇼핑몰 URL 체크
 */
function isShoppingUrl(url) {
  const shoppingDomains = [
    'coupang.com',
    'naver.com/shopping',
    '11st.co.kr',
    'gmarket.co.kr',
    'auction.co.kr'
  ];
  
  return shoppingDomains.some(domain => url.includes(domain));
}

/**
 * 컨텍스트 메뉴 생성
 */
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'scrapeSelection',
    title: '선택한 텍스트 스크래핑',
    contexts: ['selection']
  });
  
  chrome.contextMenus.create({
    id: 'translateSelection',
    title: '선택한 텍스트 번역',
    contexts: ['selection']
  });
  
  chrome.contextMenus.create({
    id: 'checkPrice',
    title: '가격 추적하기',
    contexts: ['link']
  });
});

/**
 * 컨텍스트 메뉴 클릭 처리
 */
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'scrapeSelection') {
    const selectedText = info.selectionText;
    showNotification('스크래핑 완료', `"${selectedText}" 저장됨`);
    
    chrome.storage.local.get(['scrapedData'], (result) => {
      const scrapedData = result.scrapedData || [];
      scrapedData.push({
        text: selectedText,
        url: info.pageUrl,
        timestamp: new Date().toISOString()
      });
      chrome.storage.local.set({ scrapedData: scrapedData });
    });
  }
  
  if (info.menuItemId === 'translateSelection') {
    chrome.tabs.sendMessage(tab.id, {
      action: 'translateText',
      text: info.selectionText
    });
  }
  
  if (info.menuItemId === 'checkPrice') {
    chrome.tabs.sendMessage(tab.id, {
      action: 'addPriceTracking',
      url: info.linkUrl
    });
  }
});

/**
 * 주기적 가격 체크 (알람 사용)
 */
chrome.alarms.create('priceCheck', { periodInMinutes: 60 });

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'priceCheck') {
    checkAllPrices();
  }
});

/**
 * 모든 추적 중인 가격 체크
 */
function checkAllPrices() {
  chrome.storage.local.get(['trackedPrices'], (result) => {
    const trackedPrices = result.trackedPrices || [];
    
    trackedPrices.forEach(item => {
      // 실제 구현에서는 각 URL을 방문하여 가격 체크
      console.log('가격 체크:', item.url);
    });
  });
}

console.log('백그라운드 스크립트가 로드되었습니다.');
