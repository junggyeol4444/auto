/**
 * 크롬 확장 프로그램 - 콘텐츠 스크립트
 * Content Script for page manipulation
 */

console.log('콘텐츠 스크립트가 로드되었습니다.');

// 메시지 리스너
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('콘텐츠 스크립트 메시지 수신:', request);
  
  if (request.action === 'autoTranslate') {
    autoTranslatePage();
    sendResponse({ success: true });
  }
  
  if (request.action === 'trackPrice') {
    const priceInfo = extractPriceInfo();
    sendResponse({ success: true, priceInfo: priceInfo });
  }
  
  if (request.action === 'scrapeProducts') {
    const products = scrapeProducts();
    sendResponse({ success: true, products: products });
  }
  
  if (request.action === 'fillForm') {
    fillForm(request.data);
    sendResponse({ success: true });
  }
  
  if (request.action === 'autoClick') {
    autoClick(request.selector);
    sendResponse({ success: true });
  }
  
  if (request.action === 'translateText') {
    translateSelectedText(request.text);
    sendResponse({ success: true });
  }
  
  if (request.action === 'blockAds') {
    blockAds();
    sendResponse({ success: true });
  }
  
  return true;
});

/**
 * 페이지 자동 번역
 */
function autoTranslatePage() {
  const textNodes = getTextNodes(document.body);
  
  textNodes.forEach(node => {
    if (node.textContent.trim()) {
      // 실제 구현에서는 번역 API 호출
      // node.textContent = `[번역됨] ${node.textContent}`;
    }
  });
  
  console.log('페이지 번역 완료');
}

/**
 * 텍스트 노드 가져오기
 */
function getTextNodes(element) {
  const textNodes = [];
  const walker = document.createTreeWalker(
    element,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );
  
  let node;
  while (node = walker.nextNode()) {
    if (node.textContent.trim()) {
      textNodes.push(node);
    }
  }
  
  return textNodes;
}

/**
 * 가격 정보 추출
 */
function extractPriceInfo() {
  const url = window.location.href;
  let price = null;
  let productName = null;
  
  // 쿠팡
  if (url.includes('coupang.com')) {
    price = document.querySelector('.total-price')?.textContent;
    productName = document.querySelector('.prod-buy-header__title')?.textContent;
  }
  
  // 네이버 쇼핑
  else if (url.includes('shopping.naver.com')) {
    price = document.querySelector('.price_num')?.textContent;
    productName = document.querySelector('.h_product')?.textContent;
  }
  
  // 11번가
  else if (url.includes('11st.co.kr')) {
    price = document.querySelector('.sale_price')?.textContent;
    productName = document.querySelector('.title')?.textContent;
  }
  
  // 지마켓
  else if (url.includes('gmarket.co.kr')) {
    price = document.querySelector('.price_innerwrap')?.textContent;
    productName = document.querySelector('.itemtit')?.textContent;
  }
  
  return {
    url: url,
    price: price?.replace(/[^0-9]/g, ''),
    productName: productName?.trim(),
    timestamp: new Date().toISOString()
  };
}

/**
 * 제품 정보 스크래핑
 */
function scrapeProducts() {
  const products = [];
  const url = window.location.href;
  
  // 쿠팡
  if (url.includes('coupang.com')) {
    const items = document.querySelectorAll('.search-product');
    items.forEach(item => {
      const name = item.querySelector('.name')?.textContent;
      const price = item.querySelector('.price-value')?.textContent;
      const image = item.querySelector('img')?.src;
      
      if (name && price) {
        products.push({ name, price, image });
      }
    });
  }
  
  // 네이버 쇼핑
  else if (url.includes('shopping.naver.com')) {
    const items = document.querySelectorAll('.product_item');
    items.forEach(item => {
      const name = item.querySelector('.product_title')?.textContent;
      const price = item.querySelector('.price_num')?.textContent;
      const image = item.querySelector('img')?.src;
      
      if (name && price) {
        products.push({ name, price, image });
      }
    });
  }
  
  return products;
}

