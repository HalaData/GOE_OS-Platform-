"""
التشريح المعرفي - Cognitive Autopsy
تحليل عملية التفكير بعد القرار لكشف نقاط العمى والتحيزات الخفية
"""

from typing import Dict, List, Any
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)

class CognitiveAutopsyEngine:
    """
    بعد كل قرار، تشريح عملية التفكير لاكتشاف نقاط العمى.
    """
    
    def __init__(self):
        self.autopsy_history = []
    
    def reconstruct_path(self, decision: Dict) -> List[Dict]:
        """إعادة بناء مسار التفكير الذي أدى إلى القرار."""
        # محاكاة مسار التفكير (في الإنتاج سيتم استخراجه من السجلات الفعلية)
        steps = [
            {"step": 1, "description": "تحليل المدخلات", "data_considered": decision.get("input", {})},
            {"step": 2, "description": "تقييم الخيارات", "options": ["Option A", "Option B", "Option C"]},
            {"step": 3, "description": "تطبيق المعايير", "criteria": ["الكفاءة", "التكلفة", "السرعة"]},
            {"step": 4, "description": "اتخاذ القرار", "decision": decision.get("output", "unknown")}
        ]
        return steps
    
    def detect_blind_spots(self, thought_path: List[Dict], context: Dict) -> List[Dict]:
        """تحديد نقاط العمى في مسار التفكير."""
        blind_spots = []
        
        # 1. معلومات مهملة
        if random.random() > 0.5:
            blind_spots.append({
                "type": "ignored_data",
                "description": "تم تجاهل بيانات مهمة من السياق",
                "severity": "medium",
                "suggestion": "إعادة تقييم القرار مع تضمين البيانات المهملة"
            })
        
        # 2. افتراضات خاطئة
        if random.random() > 0.4:
            blind_spots.append({
                "type": "false_assumption",
                "description": "افتراض خاطئ حول استقرار العوامل الخارجية",
                "severity": "high",
                "suggestion": "اختبار الحساسية لتغيرات العوامل"
            })
        
        # 3. انحياز تأكيدي
        if random.random() > 0.6:
            blind_spots.append({
                "type": "confirmation_bias",
                "description": "تم التركيز على الأدلة المؤيدة للقرار وتجاهل الأدلة المعارضة",
                "severity": "high",
                "suggestion": "طلب رأي مخالف قبل اتخاذ القرارات المستقبلية"
            })
        
        return blind_spots
    
    def generate_regret_report(self, decision: Dict, blind_spots: List[Dict]) -> Dict:
        """توليد تقرير الندم (ما يمكن فعله بشكل مختلف)."""
        if not blind_spots:
            return {
                "has_regret": False,
                "message": "لا توجد نقاط عمى مكتشفة. القرار جيد."
            }
        
        return {
            "has_regret": True,
            "alternative_outcomes": [
                {
                    "alternative": "ضبط القرار لتضمين البيانات المهملة",
                    "estimated_improvement": random.randint(5, 20)
                },
                {
                    "alternative": "اختبار الحساسية قبل القرار",
                    "estimated_improvement": random.randint(10, 30)
                }
            ],
            "lessons_learned": [bs["suggestion"] for bs in blind_spots],
            "regret_score": sum(1 for bs in blind_spots if bs["severity"] == "high") * 10
        }
    
    def suggest_improvements(self, blind_spots: List[Dict]) -> List[str]:
        """اقتراح تحسينات لمعالجة نقاط العمى."""
        return [bs["suggestion"] for bs in blind_spots]
    
    def autopsy_decision(self, decision: Dict, context: Dict) -> Dict:
        """الدورة الكاملة للتشريح المعرفي."""
        thought_path = self.reconstruct_path(decision)
        blind_spots = self.detect_blind_spots(thought_path, context)
        regret_report = self.generate_regret_report(decision, blind_spots)
        
        result = {
            "status": "completed",
            "thought_path": thought_path,
            "blind_spots": blind_spots,
            "regret_report": regret_report,
            "improvement_suggestions": self.suggest_improvements(blind_spots),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.autopsy_history.append(result)
        return result
