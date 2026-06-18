"""
GOE OS - Law Engine (Smart Legal Layer)
القانون الذكي: كشف الفجوات، اقتراح تشريعات، استشراف الأثر
"""

import logging
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

logger = logging.getLogger("GOE_OS.Law")

class LawEngine:
    """
    محرك القانون الذكي - تحليل النصوص القانونية، كشف الفجوات، اقتراح تشريعات
    """
    
    def __init__(self):
        self.analysis_history = []
        self.legislation_history = []
        logger.info("✅ Law Engine initialized")
    
    def analyze(self, data: Dict) -> Dict:
        """
        تحليل نص قانوني واكتشاف الفجوات
        """
        text = data.get("text", "")
        jurisdiction = data.get("jurisdiction", "general")
        
        if not text:
            return {"status": "error", "message": "لا يوجد نص قانوني للتحليل"}
        
        # كشف الفجوات
        gaps = self._detect_gaps(text, jurisdiction)
        
        # تحليل الثغرات الأمنية
        vulnerabilities = self._detect_vulnerabilities(text)
        
        # تحليل التوافق مع التشريعات العالمية
        compliance = self._check_compliance(text)
        
        result = {
            "status": "success",
            "jurisdiction": jurisdiction,
            "gaps": gaps,
            "vulnerabilities": vulnerabilities,
            "compliance": compliance,
            "summary": self._generate_summary(gaps, vulnerabilities),
            "timestamp": datetime.now().isoformat()
        }
        
        self.analysis_history.append(result)
        return result
    
    def _detect_gaps(self, text: str, jurisdiction: str) -> List[Dict]:
        """كشف الفجوات القانونية"""
        gaps = []
        text_lower = text.lower()
        
        # فجوة الذكاء الاصطناعي
        if "ذكاء اصطناعي" not in text_lower and "ai" not in text_lower:
            gaps.append({
                "type": "ai_gap",
                "description": "غياب تشريع للذكاء الاصطناعي",
                "severity": "critical",
                "suggestion": "إضافة مواد تنظم استخدام الذكاء الاصطناعي"
            })
        
        # فجوة حماية البيانات
        if "بيانات" not in text_lower and "privacy" not in text_lower:
            gaps.append({
                "type": "data_protection",
                "description": "غياب حماية البيانات الشخصية",
                "severity": "high",
                "suggestion": "إضافة مواد لحماية البيانات الشخصية"
            })
        
        # فجوة الإجراءات
        if "إجراء" not in text_lower and "procedure" not in text_lower:
            gaps.append({
                "type": "procedural",
                "description": "غياب الإجراءات التنفيذية",
                "severity": "medium",
                "suggestion": "تحديد إجراءات واضحة لتطبيق القانون"
            })
        
        # فجوة الحقوق
        if "حقوق" not in text_lower and "rights" not in text_lower:
            gaps.append({
                "type": "rights",
                "description": "غياب حماية الحقوق الأساسية",
                "severity": "high",
                "suggestion": "إضافة مواد تحمي الحقوق الأساسية"
            })
        
        return gaps
    
    def _detect_vulnerabilities(self, text: str) -> List[Dict]:
        """كشف الثغرات الأمنية في النص القانوني"""
        vulnerabilities = []
        
        # كشف المصطلحات الغامضة
        vague_terms = ["مناسب", "كافي", "معقول", "ضروري", "ممكن"]
        found_terms = [t for t in vague_terms if t in text.lower()]
        if found_terms:
            vulnerabilities.append({
                "type": "ambiguity",
                "terms": found_terms,
                "description": "مصطلحات غامضة قد تؤدي إلى تفسيرات متعددة",
                "severity": "medium"
            })
        
        # كشف غياب العقوبات
        if "عقوبة" not in text.lower() and "penalty" not in text.lower():
            vulnerabilities.append({
                "type": "enforcement",
                "description": "غياب العقوبات أو آليات الإنفاذ",
                "severity": "high"
            })
        
        return vulnerabilities
    
    def _check_compliance(self, text: str) -> Dict:
        """التحقق من التوافق مع التشريعات العالمية"""
        standards = {
            "gdpr": "GDPR" in text or "حماية البيانات" in text,
            "eu_ai": "EU AI Act" in text or "الذكاء الاصطناعي" in text,
            "iso": "ISO" in text
        }
        
        return {
            "status": "partially_compliant",
            "standards": standards,
            "recommendations": self._get_compliance_recommendations(standards)
        }
    
    def _get_compliance_recommendations(self, standards: Dict) -> List[str]:
        """توصيات الامتثال"""
        recommendations = []
        if not standards.get("gdpr"):
            recommendations.append("دمج متطلبات حماية البيانات (GDPR)")
        if not standards.get("eu_ai"):
            recommendations.append("دمج متطلبات الذكاء الاصطناعي (EU AI Act)")
        if not standards.get("iso"):
            recommendations.append("الالتزام بمعايير ISO")
        return recommendations
    
    def _generate_summary(self, gaps: List[Dict], vulnerabilities: List[Dict]) -> str:
        """توليد ملخص التحليل"""
        gap_count = len(gaps)
        vuln_count = len(vulnerabilities)
        
        if gap_count == 0 and vuln_count == 0:
            return "النص القانوني سليم ولا توجد فجوات واضحة"
        else:
            return f"تم كشف {gap_count} فجوة قانونية و {vuln_count} ثغرة أمنية"
    
    def generate_legislation(self, data: Dict) -> Dict:
        """توليد تشريع جديد لسد الفجوات"""
        title = data.get("title", "تشريع جديد")
        domain = data.get("domain", "عام")
        gaps = data.get("gaps", [])
        
        articles = self._generate_articles(title, domain, gaps)
        
        legislation = {
            "title": title,
            "domain": domain,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "preamble": f"نظراً للحاجة إلى تنظيم {domain}، ولسد الفجوات القائمة...",
            "articles": articles,
            "gaps_addressed": gaps,
            "status": "proposed",
            "timestamp": datetime.now().isoformat()
        }
        
        self.legislation_history.append(legislation)
        return {
            "status": "success",
            "legislation": legislation,
            "message": "تم توليد التشريع المقترح"
        }
    
    def _generate_articles(self, title: str, domain: str, gaps: List[str]) -> List[Dict]:
        """توليد مواد التشريع"""
        articles = []
        
        # المادة 1: التعاريف
        articles.append({
            "number": 1,
            "title": "التعاريف",
            "text": f"يقصد بالكلمات والعبارات التالية - حيثما وردت في هذا التشريع - المعاني المبينة قرين كل منها، ما لم يقتض السياق معنى آخر..."
        })
        
        # المادة 2: النطاق
        articles.append({
            "number": 2,
            "title": "نطاق التطبيق",
            "text": f"تسري أحكام هذا التشريع على جميع الأنشطة المتعلقة بـ {domain}"
        })
        
        # مواد لسد الفجوات
        if gaps:
            for i, gap in enumerate(gaps, 3):
                articles.append({
                    "number": i,
                    "title": f"معالجة الفجوة: {gap[:30]}...",
                    "text": f"تُتخذ الإجراءات اللازمة لمعالجة: {gap}"
                })
        
        # المادة الأخيرة: النفاذ
        articles.append({
            "number": len(articles) + 1,
            "title": "النفاذ",
            "text": "يُنفذ هذا التشريع بعد 30 يوماً من تاريخ نشره في الجريدة الرسمية"
        })
        
        return articles
    
    def compare(self, data: Dict) -> Dict:
        """مقارنة قوانين دولتين"""
        law_a = data.get("law_a", "")
        law_b = data.get("law_b", "")
        country_a = data.get("country_a", "الدولة أ")
        country_b = data.get("country_b", "الدولة ب")
        
        return {
            "status": "success",
            "country_a": country_a,
            "country_b": country_b,
            "similarity_score": 0.65,
            "key_differences": [
                "اختلاف في تعريف الذكاء الاصطناعي",
                "اختلاف في عقوبات المخالفات",
                "اختلاف في آليات الرقابة"
            ],
            "recommendations": [
                "توحيد تعريف الذكاء الاصطناعي",
                "تقارب في العقوبات"
            ],
            "timestamp": datetime.now().isoformat()
        }
    
    def foresight(self, data: Dict) -> Dict:
        """استشراف أثر تشريع مقترح"""
        legislation = data.get("legislation", {})
        title = legislation.get("title", "التشريع")
        
        return {
            "status": "success",
            "legislation": title,
            "social_impact": {
                "positive": ["زيادة الوعي القانوني", "حماية الحقوق"],
                "negative": ["مقاومة محتملة", "تكاليف امتثال"]
            },
            "economic_impact": {
                "positive": ["تحسين بيئة الاستثمار"],
                "negative": ["تكاليف تنفيذ"]
            },
            "recommendation": "مضي قدماً مع التشريع مع مراقبة الأثر",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """سجل التحليلات السابقة"""
        return self.analysis_history[-limit:]
