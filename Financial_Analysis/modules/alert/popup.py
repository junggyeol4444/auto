"""
윈도우 팝업 알림 모듈
"""
try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False
    print("plyer 라이브러리가 설치되지 않았습니다. 팝업 알림이 비활성화됩니다.")


class PopupAlert:
    def __init__(self):
        """팝업 알림 초기화"""
        self.enabled = PLYER_AVAILABLE
    
    def show_notification(self, title: str, message: str, timeout: int = 10) -> bool:
        """윈도우 알림 표시"""
        if not self.enabled:
            print(f"팝업 알림 (비활성화): {title} - {message}")
            return False
        
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="금융 데이터 분석",
                timeout=timeout
            )
            print(f"팝업 알림 표시: {title}")
            return True
        except Exception as e:
            print(f"팝업 알림 오류: {e}")
            return False
    
    def show_price_alert(self, asset: str, current_price: float, target_price: float) -> bool:
        """가격 알림 팝업"""
        title = f"💰 {asset} 가격 알림"
        message = f"목표가 {target_price:,.0f}원 도달!\n현재가: {current_price:,.0f}원"
        return self.show_notification(title, message)
    
    def show_alert(self, title: str, content: str, timeout: int = 10) -> bool:
        """일반 알림 팝업"""
        return self.show_notification(title, content, timeout)
