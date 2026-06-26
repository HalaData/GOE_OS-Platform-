"""
القوانين التقنية والأمنية - Technical & Security Laws
5 قوانين إضافية للحصن السيبرنطيقي المتكامل
"""

from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import hashlib
import logging
import random
import time
import psutil
import os
from enum import Enum

logger = logging.getLogger(__name__)

# ============================================================
# 1. تعريف القوانين التقنية والأمنية
# ============================================================

class TechnicalSecurityLaw:
    """
    قانون تقني أو أمني واحد.
    """
    def __init__(self, name: str, symbol: str, description: str, dimension: str,
                 check_function: Callable, auto_heal: bool = True):
        self.id = hashlib.md5(name.encode()).hexdigest()[:8]
        self.name = name
        self.symbol = symbol
        self.description = description
        self.dimension = dimension
        self.check_function = check_function
        self.auto_heal = auto_heal
        self.violations: List[Dict] = []
        self.heals: List[Dict] = []
        self.created_at = datetime.utcnow().isoformat()
        self.last_updated = self.created_at
        self.enforcement_count = 0
        self.severity_score = 0.0
    
    def check(self, context: Dict) -> Dict:
        """التحقق من تطبيق القانون."""
        self.enforcement_count += 1
        result = self.check_function(context)
        
        if not result.get("compliant", True):
            self.violations.append({
                "context": context,
                "reason": result.get("reason", "unknown"),
                "severity": result.get("severity", "medium"),
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # تحديث درجة الخطورة
            severity_map = {"critical": 1.0, "high": 0.7, "medium": 0.4, "low": 0.1}
            self.severity_score = min(1.0, self.severity_score + severity_map.get(result.get("severity", "medium"), 0.1))
            
            if self.auto_heal:
                heal_result = self._heal(context, result.get("reason", ""))
                self.heals.append(heal_result)
                result["healed"] = True
                result["heal_action"] = heal_result
        
        return result
    
    def _heal(self, context: Dict, reason: str) -> Dict:
        """محاولة الشفاء الذاتي."""
        # محاكاة الشفاء: في الإنتاج سيتم تطبيق إصلاح حقيقي
        return {
            "action": "auto_heal_attempted",
            "reason": reason,
            "success": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "symbol": self.symbol,
            "description": self.description,
            "dimension": self.dimension,
            "enforcement_count": self.enforcement_count,
            "violations_count": len(self.violations),
            "heals_count": len(self.heals),
            "severity_score": round(self.severity_score, 3),
            "auto_heal": self.auto_heal,
            "created_at": self.created_at,
            "last_updated": self.last_updated
        }

# ============================================================
# 2. محرك القوانين التقنية والأمنية
# ============================================================

class TechnicalSecurityEngine:
    """
    محرك القوانين التقنية والأمنية - الحصن السيبرنطيقي المتكامل.
    """
    
    def __init__(self):
        self.laws: Dict[str, TechnicalSecurityLaw] = {}
        self._initialize_laws()
        self.enforcement_history: List[Dict] = []
        self.security_level = 0.5
        self.anomaly_detection = AnomalyDetectionEngine()
        
        logger.info("🛡️ Technical & Security Engine initialized with 5 laws")
    
    def _initialize_laws(self):
        """تهيئة القوانين التقنية والأمنية."""
        laws_data = [
            {
                "name": "المناعة الذاتية",
                "symbol": "🛡️",
                "description": "تكتشف التهديدات وتحييدها قبل أن تؤثر على النظام",
                "dimension": "security",
                "check": self._check_self_immunity
            },
            {
                "name": "المرونة التكيفية",
                "symbol": "⚡",
                "description": "تتكيف مع أي تغير في البيئة التقنية دون انقطاع",
                "dimension": "technical",
                "check": self._check_adaptive_resilience
            },
            {
                "name": "التشفير الشامل",
                "symbol": "🔐",
                "description": "كل البيانات مشفرة، في النقل والتخزين، بدون استثناء",
                "dimension": "security",
                "check": self._check_encryption
            },
            {
                "name": "المراقبة الاستباقية",
                "symbol": "📡",
                "description": "تراقب نفسها وتتنبأ بالأعطال قبل حدوثها",
                "dimension": "technical",
                "check": self._check_proactive_monitoring
            },
            {
                "name": "الاستدامة الذاتية",
                "symbol": "♻️",
                "description": "تعيد تدوير مواردها وتقلل الهدر إلى أدنى حد",
                "dimension": "technical",
                "check": self._check_self_sustainability
            }
        ]
        
        for data in laws_data:
            law = TechnicalSecurityLaw(
                name=data["name"],
                symbol=data["symbol"],
                description=data["description"],
                dimension=data["dimension"],
                check_function=data["check"]
            )
            self.laws[law.id] = law
    
    # ===== دوال التحقق من القوانين =====
    
    def _check_self_immunity(self, context: Dict) -> Dict:
        """التحقق من المناعة الذاتية."""
        # 1. التحقق من وجود نظام كشف التهديدات
        has_threat_detection = context.get("threat_detection", False)
        if not has_threat_detection:
            return {
                "compliant": False,
                "reason": "نظام كشف التهديدات غير موجود",
                "severity": "critical"
            }
        
        # 2. التحقق من وجود نظام تحييد التهديدات
        has_threat_neutralization = context.get("threat_neutralization", False)
        if not has_threat_neutralization:
            return {
                "compliant": False,
                "reason": "نظام تحييد التهديدات غير موجود",
                "severity": "high"
            }
        
        # 3. التحقق من سرعة الاستجابة
        response_time = context.get("response_time_ms", 1000)
        if response_time > 500:
            return {
                "compliant": False,
                "reason": f"زمن الاستجابة بطيء ({response_time}ms)",
                "severity": "medium"
            }
        
        return {"compliant": True}
    
    def _check_adaptive_resilience(self, context: Dict) -> Dict:
        """التحقق من المرونة التكيفية."""
        # 1. التحقق من قدرة التكيف مع التغيرات
        adapts_to_change = context.get("adapts_to_change", False)
        if not adapts_to_change:
            return {
                "compliant": False,
                "reason": "لا تتكيف مع التغيرات البيئية",
                "severity": "high"
            }
        
        # 2. التحقق من وجود خطط استمرارية
        has_continuity_plan = context.get("continuity_plan", False)
        if not has_continuity_plan:
            return {
                "compliant": False,
                "reason": "لا توجد خطط استمرارية",
                "severity": "medium"
            }
        
        return {"compliant": True}
    
    def _check_encryption(self, context: Dict) -> Dict:
        """التحقق من التشفير الشامل."""
        # 1. التحقق من تشفير البيانات في النقل
        transport_encrypted = context.get("transport_encrypted", False)
        if not transport_encrypted:
            return {
                "compliant": False,
                "reason": "البيانات في النقل غير مشفرة",
                "severity": "critical"
            }
        
        # 2. التحقق من تشفير البيانات في التخزين
        storage_encrypted = context.get("storage_encrypted", False)
        if not storage_encrypted:
            return {
                "compliant": False,
                "reason": "البيانات في التخزين غير مشفرة",
                "severity": "critical"
            }
        
        # 3. التحقق من قوة التشفير
        encryption_strength = context.get("encryption_strength", 0)
        if encryption_strength < 256:
            return {
                "compliant": False,
                "reason": f"قوة التشفير ضعيفة ({encryption_strength} بت)",
                "severity": "high"
            }
        
        return {"compliant": True}
    
    def _check_proactive_monitoring(self, context: Dict) -> Dict:
        """التحقق من المراقبة الاستباقية."""
        # 1. التحقق من وجود نظام مراقبة
        has_monitoring = context.get("monitoring", False)
        if not has_monitoring:
            return {
                "compliant": False,
                "reason": "نظام المراقبة غير موجود",
                "severity": "high"
            }
        
        # 2. التحقق من التنبؤ بالأعطال
        predicts_failures = context.get("predicts_failures", False)
        if not predicts_failures:
            return {
                "compliant": False,
                "reason": "لا تتنبأ بالأعطال قبل حدوثها",
                "severity": "medium"
            }
        
        # 3. التحقق من وجود تنبيهات استباقية
        has_alerts = context.get("proactive_alerts", False)
        if not has_alerts:
            return {
                "compliant": False,
                "reason": "لا توجد تنبيهات استباقية",
                "severity": "low"
            }
        
        return {"compliant": True}
    
    def _check_self_sustainability(self, context: Dict) -> Dict:
        """التحقق من الاستدامة الذاتية."""
        # 1. التحقق من إعادة تدوير الموارد
        recycles_resources = context.get("recycles_resources", False)
        if not recycles_resources:
            return {
                "compliant": False,
                "reason": "لا تعيد تدوير الموارد",
                "severity": "medium"
            }
        
        # 2. التحقق من كفاءة الطاقة
        energy_efficient = context.get("energy_efficient", False)
        if not energy_efficient:
            return {
                "compliant": False,
                "reason": "ليست موفرة للطاقة",
                "severity": "low"
            }
        
        return {"compliant": True}
    
    # ===== واجهات عامة =====
    
    def enforce_all(self, context: Dict) -> Dict:
        """تطبيق جميع القوانين التقنية والأمنية."""
        results = {}
        all_compliant = True
        
        for law_id, law in self.laws.items():
            result = law.check(context)
            results[law_id] = result
            if not result.get("compliant", True):
                all_compliant = False
        
        self.enforcement_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "context": context,
            "results": results,
            "all_compliant": all_compliant
        })
        
        # تحديث مستوى الأمان
        if all_compliant:
            self.security_level = min(1.0, self.security_level + 0.02)
        else:
            self.security_level = max(0.0, self.security_level - 0.01)
        
        return {
            "results": results,
            "all_compliant": all_compliant,
            "security_level": round(self.security_level, 3)
        }
    
    def get_law_status(self) -> Dict:
        """حالة جميع القوانين التقنية والأمنية."""
        return {
            "total_laws": len(self.laws),
            "laws": {law_id: law.to_dict() for law_id, law in self.laws.items()},
            "total_enforcements": len(self.enforcement_history),
            "security_level": round(self.security_level, 3)
        }
    
    def get_violations(self, law_id: str = None) -> List[Dict]:
        """استرجاع الانتهاكات التقنية والأمنية."""
        if law_id:
            law = self.laws.get(law_id)
            return law.violations if law else []
        
        all_violations = []
        for law in self.laws.values():
            all_violations.extend(law.violations)
        return all_violations

