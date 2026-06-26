"""
البوصلة الأخلاقية الزمنية - Temporal Ethical Compass v3.0
تجمع: الذاكرة الأخلاقية، الاستشراف الأخلاقي، والتطور الزمني
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import hashlib
import json
import logging
import random
from collections import defaultdict
import numpy as np

logger = logging.getLogger(__name__)

# ============================================================
# 1. الذاكرة الأخلاقية (Ethical Memory)
# ============================================================

class EthicalMemory:
    """
    تسجل القرارات الأخلاقية عبر الزمن وتحلل الأنماط المتكررة.
    """
    
    def __init__(self):
        self.records: List[Dict] = []
        self.patterns: Dict[str, List[Dict]] = defaultdict(list)
        self.decision_timeline: Dict[str, List[Dict]] = defaultdict(list)
    
    def record_decision(self, decision: Dict, outcome: Dict, timestamp: str = None) -> None:
        """
        تسجيل قرار أخلاقي ونتيجته.
        """
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat()
        
        record = {
            "decision": decision,
            "outcome": outcome,
            "timestamp": timestamp,
            "ethical_score": decision.get("ethical_score", 0.5),
            "context": decision.get("context", {})
        }
        self.records.append(record)
        
        # تجميع حسب نوع القرار
        decision_type = decision.get("type", "unknown")
        self.decision_timeline[decision_type].append(record)
        
        # تحديث الأنماط
        self._update_patterns(record)
        
        logger.info(f"📝 Ethical decision recorded: {decision.get('id', 'unknown')}")
    
    def _update_patterns(self, record: Dict) -> None:
        """تحديد الأنماط المتكررة في القرارات الأخلاقية."""
        # محاكاة: في الإنتاج سيتم تحليل أعمق
        pattern_key = f"{record['decision'].get('type', 'unknown')}_{record['outcome'].get('status', 'unknown')}"
        self.patterns[pattern_key].append(record)
    
    def get_patterns(self, min_occurrences: int = 3) -> Dict[str, List[Dict]]:
        """استرجاع الأنماط المتكررة."""
        return {
            pattern: records for pattern, records in self.patterns.items()
            if len(records) >= min_occurrences
        }
    
    def get_recent_decisions(self, days: int = 30) -> List[Dict]:
        """استرجاع القرارات الأخلاقية خلال الأيام الماضية."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        return [r for r in self.records if datetime.fromisoformat(r["timestamp"]) > cutoff]
    
    def get_decision_timeline(self, decision_type: str = None) -> Dict[str, List[Dict]]:
        """استرجاع الجدول الزمني للقرارات."""
        if decision_type:
            return {decision_type: self.decision_timeline.get(decision_type, [])}
        return self.decision_timeline

# ============================================================
# 2. الاستشراف الأخلاقي (Ethical Foresight)
# ============================================================

