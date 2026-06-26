"""
المُنسق الذاتي - Self-Orchestrator (DevOps Engine)
يدير البنية التحتية والموارد والتزامن تلقائياً واستباقياً
يُطبق النظرية على النظام نفسه لضمان الجودة واللانهائية
"""

import asyncio
import time
import psutil
import os
import threading
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import logging
from collections import deque
import numpy as np

logger = logging.getLogger(__name__)

# ============================================================
# 1. بيانات الحالة (State Data)
# ============================================================

@dataclass
class SystemMetrics:
    """قراءة لحظية لأداء النظام."""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_io_read: float
    disk_io_write: float
    api_response_time_avg: float
    api_requests_per_sec: float
    db_query_time_avg: float
    db_connection_pool_usage: float
    active_workers: int
    cache_hit_ratio: float
    error_rate: float

@dataclass
class ResourceDecision:
    """قرار توزيع الموارد."""
    action: str  # 'scale_workers', 'adjust_cache', 'reduce_depth', 'restart_component'
    value: Any
    reason: str
    priority: int

# ============================================================
# 2. المستشعر السيبرنطيقي (Cyber-Sensor)
# ============================================================

class CyberSensor:
    """
    يراقب أداء النظام بشكل لحظي ويُصدر بطاقة أداء.
    """

    def __init__(self):
        self.history: deque = deque(maxlen=1000)  # آخر 1000 قراءة
        self._start_time = time.time()
        self._last_io = psutil.disk_io_counters()
        self._request_counter = 0
        self._request_times = deque(maxlen=200)

    def sample(self) -> SystemMetrics:
        """جمع قراءة حالية للنظام."""
        # CPU & Memory
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent

        # Disk I/O
        current_io = psutil.disk_io_counters()
        read_speed = (current_io.read_bytes - self._last_io.read_bytes) / (1024 * 1024) if self._last_io else 0
        write_speed = (current_io.write_bytes - self._last_io.write_bytes) / (1024 * 1024) if self._last_io else 0
        self._last_io = current_io

        # API Metrics (محاكاة: سيتم ربطها بـ FastAPI middleware)
        avg_response = sum(self._request_times) / len(self._request_times) if self._request_times else 0
        req_per_sec = self._request_counter / (time.time() - self._start_time + 0.01)

        # Database (محاكاة)
        db_query_time = 0.05  # 50ms
        db_pool_usage = 0.3  # 30%

        # Workers
        active_workers = threading.active_count()

        # Cache (محاكاة)
        cache_hit = 0.85

        # Error Rate (محاكاة)
        error_rate = 0.02

        metrics = SystemMetrics(
            timestamp=datetime.utcnow().isoformat(),
            cpu_percent=round(cpu, 1),
            memory_percent=round(mem, 1),
            disk_io_read=round(read_speed, 2),
            disk_io_write=round(write_speed, 2),
            api_response_time_avg=round(avg_response * 1000, 2),
            api_requests_per_sec=round(req_per_sec, 2),
            db_query_time_avg=round(db_query_time * 1000, 2),
            db_connection_pool_usage=round(db_pool_usage, 2),
            active_workers=active_workers,
            cache_hit_ratio=round(cache_hit, 2),
            error_rate=round(error_rate, 4)
        )

        self.history.append(metrics)
        return metrics

    def record_request(self, duration: float):
        """تسجيل وقت استجابة طلب API."""
        self._request_counter += 1
        self._request_times.append(duration)

    def get_trend(self, metric: str, window: int = 20) -> float:
        """تحليل اتجاه مقياس معين خلال آخر N قراءة."""
        if len(self.history) < window:
            return 0.0
        values = [getattr(m, metric) for m in list(self.history)[-window:]]
        if len(values) < 2:
            return 0.0
        # انحدار خطي بسيط (الاتجاه)
        x = np.arange(len(values))
        slope, _ = np.polyfit(x, values, 1)
        return float(slope)

# ============================================================
# 3. المحلل التنبؤي (Predictive Analyzer)
# ============================================================

