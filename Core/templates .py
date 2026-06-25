"""
القوالب الجاهزة
"""

from typing import Dict, List

class TemplateSystem:
    TEMPLATES = {
        "policy_analysis": {
            "id": "policy_analysis",
            "name": "📜 تحليل السياسات الحكومية",
            "description": "تحليل نصوص السياسات والتشريعات",
            "fields": ["النص السياسي", "الدولة", "السنة"],
            "indicators": ["ERI", "FQI", "PAI", "LRI"]
        },
        "investment_opportunity": {
            "id": "investment_opportunity",
            "name": "💰 تحليل فرص الاستثمار",
            "description": "تحليل جاذبية الأسواق الناشئة",
            "fields": ["الدولة", "القطاع", "حجم الاستثمار"],
            "indicators": ["PAI", "CGI", "AGI", "LRI"]
        },
        "educational_curriculum": {
            "id": "educational_curriculum",
            "name": "📚 تحليل المناهج التعليمية",
            "description": "تحليل المناهج الدراسية",
            "fields": ["نص المنهج", "المرحلة", "المادة"],
            "indicators": ["DIC", "MCI", "SAI", "FQI"]
        },
        "scientific_research": {
            "id": "scientific_research",
            "name": "🔬 تحليل الأبحاث العلمية",
            "description": "تحليل الأوراق البحثية",
            "fields": ["نص البحث", "المجال", "السنة"],
            "indicators": ["ERI", "FQI", "DIC", "MCI"]
        },
        "corporate_governance": {
            "id": "corporate_governance",
            "name": "🏢 تحليل حوكمة الشركات",
            "description": "تحليل تقارير الحوكمة",
            "fields": ["نص التقرير", "الشركة", "السنة"],
            "indicators": ["CGI", "AGI", "PAI", "LRI"]
        }
    }
    
    @classmethod
    def get_all_templates(cls) -> List[Dict]:
        return list(cls.TEMPLATES.values())
    
    @classmethod
    def get_template(cls, template_id: str) -> Dict:
        return cls.TEMPLATES.get(template_id)