# ============================================================
# 3. نظام كشف الشذوذ المتقدم (Anomaly Detection)
# ============================================================

class AnomalyDetectionEngine:
    """
    يكتشف الأنماط غير الطبيعية في النظام قبل أن تصبح تهديدات.
    """
    
    def __init__(self):
        self.baseline = {}
        self.anomalies: List[Dict] = []
        self.threshold = 0.7
    
    def detect(self, system_metrics: Dict) -> List[Dict]:
        """
        كشف الشذوذ في مقاييس النظام.
        """
        anomalies = []
        
        # 1. تحليل استخدام المعالج
        cpu_usage = system_metrics.get("cpu_percent", 0)
        if cpu_usage > 90:
            anomalies.append({
                "type": "high_cpu_usage",
                "value": cpu_usage,
                "severity": "high",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # 2. تحليل استخدام الذاكرة
        memory_usage = system_metrics.get("memory_percent", 0)
        if memory_usage > 85:
            anomalies.append({
                "type": "high_memory_usage",
                "value": memory_usage,
                "severity": "medium",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # 3. تحليل معدل الأخطاء
        error_rate = system_metrics.get("error_rate", 0)
        if error_rate > 5:  # 5% معدل أخطاء
            anomalies.append({
                "type": "high_error_rate",
                "value": error_rate,
                "severity": "critical",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # 4. تحليل وقت الاستجابة
        response_time = system_metrics.get("response_time_ms", 0)
        if response_time > 1000:  # 1 ثانية
            anomalies.append({
                "type": "high_response_time",
                "value": response_time,
                "severity": "medium",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        if anomalies:
            self.anomalies.extend(anomalies)
        
        return anomalies
    
    def predict_future_anomaly(self, metrics_history: List[Dict]) -> Dict:
        """
        توقع الشذوذ المستقبلي بناءً على التاريخ.
        """
        # محاكاة: في الإنتاج سيتم استخدام نماذج تنبؤية
        if len(metrics_history) < 5:
            return {"probability": 0.1, "type": "insufficient_data"}
        
        # حساب اتجاهات
        cpu_trend = self._calculate_trend(metrics_history, "cpu_percent")
        memory_trend = self._calculate_trend(metrics_history, "memory_percent")
        
        if cpu_trend > 0.5 and memory_trend > 0.5:
            return {
                "probability": 0.8,
                "type": "resource_exhaustion",
                "expected_in_minutes": 30,
                "recommendation": "زيادة الموارد أو تقليل الحمل"
            }
        elif cpu_trend > 0.3:
            return {
                "probability": 0.6,
                "type": "high_cpu_forecast",
                "expected_in_minutes": 45,
                "recommendation": "مراقبة المعالج"
            }
        else:
            return {"probability": 0.2, "type": "stable"}
    
    def _calculate_trend(self, history: List[Dict], metric: str) -> float:
        """حساب اتجاه مقياس معين."""
        values = [h.get(metric, 0) for h in history[-10:]]
        if len(values) < 2:
            return 0.0
        
        # اتجاه بسيط (زيادة أو نقصان)
        first = values[0] if values else 0
        last = values[-1] if values else 0
        
        if first == 0:
            return 0.0
        
        return (last - first) / first

# ============================================================
# 4. نقاط النهاية API
# ============================================================

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v2/technical-security", tags=["Technical & Security"])

_engine = None
_anomaly = None

def get_engine() -> TechnicalSecurityEngine:
    global _engine
    if _engine is None:
        _engine = TechnicalSecurityEngine()
    return _engine

def get_anomaly() -> AnomalyDetectionEngine:
    global _anomaly
    if _anomaly is None:
        _anomaly = AnomalyDetectionEngine()
    return _anomaly

@router.get("/laws")
async def get_all_laws():
    """جميع القوانين التقنية والأمنية."""
    engine = get_engine()
    return {
        "laws": {law_id: law.to_dict() for law_id, law in engine.laws.items()},
        "total": len(engine.laws)
    }

@router.get("/laws/{law_id}")
async def get_law(law_id: str):
    """قانون تقني أو أمني معين."""
    engine = get_engine()
    law = engine.laws.get(law_id)
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")
    return law.to_dict()

@router.post("/enforce")
async def enforce_laws(context: Dict):
    """تطبيق جميع القوانين التقنية والأمنية."""
    engine = get_engine()
    return engine.enforce_all(context)

@router.get("/violations")
async def get_violations(law_id: str = None):
    """استرجاع الانتهاكات التقنية والأمنية."""
    engine = get_engine()
    return {"violations": engine.get_violations(law_id)}

@router.get("/status")
async def get_status():
    """حالة محرك القوانين التقنية والأمنية."""
    engine = get_engine()
    return engine.get_law_status()

@router.get("/security-level")
async def get_security_level():
    """مستوى الأمان الحالي."""
    engine = get_engine()
    return {"security_level": engine.security_level}

@router.post("/anomaly/detect")
async def detect_anomaly(metrics: Dict):
    """كشف الشذوذ في النظام."""
    anomaly = get_anomaly()
    return {"anomalies": anomaly.detect(metrics)}

@router.post("/anomaly/predict")
async def predict_anomaly(history: List[Dict]):
    """توقع الشذوذ المستقبلي."""
    anomaly = get_anomaly()
    return {"prediction": anomaly.predict_future_anomaly(history)}