class EthicalForesight:
    """
    محاكاة الأثر الأخلاقي للقرارات على المدى البعيد.
    """
    
    def __init__(self, memory: EthicalMemory):
        self.memory = memory
        self.scenario_history: List[Dict] = []
    
    def forecast_impact(self, decision: Dict, horizons: List[int] = [1, 3, 5]) -> Dict:
        """
        محاكاة الأثر الأخلاقي للقرار على مدى 1، 3، 5 سنوات.
        """
        scenarios = {}
        
        for years in horizons:
            scenario = self._simulate_scenario(decision, years)
            scenarios[f"{years}_years"] = scenario
        
        # حساب درجة الاستدامة الأخلاقية
        sustainability_score = self._calculate_sustainability(scenarios)
        
        result = {
            "decision_id": decision.get("id", "unknown"),
            "scenarios": scenarios,
            "sustainability_score": round(sustainability_score, 3),
            "recommendation": self._get_foresight_recommendation(sustainability_score),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.scenario_history.append(result)
        return result
    
    def _simulate_scenario(self, decision: Dict, years: int) -> Dict:
        """محاكاة سيناريو أخلاقي واحد."""
        # محاكاة: في الإنتاج سيتم استخدام نماذج تنبؤية أكثر تعقيدًا
        base_ethical_score = decision.get("ethical_score", 0.5)
        
        # تأثير الزمن: القرارات الأخلاقية العالية تتحسن مع الزمن، والمنخفضة تتدهور
        if base_ethical_score > 0.7:
            projected_score = min(1.0, base_ethical_score + (years * 0.05))
        elif base_ethical_score > 0.4:
            projected_score = base_ethical_score + (years * 0.01)
        else:
            projected_score = max(0.0, base_ethical_score - (years * 0.05))
        
        return {
            "years": years,
            "projected_ethical_score": round(projected_score, 3),
            "status": "sustainable" if projected_score > 0.6 else "declining" if projected_score > 0.3 else "critical",
            "risks": self._identify_risks(decision, years),
            "opportunities": self._identify_opportunities(decision, years)
        }
    
    def _identify_risks(self, decision: Dict, years: int) -> List[str]:
        """تحديد المخاطر الأخلاقية طويلة المدى."""
        risks = []
        if decision.get("ethical_score", 0.5) < 0.5:
            risks.append("خطر تآكل المبادئ الأخلاقية مع مرور الزمن")
        if years > 3:
            risks.append("خطر عدم قدرة القرار على التكيف مع المتغيرات الأخلاقية المستقبلية")
        return risks
    
    def _identify_opportunities(self, decision: Dict, years: int) -> List[str]:
        """تحديد الفرص الأخلاقية طويلة المدى."""
        opportunities = []
        if decision.get("ethical_score", 0.5) > 0.7:
            opportunities.append("فرصة لتعزيز المبادئ الأخلاقية في النظام البيئي الأوسع")
        if years > 3:
            opportunities.append("فرصة لأن يصبح القرار نموذجًا أخلاقيًا يُحتذى به")
        return opportunities
    
    def _calculate_sustainability(self, scenarios: Dict) -> float:
        """حساب درجة الاستدامة الأخلاقية."""
        scores = [s["projected_ethical_score"] for s in scenarios.values()]
        return sum(scores) / len(scores) if scores else 0.5
    
    def _get_foresight_recommendation(self, sustainability: float) -> str:
        """توصية بناءً على درجة الاستدامة الأخلاقية."""
        if sustainability > 0.7:
            return "✅ القرار أخلاقيًا مستدام على المدى الطويل"
        elif sustainability > 0.4:
            return "🟡 القرار يحتاج إلى مراجعة لتعزيز استدامته الأخلاقية"
        else:
            return "🔴 القرار غير مستدام أخلاقيًا على المدى الطويل"

# ============================================================
# 3. التطور الزمني (Temporal Evolution)
# ============================================================

class TemporalEvolution:
    """
    تتغير المبادئ الأخلاقية بمرور الزمن بناءً على التعلم التاريخي.
    """
    
    def __init__(self, memory: EthicalMemory, foresight: EthicalForesight):
        self.memory = memory
        self.foresight = foresight
        self.evolution_history: List[Dict] = []
        self.ethical_trends: Dict[str, float] = {}
    
    def evolve_principles(self, principles: List[Dict]) -> List[Dict]:
        """
        تطور المبادئ الأخلاقية بناءً على التاريخ والاستشراف.
        """
        evolved_principles = []
        
        for principle in principles:
            # 1. استرجاع تاريخ المبدأ
            history = self._get_principle_history(principle["id"])
            
            # 2. تحليل الاتجاهات
            trend = self._analyze_trend(history)
            
            # 3. تطبيق التطور
            evolved = self._apply_evolution(principle, history, trend)
            evolved_principles.append(evolved)
            
            # 4. تسجيل التطور
            self.evolution_history.append({
                "principle_id": principle["id"],
                "old_weight": principle.get("weight", 0.5),
                "new_weight": evolved["weight"],
                "trend": trend,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        return evolved_principles
    
    def _get_principle_history(self, principle_id: str) -> List[Dict]:
        """استرجاع تاريخ مبدأ معين."""
        # محاكاة: في الإنتاج سيتم استرجاعها من قاعدة البيانات
        return [
            {"timestamp": (datetime.utcnow() - timedelta(days=30)).isoformat(), "weight": 0.5},
            {"timestamp": (datetime.utcnow() - timedelta(days=20)).isoformat(), "weight": 0.6},
            {"timestamp": (datetime.utcnow() - timedelta(days=10)).isoformat(), "weight": 0.7}
        ]
    
    def _analyze_trend(self, history: List[Dict]) -> str:
        """تحليل اتجاه المبدأ عبر الزمن."""
        if len(history) < 2:
            return "stable"
        
        weights = [h["weight"] for h in history]
        if weights[-1] > weights[0]:
            return "increasing"
        elif weights[-1] < weights[0]:
            return "decreasing"
        else:
            return "stable"
    
    def _apply_evolution(self, principle: Dict, history: List[Dict], trend: str) -> Dict:
        """تطبيق التطور على المبدأ."""
        evolved = principle.copy()
        current_weight = principle.get("weight", 0.5)
        
        if trend == "increasing":
            evolved["weight"] = min(1.0, current_weight + 0.05)
        elif trend == "decreasing":
            evolved["weight"] = max(0.1, current_weight - 0.05)
        else:
            # إذا كان مستقرًا، نحافظ على الوزن
            evolved["weight"] = current_weight
        
        evolved["last_evolved"] = datetime.utcnow().isoformat()
        evolved["evolution_reason"] = f"تطور بناءً على اتجاه {trend} في التاريخ الأخلاقي"
        
        return evolved
    
    def get_ethical_trends(self) -> Dict[str, float]:
        """الحصول على الاتجاهات الأخلاقية العامة."""
        # محاكاة: تحليل اتجاهات المبادئ
        return {
            "social_justice": 0.8,
            "compassion": 0.7,
            "responsibility": 0.6,
            "truth": 0.9,
            "dignity": 0.8
        }

# ============================================================
# 4. المحرك الأخلاقي الزمني (Temporal Ethical Compass)
# ============================================================

class TemporalEthicalCompass:
    """
    البوصلة الأخلاقية الزمنية - تجمع الذاكرة، الاستشراف، والتطور الزمني.
    """
    
    def __init__(self, name: str = "GOE OS"):
        self.name = name
        self.id = hashlib.md5(name.encode()).hexdigest()[:16]
        self.created_at = datetime.utcnow().isoformat()
        
        # المكونات الثلاثة
        self.memory = EthicalMemory()
        self.foresight = EthicalForesight(self.memory)
        self.evolution = TemporalEvolution(self.memory, self.foresight)
        
        # المبادئ الحالية
        self.current_principles = self._initialize_principles()
        
        logger.info("🧭 Temporal Ethical Compass v3.0 initialized")
    
    def _initialize_principles(self) -> List[Dict]:
        """تهيئة المبادئ الأولية."""
        return [
            {"id": "justice", "name": "العدالة", "weight": 0.8, "category": "social"},
            {"id": "mercy", "name": "الرحمة", "weight": 0.7, "category": "compassion"},
            {"id": "responsibility", "name": "المسؤولية", "weight": 0.85, "category": "responsibility"},
            {"id": "truth", "name": "الصدق", "weight": 0.9, "category": "truth"},
            {"id": "dignity", "name": "الكرامة", "weight": 0.8, "category": "dignity"}
        ]
    
    def evaluate_decision(self, decision: Dict) -> Dict:
        """
        تقييم قرار باستخدام الأبعاد الزمنية الثلاثة.
        """
        # 1. تسجيل القرار في الذاكرة
        self.memory.record_decision(decision, {"status": "evaluated"})
        
        # 2. الاستشراف الأخلاقي
        foresight_result = self.foresight.forecast_impact(decision)
        
        # 3. تقييم الحاضر
        present_score = self._evaluate_present(decision)
        
        # 4. الدمج: الحاضر + الاستشراف
        combined_score = (present_score * 0.5) + (foresight_result["sustainability_score"] * 0.5)
        
        # 5. تطور المبادئ (التعلم التاريخي)
        self.current_principles = self.evolution.evolve_principles(self.current_principles)
        
        return {
            "decision_id": decision.get("id", "unknown"),
            "present_ethical_score": round(present_score, 3),
            "foresight_score": foresight_result,
            "combined_ethical_score": round(combined_score, 3),
            "status": "approved" if combined_score > 0.7 else "review_required" if combined_score > 0.4 else "rejected",
            "principles_used": self.current_principles,
            "trends": self.evolution.get_ethical_trends(),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _evaluate_present(self, decision: Dict) -> float:
        """تقييم القرار في الحاضر (محاكاة)."""
        # محاكاة: في الإنتاج سيتم تقييم أعمق
        base_score = 0.5
        if "justice" in str(decision).lower():
            base_score += 0.2
        if "truth" in str(decision).lower():
            base_score += 0.2
        return min(1.0, base_score)
    
    def get_ethical_status(self) -> Dict:
        """الحالة الأخلاقية الكاملة للمنصة."""
        return {
            "name": self.name,
            "id": self.id,
            "created_at": self.created_at,
            "total_decisions": len(self.memory.records),
            "patterns": self.memory.get_patterns(),
            "current_principles": self.current_principles,
            "trends": self.evolution.get_ethical_trends(),
            "recent_decisions": self.memory.get_recent_decisions(days=7)
        }

# ============================================================
# 5. نقاط النهاية API
# ============================================================

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v2/temporal-ethical-compass", tags=["Temporal Ethical Compass"])

_engine = None

def get_engine() -> TemporalEthicalCompass:
    global _engine
    if _engine is None:
        _engine = TemporalEthicalCompass("GOE OS")
    return _engine

@router.post("/evaluate")
async def evaluate_decision(decision: Dict):
    """تقييم قرار باستخدام الأبعاد الزمنية الثلاثة."""
    engine = get_engine()
    return engine.evaluate_decision(decision)

@router.get("/memory")
async def get_ethical_memory(decision_type: str = None, days: int = 30):
    """الحصول على الذاكرة الأخلاقية."""
    engine = get_engine()
    if decision_type:
        timeline = engine.memory.get_decision_timeline(decision_type)
    else:
        timeline = engine.memory.get_decision_timeline()
    return {
        "recent": engine.memory.get_recent_decisions(days),
        "timeline": timeline,
        "patterns": engine.memory.get_patterns()
    }

@router.get("/foresight/history")
async def get_foresight_history(limit: int = 10):
    """سجل الاستشراف الأخلاقي."""
    engine = get_engine()
    return {"history": engine.foresight.scenario_history[-limit:]}

@router.get("/principles")
async def get_principles():
    """الحصول على المبادئ الأخلاقية الحالية مع تاريخ تطورها."""
    engine = get_engine()
    return {
        "current_principles": engine.current_principles,
        "evolution_history": engine.evolution.evolution_history[-10:]
    }

@router.get("/trends")
async def get_ethical_trends():
    """الاتجاهات الأخلاقية العامة."""
    engine = get_engine()
    return {"trends": engine.evolution.get_ethical_trends()}

@router.get("/status")
async def get_ethical_status():
    """الحالة الأخلاقية الكاملة."""
    engine = get_engine()
    return engine.get_ethical_status()
