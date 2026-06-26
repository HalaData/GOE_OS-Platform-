"""
المعرفة الظرفية - Contextual Omniscience
تحليل السياق الكامل للنص (جغرافي، زمني، ثقافي، نفسي)
"""

from typing import Dict, List, Any
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)

class ContextualOmniscience:
    """
    يحلل السياق الكامل المحيط بالنص (الجغرافي، الزمني، الثقافي، النفسي).
    """
    
    def __init__(self):
        self.context_history = []
    
    def analyze_geography(self, location: str) -> Dict:
        """تحليل السياق الجغرافي."""
        geo_contexts = {
            "global": {"impact": 0.5, "description": "سياق عالمي محايد"},
            "middle_east": {"impact": 0.7, "description": "سياق شرق أوسطي، حساسية سياسية عالية"},
            "europe": {"impact": 0.3, "description": "سياق أوروبي، تركيز على القانون والتنظيم"},
            "asia": {"impact": 0.4, "description": "سياق آسيوي، تركيز على الجماعية"},
            "africa": {"impact": 0.6, "description": "سياق أفريقي، تركيز على التنمية"}
        }
        return geo_contexts.get(location, geo_contexts["global"])
    
    def analyze_temporal(self, timestamp: str) -> Dict:
        """تحليل السياق الزمني."""
        try:
            dt = datetime.fromisoformat(timestamp)
            hour = dt.hour
            month = dt.month
        except:
            hour = 12
            month = 6
        
        return {
            "hour": hour,
            "month": month,
            "time_of_day": "صباح" if 5 <= hour < 12 else "ظهر" if 12 <= hour < 16 else "مساء" if 16 <= hour < 20 else "ليل",
            "season": "ربيع" if 3 <= month <= 5 else "صيف" if 6 <= month <= 8 else "خريف" if 9 <= month <= 11 else "شتاء",
            "impact": 0.3 if 6 <= hour <= 18 else 0.7
        }
    
    def analyze_culture(self, text: str) -> Dict:
        """تحليل السياق الثقافي."""
        cultural_indicators = {
            "collectivism": ["نحن", "مجتمع", "جماعة", "معاً"],
            "individualism": ["أنا", "خاصتي", "فردي", "حرية"],
            "hierarchy": ["رئيس", "مسؤول", "مرؤوس", "أوامر"],
            "equality": ["مساواة", "حقوق", "عدالة", "جميع"]
        }
        
        detected = {}
        for culture_type, keywords in cultural_indicators.items():
            count = sum(1 for k in keywords if k in text)
            detected[culture_type] = min(1.0, count / len(keywords) * 2)
        
        dominant = max(detected, key=detected.get) if detected else "neutral"
        
        return {
            "detected_patterns": detected,
            "dominant_culture": dominant,
            "cultural_complexity": len([v for v in detected.values() if v > 0.3]),
            "impact": 0.5 + (len([v for v in detected.values() if v > 0.5]) * 0.1)
        }
    
    def analyze_psychology(self, text: str) -> Dict:
        """تحليل السياق النفسي."""
        emotional_indicators = {
            "optimism": ["أمل", "مستقبل", "تحسن", "نجاح"],
            "anxiety": ["خوف", "قلق", "خطر", "مشكلة"],
            "anger": ["غضب", "عدوان", "رفض", "تحدي"],
            "sadness": ["حزن", "فقد", "ألم", "خيبة"],
            "neutral": ["ربما", "قد", "نأمل", "نتوقع"]
        }
        
        detected = {}
        for emotion, keywords in emotional_indicators.items():
            count = sum(1 for k in keywords if k in text)
            detected[emotion] = min(1.0, count / len(keywords) * 2)
        
        dominant = max(detected, key=detected.get) if detected else "neutral"
        
        return {
            "emotional_state": dominant,
            "intensity": max(detected.values()) if detected else 0.3,
            "psychological_complexity": len([v for v in detected.values() if v > 0.3]),
            "impact": 0.5 + (max(detected.values()) * 0.3 if detected else 0)
        }
    
    def analyze_context(self, text: str, meta: Dict) -> Dict:
        """التحليل الشامل للسياق."""
        geography = self.analyze_geography(meta.get("location", "global"))
        temporal = self.analyze_temporal(meta.get("timestamp", datetime.utcnow().isoformat()))
        culture = self.analyze_culture(text)
        psychology = self.analyze_psychology(text)
        
        # الوزن النهائي
        weighted_meaning = {
            "text": text,
            "geo_weight": geography["impact"],
            "temporal_weight": temporal["impact"],
            "cultural_weight": culture["impact"],
            "psychological_weight": psychology["impact"],
            "total_context_weight": (geography["impact"] + temporal["impact"] + culture["impact"] + psychology["impact"]) / 4
        }
        
        result = {
            "geography": geography,
            "temporal": temporal,
            "culture": culture,
            "psychology": psychology,
            "weighted_meaning": weighted_meaning,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.context_history.append(result)
        return result
