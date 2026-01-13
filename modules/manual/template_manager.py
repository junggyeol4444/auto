"""
Template manager for manuals
"""
import json


class TemplateManager:
    """Manage manual templates"""
    
    def __init__(self, template_path):
        self.template_path = template_path
        self.template = self._load_template()
    
    def _load_template(self):
        """Load template from file"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"템플릿 로드 오류: {str(e)}")
    
    def get_sections(self):
        """Get template sections"""
        return self.template.get('sections', [])
    
    def get_template_string(self, key):
        """Get specific template string"""
        templates = self.template.get('templates', {})
        return templates.get(key, '')
    
    def format_template(self, key, **kwargs):
        """Format template with provided values"""
        template = self.get_template_string(key)
        try:
            return template.format(**kwargs)
        except KeyError as e:
            return template
