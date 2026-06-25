"""
محرك الملاذات الآمنة المتقدم - النسخة النهائية
يجمع بين تحليل السياسات، التشريعات، والملاذات الآمنة
مع تطبيق الموجهات الخمسة ونقاط قوة المنافسين
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import logging
import hashlib
import random
from collections import defaultdict
import re

logger = logging.getLogger(__name__)

# ============================================================
# 1. المؤشرات التسعة (مطبقة بالكامل)
# ============================================================

class GovernanceIndicators:
    """
    المؤشرات التسعة للحوكمة المعرفية - المطبقة على السياسات والتشريعات
    """
    
    @staticmethod
    def analyze(text: str, context: Dict = None) -> Dict:
        indicators = {}
        
        # 1. الجمود المعرفي (ERI)
        certainty_words = ["قطعاً", "حتماً", "لا شك", "بالتأكيد", "سوف", "must", "certainly"]
        doubt_words = ["ربما", "قد", "نأمل", "نتوقع", "في حال", "maybe", "perhaps"]
        c_count = sum(1 for w in certainty_words if w.lower() in text.lower())
        d_count = sum(1 for w in doubt_words if w.lower() in text.lower())
        total = c_count + d_count
        indicators["ERI"] = round(c_count / (total + 0.01), 2)
        
        # 2. الأسئلة المحرمة (FQI)
        critical_words = ["لماذا", "كيف", "لكن", "رغم", "مع أن", "why", "how", "but"]
        count = sum(1 for w in critical_words if w.lower() in text.lower())
        indicators["FQI"] = round(min(count / 20, 1.0), 2)
        
        # 3. الغياب الإجرائي (PAI)
        excluded_entities = ["الشركات الصغرى", "المجتمع المدني", "المنظمات غير الحكومية"]
        count = sum(1 for e in excluded_entities if e in text)
        indicators["PAI"] = round(min(count / 5, 1.0), 2)
        
        # 4. فجوة المصداقية (CGI)
        promises = ["نعد", "نلتزم", "نسعى", "نعمل على", "promise", "commit"]
        actions = ["أنجزنا", "حققنا", "نفذنا", "achieved", "implemented"]
        p_count = sum(1 for w in promises if w.lower() in text.lower())
        a_count = sum(1 for w in actions if w.lower() in text.lower())
        indicators["CGI"] = round(max(0, 1 - (a_count / (p_count + 0.01))), 2) if p_count > 0 else 0.5
        
        # 5. فجوة الفاعلين (AGI)
        actors = ["الرئيس", "الوزير", "المجلس", "اللجنة", "president", "minister"]
        count = sum(1 for a in actors if a in text)
        indicators["AGI"] = round(min(count / 10, 1.0), 2)
        
        # 6. التنوع المعرفي (DIC)
        perspectives = ["اقتصادي", "سياسي", "اجتماعي", "بيئي", "أمني", "economic", "political", "social"]
        count = sum(1 for p in perspectives if p in text)
        indicators["DIC"] = round(min(count / 5, 1.0), 2)
        
        # 7. التواضع المعرفي (MCI)
        humility_words = ["نعترف", "نحن بحاجة", "لا نعلم", "نقدر", "acknowledge", "need"]
        count = sum(1 for w in humility_words if w.lower() in text.lower())
        indicators["MCI"] = round(min(count / 10, 1.0), 2)
        
        # 8. الجمود التشريعي (LRI)
        old_references = ["استمرار", "نفس", "كالعادة", "قبل", "continue", "same"]
        count = sum(1 for w in old_references if w.lower() in text.lower())
        indicators["LRI"] = round(min(count / 5, 1.0), 2)
        
        # 9. الاغتراب الدلالي (SAI)
        complex_terms = ["سيادة", "شرعية", "استراتيجي", "جيوسياسي", "hegemony", "geopolitical"]
        count = sum(1 for t in complex_terms if t.lower() in text.lower())
        indicators["SAI"] = round(min(count / 5, 1.0), 2)
        
        return indicators

# ============================================================
# 2. نظام البحث المتكامل (مستوحى من Glean)
# ============================================================

class UnifiedSearchEngine:
    """محرك بحث متكامل في السياسات والتشريعات"""
    
    def __init__(self):
        self.policy_index = {}
        self.legislation_index = {}
    
    def index_policy(self, policy_id: str, text: str, metadata: Dict):
        """فهرسة سياسة جديدة"""
        self.policy_index[policy_id] = {
            "text": text,
            "metadata": metadata,
            "timestamp": datetime.utcnow().isoformat(),
            "indicators": GovernanceIndicators.analyze(text)
        }
    
    def search_policies(self, query: str) -> List[Dict]:
        """البحث في السياسات"""
        results = []
        for policy_id, policy in self.policy_index.items():
            if query.lower() in policy["text"].lower():
                results.append({
                    "id": policy_id,
                    "metadata": policy["metadata"],
                    "indicators": policy["indicators"],
                    "relevance": self._calculate_relevance(query, policy["text"])
                })
        return sorted(results, key=lambda x: x["relevance"], reverse=True)[:10]
    
    def _calculate_relevance(self, query: str, text: str) -> float:
        """حساب درجة الصلة"""
        query_words = set(query.lower().split())
        text_words = set(text.lower().split())
        overlap = len(query_words & text_words)
        return overlap / (len(query_words) + 0.01)

# ============================================================
# 3. نظام تحليل الفجوات (مستوحى من Inkeep)
# ============================================================

class GapAnalyzer:
    """تحليل الفجوات في السياسات والتشريعات"""
    
    def __init__(self):
        self.gap_history = []
    
    def analyze(self, policy_text: str, indicators: Dict) -> List[Dict]:
        """تحليل الفجوات"""
        gaps = []
        
        # 1. فجوة الجمود المعرفي
        if indicators.get("ERI", 0.5) > 0.6:
            gaps.append({
                "type": "epistemic_rigidity",
                "severity": "high",
                "description": "جمود معرفي مرتفع، السياسة تفتقر إلى المرونة",
                "suggestion": "إضافة آليات للمراجعة الدورية والتكيف",
                "indicator": "ERI"
            })
        
        # 2. فجوة الأسئلة المحرمة
        if indicators.get("FQI", 0.5) < 0.3:
            gaps.append({
                "type": "forbidden_questions",
                "severity": "high",
                "description": "غياب الأسئلة النقدية، وجود تابوهات فكرية",
                "suggestion": "خلق مساحات للحوار النقدي",
                "indicator": "FQI"
            })
        
        # 3. فجوة المصداقية
        if indicators.get("CGI", 0.5) > 0.5:
            gaps.append({
                "type": "credibility_gap",
                "severity": "medium",
                "description": "فجوة بين الوعود والتنفيذ",
                "suggestion": "وضع آليات للمتابعة والتقييم",
                "indicator": "CGI"
            })
        
        # 4. فجوة الجمود التشريعي
        if indicators.get("LRI", 0.5) > 0.5:
            gaps.append({
                "type": "legislative_rigidity",
                "severity": "high",
                "description": "جمود تشريعي، القوانين قديمة",
                "suggestion": "مراجعة وتحديث التشريعات",
                "indicator": "LRI"
            })
        
        self.gap_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "gaps": gaps
        })
        
        return gaps

# ============================================================
# 4. نظام الميزة التنافسية (Competitive Edge)
# ============================================================

class CompetitiveEdgeEngine:
    """تحليل الميزة التنافسية للسياسات"""
    
    @staticmethod
    def analyze(policy_text: str, indicators: Dict) -> Dict:
        """تحليل الميزة التنافسية"""
        # 1. نقاط القوة
        strengths = []
        if indicators.get("DIC", 0.5) > 0.6:
            strengths.append("تنوع معرفي عالٍ")
        if indicators.get("MCI", 0.5) > 0.5:
            strengths.append("تواضع معرفي، استعداد للتعلم")
        if indicators.get("FQI", 0.5) > 0.5:
            strengths.append("ثقافة نقدية قوية")
        
        # 2. نقاط الضعف
        weaknesses = []
        if indicators.get("ERI", 0.5) > 0.6:
            weaknesses.append("جمود معرفي")
        if indicators.get("LRI", 0.5) > 0.5:
            weaknesses.append("جمود تشريعي")
        if indicators.get("CGI", 0.5) > 0.5:
            weaknesses.append("فجوة مصداقية")
        
        # 3. الفرص
        opportunities = []
        if indicators.get("SAI", 0.5) > 0.5:
            opportunities.append("تحسين التواصل مع الجمهور")
        if indicators.get("PAI", 0.5) > 0.5:
            opportunities.append("إشراك الفئات المهمشة")
        
        # 4. التهديدات
        threats = []
        if indicators.get("AGI", 0.5) > 0.6:
            threats.append("تركيز السلطة")
        if indicators.get("ERI", 0.5) > 0.6 and indicators.get("LRI", 0.5) > 0.5:
            threats.append("خطر التخلف عن المنافسين")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "opportunities": opportunities,
            "threats": threats,
            "score": round((len(strengths) + len(opportunities)) / (len(weaknesses) + len(threats) + 1), 2)
        }

# ============================================================
# 5. نظام توليد الملاذات الآمنة (Safe Haven Generator)
# ============================================================

class SafeHavenGenerator:
    """توليد ملاذات آمنة بناءً على تحليل السياسات"""
    
    def __init__(self):
        self.safe_havens = []
    
    def generate(self, country: str, indicators: Dict, gaps: List[Dict]) -> Dict:
        """توليد ملاذات آمنة مخصصة"""
        safe_havens = {
            "recommendations": [],
            "contract_provisions": [],
            "institutional_safeguards": []
        }
        
        # 1. توصيات عامة
        if indicators.get("ERI", 0.5) > 0.6:
            safe_havens["recommendations"].append("إنشاء منطقة اقتصادية خاصة ذات أنظمة مرنة")
        if indicators.get("LRI", 0.5) > 0.5:
            safe_havens["recommendations"].append("اعتماد عقود استثمارية محصنة بالتحكيم الدولي")
        if indicators.get("CGI", 0.5) > 0.5:
            safe_havens["recommendations"].append("إنشاء صندوق ضمان لتغطية مخاطر تغيير السياسات")
        
        # 2. بنود تعاقدية
        safe_havens["contract_provisions"] = [
            {
                "title": "شرط التحكيم الدولي",
                "description": "تحديد هيئة تحكيم دولية (غرفة باريس/لندن) لحل النزاعات"
            },
            {
                "title": "بند التعويض",
                "description": "تعويض المستثمر عن أي تغييرات قانونية أو سياسية"
            },
            {
                "title": "بند التثبيت المالي",
                "description": "تثبيت سعر الصرف والحوافز الضريبية لمدة 10 سنوات"
            }
        ]
        
        # 3. ضمانات مؤسسية
        safe_havens["institutional_safeguards"] = [
            {
                "title": "نافذة واحدة للمستثمرين",
                "description": "جهة واحدة لإنجاز جميع المعاملات الحكومية"
            },
            {
                "title": "آلية فض النزاعات السريعة",
                "description": "هيئة تحكيم متخصصة تصدر قراراتها خلال 60 يوماً"
            },
            {
                "title": "صندوق الضمان الذاتي",
                "description": "صندوق يُموَّل من إيرادات المنطقة لتعويض المستثمرين"
            }
        ]
        
        self.safe_havens.append({
            "country": country,
            "timestamp": datetime.utcnow().isoformat(),
            "safe_havens": safe_havens
        })
        
        return safe_havens

# ============================================================
# 6. المحرك الرئيسي - الحوكمة المتقدمة
# ============================================================

class AdvancedGovernanceEngine:
    """
    المحرك الرئيسي المتقدم للحوكمة
    يجمع جميع المكونات مع تطبيق الموجهات والنظرية
    """
    
    def __init__(self):
        self.search_engine = UnifiedSearchEngine()
        self.gap_analyzer = GapAnalyzer()
        self.competitive_engine = CompetitiveEdgeEngine()
        self.safe_haven_generator = SafeHavenGenerator()
        self.history = []
    
    def analyze_policy(self, country: str, policy_text: str, metadata: Dict = None) -> Dict:
        """
        تحليل شامل لسياسة معينة
        """
        # 1. المؤشرات التسعة
        indicators = GovernanceIndicators.analyze(policy_text)
        
        # 2. تحليل الفجوات
        gaps = self.gap_analyzer.analyze(policy_text, indicators)
        
        # 3. الميزة التنافسية
        competitive = self.competitive_engine.analyze(policy_text, indicators)
        
        # 4. توليد الملاذات الآمنة
        safe_havens = self.safe_haven_generator.generate(country, indicators, gaps)
        
        # 5. فهرسة السياسة
        policy_id = hashlib.md5(f"{country}{policy_text[:100]}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
        self.search_engine.index_policy(policy_id, policy_text, metadata or {"country": country})
        
        result = {
            "country": country,
            "policy_id": policy_id,
            "timestamp": datetime.utcnow().isoformat(),
            "indicators": indicators,
            "gaps": gaps,
            "competitive": competitive,
            "safe_havens": safe_havens,
            "summary": self._generate_summary(indicators, gaps, competitive)
        }
        
        self.history.append(result)
        return result
    
    def _generate_summary(self, indicators: Dict, gaps: List[Dict], competitive: Dict) -> str:
        """توليد ملخص تحليلي"""
        return f"""
        📊 ملخص تحليل السياسة
        ========================================
        
        📈 المؤشرات:
        • ERI (الجمود المعرفي): {indicators.get('ERI', 0.5):.2f}
        • FQI (الأسئلة المحرمة): {indicators.get('FQI', 0.5):.2f}
        • PAI (الغياب الإجرائي): {indicators.get('PAI', 0.5):.2f}
        • CGI (فجوة المصداقية): {indicators.get('CGI', 0.5):.2f}
        • LRI (الجمود التشريعي): {indicators.get('LRI', 0.5):.2f}
        
        🔍 الفجوات المكتشفة: {len(gaps)}
        🏆 درجة التنافسية: {competitive.get('score', 0) * 100:.1f}%
        🛡️ عدد توصيات الملاذ الآمن: {len(competitive.get('safe_havens', {}).get('recommendations', []))}
        """

# ============================================================
# 7. نقاط النهاية API
# ============================================================

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v2/advanced-governance", tags=["Advanced Governance"])

_engine = None

def get_engine() -> AdvancedGovernanceEngine:
    global _engine
    if _engine is None:
        _engine = AdvancedGovernanceEngine()
    return _engine

@router.get("/health")
async def health():
    return {"status": "healthy", "module": "Advanced Governance Engine"}

@router.post("/analyze-policy")
async def analyze_policy(country: str, policy_text: str, metadata: Dict = None):
    """تحليل شامل لسياسة معينة"""
    engine = get_engine()
    return engine.analyze_policy(country, policy_text, metadata)

@router.get("/indicators")
async def get_indicators():
    """الحصول على المؤشرات التسعة"""
    return {
        "indicators": [
            {"name": "ERI", "description": "الجمود المعرفي"},
            {"name": "FQI", "description": "الأسئلة المحرمة"},
            {"name": "PAI", "description": "الغياب الإجرائي"},
            {"name": "CGI", "description": "فجوة المصداقية"},
            {"name": "AGI", "description": "فجوة الفاعلين"},
            {"name": "DIC", "description": "التنوع المعرفي"},
            {"name": "MCI", "description": "التواضع المعرفي"},
            {"name": "LRI", "description": "الجمود التشريعي"},
            {"name": "SAI", "description": "الاغتراب الدلالي"}
        ]
    }

@router.get("/safe-haven/suggestions")
async def get_safe_haven_suggestions():
    """الحصول على اقتراحات الملاذات الآمنة"""
    return {
        "suggestions": [
            "مناطق اقتصادية خاصة ذات أنظمة مرنة",
            "عقود استثمارية محصنة بالتحكيم الدولي",
            "صناديق ضمان لتغطية مخاطر تغيير السياسات",
            "نافذة واحدة للمستثمرين",
            "آلية فض النزاعات السريعة (60 يوماً)"
        ]
    }
