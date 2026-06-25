"""
المحرك الأخلاقي السيبرنطيقى المتقدم - GOE OS Advanced Ethical Engine
يجمع بين: الاستباقية، التشاركية، السياقية، والتطورية
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import logging
import hashlib
import random
import requests
from collections import defaultdict
import re

logger = logging.getLogger(__name__)

# ============================================================
# 1. البعد الاستباقي: نظام الإنذار المبكر الأخلاقي (Proactive Ethics)
# ============================================================

class ProactiveEthics:
    """
    يمنع الانتهاكات الأخلاقية قبل حدوثها باستخدام التنبؤ والتحليل الاستباقي
    """
    
    def __init__(self):
        self.prediction_models = {}
        self.risk_history = []
    
    def predict_risk(self, action: Dict) -> Dict:
        """
        توقع المخاطر الأخلاقية للفعل قبل تنفيذه
        """
        risk_score = self._calculate_risk_score(action)
        
        # تحديد مستوى الخطر
        if risk_score > 0.8:
            risk_level = "critical"
            recommendation = "⛔ ممنوع: هذا الفعل ينتهك المبادئ الأخلاقية الأساسية"
        elif risk_score > 0.6:
            risk_level = "high"
            recommendation = "⚠️ خطر مرتفع: يوصى بمراجعة الفعل وتعديله"
        elif risk_score > 0.4:
            risk_level = "medium"
            recommendation = "🟡 خطر متوسط: يُنصح بالحذر ومراقبة النتائج"
        else:
            risk_level = "low"
            recommendation = "✅ آمن: الفعل يتوافق مع المبادئ الأخلاقية"
        
        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "recommendation": recommendation,
            "preventive_actions": self._get_preventive_actions(risk_score),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _calculate_risk_score(self, action: Dict) -> float:
        """
        حساب درجة المخاطر بناءً على عدة عوامل
        """
        score = 0.0
        
        # 1. عامل البيانات الحساسة
        sensitive_keywords = ["password", "credit", "health", "private", "personal"]
        text = str(action).lower()
        if any(kw in text for kw in sensitive_keywords):
            score += 0.3
        
        # 2. عامل التأثير المجتمعي
        if action.get("impact") == "high":
            score += 0.3
        
        # 3. عامل السابقة التاريخية
        if action.get("type") in self._get_high_risk_types():
            score += 0.2
        
        # 4. عامل عدم اليقين
        if action.get("confidence", 1.0) < 0.6:
            score += 0.2
        
        return min(score, 1.0)
    
    def _get_high_risk_types(self) -> List[str]:
        return ["surveillance", "mass_data_processing", "automated_decision", "bias_amplification"]
    
    def _get_preventive_actions(self, risk_score: float) -> List[str]:
        if risk_score > 0.7:
            return ["تعقيم البيانات", "إضافة طبقة مراجعة بشرية", "تقييد الوصول"]
        elif risk_score > 0.4:
            return ["مراجعة إضافية", "توثيق القرار", "مراقبة النتائج"]
        else:
            return ["لا توجد إجراءات وقائية ضرورية"]

# ============================================================
# 2. البعد التشاركي: نظام التصويت المجتمعي (Participatory Ethics)
# ============================================================

class ParticipatoryEthics:
    """
    يشارك المجتمع في تحديد الأخلاقيات عبر نظام تصويت ومراجعة
    """
    
    def __init__(self):
        self.proposals = {}
        self.votes = {}
        self.reviews = []
    
    def submit_proposal(self, user_id: str, proposal: Dict) -> str:
        """
        تقديم اقتراح أخلاقي جديد من المجتمع
        """
        proposal_id = hashlib.md5(f"{user_id}{proposal['title']}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
        
        self.proposals[proposal_id] = {
            "id": proposal_id,
            "user_id": user_id,
            "title": proposal.get("title", "اقتراح أخلاقي"),
            "description": proposal.get("description", ""),
            "category": proposal.get("category", "general"),
            "status": "pending",
            "votes_for": 0,
            "votes_against": 0,
            "created_at": datetime.utcnow().isoformat()
        }
        
        return proposal_id
    
    def vote(self, proposal_id: str, user_id: str, vote: bool) -> Dict:
        """
        التصويت على اقتراح أخلاقي
        """
        if proposal_id not in self.proposals:
            return {"error": "Proposal not found"}
        
        if user_id in self.votes.get(proposal_id, {}):
            return {"error": "Already voted"}
        
        if proposal_id not in self.votes:
            self.votes[proposal_id] = {}
        
        self.votes[proposal_id][user_id] = vote
        
        if vote:
            self.proposals[proposal_id]["votes_for"] += 1
        else:
            self.proposals[proposal_id]["votes_against"] += 1
        
        # إذا تجاوزت الأصوات الحد الأدنى، يتم تغيير الحالة
        total_votes = self.proposals[proposal_id]["votes_for"] + self.proposals[proposal_id]["votes_against"]
        if total_votes >= 10:
            approval_rate = self.proposals[proposal_id]["votes_for"] / total_votes
            if approval_rate > 0.7:
                self.proposals[proposal_id]["status"] = "approved"
            else:
                self.proposals[proposal_id]["status"] = "rejected"
        
        return {
            "proposal_id": proposal_id,
            "status": self.proposals[proposal_id]["status"],
            "votes_for": self.proposals[proposal_id]["votes_for"],
            "votes_against": self.proposals[proposal_id]["votes_against"]
        }
    
    def get_active_proposals(self) -> List[Dict]:
        return [p for p in self.proposals.values() if p["status"] == "pending"]

# ============================================================
# 3. البعد السياقي: محرك السياق الأخلاقي (Contextual Ethics)
# ============================================================

class ContextualEthics:
    """
    يُطبّق الأخلاقيات حسب السياق الثقافي والاجتماعي والجغرافي
    """
    
    def __init__(self):
        self.context_rules = {}
        self.global_defaults = {
            "privacy": 0.8,
            "fairness": 0.7,
            "transparency": 0.9,
            "accountability": 0.8
        }
    
    def apply_context(self, country: str, action: Dict) -> Dict:
        """
        تطبيق الأخلاقيات حسب السياق الجغرافي
        """
        # الحصول على قواعد السياق الخاصة بالدولة
        context = self._get_context(country)
        
        # تعديل الإجراء حسب السياق
        adjusted_action = self._adjust_action(action, context)
        
        return {
            "country": country,
            "context": context,
            "adjusted_action": adjusted_action,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _get_context(self, country: str) -> Dict:
        """
        الحصول على قواعد السياق لدولة معينة
        """
        # محاكاة: في الواقع سيتم جلب البيانات من قاعدة بيانات السياقات
        if country in ["مصر", "السعودية", "الإمارات"]:
            return {
                "privacy": 0.7,
                "fairness": 0.8,
                "transparency": 0.9,
                "accountability": 0.8,
                "cultural_sensitivity": "high"
            }
        elif country in ["ألمانيا", "فرنسا"]:
            return {
                "privacy": 0.95,
                "fairness": 0.9,
                "transparency": 0.95,
                "accountability": 0.9,
                "cultural_sensitivity": "medium"
            }
        else:
            return self.global_defaults
    
    def _adjust_action(self, action: Dict, context: Dict) -> Dict:
        """
        تعديل الإجراء حسب السياق
        """
        adjusted = action.copy()
        
        # تعديل مستوى الخصوصية
        if context.get("privacy", 0.5) > 0.8:
            adjusted["privacy_level"] = "high"
        
        # تعديل مستوى الشفافية
        if context.get("transparency", 0.5) > 0.8:
            adjusted["transparency_level"] = "full"
        
        return adjusted

# ============================================================
# 4. البعد التطوري: نظام التطور الأخلاقي (Evolutionary Ethics)
# ============================================================

class EvolutionaryEthics:
    """
    يتعلم الأخلاقيات من التاريخ ويتكيف مع القيم المتغيرة
    """
    
    def __init__(self):
        self.historical_lessons = []
        self.evolution_cycles = 0
    
    def learn_from_history(self, ethical_event: Dict) -> Dict:
        """
        التعلم من الأحداث الأخلاقية التاريخية
        """
        lesson = {
            "id": hashlib.md5(f"{ethical_event.get('type', '')}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16],
            "event_type": ethical_event.get("type", "unknown"),
            "description": ethical_event.get("description", ""),
            "outcome": ethical_event.get("outcome", ""),
            "lesson_learned": self._extract_lesson(ethical_event),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.historical_lessons.append(lesson)
        return lesson
    
    def _extract_lesson(self, event: Dict) -> str:
        """
        استخلاص الدرس من الحدث الأخلاقي
        """
        if event.get("outcome") == "failure":
            return "تجنب: " + event.get("description", "")
        elif event.get("outcome") == "success":
            return "اعتماد: " + event.get("description", "")
        else:
            return "مراجعة: " + event.get("description", "")
    
    def evolve(self) -> Dict:
        """
        تطور النظام الأخلاقي بناءً على الدروس التاريخية
        """
        self.evolution_cycles += 1
        
        # تحليل الدروس التاريخية
        if len(self.historical_lessons) > 10:
            # استخراج الأنماط
            patterns = {}
            for lesson in self.historical_lessons[-20:]:
                key = lesson["event_type"]
                if key not in patterns:
                    patterns[key] = {"success": 0, "failure": 0}
                if "تجنب" in lesson["lesson_learned"]:
                    patterns[key]["failure"] += 1
                elif "اعتماد" in lesson["lesson_learned"]:
                    patterns[key]["success"] += 1
            
            # توليد توصيات التطور
            recommendations = []
            for key, values in patterns.items():
                if values["failure"] > values["success"]:
                    recommendations.append(f"مراجعة سياسة {key}: نسبة الفشل مرتفعة")
                elif values["success"] > values["failure"] * 2:
                    recommendations.append(f"تعزيز سياسة {key}: نسبة النجاح ممتازة")
            
            return {
                "evolution_cycle": self.evolution_cycles,
                "recommendations": recommendations,
                "patterns": patterns
            }
        
        return {
            "evolution_cycle": self.evolution_cycles,
            "recommendations": ["لا توجد بيانات كافية للتطور"],
            "patterns": {}
        }

# ============================================================
# 5. المحرك الأخلاقي المتقدم (Advanced Ethical Engine)
# ============================================================

class AdvancedEthicalEngine:
    """
    المحرك الأخلاقي المتقدم - يجمع الأبعاد الأربعة
    """
    
    def __init__(self):
        self.proactive = ProactiveEthics()
        self.participatory = ParticipatoryEthics()
        self.contextual = ContextualEthics()
        self.evolutionary = EvolutionaryEthics()
        self.history = []
        self.self_improvement_count = 0
    
    def evaluate_action(self, action: Dict, country: str = None) -> Dict:
        """
        تقييم إجراء باستخدام جميع الأبعاد الأخلاقية
        """
        # 1. البعد الاستباقي: توقع المخاطر
        risk_prediction = self.proactive.predict_risk(action)
        
        # 2. البعد السياقي: تطبيق السياق
        context = self.contextual.apply_context(country or "global", action)
        
        # 3. البعد التطوري: التعلم من التاريخ
        historical_lesson = self.evolutionary.learn_from_history({
            "type": action.get("type", "unknown"),
            "description": action.get("description", ""),
            "outcome": "pending"
        })
        
        # 4. القرار النهائي
        if risk_prediction["risk_level"] == "critical":
            decision = "rejected"
            reason = "انتهاك أخلاقي حاد"
        elif risk_prediction["risk_level"] == "high" and not self._has_override(action):
            decision = "pending_review"
            reason = "يحتاج إلى مراجعة إضافية"
        else:
            decision = "approved"
            reason = "يتوافق مع المعايير الأخلاقية"
        
        result = {
            "action": action,
            "decision": decision,
            "reason": reason,
            "risk_prediction": risk_prediction,
            "context": context,
            "historical_lesson": historical_lesson,
            "timestamp": datetime.utcnow().isoformat(),
            "ethics_score": self._calculate_ethics_score(risk_prediction, context)
        }
        
        self.history.append(result)
        
        # التحسين الذاتي كل 10 تقييمات
        if len(self.history) % 10 == 0:
            self._self_improve()
        
        return result
    
    def _has_override(self, action: Dict) -> bool:
        """
        التحقق من وجود تجاوز للقرار (مثل موافقة إدارية خاصة)
        """
        return action.get("override", False)
    
    def _calculate_ethics_score(self, risk: Dict, context: Dict) -> float:
        """
        حساب درجة الأخلاقيات الإجمالية
        """
        base_score = 1.0 - risk.get("risk_score", 0.5)
        context_factor = context.get("context", {}).get("privacy", 0.5)
        return round((base_score * 0.6) + (context_factor * 0.4), 2)
    
    def _self_improve(self):
        """
        التحسين الذاتي للنظام الأخلاقي
        """
        self.self_improvement_count += 1
        
        # تحليل القرارات السابقة
        recent_decisions = self.history[-20:]
        approved = len([d for d in recent_decisions if d["decision"] == "approved"])
        rejected = len([d for d in recent_decisions if d["decision"] == "rejected"])
        
        # تحسين معايير التقييم بناءً على النتائج
        if rejected > approved and approved > 0:
            # زيادة التسامح
            pass
        elif approved > rejected * 2 and rejected > 0:
            # زيادة الصرامة
            pass
    
    def get_community_proposals(self) -> List[Dict]:
        """
        الحصول على اقتراحات المجتمع الأخلاقية
        """
        return self.participatory.get_active_proposals()
    
    def submit_proposal(self, user_id: str, proposal: Dict) -> str:
        """
        تقديم اقتراح أخلاقي
        """
        return self.participatory.submit_proposal(user_id, proposal)
    
    def vote_proposal(self, proposal_id: str, user_id: str, vote: bool) -> Dict:
        """
        التصويت على اقتراح
        """
        return self.participatory.vote(proposal_id, user_id, vote)

# ============================================================
# 6. نقاط النهاية API
# ============================================================

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v2/advanced-ethics", tags=["Advanced Ethics"])

_ethical_engine = None

def get_ethical_engine() -> AdvancedEthicalEngine:
    global _ethical_engine
    if _ethical_engine is None:
        _ethical_engine = AdvancedEthicalEngine()
    return _ethical_engine

@router.post("/evaluate")
async def evaluate_action(action: Dict, country: str = None):
    """تقييم إجراء باستخدام جميع الأبعاد الأخلاقية"""
    engine = get_ethical_engine()
    return engine.evaluate_action(action, country)

@router.post("/proposal/submit")
async def submit_proposal(user_id: str, proposal: Dict):
    """تقديم اقتراح أخلاقي للمجتمع"""
    engine = get_ethical_engine()
    proposal_id = engine.submit_proposal(user_id, proposal)
    return {"proposal_id": proposal_id, "status": "submitted"}

@router.post("/proposal/vote")
async def vote_proposal(proposal_id: str, user_id: str, vote: bool):
    """التصويت على اقتراح أخلاقي"""
    engine = get_ethical_engine()
    return engine.vote_proposal(proposal_id, user_id, vote)

@router.get("/proposals/active")
async def get_active_proposals():
    """الحصول على الاقتراحات الأخلاقية النشطة"""
    engine = get_ethical_engine()
    return {"proposals": engine.get_community_proposals()}

@router.get("/status")
async def get_ethical_status():
    """حالة النظام الأخلاقي المتقدم"""
    engine = get_ethical_engine()
    return {
        "self_improvement_cycles": engine.self_improvement_count,
        "total_evaluations": len(engine.history),
        "historical_lessons": len(engine.evolutionary.historical_lessons),
        "active_proposals": len(engine.get_community_proposals()),
        "evolution_cycles": engine.evolutionary.evolution_cycles
    }

@router.post("/self-improve")
async def trigger_ethical_improvement():
    """تشغيل التحسين الذاتي الأخلاقي"""
    engine = get_ethical_engine()
    return engine._self_improve()
