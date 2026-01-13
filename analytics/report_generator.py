"""
리포트 자동 생성 도구
Report Generator
"""
import logging
from datetime import datetime
from typing import Dict, List
import matplotlib
matplotlib.use('Agg')  # GUI 없이 사용
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

logger = logging.getLogger('report_generator')


class ReportGenerator:
    """리포트 생성 클래스"""
    
    def __init__(self, output_dir='output/reports'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs('output/graphs', exist_ok=True)
        
        # 한글 폰트 설정 시도
        try:
            # Windows 기본 폰트
            font_paths = [
                'C:/Windows/Fonts/malgun.ttf',  # 맑은 고딕
                'C:/Windows/Fonts/gulim.ttc',   # 굴림
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont('Korean', font_path))
                    self.korean_font = 'Korean'
                    break
            else:
                self.korean_font = 'Helvetica'
        except:
            self.korean_font = 'Helvetica'
        
        # Matplotlib 한글 폰트 설정
        try:
            plt.rcParams['font.family'] = 'Malgun Gothic'
            plt.rcParams['axes.unicode_minus'] = False
        except:
            pass
    
    def create_traffic_graph(self, data: List[Dict], output_file: str):
        """트래픽 그래프 생성"""
        try:
            dates = [d['date'] for d in data]
            users = [d['users'] for d in data]
            
            plt.figure(figsize=(12, 6))
            plt.plot(dates, users, marker='o', linewidth=2, markersize=6)
            plt.title('웹 트래픽 추이', fontsize=16, fontweight='bold')
            plt.xlabel('날짜', fontsize=12)
            plt.ylabel('사용자 수', fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f'트래픽 그래프 생성: {output_file}')
            return output_file
        except Exception as e:
            logger.error(f'그래프 생성 실패: {str(e)}')
            return None
    
    def create_price_graph(self, data: List[Dict], output_file: str):
        """가격 그래프 생성"""
        try:
            dates = [d['timestamp'][:10] for d in data]
            prices = [d['price'] for d in data]
            
            plt.figure(figsize=(12, 6))
            plt.plot(dates, prices, marker='o', linewidth=2, markersize=6, color='#2ecc71')
            
            # 최저가, 최고가 표시
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) / len(prices)
            
            plt.axhline(y=min_price, color='g', linestyle='--', label=f'최저가: {min_price:,.0f}원')
            plt.axhline(y=max_price, color='r', linestyle='--', label=f'최고가: {max_price:,.0f}원')
            plt.axhline(y=avg_price, color='b', linestyle='--', label=f'평균가: {avg_price:,.0f}원')
            
            plt.title('가격 변동 추이', fontsize=16, fontweight='bold')
            plt.xlabel('날짜', fontsize=12)
            plt.ylabel('가격 (원)', fontsize=12)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f'가격 그래프 생성: {output_file}')
            return output_file
        except Exception as e:
            logger.error(f'그래프 생성 실패: {str(e)}')
            return None
    
    def create_pie_chart(self, data: Dict, title: str, output_file: str):
        """파이 차트 생성"""
        try:
            labels = list(data.keys())
            sizes = list(data.values())
            colors_list = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
            
            plt.figure(figsize=(10, 8))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors_list[:len(labels)],
                   startangle=90)
            plt.title(title, fontsize=16, fontweight='bold')
            plt.axis('equal')
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f'파이 차트 생성: {output_file}')
            return output_file
        except Exception as e:
            logger.error(f'차트 생성 실패: {str(e)}')
            return None
    
    def create_bar_chart(self, data: Dict, title: str, xlabel: str, ylabel: str, 
                        output_file: str):
        """막대 차트 생성"""
        try:
            labels = list(data.keys())
            values = list(data.values())
            
            plt.figure(figsize=(12, 6))
            plt.bar(labels, values, color='#3498db', alpha=0.8)
            plt.title(title, fontsize=16, fontweight='bold')
            plt.xlabel(xlabel, fontsize=12)
            plt.ylabel(ylabel, fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f'막대 차트 생성: {output_file}')
            return output_file
        except Exception as e:
            logger.error(f'차트 생성 실패: {str(e)}')
            return None
    
    def generate_pdf_report(self, title: str, data: Dict, output_file: str = None):
        """PDF 리포트 생성"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(self.output_dir, f'report_{timestamp}.pdf')
        
        try:
            doc = SimpleDocTemplate(output_file, pagesize=A4)
            story = []
            
            # 스타일 설정
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName=self.korean_font,
                fontSize=24,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=30
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontName=self.korean_font,
                fontSize=16,
                textColor=colors.HexColor('#34495e'),
                spaceAfter=12
            )
            
            # 제목
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 0.2 * inch))
            
            # 날짜
            date_text = f"생성일: {datetime.now().strftime('%Y년 %m월 %d일')}"
            story.append(Paragraph(date_text, styles['Normal']))
            story.append(Spacer(1, 0.3 * inch))
            
            # 데이터 섹션 추가
            for section_title, section_data in data.items():
                story.append(Paragraph(section_title, heading_style))
                
                if isinstance(section_data, dict):
                    # 테이블로 표시
                    table_data = [['항목', '값']]
                    for key, value in section_data.items():
                        table_data.append([str(key), str(value)])
                    
                    t = Table(table_data)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), self.korean_font),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    
                    story.append(t)
                
                elif isinstance(section_data, str) and os.path.exists(section_data):
                    # 이미지 파일 경로인 경우
                    img = Image(section_data, width=6*inch, height=3*inch)
                    story.append(img)
                
                story.append(Spacer(1, 0.3 * inch))
            
            # PDF 생성
            doc.build(story)
            logger.info(f'PDF 리포트 생성: {output_file}')
            return output_file
        
        except Exception as e:
            logger.error(f'PDF 생성 실패: {str(e)}')
            return None
    
    def generate_weekly_report(self, analytics_data: Dict, price_data: Dict = None):
        """주간 리포트 생성"""
        timestamp = datetime.now().strftime('%Y%m%d')
        
        # 그래프 생성
        graphs = {}
        
        if 'traffic_data' in analytics_data:
            graph_file = f'output/graphs/traffic_{timestamp}.png'
            self.create_traffic_graph(analytics_data['traffic_data'], graph_file)
            graphs['트래픽 추이'] = graph_file
        
        if price_data and 'price_history' in price_data:
            graph_file = f'output/graphs/price_{timestamp}.png'
            self.create_price_graph(price_data['price_history'], graph_file)
            graphs['가격 추이'] = graph_file
        
        # PDF 리포트 생성
        report_data = {
            '개요': analytics_data.get('overview', {}),
            **graphs
        }
        
        output_file = os.path.join(self.output_dir, f'weekly_report_{timestamp}.pdf')
        return self.generate_pdf_report('주간 리포트', report_data, output_file)
    
    def generate_monthly_report(self, analytics_data: Dict):
        """월간 리포트 생성"""
        timestamp = datetime.now().strftime('%Y%m')
        output_file = os.path.join(self.output_dir, f'monthly_report_{timestamp}.pdf')
        return self.generate_pdf_report('월간 리포트', analytics_data, output_file)


if __name__ == '__main__':
    generator = ReportGenerator()
    print("리포트 생성 도구가 로드되었습니다.")
