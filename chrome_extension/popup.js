/**
 * 크롬 확장 프로그램 - 팝업 스크립트
 * Popup UI Logic
 */

// 상태 메시지 업데이트
function updateStatus(message) {
  const statusDiv = document.getElementById('status');
  const timestamp = new Date().toLocaleTimeString('ko-KR');
  statusDiv.textContent = `[${timestamp}] ${message}`;
}

// 현재 탭 가져오기
async function getCurrentTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

// 설정 로드
chrome.storage.sync.get(
  ['autoTranslate', 'priceTracking', 'adBlock', 'notifications'],
  (settings) => {
    document.getElementById('autoTranslate').checked = settings.autoTranslate || false;
    document.getElementById('priceTracking').checked = settings.priceTracking !== false;
    document.getElementById('adBlock').checked = settings.adBlock || false;
    document.getElementById('notifications').checked = settings.notifications !== false;
  }
);

// 폼 자동 작성 버튼
document.getElementById('autoFillBtn').addEventListener('click', async () => {
  updateStatus('폼 자동 작성 중...');
  
  const tab = await getCurrentTab();
  
  // 예시 데이터 (실제로는 사용자가 설정)
  const formData = {
    'input[name="name"]': '홍길동',
    'input[name="email"]': 'test@example.com',
    'input[name="phone"]': '010-1234-5678'
  };
  
  chrome.tabs.sendMessage(tab.id, {
    action: 'fillForm',
    data: formData
  }, (response) => {
    if (response && response.success) {
      updateStatus('폼 작성 완료!');
    } else {
      updateStatus('폼 작성 실패');
    }
  });
});

// 데이터 수집 버튼
document.getElementById('scrapeBtn').addEventListener('click', async () => {
  updateStatus('데이터 수집 중...');
  
  const tab = await getCurrentTab();
  
  chrome.tabs.sendMessage(tab.id, {
    action: 'scrapeProducts'
  }, (response) => {
    if (response && response.success) {
      updateStatus(`${response.products.length}개 제품 수집 완료!`);
      
      // 데이터 저장
      chrome.runtime.sendMessage({
        action: 'scrapeData',
        data: {
          url: tab.url,
          products: response.products
        }
      });
    } else {
      updateStatus('데이터 수집 실패');
    }
  });
});

// 가격 비교 버튼
document.getElementById('comparePrice').addEventListener('click', async () => {
  updateStatus('가격 비교 중...');
  
  const tab = await getCurrentTab();
  
  chrome.tabs.sendMessage(tab.id, {
    action: 'trackPrice'
  }, (response) => {
    if (response && response.success && response.priceInfo) {
      const priceInfo = response.priceInfo;
      updateStatus(`현재가: ${priceInfo.price}원`);
      
      // 가격 기록 저장
      chrome.storage.local.get(['priceHistory'], (result) => {
        const priceHistory = result.priceHistory || {};
        
        if (!priceHistory[priceInfo.url]) {
          priceHistory[priceInfo.url] = [];
        }
        
        priceHistory[priceInfo.url].push({
          price: priceInfo.price,
          timestamp: priceInfo.timestamp
        });
        
        chrome.storage.local.set({ priceHistory: priceHistory });
      });
    } else {
      updateStatus('가격 정보를 찾을 수 없습니다.');
    }
  });
});

// 페이지 번역 버튼
document.getElementById('translateBtn').addEventListener('click', async () => {
  updateStatus('페이지 번역 중...');
  
  const tab = await getCurrentTab();
  
  chrome.tabs.sendMessage(tab.id, {
    action: 'autoTranslate'
  }, (response) => {
    if (response && response.success) {
      updateStatus('번역 완료!');
    } else {
      updateStatus('번역 실패');
    }
  });
});

// 광고 차단 버튼
document.getElementById('blockAdsBtn').addEventListener('click', async () => {
  updateStatus('광고 차단 중...');
  
  const tab = await getCurrentTab();
  
  chrome.tabs.sendMessage(tab.id, {
    action: 'blockAds'
  }, (response) => {
    if (response && response.success) {
      updateStatus('광고 차단 완료!');
    } else {
      updateStatus('광고 차단 실패');
    }
  });
});

// 수집 데이터 보기 버튼
document.getElementById('viewDataBtn').addEventListener('click', () => {
  updateStatus('데이터 로드 중...');
  
  chrome.storage.local.get(['scrapedData'], (result) => {
    const scrapedData = result.scrapedData || [];
    
    if (scrapedData.length > 0) {
      updateStatus(`총 ${scrapedData.length}개 데이터 수집됨`);
      console.log('수집된 데이터:', scrapedData);
      
      // 데이터 다운로드
      const dataStr = JSON.stringify(scrapedData, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      
      chrome.downloads.download({
        url: url,
        filename: `scraped_data_${Date.now()}.json`,
        saveAs: true
      });
    } else {
      updateStatus('수집된 데이터가 없습니다.');
    }
  });
});

// 설정 토글 리스너
document.getElementById('autoTranslate').addEventListener('change', (e) => {
  chrome.storage.sync.set({ autoTranslate: e.target.checked });
  updateStatus(`자동 번역: ${e.target.checked ? 'ON' : 'OFF'}`);
});

document.getElementById('priceTracking').addEventListener('change', (e) => {
  chrome.storage.sync.set({ priceTracking: e.target.checked });
  updateStatus(`가격 추적: ${e.target.checked ? 'ON' : 'OFF'}`);
});

document.getElementById('adBlock').addEventListener('change', async (e) => {
  chrome.storage.sync.set({ adBlock: e.target.checked });
  updateStatus(`광고 차단: ${e.target.checked ? 'ON' : 'OFF'}`);
  
  if (e.target.checked) {
    const tab = await getCurrentTab();
    chrome.tabs.sendMessage(tab.id, { action: 'blockAds' });
  }
});

document.getElementById('notifications').addEventListener('change', (e) => {
  chrome.storage.sync.set({ notifications: e.target.checked });
  updateStatus(`알림: ${e.target.checked ? 'ON' : 'OFF'}`);
});

// 초기 상태 메시지
updateStatus('준비됨');
