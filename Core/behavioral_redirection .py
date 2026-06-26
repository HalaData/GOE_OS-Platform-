"""
طبقة فك الشيفرة السلوكية وإعادة التوجيه (Behavioural Decryption & Redirection Layer)
مستوحاة من قصة الباحث ناوكي تسوكاهارا والغربان في اليابان.

تقوم بـ:
1. رصد السلوكيات غير المرغوب فيها.
2. فك شيفرة "الإشارات" التي تسبقها (مثل الأصوات في قصة الغربان).
3. بناء "قاموس إشارات" (Signal Dictionary) يربط بين الإشارات والسلوكيات.
4. الاستباق: إرسال إشارات "الخطر" أو "الطعام" لإعادة توجيه السلوك قبل حدوثه.
5. التعلم التراكمي: تحسين القاموس مع كل تفاعل جديد.
"""

from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import hashlib
import json
import logging
import random
import numpy as np
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

# ============================================================
# 1. تعريفات البيانات الأساسية (الغربان والغذاء والمواقف)
# ============================================================

@dataclass
class BehavioralSignal:
    """إشارة سلوكية (مثل صوت الغراب)."""
    id: str
    signal_type: str  # 'sound', 'text_pattern', 'market_trend', 'code_smell'
    content: str  # النص أو تردد الصوت أو نمط الكود
    observed_behavior: str  # السلوك المرتبط بهذه الإشارة
    confidence: float = 0.5  # درجة الثقة
    first_observed: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    last_observed: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    occurrence_count: int = 0

@dataclass
class BehavioralAgent:
    """كيان سلوكي (غراب، مستخدم، وكيل ذكاء اصطناعي)."""
    id: str
    type: str  # 'crow', 'trader', 'politician', 'ai_agent'
    signals_history: List[str] = field(default_factory=list)  # قائمة معرفات الإشارات التي أصدرها
    behaviors_history: List[str] = field(default_factory=list)  # سلوكياته السابقة
    trust_score: float = 0.5  # درجة الثقة به

@dataclass
class RedirectionPlan:
    """خطة إعادة توجيه (مثل وضع مكبرات الصوت)."""
    id: str
    agent_id: str
    target_behavior: str  # السلوك المطلوب تغييره
    trigger_signal_id: str  # الإشارة التي ستُستخدم
    broadcast_channel: str  # قناة البث (API، إشعار، مكبر صوت)
    scheduled_time: str
    status: str = 'pending'  # pending, active, completed, failed

# ============================================================
# 2. راصد الإشارات والسلوك (Signal & Behavior Observer)
# ============================================================

class BehavioralObserver:
    """
    يرصد الإشارات (الأصوات، الأنماط النصية، اتجاهات السوق)
    والسلوكيات المرتبطة بها.
    """

    def __init__(self):
        self.signals: Dict[str, BehavioralSignal] = {}
        self.agents: Dict[str, BehavioralAgent] = {}
        self.signal_behavior_map: Dict[str, Counter] = defaultdict(Counter)

    def observe(self, agent_id: str, signal_content: str, behavior: str, context: Dict = None) -> str:
        """
        رصد إشارة وسلوك مرتبط بها (مثل: سمع صوت "خطر" ثم هرب).
        """
        if agent_id not in self.agents:
            self.agents[agent_id] = BehavioralAgent(id=agent_id, type=context.get('type', 'unknown'))

        # 1. معالجة الإشارة (تطبيع، استخراج الهاش)
        signal_hash = hashlib.md5(f"{signal_content}_{behavior}".encode()).hexdigest()[:16]

        # 2. تحديث الإشارة الموجودة أو إنشاؤها
        if signal_hash in self.signals:
            signal = self.signals[signal_hash]
            signal.occurrence_count += 1
            signal.last_observed = datetime.utcnow().isoformat()
            # تحديث الثقة (زيادة عند تكرار نفس الارتباط)
            signal.confidence = min(1.0, signal.confidence + 0.05)
        else:
            signal = BehavioralSignal(
                id=signal_hash,
                signal_type=context.get('signal_type', 'text_pattern'),
                content=signal_content,
                observed_behavior=behavior,
                confidence=0.5,
                occurrence_count=1
            )
            self.signals[signal_hash] = signal

        # 3. تحديث سجل الوكيل
        self.agents[agent_id].signals_history.append(signal_hash)
        self.agents[agent_id].behaviors_history.append(behavior)

        # 4. تحديث خريطة الإشارات ← السلوكيات
        self.signal_behavior_map[signal_hash][behavior] += 1

        logger.info(f"👀 Observed: Agent {agent_id} -> Signal '{signal_content}' -> Behavior '{behavior}'")
        return signal_hash

    def get_signal_dictionary(self, min_confidence: float = 0.6) -> Dict[str, List[str]]:
        """
        استخراج قاموس الإشارات (مثل قاموس الغربان الـ 40 كلمة).
        """
        dictionary = {}
        for sig_id, signal in self.signals.items():
            if signal.confidence >= min_confidence:
                # أكثر سلوك شيوعاً لهذه الإشارة
                top_behavior = self.signal_behavior_map[sig_id].most_common(1)
                if top_behavior:
                    dictionary[signal.content] = top_behavior[0][0]
        return dictionary

    def get_agent_behavior_profile(self, agent_id: str) -> Dict:
        """ملف سلوكي لوكيل معين."""
        agent = self.agents.get(agent_id)
        if not agent:
            return {}
        behaviors = Counter(agent.behaviors_history)
        return {
            "agent_id": agent_id,
            "type": agent.type,
            "top_behaviors": behaviors.most_common(5),
            "total_signals": len(agent.signals_history),
            "trust_score": agent.trust_score
        }

