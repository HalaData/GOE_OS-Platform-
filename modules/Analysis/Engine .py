"""
GOE OS - Analysis Engine
محرك التحليل العميق: كشف المسلمات، الأنماط، الفجوات
"""

import logging
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger("GOE_OS.Analysis")

class AnalysisEngine:
    """
    محرك التحليل العميق - كشف المسلمات والفجوات والأنماط
    """
    
    def __init__(self):
        self.patterns = self._init_patterns()
        self.analysis_history = []
        logger.info("✅ Analysis Engine initialized")
    
    def _init_patterns(self) -> Dict:
        """تهيئة أنماط التحليل"""
        return {
            "dogma": {
                "name": "المسلمات",
                "markers": ["it is well known", "there is no doubt", "obviously", "certainly", "must be", "always", "never"],
                "weight": 1.0
            },
            "silence": {
                "name": "الصمت",
                "markers": ["not mentioned", "avoid", "ignore", "overlook", "absent", "silent"],
                "weight": 0.8
            },
            "contradiction": {
                "name": "التناقض",
                "markers": ["but", "however", "although", "despite", "yet", "nevertheless"],
                "weight": 0.6
            },
            "certainty": {
                "name": "اليقين المفرط",
                "markers": ["absolutely", "undoubtedly", "no doubt", "certainly", "definitely", "without question"],
                "weight": 0.7
            }
        }
    
    def analyze(self, data: Dict) -> Dict:
        """
        تحليل عميق للنص
        """
        text = data.get("text", "")
        depth = data.get("depth", "standard")
        analyst_position = data.get("analyst_position", None)
        
        if not text:
            return {"status": "error", "message": "لا يوجد نص للتحليل"}
        
        # كشف الأنماط
        findings = self._detect_patterns(text)
        
        # كشف المسلمات
        dogmas = self._extract_dogmas(text)
        
        # تحليل العمق
        depth_analysis = self._analyze_depth(text, depth)
        
        # توليد أسئلة محرمة
        forbidden_questions = self._generate_questions(text, findings)
        
        result = {
            "status": "success",
            "depth": depth,
            "analyst_position": analyst_position,
            "text_length": len(text),
            "findings": findings,
            "dogmas": dogmas,
            "depth_analysis": depth_analysis,
            "forbidden_questions": forbidden_questions,
            "ail": "This analysis reveals limits of current knowledge, not new certainty.",
            "timestamp": datetime.now().isoformat()
        }
        
        self.analysis_history.append(result)
        return result
    
    def _detect_patterns(self, text: str) -> List[Dict]:
        """كشف الأنماط في النص"""
        findings = []
        text_lower = text.lower()
        
        for pattern_id, pattern in self.patterns.items():
            count = 0
            for marker in pattern["markers"]:
                count += text_lower.count(marker)
            
            if count > 0:
                severity = "high" if count > 5 else "medium" if count > 2 else "low"
                findings.append({
                    "pattern": pattern["name"],
                    "count": count,
                    "severity": severity,
                    "markers_found": [m for m in pattern["markers"] if m in text_lower][:3]
                })
        
        return findings
    
    def _extract_dogmas(self, text: str) -> List[Dict]:
        """استخراج المسلمات من النص"""
        dogmas = []
        sentences = re.split(r'[.!?]\s+', text)
        markers = self.patterns["dogma"]["markers"]
        
        for sent in sentences:
            sent_lower = sent.lower()
            for marker in markers:
                if marker in sent_lower:
                    dogmas.append({
                        "sentence": sent.strip()[:200],
                        "marker": marker,
                        "confidence": 0.8,
                        "forbidden_question": f"What if the opposite of '{sent.strip()[:100]}...' were true?"
                    })
                    break
        
        return dogmas[:5]
    
    def _analyze_depth(self, text: str, depth: str) -> Dict:
        """تحليل عمق النص"""
        if depth == "mini":
            return {
                "level": "سريع",
                "scan": len(text) // 10,
                "description": "مسح سريع للنص"
            }
        elif depth == "deep":
            return {
                "level": "عميق",
                "patterns_analyzed": len(self.patterns),
                "contexts": 5,
                "description": "تحليل عميق متعدد الأبعاد"
            }
        else:  # standard
            return {
                "level": "قياسي",
                "analysis_points": len(text) // 50,
                "description": "تحليل قياسي متوازن"
            }
    
    def _generate_questions(self, text: str, findings: List[Dict]) -> List[str]:
        """توليد أسئلة محرمة بناءً على النتائج"""
        questions = []
        
        for finding in findings:
            if finding["severity"] in ["high", "medium"]:
                questions.append(f"ما هو السؤال المحرم الذي يكشفه نمط '{finding['pattern']}'؟")
        
        if not questions:
            questions = ["ما هو السؤال الذي يخاف هذا النص طرحه على نفسه؟"]
        
        return questions[:3]
    
    def extract_dogmas(self, data: Dict) -> Dict:
        """استخراج المسلمات فقط"""
        text = data.get("text", "")
        if not text:
            return {"status": "error", "message": "لا يوجد نص"}
        
        dogmas = self._extract_dogmas(text)
        return {
            "status": "success",
            "dogmas": dogmas,
            "count": len(dogmas)
        }
    
    def get_history(self, limit: int = 10) -> List[Dict]:
        """سجل التحليلات السابقة"""
        return self.analysis_history[-limit:]
