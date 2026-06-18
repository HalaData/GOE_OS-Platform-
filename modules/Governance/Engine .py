"""
GOE OS - Governance Engine
محرك الحوكمة المعرفية: المؤشرات، التشخيص، الأسئلة المحرمة
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

logger = logging.getLogger("GOE_OS.Governance")

class GovernanceEngine:
    """
    محرك الحوكمة - مسؤول عن التحليل والتشخيص المعرفي
    """
    
    def __init__(self):
        self.indicators = self._load_indicators()
        self.analysis_history = []
        self.consent_log = {}
        logger.info(f"✅ Governance Engine initialized with {len(self.indicators)} indicators")
    
    def _load_indicators(self) -> Dict:
        """تحميل المؤشرات من ملفات YAML"""
        indicators = {}
        indicator_dir = Path("indicators/definitions")
        
        if not indicator_dir.exists():
            logger.warning(f"Indicator directory not found: {indicator_dir}")
            return self._default_indicators()
        
        for file in indicator_dir.glob("*.yaml"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and data.get('id'):
                        indicators[data['id']] = data
            except Exception as e:
                logger.error(f"Error loading {file}: {e}")
        
        return indicators or self._default_indicators()
    
    def _default_indicators(self) -> Dict:
        """المؤشرات الافتراضية"""
        return {
            "PAI": {
                "id": "PAI",
                "name": "Procedural Absence Index",
                "question": "Who has not yet been invited to this table?",
                "forbidden_question": "When does our zeal to invite become a veto?",
                "threshold": 0.7,
                "measurement_class": "mathematical",
                "formula": "PAI",
                "keywords": ["invited", "participated", "consulted", "transparency"],
                "ecc": 1.0
            },
            "CGI": {
                "id": "CGI",
                "name": "Credibility Gap Index",
                "question": "How many promises have we made, and how many have we kept?",
                "forbidden_question": "What promise are we afraid to admit we broke?",
                "threshold": 0.7,
                "measurement_class": "semi_mathematical",
                "keywords": ["promise", "commitment", "deliver", "pledge"],
                "weights": {"promise": 1.0, "commitment": 1.0, "deliver": -0.5},
                "ecc": 0.7
            },
            "ERI": {
                "id": "ERI",
                "name": "Epistemic Rigidity Index",
                "question": "Is our certainty our prison?",
                "forbidden_question": "What if the opposite is true?",
                "threshold": 0.65,
                "measurement_class": "mathematical",
                "formula": "ERI",
                "keywords": ["certainly", "undoubtedly", "absolutely", "definitely"],
                "ecc": 0.95
            }
        }
    
    def analyze(self, data: Dict) -> Dict:
        """
        تحليل نص أو بيانات باستخدام المؤشرات
        """
        text = data.get("text", "")
        domain = data.get("domain", "general")
        consent = data.get("consent_given", False)
        depth = data.get("depth", "standard")
        
        if not consent:
            return {
                "status": "consent_required",
                "message": "الموافقة مطلوبة قبل التشخيص",
                "consent_request": self._generate_consent_request(domain)
            }
        
        if not text:
            return {"status": "error", "message": "لا يوجد نص للتحليل"}
        
        # تطبيق المؤشرات
        results = {}
        for indicator_id, indicator in self.indicators.items():
            score = self._apply_indicator(indicator, text)
            if score is not None:
                results[indicator_id] = {
                    "score": score,
                    "name": indicator.get("name", indicator_id),
                    "threshold": indicator.get("threshold", 0.7),
                    "question": indicator.get("question", "")
                }
        
        # حساب درجة اليقظة
        vigilance_score = self._calculate_vigilance(results)
        
        # توليد أسئلة محرمة
        forbidden_questions = self._generate_forbidden_questions(results)
        
        # كشف المسلمات
        dogmas = self._detect_dogmas(text)
        
        result = {
            "status": "success",
            "domain": domain,
            "depth": depth,
            "vigilance_score": vigilance_score,
            "indicators": results,
            "forbidden_questions": forbidden_questions,
            "dogmas": dogmas,
            "text_length": len(text),
            "timestamp": datetime.now().isoformat()
        }
        
        self.analysis_history.append(result)
        return result
    
    def _apply_indicator(self, indicator: Dict, text: str) -> Optional[float]:
        """تطبيق مؤشر على النص"""
        indicator_type = indicator.get("measurement_class", "mathematical")
        text_lower = text.lower()
        
        if indicator_type == "mathematical":
            formula = indicator.get("formula")
            
            if formula == "PAI":
                keywords = indicator.get("keywords", [])
                found = sum(1 for k in keywords if k in text_lower)
                total = len(keywords)
                return 1 - (found / total) if total > 0 else 1.0
            
            elif formula == "LRI":
                amendments = text_lower.count("amend") + text_lower.count("review")
                return 1 / (amendments + 1) if amendments > 0 else 1.0
            
            elif formula == "ERI":
                certainty = sum(text_lower.count(w) for w in ["certainly", "undoubtedly", "absolutely", "definitely"])
                doubt = sum(text_lower.count(w) for w in ["perhaps", "maybe", "possibly", "uncertain"])
                return certainty / (certainty + doubt + 0.01) if (certainty + doubt) > 0 else 0.5
        
        elif indicator_type == "semi_mathematical":
            keywords = indicator.get("keywords", [])
            weights = indicator.get("weights", {})
            
            if not keywords:
                return None
            
            total_weight = sum(weights.values()) or 1
            score = 0
            for k in keywords:
                weight = weights.get(k, 1.0)
                count = text_lower.count(k)
                score += count * weight
            
            return min(1.0, score / (total_weight * 10))
        
        return None
    
    def _calculate_vigilance(self, results: Dict) -> float:
        """حساب درجة اليقظة من نتائج المؤشرات"""
        scores = [r["score"] for r in results.values() if r.get("score") is not None]
        if not scores:
            return 0.0
        return round(sum(scores) / len(scores) * 100, 1)
    
    def _generate_forbidden_questions(self, results: Dict) -> List[str]:
        """توليد أسئلة محرمة بناءً على النتائج"""
        questions = []
        
        for indicator_id, result in results.items():
            if result.get("score", 0) > result.get("threshold", 0.7):
                questions.append(result.get("question", f"ما هو السؤال المحرم لـ {indicator_id}؟"))
        
        # إضافة أسئلة عامة
        if not questions:
            questions = ["ما هو السؤال الذي يخاف النظام طرحه على نفسه؟"]
        
        return questions[:3]
    
    def _detect_dogmas(self, text: str) -> List[Dict]:
        """كشف المسلمات في النص"""
        dogmas = []
        markers = ["it is well known", "there is no doubt", "obviously", "certainly", "must be", "always", "never"]
        
        sentences = re.split(r'[.!?]\s+', text)
        for sent in sentences:
            sent_lower = sent.lower()
            for marker in markers:
                if marker in sent_lower:
                    dogmas.append({
                        "sentence": sent.strip()[:200],
                        "marker": marker,
                        "confidence": 0.8
                    })
                    break
        
        return dogmas[:5]
    
    def _generate_consent_request(self, domain: str) -> str:
        """توليد طلب موافقة"""
        return f"""
        You are about to diagnose a system in the {domain} domain.
        This diagnosis is not neutral; it is an intervention that may alter the system.
        Do you consent to proceed? (Set consent_given: true)
        """
    
    def create_indicator(self, data: Dict) -> Dict:
        """إنشاء مؤشر جديد"""
        indicator = {
            "id": data.get("id", f"IND_{datetime.now().timestamp()}"),
            "name": data.get("name", "مؤشر جديد"),
            "question": data.get("question", "ما هو السؤال الذي يجيب عليه هذا المؤشر؟"),
            "forbidden_question": data.get("forbidden_question", "ما هو السؤال المحرم لهذا المؤشر؟"),
            "threshold": data.get("threshold", 0.7),
            "measurement_class": data.get("measurement_class", "semi_mathematical"),
            "keywords": data.get("keywords", []),
            "weights": data.get("weights", {}),
            "ecc": data.get("ecc", 0.7)
        }
        
        self.indicators[indicator["id"]] = indicator
        return {"status": "created", "indicator": indicator}
    
    def get_indicators(self) -> Dict:
        """جميع المؤشرات"""
        return self.indicators
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """سجل التحليلات السابقة"""
        return self.analysis_history[-limit:]
