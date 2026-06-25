"""
طبقة التطور المؤسسي - Enterprise Evolution Layer
تحول المؤسسة إلى كيان حي يتطور ذاتياً بالتفاعل مع المنصة
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import logging
import hashlib
import random
import time
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

# ============================================================
# 1. الذاكرة المؤسسية (Enterprise Memory)
# ============================================================

class EnterpriseMemory:
    """
    ذاكرة المؤسسة - تسجل كل ما يحدث وتتعلم منه
    """
    
    def __init__(self):
        self.events = []
        self.lessons = []
        self.patterns = defaultdict(int)
        self.decisions = []
    
    def record_event(self, event_type: str, event_data: Dict) -> str:
        """
        تسجيل حدث في ذاكرة المؤسسة
        """
        event_id = hashlib.md5(f"{event_type}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16]
        
        event = {
            "id": event_id,
            "type": event_type,
            "data": event_data,
            "timestamp": datetime.utcnow().isoformat(),
            "importance": self._calculate_importance(event_type, event_data)
        }
        
        self.events.append(event)
        self._extract_patterns(event)
        self._learn_lesson(event)
        
        return event_id
    
    def _calculate_importance(self, event_type: str, event_data: Dict) -> float:
        """حساب أهمية الحدث"""
        importance = 0.5
        
        if event_type == "decision":
            importance = 0.9
        elif event_type == "anomaly":
            importance = 0.8
        elif event_type == "feedback":
            importance = 0.6
        
        if "critical" in event_data.get("tags", []):
            importance = 1.0
        
        return importance
    
    def _extract_patterns(self, event: Dict):
        """استخراج الأنماط من الأحداث"""
        key = f"{event['type']}_{event['data'].get('category', 'general')}"
        self.patterns[key] += 1
    
    def _learn_lesson(self, event: Dict):
        """استخلاص درس من الحدث"""
        if event["importance"] > 0.7:
            lesson = {
                "from_event": event["id"],
                "lesson": self._extract_lesson(event),
                "timestamp": datetime.utcnow().isoformat()
            }
            self.lessons.append(lesson)
    
    def _extract_lesson(self, event: Dict) -> str:
        """استخلاص الدرس من الحدث"""
        if event["type"] == "decision" and event["data"].get("outcome") == "success":
            return f"القرار {event['data'].get('decision', 'غير معروف')} كان ناجحاً"
        elif event["type"] == "decision" and event["data"].get("outcome") == "failure":
            return f"القرار {event['data'].get('decision', 'غير معروف')} يحتاج إلى مراجعة"
        elif event["type"] == "anomaly":
            return f"تم اكتشاف شذوذ: {event['data'].get('description', '')}"
        else:
            return f"حدث {event['type']} تم تسجيله"

# ============================================================
# 2. مولد المعرفة المؤسسية (Enterprise Knowledge Generator)
# ============================================================

class EnterpriseKnowledgeGenerator:
    """
    يولد معرفة جديدة خاصة بالمؤسسة (كتب، استراتيجيات، تقارير)
    """
    
    def __init__(self, memory: EnterpriseMemory):
        self.memory = memory
        self.knowledge_products = []
    
    def generate_book(self, enterprise_id: str, theme: str) -> Dict:
        """
        توليد كتاب مخصص للمؤسسة
        """
        lessons = self.memory.lessons[-20:]  # آخر 20 درساً
        
        book = {
            "enterprise_id": enterprise_id,
            "title": f"رحلة {enterprise_id} في الحوكمة المعرفية",
            "chapters": [
                {
                    "title": "التشخيص الأولي",
                    "content": self._generate_diagnosis_chapter(lessons)
                },
                {
                    "title": "التحديات والتغلب عليها",
                    "content": self._generate_challenges_chapter(lessons)
                },
                {
                    "title": "الاستراتيجيات الناجحة",
                    "content": self._generate_strategies_chapter(lessons)
                },
                {
                    "title": "الدروس المستفادة",
                    "content": self._generate_lessons_chapter(lessons)
                },
                {
                    "title": "الخطوات القادمة",
                    "content": self._generate_future_chapter(lessons)
                }
            ],
            "generated_at": datetime.utcnow().isoformat(),
            "relevance": self._calculate_relevance(lessons)
        }
        
        self.knowledge_products.append(book)
        return book
    
    def _generate_diagnosis_chapter(self, lessons: List) -> str:
        """توليد فصل التشخيص"""
        if not lessons:
            return "لم يتم جمع بيانات كافية للتشخيص بعد"
        return f"تم تحليل {len(lessons)} حدثاً لتحديد حالة المؤسسة الحالية"
    
    def _generate_challenges_chapter(self, lessons: List) -> str:
        """توليد فصل التحديات"""
        anomalies = [l for l in lessons if "شذوذ" in l["lesson"]]
        if anomalies:
            return f"تم اكتشاف {len(anomalies)} تحدياً رئيسياً يحتاج إلى معالجة"
        return "لم يتم اكتشاف تحديات كبيرة"
    
    def _generate_strategies_chapter(self, lessons: List) -> str:
        """توليد فصل الاستراتيجيات"""
        successes = [l for l in lessons if "ناجح" in l["lesson"]]
        if successes:
            return f"تم تحديد {len(successes)} استراتيجية ناجحة يمكن تعميمها"
        return "يوصى بتطوير استراتيجيات جديدة"
    
    def _generate_lessons_chapter(self, lessons: List) -> str:
        """توليد فصل الدروس المستفادة"""
        if not lessons:
            return "لم يتم استخلاص دروس كافية بعد"
        lessons_text = "\n".join([f"- {l['lesson']}" for l in lessons[-5:]])
        return f"الدروس المستفادة:\n{lessons_text}"
    
    def _generate_future_chapter(self, lessons: List) -> str:
        """توليد فصل المستقبل"""
        return "بناءً على التحليل، يوصى بالتركيز على تحسين الشفافية والتواصل الداخلي"
    
    def _calculate_relevance(self, lessons: List) -> float:
        """حساب مدى صلة الكتاب بالمؤسسة"""
        return min(1.0, len(lessons) / 20)

# ============================================================
# 3. المحرك التكيفي (Adaptive Engine)
# ============================================================

class AdaptiveEnterpriseEngine:
    """
    محرك تكيفي يغير المؤشرات والبروتوكولات حسب تطور المؤسسة
    """
    
    def __init__(self, memory: EnterpriseMemory):
        self.memory = memory
        self.adaptive_thresholds = {}
        self.evolution_stage = 1  # 1: بداية، 2: نمو، 3: نضج، 4: ريادة
    
    def adapt_indicators(self, current_indicators: Dict) -> Dict:
        """
        تكييف المؤشرات حسب مرحلة تطور المؤسسة
        """
        # تحليل مرحلة التطور
        self._determine_evolution_stage()
        
        adapted_indicators = current_indicators.copy()
        
        # تعديل العتبات حسب المرحلة
        if self.evolution_stage == 1:  # بداية
            adapted_indicators["thresholds"] = {
                "ERI": 0.7,
                "FQI": 0.3,
                "PAI": 0.5,
                "CGI": 0.6
            }
        elif self.evolution_stage == 2:  # نمو
            adapted_indicators["thresholds"] = {
                "ERI": 0.6,
                "FQI": 0.4,
                "PAI": 0.4,
                "CGI": 0.5
            }
        elif self.evolution_stage == 3:  # نضج
            adapted_indicators["thresholds"] = {
                "ERI": 0.5,
                "FQI": 0.5,
                "PAI": 0.3,
                "CGI": 0.4
            }
        else:  # ريادة
            adapted_indicators["thresholds"] = {
                "ERI": 0.4,
                "FQI": 0.6,
                "PAI": 0.2,
                "CGI": 0.3
            }
        
        return adapted_indicators
    
    def _determine_evolution_stage(self):
        """تحديد مرحلة تطور المؤسسة"""
        total_events = len(self.memory.events)
        unique_patterns = len(self.memory.patterns)
        lessons_count = len(self.memory.lessons)
        
        if total_events < 50:
            self.evolution_stage = 1
        elif total_events < 200:
            self.evolution_stage = 2
        elif total_events < 500:
            self.evolution_stage = 3
        else:
            self.evolution_stage = 4
        
        # تعديل حسب الأنماط والدروس
        if unique_patterns > 10 and lessons_count > 5:
            self.evolution_stage = min(4, self.evolution_stage + 1)

# ============================================================
# 4. المحرك المؤسسي الحي (Living Enterprise Engine)
# ============================================================

class LivingEnterpriseEngine:
    """
    المحرك المؤسسي الحي - يجمع جميع المكونات في نظام حي متكامل
    """
    
    def __init__(self):
        self.memory = EnterpriseMemory()
        self.knowledge = EnterpriseKnowledgeGenerator(self.memory)
        self.adaptive = AdaptiveEnterpriseEngine(self.memory)
        self.living_history = []
    
    def process_event(self, enterprise_id: str, event_type: str, event_data: Dict) -> Dict:
        """
        معالجة حدث جديد وتحديث ذاكرة المؤسسة
        """
        # 1. تسجيل الحدث في الذاكرة
        event_id = self.memory.record_event(event_type, event_data)
        
        # 2. تحليل التأثير
        impact = self._analyze_impact(event_type, event_data)
        
        # 3. توليد توصيات فورية
        recommendations = self._generate_recommendations(event_type, event_data)
        
        # 4. تحديث التكيف
        current_indicators = self._get_current_indicators(enterprise_id)
        adapted_indicators = self.adaptive.adapt_indicators(current_indicators)
        
        # 5. توليد معرفة جديدة (إذا لزم الأمر)
        knowledge = None
        if len(self.memory.events) % 10 == 0:
            knowledge = self.knowledge.generate_book(enterprise_id, "التطور المؤسسي")
        
        result = {
            "enterprise_id": enterprise_id,
            "event_id": event_id,
            "impact": impact,
            "recommendations": recommendations,
            "adapted_indicators": adapted_indicators,
            "knowledge": knowledge,
            "evolution_stage": self.adaptive.evolution_stage,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.living_history.append(result)
        return result
    
    def _analyze_impact(self, event_type: str, event_data: Dict) -> Dict:
        """تحليل تأثير الحدث"""
        return {
            "severity": "high" if event_type == "critical" else "medium",
            "category": event_data.get("category", "general"),
            "learning_opportunity": self._is_learning_opportunity(event_type, event_data)
        }
    
    def _is_learning_opportunity(self, event_type: str, event_data: Dict) -> bool:
        """تحديد ما إذا كان الحدث فرصة للتعلم"""
        return event_type in ["anomaly", "feedback", "decision"]
    
    def _generate_recommendations(self, event_type: str, event_data: Dict) -> List[str]:
        """توليد توصيات فورية"""
        recommendations = []
        
        if event_type == "anomaly":
            recommendations.append("🔍 دراسة الشذوذ لتحديد السبب الجذري")
        elif event_type == "feedback" and event_data.get("sentiment") == "negative":
            recommendations.append("💬 عقد جلسة استماع مع الفريق المتأثر")
        elif event_type == "decision" and event_data.get("outcome") == "failure":
            recommendations.append("📝 مراجعة عملية اتخاذ القرار وتعديلها")
        
        return recommendations
    
    def _get_current_indicators(self, enterprise_id: str) -> Dict:
        """الحصول على المؤشرات الحالية للمؤسسة"""
        # محاكاة: في الواقع ستُجلَب من قاعدة البيانات
        return {
            "ERI": 0.6,
            "FQI": 0.4,
            "PAI": 0.3,
            "CGI": 0.5
        }
    
    def get_evolution_status(self, enterprise_id: str) -> Dict:
        """
        الحالة الكاملة لتطور المؤسسة
        """
        return {
            "enterprise_id": enterprise_id,
            "total_events": len(self.memory.events),
            "total_lessons": len(self.memory.lessons),
            "unique_patterns": len(self.memory.patterns),
            "evolution_stage": self.adaptive.evolution_stage,
            "knowledge_products": len(self.knowledge.knowledge_products),
            "stage_name": self._get_stage_name(self.adaptive.evolution_stage)
        }
    
    def _get_stage_name(self, stage: int) -> str:
        """الحصول على اسم المرحلة"""
        stages = {
            1: "بداية (البذرة)",
            2: "نمو (النبتة)",
            3: "نضج (الشجرة)",
            4: "ريادة (الغابة)"
        }
        return stages.get(stage, "غير معروف")

# ============================================================
# 5. نقاط النهاية API
# ============================================================

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v2/enterprise-evolution", tags=["Enterprise Evolution"])

_living_engine = None

def get_living_engine() -> LivingEnterpriseEngine:
    global _living_engine
    if _living_engine is None:
        _living_engine = LivingEnterpriseEngine()
    return _living_engine

@router.post("/event")
async def process_event(enterprise_id: str, event_type: str, event_data: Dict):
    """معالجة حدث جديد وتحديث ذاكرة المؤسسة"""
    engine = get_living_engine()
    return engine.process_event(enterprise_id, event_type, event_data)

@router.get("/memory/{enterprise_id}")
async def get_memory(enterprise_id: str, limit: int = 50):
    """الحصول على ذاكرة المؤسسة"""
    engine = get_living_engine()
    return {
        "enterprise_id": enterprise_id,
        "events": engine.memory.events[-limit:],
        "patterns": dict(engine.memory.patterns),
        "lessons": engine.memory.lessons[-20:]
    }

@router.get("/knowledge/{enterprise_id}")
async def get_knowledge(enterprise_id: str):
    """الحصول على المعرفة المولدة للمؤسسة"""
    engine = get_living_engine()
    return {
        "enterprise_id": enterprise_id,
        "books": engine.knowledge.knowledge_products,
        "total": len(engine.knowledge.knowledge_products)
    }

@router.get("/evolution/{enterprise_id}")
async def get_evolution(enterprise_id: str):
    """الحالة الكاملة لتطور المؤسسة"""
    engine = get_living_engine()
    return engine.get_evolution_status(enterprise_id)

@router.post("/generate-book")
async def generate_book(enterprise_id: str, theme: str):
    """توليد كتاب مخصص للمؤسسة"""
    engine = get_living_engine()
    # محاكاة: في الواقع سيتم استخدام المعرفة المتراكمة
    book = engine.knowledge.generate_book(enterprise_id, theme)
    return book