class PredictiveAnalyzer:
    """
    يحلل اتجاهات النظام ويتنبأ بالاحتياجات المستقبلية.
    """

    def __init__(self, sensor: CyberSensor):
        self.sensor = sensor
        self.predictions = {}

    def predict_load(self, horizon_seconds: int = 600) -> Dict:
        """
        توقع الحمل خلال الدقائق العشر القادمة.
        """
        history = list(self.sensor.history)
        if len(history) < 10:
            return {"confidence": 0.0, "cpu": 0, "mem": 0, "requests": 0}

        # استخدام المتوسط المتحرك المرجح
        weights = np.arange(1, len(history) + 1)
        weights = weights / weights.sum()

        cpu_values = [h.cpu_percent for h in history]
        mem_values = [h.memory_percent for h in history]
        req_values = [h.api_requests_per_sec for h in history]

        # توقع بسيط: الوزن للقيم الحديثة أكبر
        pred_cpu = np.average(cpu_values, weights=weights[-len(cpu_values):])
        pred_mem = np.average(mem_values, weights=weights[-len(mem_values):])
        pred_req = np.average(req_values, weights=weights[-len(req_values):])

        # إضافة عامل النمو (الاتجاه)
        trend_cpu = self.sensor.get_trend('cpu_percent', 10)
        trend_req = self.sensor.get_trend('api_requests_per_sec', 10)

        pred_cpu = min(100, pred_cpu + trend_cpu * 2)
        pred_mem = min(100, pred_mem + trend_cpu * 1)
        pred_req = max(0, pred_req + trend_req * 0.5)

        confidence = min(1.0, len(history) / 50)

        return {
            "confidence": round(confidence, 2),
            "cpu": round(pred_cpu, 1),
            "memory": round(pred_mem, 1),
            "requests": round(pred_req, 2),
            "trend": "تصاعدي" if trend_req > 0.1 else "تنازلي" if trend_req < -0.1 else "مستقر"
        }

    def analyze_system_indicators(self, metrics: SystemMetrics) -> Dict:
        """
        تطبيق المؤشرات التسعة على أداء النظام نفسه.
        """
        indicators = {}

        # ERI (الجمود المعرفي للنظام): عدم تغير أنماط التحميل
        trend = self.sensor.get_trend('cpu_percent', 30)
        indicators["ERI_system"] = round(min(1.0, abs(trend) * 2), 2)

        # PAI (الغياب الإجرائي): تجاهل بعض المكونات (مثل Redis)
        if metrics.cache_hit_ratio < 0.5:
            indicators["PAI_system"] = 0.8
        else:
            indicators["PAI_system"] = 0.2

        # CGI (فجوة المصداقية): الفجوة بين وقت الاستجابة المتوقع والفعلي
        if metrics.api_response_time_avg > 200:  # 200ms
            indicators["CGI_system"] = 0.7
        else:
            indicators["CGI_system"] = 0.2

        # باقي المؤشرات (محاكاة)
        indicators["FQI_system"] = 0.3
        indicators["AGI_system"] = 0.2
        indicators["DIC_system"] = 0.5
        indicators["MCI_system"] = 0.4
        indicators["LRI_system"] = 0.1
        indicators["SAI_system"] = 0.3

        return indicators

# ============================================================
# 4. محرك القرار (Decision Engine)
# ============================================================