/**
 * 폼 자동 작성
 */
function fillForm(data) {
  for (const [selector, value] of Object.entries(data)) {
    const element = document.querySelector(selector);
    
    if (element) {
      if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
        element.value = value;
        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }
  }
  
  console.log('폼 작성 완료');
}

/**
 * 자동 클릭
 */
function autoClick(selector) {
  const element = document.querySelector(selector);
  
  if (element) {
    element.click();
    console.log('클릭 완료:', selector);
  } else {
    console.log('요소를 찾을 수 없음:', selector);
  }
}

/**
 * 선택한 텍스트 번역
 */
function translateSelectedText(text) {
  // 번역 결과를 툴팁으로 표시
  const tooltip = document.createElement('div');
  tooltip.id = 'translation-tooltip';
  tooltip.style.position = 'fixed';
  tooltip.style.backgroundColor = '#333';
  tooltip.style.color = '#fff';
  tooltip.style.padding = '10px';
  tooltip.style.borderRadius = '5px';
  tooltip.style.zIndex = '10000';
  tooltip.textContent = `번역 중: ${text}`;
  
  // 마우스 위치에 표시
  const selection = window.getSelection();
  const range = selection.getRangeAt(0);
  const rect = range.getBoundingClientRect();
  
  tooltip.style.top = `${rect.top - 40}px`;
  tooltip.style.left = `${rect.left}px`;
  
  document.body.appendChild(tooltip);
  
  // 3초 후 제거
  setTimeout(() => {
    tooltip.remove();
  }, 3000);
  
  // 실제 번역 API 호출
  chrome.runtime.sendMessage({
    action: 'translate',
    text: text,
    targetLang: 'ko'
  }, (response) => {
    if (response.success) {
      tooltip.textContent = response.translatedText;
    }
  });
}

/**
 * 광고 차단
 */
function blockAds() {
  const adSelectors = [
    '.ad',
    '.advertisement',
    '.google-ad',
    '[id*="ad"]',
    '[class*="ad-"]',
    'iframe[src*="doubleclick"]',
    'iframe[src*="googlesyndication"]'
  ];
  
  adSelectors.forEach(selector => {
    const ads = document.querySelectorAll(selector);
    ads.forEach(ad => {
      ad.style.display = 'none';
      console.log('광고 차단:', selector);
    });
  });
}

/**
 * DOM 변경 감지 (광고 동적 삽입 대응)
 */
const observer = new MutationObserver((mutations) => {
  chrome.storage.sync.get(['adBlock'], (settings) => {
    if (settings.adBlock) {
      blockAds();
    }
  });
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});

/**
 * 가격 비교 테이블 삽입
 */
function insertPriceComparisonTable(prices) {
  const table = document.createElement('div');
  table.id = 'price-comparison-table';
  table.style.position = 'fixed';
  table.style.top = '10px';
  table.style.right = '10px';
  table.style.backgroundColor = 'white';
  table.style.border = '1px solid #ccc';
  table.style.padding = '10px';
  table.style.zIndex = '10000';
  table.style.maxWidth = '300px';
  
  let html = '<h3>가격 비교</h3><table>';
  html += '<tr><th>쇼핑몰</th><th>가격</th></tr>';
  
  prices.forEach(item => {
    html += `<tr><td>${item.site}</td><td>${item.price}</td></tr>`;
  });
  
  html += '</table>';
  table.innerHTML = html;
  
  document.body.appendChild(table);
}

/**
 * 뉴스 헤드라인 스크래핑
 */
function scrapeNewsHeadlines() {
  const headlines = [];
  
  // 네이버 뉴스
  if (window.location.href.includes('news.naver.com')) {
    const items = document.querySelectorAll('.list_body .article_tit');
    items.forEach(item => {
      headlines.push(item.textContent.trim());
    });
  }
  
  return headlines;
}

console.log('콘텐츠 스크립트 준비 완료');