# ============================================================
# 3. محلل التنبؤ الاستباقي (Predictive Scheduler)
# ============================================================

class PredictiveScheduler:
    """
    يتنبأ بموعد حدوث السلوك غير المرغوب فيه (مثل موعد خروج القمامة).
    """

    def __init__(self, observer: BehavioralObserver):
        self.observer = observer
        self.historical_patterns: Dict[str, List[str]] = defaultdict(list)

    def predict_behavior_time(self, behavior: str, agent_id: str = None) -> Optional[datetime]:
        """
        توقع وقت حدوث سلوك معين بناءً على التاريخ.
        """
        # 1. استرجاع جميع أوقات حدوث هذا السلوك
        if agent_id:
            agent = self.observer.agents.get(agent_id)
            if not agent:
                return None
            times = [agent.behaviors_history[i] for i, b in enumerate(agent.behaviors_history) if b == behavior]
        else:
            # جميع الوكلاء
            times = []
            for ag in self.observer.agents.values():
                times.extend([ag.behaviors_history[i] for i, b in enumerate(ag.behaviors_history) if b == behavior])

        if len(times) < 2:
            return None

        # 2. محاكاة تحليل النمط الزمني (في الواقع سيتم استخدام ARIMA أو Prophet)
        # مثال بسيط: المتوسط الحسابي للفروق الزمنية
        # هنا نُعيد تاريخاً تقديرياً (بعد 24 ساعة من آخر حدوث)
        last_time = datetime.utcnow()
        if agent_id and agent_id in self.observer.agents:
            last_time = datetime.utcnow() + timedelta(hours=random.randint(2, 6))

        return last_time

    def get_behavior_schedule(self, agent_id: str) -> List[Tuple[str, datetime]]:
        """جدول زمني متوقع للسلوكيات."""
        agent = self.observer.agents.get(agent_id)
        if not agent:
            return []
        schedule = []
        for behavior in set(agent.behaviors_history):
            predicted_time = self.predict_behavior_time(behavior, agent_id)
            if predicted_time:
                schedule.append((behavior, predicted_time))
        return sorted(schedule, key=lambda x: x[1])

# ============================================================
# 4. محرك إعادة التوجيه (Redirection Engine) - مكبرات الصوت الذكية
# ============================================================

