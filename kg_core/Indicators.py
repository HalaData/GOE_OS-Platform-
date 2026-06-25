"""
المؤشرات التسعة الأساسية
"""

class KnowledgeIndicators:
    PAI = "الغياب الإجرائي"
    CGI = "فجوة المصداقية"
    ERI = "الجمود المعرفي"
    FQI = "الأسئلة المحرمة"
    AGI = "فجوة الفاعلين"
    DIC = "التنوع المعرفي"
    MCI = "التواضع المعرفي"
    LRI = "الجمود التشريعي"
    SAI = "الاغتراب الدلالي"
    
    @staticmethod
    def get_all_indicators():
        return [
            {"name": KnowledgeIndicators.PAI, "min": 0, "max": 1, "threshold_good": 0.3},
            {"name": KnowledgeIndicators.CGI, "min": 0, "max": 1, "threshold_good": 0.4},
            {"name": KnowledgeIndicators.ERI, "min": 0, "max": 1, "threshold_good": 0.4},
            {"name": KnowledgeIndicators.FQI, "min": 0, "max": 1, "threshold_good": 0.5},
            {"name": KnowledgeIndicators.AGI, "min": 0, "max": 1, "threshold_good": 0.3},
            {"name": KnowledgeIndicators.DIC, "min": 0, "max": 1, "threshold_good": 0.6},
            {"name": KnowledgeIndicators.MCI, "min": 0, "max": 1, "threshold_good": 0.5},
            {"name": KnowledgeIndicators.LRI, "min": 0, "max": 1, "threshold_good": 0.3},
            {"name": KnowledgeIndicators.SAI, "min": 0, "max": 1, "threshold_good": 0.4}
        ]
