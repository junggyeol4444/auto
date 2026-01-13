"""
Content Restructuring Module
Generates scripts from crawled content using templates
"""
import logging
from typing import Dict, List
import json
import os

logger = logging.getLogger(__name__)


class ScriptTemplate:
    """Base class for script templates"""
    
    def format(self, data: Dict) -> str:
        """Format data into script"""
        raise NotImplementedError


class NewsReportTemplate(ScriptTemplate):
    """Template for news report style videos"""
    
    def format(self, data: Dict) -> str:
        """Format news articles into a report script"""
        topic = data.get('topic', 'Unknown Topic')
        articles = data.get('news_articles', [])
        
        if not articles:
            return "No content available to create script."
        
        # Build script
        script = f"안녕하세요. 오늘은 '{topic}'에 대한 최신 소식을 전해드립니다.\n\n"
        
        for i, article in enumerate(articles[:5], 1):  # Limit to 5 articles
            title = article.get('title', '')
            description = article.get('description', '')
            
            if title:
                script += f"{i}. {title}\n"
                if description:
                    script += f"{description}\n\n"
        
        script += "이상으로 오늘의 뉴스를 마치겠습니다. 시청해 주셔서 감사합니다."
        
        return script


class InformationalTemplate(ScriptTemplate):
    """Template for informational/educational videos"""
    
    def format(self, data: Dict) -> str:
        """Format wiki content into an informational script"""
        topic = data.get('topic', 'Unknown Topic')
        wiki_content = data.get('wiki_content', {})
        
        script = f"안녕하세요. 오늘은 '{topic}'에 대해 알아보겠습니다.\n\n"
        
        # Try Wikipedia first
        wiki_data = wiki_content.get('wikipedia') or wiki_content.get('namuwiki')
        
        if wiki_data and wiki_data.get('content'):
            content = wiki_data['content']
            
            # Split into paragraphs and format
            paragraphs = content.split('\n\n')
            
            for paragraph in paragraphs[:5]:  # Limit to 5 paragraphs
                if paragraph.strip():
                    script += f"{paragraph.strip()}\n\n"
        else:
            script += f"{topic}에 대한 정보를 찾을 수 없습니다.\n\n"
        
        script += f"이상으로 '{topic}'에 대한 설명을 마치겠습니다. 시청해 주셔서 감사합니다."
        
        return script


class StorytellingTemplate(ScriptTemplate):
    """Template for storytelling style videos"""
    
    def format(self, data: Dict) -> str:
        """Format content into a storytelling script"""
        topic = data.get('topic', 'Unknown Topic')
        wiki_content = data.get('wiki_content', {})
        articles = data.get('news_articles', [])
        
        script = f"여러분 안녕하세요. 오늘은 '{topic}'에 대한 흥미로운 이야기를 들려드리겠습니다.\n\n"
        
        # Try to use wiki content for main story
        wiki_data = wiki_content.get('wikipedia') or wiki_content.get('namuwiki')
        
        if wiki_data and wiki_data.get('content'):
            content = wiki_data['content']
            paragraphs = content.split('\n\n')
            
            script += "먼저, 기본적인 내용부터 살펴볼까요?\n\n"
            
            for paragraph in paragraphs[:3]:
                if paragraph.strip():
                    script += f"{paragraph.strip()}\n\n"
        
        # Add recent news if available
        if articles:
            script += "그리고 최근에는 이런 소식들이 있었습니다.\n\n"
            
            for i, article in enumerate(articles[:3], 1):
                title = article.get('title', '')
                description = article.get('description', '')
                
                if title:
                    script += f"{title}"
                    if description:
                        script += f" - {description}"
                    script += "\n\n"
        
        script += f"이것으로 '{topic}'에 대한 이야기를 마치겠습니다. 재미있으셨나요? 시청해 주셔서 감사합니다."
        
        return script


class ContentRestructurer:
    """Main class for restructuring crawled content into scripts"""
    
    def __init__(self):
        self.templates = {
            'news': NewsReportTemplate(),
            'informational': InformationalTemplate(),
            'storytelling': StorytellingTemplate()
        }
    
    def generate_script(self, content_data: Dict, template_type: str = 'informational') -> str:
        """Generate a script from content data using the specified template"""
        
        if template_type not in self.templates:
            logger.warning(f"Unknown template type: {template_type}. Using 'informational'.")
            template_type = 'informational'
        
        template = self.templates[template_type]
        script = template.format(content_data)
        
        logger.info(f"Generated script with {len(script)} characters using {template_type} template")
        
        return script
    
    def generate_metadata(self, content_data: Dict, script: str) -> Dict:
        """Generate SEO-optimized metadata for the video"""
        topic = content_data.get('topic', 'Unknown Topic')
        
        # Generate title
        title = f"{topic} - 완벽 정리"
        
        # Generate description
        description = f"{topic}에 대한 자세한 정보를 제공합니다.\n\n"
        description += script[:200] + "...\n\n"
        description += "이 영상이 도움이 되셨다면 좋아요와 구독 부탁드립니다!\n"
        description += "#" + topic.replace(' ', '') + " #정보 #교육"
        
        # Generate tags
        tags = [
            topic,
            topic + " 정보",
            topic + " 설명",
            "정보",
            "교육",
            "뉴스"
        ]
        
        metadata = {
            'title': title[:100],  # YouTube title limit
            'description': description[:5000],  # YouTube description limit
            'tags': tags[:15],  # YouTube recommends max 15 tags
            'category': '22',  # People & Blogs
            'privacy_status': 'public'
        }
        
        return metadata
    
    def save_script(self, script: str, filepath: str) -> bool:
        """Save generated script to file"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(script)
            logger.info(f"Script saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving script: {e}")
            return False
    
    def load_script(self, filepath: str) -> str:
        """Load script from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                script = f.read()
            logger.info(f"Script loaded from {filepath}")
            return script
        except Exception as e:
            logger.error(f"Error loading script: {e}")
            return ""