class DecisionEngine:
    """
    يتخذ قرارات توزيع الموارد بناءً على التحليلات.
    """

    def __init__(self):
        self.decision_history: List[Dict] = []
        self.last_decision_time = datetime.utcnow()

    def decide(self, metrics: SystemMetrics, prediction: Dict, indicators: Dict) -> List[ResourceDecision]:
        """
        توليد قائمة بالقرارات بناءً على حالة النظام.
        """
        decisions = []

        # 1. توقع زيادة الحمل (استباقي)
        if prediction.get("confidence", 0) > 0.7 and prediction.get("cpu", 0) > 75:
            decisions.append(ResourceDecision(
                action="scale_workers",
                value=threading.active_count() + 2,
                reason=f"توقع ارتفاع الحمل (CPU: {prediction['cpu']}%)",
                priority=1
            ))

        # 2. ارتفاع الذاكرة
        if metrics.memory_percent > 85:
            decisions.append(ResourceDecision(
                action="adjust_cache",
                value="reduce_size",
                reason=f"ذاكرة عالية ({metrics.memory_percent}%)",
                priority=2
            ))

        # 3. بطء الاستجابة (جودة المعلومات)
        if metrics.api_response_time_avg > 300:
            decisions.append(ResourceDecision(
                action="reduce_depth",
                value="skip_z3",
                reason=f"زمن استجابة مرتفع ({metrics.api_response_time_avg}ms)",
                priority=1
            ))

        # 4. معدل أخطاء مرتفع (شفاء ذاتي)
        if metrics.error_rate > 0.05:
            decisions.append(ResourceDecision(
                action="restart_component",
                value="analysis_workers",
                reason=f"معدل أخطاء مرتفع ({metrics.error_rate*100:.1f}%)",
                priority=1
            ))

        # 5. استغلال أقل من اللازم (توفير الموارد)
        if metrics.cpu_percent < 20 and metrics.memory_percent < 30:
            decisions.append(ResourceDecision(
                action="scale_workers",
                value=max(1, threading.active_count() - 1),
                reason="استغلال منخفض للموارد",
                priority=3
            ))

        # 6. تحسين الـ Cache
        if metrics.cache_hit_ratio < 0.7:
            decisions.append(ResourceDecision(
                action="adjust_cache",
                value="increase_ttl",
                reason=f"نسبة نجاح Cache منخفضة ({metrics.cache_hit_ratio})",
                priority=2
            ))

        return decisions

    def execute(self, decisions: List[ResourceDecision]) -> List[Dict]:
        """
        تنفيذ القرارات (محاكاة + تطبيق فعلي).
        """
        executed = []
        for decision in decisions:
            try:
                if decision.action == "scale_workers":
                    # محاكاة تغيير عدد العمال (في الواقع، سيتم تعديل تجمع العمال)
                    logger.info(f"⚙️ قرار: تغيير عدد العمال إلى {decision.value}")
                elif decision.action == "adjust_cache":
                    logger.info(f"⚙️ قرار: تعديل Cache: {decision.value}")
                elif decision.action == "reduce_depth":
                    # تغيير متغير بيئي لتقليل عمق التحليل
                    os.environ["COGNITIVE_DEPTH"] = "reduced"
                    logger.info(f"⚙️ قرار: تقليل عمق التحليل (تخطي Z3)")
                elif decision.action == "restart_component":
                    logger.info(f"⚙️ قرار: إعادة تشغيل المكون: {decision.value}")

                executed.append({
                    "action": decision.action,
                    "value": decision.value,
                    "reason": decision.reason,
                    "status": "executed",
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                executed.append({
                    "action": decision.action,
                    "value": decision.value,
                    "reason": decision.reason,
                    "status": "failed",
                    "error": str(e)
                })

        self.decision_history.extend(executed)
        return executed

# ============================================================
# 5. سجل التطور الذاتي (Self-Evolution Log)
# ============================================================

class SelfEvolutionLog:
    """
    يسجل كل قرار ونتيجته لتحسين القرارات المستقبلية.
    """

    def __init__(self):
        self.history: List[Dict] = []
        self.knowledge_base: Dict = {}

    def record(self, decision: Dict, outcome: Dict):
        """
        تسجيل قرار ونتيجته.
        """
        record = {
            "decision": decision,
            "outcome": outcome,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.history.append(record)

        # تحديث قاعدة المعرفة (ما نجح وما فشل)
        if outcome.get("status") == "success":
            key = f"{decision['action']}_{decision['value']}"
            self.knowledge_base[key] = self.knowledge_base.get(key, 0) + 1
        else:
            key = f"{decision['action']}_{decision['value']}"
            self.knowledge_base[key] = self.knowledge_base.get(key, 0) - 1

    def get_best_decision(self, action: str) -> Optional[str]:
        """استرجاع أنجح قرار لنوع معين من الإجراءات."""
        candidates = {k: v for k, v in self.knowledge_base.items() if k.startswith(action)}
        if not candidates:
            return None
        return max(candidates, key=candidates.get)

# ============================================================
# 6. المنسق الذاتي (Self-Orchestrator) - المحرك الرئيسي
# ============================================================

class SelfOrchestrator:
    """
    المحرك الرئيسي - يدير دورة (مراقبة → تحليل → قرار → تنفيذ → تعلم).
    """

    def __init__(self, interval_seconds: int = 10):
        self.sensor = CyberSensor()
        self.analyzer = PredictiveAnalyzer(self.sensor)
        self.decision_engine = DecisionEngine()
        self.evolution_log = SelfEvolutionLog()
        self.interval = interval_seconds
        self.running = False
        self._task = None
        self.last_executed_decisions: List[Dict] = []

        logger.info("🚀 Self-Orchestrator initialized.")

    async def start(self):
        """بدء دورة التنسيق الذاتي."""
        self.running = True
        self._task = asyncio.create_task(self._loop())
        logger.info("🔄 Self-Orchestrator started.")

    async def stop(self):
        """إيقاف الدورة."""
        self.running = False
        if self._task:
            self._task.cancel()
        logger.info("🛑 Self-Orchestrator stopped.")

    async def _loop(self):
        """حلقة التشغيل الرئيسية."""
        while self.running:
            try:
                await self._cycle()
            except Exception as e:
                logger.error(f"❌ Cycle failed: {e}")
            await asyncio.sleep(self.interval)

    async def _cycle(self):
        """دورة واحدة: مراقبة → تحليل → قرار → تنفيذ → تسجيل."""
        # 1. المراقبة
        metrics = self.sensor.sample()
        logger.info(f"📊 Metrics: CPU={metrics.cpu_percent}%, MEM={metrics.memory_percent}%, ERR={metrics.error_rate}")

        # 2. التحليل (تنبؤ + مؤشرات)
        prediction = self.analyzer.predict_load()
        indicators = self.analyzer.analyze_system_indicators(metrics)

        # 3. القرار
        decisions = self.decision_engine.decide(metrics, prediction, indicators)

        # 4. التنفيذ
        executed = []
        if decisions:
            executed = self.decision_engine.execute(decisions)

        # 5. التسجيل والتعلم (محاكاة)
        for dec in executed:
            # محاكاة نتيجة القرار (في الواقع ستُستنتج من أداء النظام لاحقاً)
            outcome = {"status": "success", "effect": "improved"}
            self.evolution_log.record(dec, outcome)

        self.last_executed_decisions = executed

    def record_api_request(self, duration: float):
        """تسجيل طلب API للمراقبة."""
        self.sensor.record_request(duration)

    def get_status(self) -> Dict:
        """الحالة الحالية للمُنسق الذاتي."""
        metrics = self.sensor.sample()
        prediction = self.analyzer.predict_load()
        indicators = self.analyzer.analyze_system_indicators(metrics)
        return {
            "running": self.running,
            "metrics": metrics.__dict__,
            "prediction": prediction,
            "indicators": indicators,
            "last_decisions": self.last_executed_decisions[-5:],
            "evolution_confidence": len(self.evolution_log.history)
        }

# ============================================================
# 7. دمج المنسق الذاتي مع واجهة FastAPI (Middleware)
# ============================================================

from fastapi import FastAPI, Request, Response
import time

_orchestrator = None

def get_orchestrator() -> SelfOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = SelfOrchestrator(interval_seconds=10)
        # تشغيل المنسق في الخلفية عند أول استدعاء
        try:
            asyncio.create_task(_orchestrator.start())
        except RuntimeError:
            # إذا لم يكن هناك حلقة تشغيل، نستخدم threading
            import threading
            threading.Thread(target=asyncio.run, args=(_orchestrator.start(),)).start()
    return _orchestrator

# Middleware لقياس زمن الاستجابة
async def orchestrator_middleware(request: Request, call_next):
    """Middleware لتسجيل أداء API."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    orchestrator = get_orchestrator()
    orchestrator.record_api_request(duration)
    return response

# نقاط النهاية API
from fastapi import APIRouter
router = APIRouter(prefix="/api/v2/devops", tags=["Self-Orchestrator"])

@router.get("/status")
async def get_devops_status():
    """الحالة الحالية للمُنسق الذاتي."""
    orchestrator = get_orchestrator()
    return orchestrator.get_status()

@router.post("/restart")
async def restart_orchestrator():
    """إعادة تشغيل دورة التنسيق."""
    orchestrator = get_orchestrator()
    await orchestrator.stop()
    await orchestrator.start()
    return {"status": "restarted"}

@router.get("/evolution/history")
async def get_evolution_history(limit: int = 20):
    """سجل التطور الذاتي للقرارات."""
    orchestrator = get_orchestrator()
    return {"history": orchestrator.evolution_log.history[-limit:]}