class RedirectionEngine:
    """
    يخطط وينفذ عمليات إعادة التوجيه (مثل تشغيل عبارة "خطر" أو "غذاء").
    """

    def __init__(self, observer: BehavioralObserver, scheduler: PredictiveScheduler):
        self.observer = observer
        self.scheduler = scheduler
        self.plans: List[RedirectionPlan] = []
        self.executed_plans: List[Dict] = []

    def create_redirection_plan(self, agent_id: str, target_behavior: str, desired_behavior: str) -> RedirectionPlan:
        """
        إنشاء خطة إعادة توجيه (مثل وضع مكبر صوت بجوار القمامة).
        """
        # 1. البحث عن إشارة تؤدي إلى السلوك المطلوب (مثل إشارة "غذاء" -> "توجه للمكان المخصص")
        signal_id = None
        for sig_id, sig in self.observer.signals.items():
            if sig.observed_behavior == desired_behavior and sig.confidence > 0.6:
                signal_id = sig_id
                break

        if not signal_id:
            # إنشاء إشارة جديدة (محاكاة)
            signal_id = hashlib.md5(f"custom_{desired_behavior}_{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
            self.observer.signals[signal_id] = BehavioralSignal(
                id=signal_id,
                signal_type="broadcast",
                content=f"إشارة محفزة لـ {desired_behavior}",
                observed_behavior=desired_behavior,
                confidence=0.7
            )

        # 2. توقع وقت حدوث السلوك المستهدف
        target_time = self.scheduler.predict_behavior_time(target_behavior, agent_id)
        if not target_time:
            target_time = datetime.utcnow() + timedelta(hours=1)

        plan = RedirectionPlan(
            id=hashlib.md5(f"{agent_id}_{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16],
            agent_id=agent_id,
            target_behavior=target_behavior,
            trigger_signal_id=signal_id,
            broadcast_channel="api_notification",
            scheduled_time=target_time.isoformat()
        )

        self.plans.append(plan)
        logger.info(f"📢 Redirection plan created for Agent {agent_id}: Use '{desired_behavior}' signal to replace '{target_behavior}'")
        return plan

    def execute_plan(self, plan_id: str) -> Dict:
        """
        تنفيذ خطة إعادة توجيه (تشغيل مكبر الصوت).
        """
        plan = next((p for p in self.plans if p.id == plan_id), None)
        if not plan:
            return {"status": "failed", "reason": "Plan not found"}

        # 1. الحصول على الإشارة المحفزة
        signal = self.observer.signals.get(plan.trigger_signal_id)
        if not signal:
            return {"status": "failed", "reason": "Signal not found"}

        # 2. محاكاة البث (في الواقع، سيتم إرسال إشعار أو تغيير متغير بيئي)
        # هذا هو "مكبر الصوت" الرقمي
        logger.info(f"📢 BROADCAST to Agent {plan.agent_id}: Signal '{signal.content}' (Behavior: {signal.observed_behavior})")

        # 3. تسجيل التنفيذ
        execution_record = {
            "plan_id": plan_id,
            "agent_id": plan.agent_id,
            "broadcast_signal": signal.content,
            "target_behavior": plan.target_behavior,
            "desired_behavior": signal.observed_behavior,
            "status": "executed",
            "timestamp": datetime.utcnow().isoformat()
        }
        self.executed_plans.append(execution_record)
        plan.status = "active"

        # 4. تحديث سلوك الوكيل (محاكاة: في الواقع سننتظر الرد الفعلي)
        # نضيف إشارة جديدة إلى تاريخ الوكيل (وكأنه استجاب)
        agent = self.observer.agents.get(plan.agent_id)
        if agent:
            agent.behaviors_history.append(signal.observed_behavior)

        return execution_record

    def get_active_plans(self) -> List[RedirectionPlan]:
        """جميع الخطط النشطة."""
        return [p for p in self.plans if p.status in ['pending', 'active']]

# ============================================================
# 5. المحرك الرئيسي - إعادة التوجيه السلوكي المتكامل
# ============================================================

class BehavioralRedirectionEngine:
    """
    المحرك الرئيسي (المستوحى من قصة الغربان).
    يجمع: الرصد، فك الشيفرة، الاستباق، وإعادة التوجيه.
    """

    def __init__(self):
        self.observer = BehavioralObserver()
        self.scheduler = PredictiveScheduler(self.observer)
        self.redirector = RedirectionEngine(self.observer, self.scheduler)
        self.history: List[Dict] = []

        logger.info("🐦 Behavioral Redirection Engine initialized (Inspired by Japan's Crows).")

    def observe_and_learn(self, agent_id: str, signal: str, behavior: str, context: Dict = None) -> Dict:
        """
        الخطوة 1: رصد وتعلم لغة السلوك.
        """
        signal_id = self.observer.observe(agent_id, signal, behavior, context)
        return {
            "signal_id": signal_id,
            "agent": agent_id,
            "signal": signal,
            "behavior": behavior,
            "dictionary_size": len(self.observer.get_signal_dictionary())
        }

    def get_behavior_dictionary(self) -> Dict:
        """
        الخطوة 2: استخراج قاموس السلوك (مثل قاموس الغربان الـ 40 كلمة).
        """
        return self.observer.get_signal_dictionary()

    def predict_behavior(self, agent_id: str, behavior: str) -> Dict:
        """
        الخطوة 3: توقع متى سيحدث السلوك.
        """
        predicted_time = self.scheduler.predict_behavior_time(behavior, agent_id)
        schedule = self.scheduler.get_behavior_schedule(agent_id)
        return {
            "agent_id": agent_id,
            "behavior": behavior,
            "predicted_time": predicted_time.isoformat() if predicted_time else None,
            "full_schedule": schedule
        }

    def redirect_behavior(self, agent_id: str, target_behavior: str, desired_behavior: str) -> Dict:
        """
        الخطوة 4: إعادة التوجيه (وضع مكبر الصوت).
        """
        plan = self.redirector.create_redirection_plan(agent_id, target_behavior, desired_behavior)
        execution = self.redirector.execute_plan(plan.id)

        # تسجيل في التاريخ
        self.history.append({
            "action": "redirect",
            "agent_id": agent_id,
            "target": target_behavior,
            "desired": desired_behavior,
            "execution": execution,
            "timestamp": datetime.utcnow().isoformat()
        })

        return {
            "plan": plan,
            "execution": execution,
            "message": f"✅ تم إرسال إشارة '{desired_behavior}' إلى {agent_id} لإعادة توجيه السلوك '{target_behavior}'."
        }

    def get_system_status(self) -> Dict:
        """
        الحالة الكاملة للنظام (كم عدد الغربان التي تم تدريبها؟).
        """
        return {
            "total_agents": len(self.observer.agents),
            "total_signals": len(self.observer.signals),
            "dictionary_size": len(self.observer.get_signal_dictionary()),
            "active_plans": len(self.redirector.get_active_plans()),
            "executed_plans": len(self.redirector.executed_plans),
            "trusted_agents": len([a for a in self.observer.agents.values() if a.trust_score > 0.7])
        }

# ============================================================
# 6. نقاط النهاية API (تطبيق قصة الغربان رقمياً)
# ============================================================

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v2/behavioral-redirection", tags=["Behavioral Redirection (Crows)"])

_engine = None

def get_engine() -> BehavioralRedirectionEngine:
    global _engine
    if _engine is None:
        _engine = BehavioralRedirectionEngine()
    return _engine

@router.post("/observe")
async def observe_behavior(agent_id: str, signal: str, behavior: str, context: Dict = None):
    """رصد سلوك وإشارة (مثل تسجيل صوت الغراب)."""
    engine = get_engine()
    return engine.observe_and_learn(agent_id, signal, behavior, context)

@router.get("/dictionary")
async def get_dictionary():
    """استخراج قاموس الإشارات ← السلوكيات (مثل قاموس الغربان)."""
    engine = get_engine()
    return {"dictionary": engine.get_behavior_dictionary()}

@router.get("/predict/{agent_id}")
async def predict_behavior(agent_id: str, behavior: str):
    """توقع متى سيحدث سلوك معين (مثل موعد خروج القمامة)."""
    engine = get_engine()
    return engine.predict_behavior(agent_id, behavior)

@router.post("/redirect")
async def redirect_behavior(agent_id: str, target_behavior: str, desired_behavior: str):
    """
    إعادة توجيه السلوك (مثل تشغيل مكبر الصوت بعبارة "خطر" أو "غذاء").
    """
    engine = get_engine()
    return engine.redirect_behavior(agent_id, target_behavior, desired_behavior)

@router.get("/status")
async def get_status():
    """حالة النظام (كم عدد الغربان التي تم تدريبها؟)."""
    engine = get_engine()
    return engine.get_system_status()

@router.get("/history")
async def get_history(limit: int = 20):
    """سجل عمليات إعادة التوجيه."""
    engine = get_engine()
    return {"history": engine.history[-limit:]}
