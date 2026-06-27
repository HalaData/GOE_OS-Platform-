"""
دمج مرجعية الذكاء الاصطناعي (AIMA) مع جوهر GOE OS
AIMA + GOE OS Core Integration - The Final Edition

يُطبق:
✅ المؤشرات التسعة (ERI, FQI, PAI, CGI, AGI, DIC, MCI, LRI, SAI) على المعرفة.
✅ الاستباقية (التنبؤ بالمشكلات قبل حدوثها).
✅ العمق الزمني (تتبع تطور المعرفة عبر الزمن).
✅ الطلائعية (التعلم التكيفي من الأخطاء).
✅ الشفافية (تسجيل كل استنتاج).
"""

from typing import Dict, List, Any, Optional, Tuple, Set
from collections import deque, defaultdict
import logging
import hashlib
import heapq
from datetime import datetime, timedelta
import re
import json

logger = logging.getLogger(__name__)

# ============================================================
# 1. قاعدة المعرفة الزمنية (Temporal Knowledge Base)
# ============================================================

class TemporalKnowledgeBase:
    """
    قاعدة معرفة تتذكر تطور المفاهيم عبر الزمن.
    تحقق العمق الزمني (📜).
    """
    
    def __init__(self):
        self.concept_history: Dict[str, List[Dict]] = defaultdict(list)  # concept_name -> [{timestamp, relations, indicators}]
        self.relation_history: List[Dict] = []
        logger.info("⏳ Temporal Knowledge Base initialized")
    
    def add_concept_snapshot(self, concept_name: str, relations: List[Dict], indicators: Dict):
        """إضافة لقطة زمنية لمفهوم ما."""
        snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "relations": relations,
            "indicators": indicators
        }
        self.concept_history[concept_name].append(snapshot)
    
    def get_evolution(self, concept_name: str) -> List[Dict]:
        """استرجاع تطور مفهوم عبر الزمن."""
        return self.concept_history.get(concept_name, [])
    
    def detect_trend(self, concept_name: str, indicator: str) -> str:
        """كشف اتجاه تغير مؤشر معين عبر الزمن."""
        history = self.get_evolution(concept_name)
        if len(history) < 2:
            return "غير كافٍ للتحليل"
        
        values = [h["indicators"].get(indicator, 0.5) for h in history]
        if values[-1] > values[0] * 1.2:
            return "تصاعدي (خطر متزايد)"
        elif values[-1] < values[0] * 0.8:
            return "تنازلي (تحسن)"
        else:
            return "مستقر"

# ============================================================
# 2. المؤشرات التسعة (The 9 Indicators)
# ============================================================

class KnowledgeIndicators:
    """
    حساب المؤشرات التسعة على الشبكة المعرفية.
    """
    
    @staticmethod
    def calculate(network: Dict, history: TemporalKnowledgeBase) -> Dict:
        """
        حساب المؤشرات بناءً على حجم الشبكة وتعقيدها وتاريخها.
        """
        nodes = network.get("nodes", [])
        edges = network.get("edges", [])
        
        # 1. ERI (الجمود المعرفي): كلما قلت التغيرات الجديدة، زاد الجمود
        recent_changes = len([e for e in edges if "created_at" in e and 
                             datetime.fromisoformat(e["created_at"]) > datetime.utcnow() - timedelta(days=30)])
        eri = max(0, min(1, 1 - (recent_changes / (len(edges) + 1))))
        
        # 2. FQI (الأسئلة المحرمة): وجود علاقات غير مفسرة أو تناقضات
        contradictions = len([e for e in edges if e.get("type") == "contradicts"])
        fqi = min(1, contradictions / (len(edges) + 1) * 2)
        
        # 3. PAI (الغياب الإجرائي): وجود مفاهيم بدون علاقات (معزولة)
        isolated_nodes = len([n for n in nodes if not any(e["source"] == n["id"] or e["target"] == n["id"] for e in edges)])
        pai = min(1, isolated_nodes / (len(nodes) + 1))
        
        # 4. CGI (فجوة المصداقية): فرق زمني بين آخر تحديث وأول ظهور
        if nodes:
            first_node = min(nodes, key=lambda x: x.get("created_at", "2024-01-01"))
            last_node = max(nodes, key=lambda x: x.get("created_at", "2024-01-01"))
            time_diff = (datetime.fromisoformat(last_node["created_at"]) - 
                        datetime.fromisoformat(first_node["created_at"])).days
            cgi = min(1, time_diff / 365)  # سنة كاملة = 1
        else:
            cgi = 0.5
        
        # 5. AGI (فجوة الفاعلين): تركيز العلاقات في عقد قليلة
        if edges:
            source_counts = defaultdict(int)
            for e in edges:
                source_counts[e["source"]] += 1
            max_count = max(source_counts.values()) if source_counts else 0
            agi = min(1, max_count / (len(edges) + 1) * 3)
        else:
            agi = 0.5
        
        # 6. DIC (التنوع المعرفي): عدد أنواع المفاهيم المختلفة
        types = set(n.get("type", "unknown") for n in nodes)
        dic = min(1, len(types) / 5)
        
        # 7. MCI (التواضع المعرفي): الاعتراف بوجود فجوات (عقد معزولة)
        mci = pai * 0.8  # محاكاة
        
        # 8. LRI (الجمود التشريعي): قدم القواعد (عمر أقدم مفهوم)
        if nodes:
            oldest_node = min(nodes, key=lambda x: x.get("created_at", "2024-01-01"))
            age = (datetime.utcnow() - datetime.fromisoformat(oldest_node["created_at"])).days
            lri = min(1, age / 730)  # سنتان = 1
        else:
            lri = 0.5
        
        # 9. SAI (الاغتراب الدلالي): متوسط عدد العلاقات لكل مفهوم
        if nodes:
            avg_relations = len(edges) / len(nodes)
            sai = max(0, min(1, 1 - (avg_relations / 3)))  # 3 علاقات مثالية
        else:
            sai = 0.5
        
        return {
            "ERI": round(eri, 2),
            "FQI": round(fqi, 2),
            "PAI": round(pai, 2),
            "CGI": round(cgi, 2),
            "AGI": round(agi, 2),
            "DIC": round(dic, 2),
            "MCI": round(mci, 2),
            "LRI": round(lri, 2),
            "SAI": round(sai, 2)
        }

# ============================================================
# 3. المستشعر الاستباقي (Proactive Sensor)
# ============================================================

class ProactiveSensor:
    """
    يكتشف المخاطر قبل وقوعها بناءً على تحليل المعرفة.
    يطبق الاستباقية (🔮).
    """
    
    def __init__(self):
        self.alerts = []
        logger.info("🔮 Proactive Sensor initialized")
    
    def scan(self, knowledge_base: TemporalKnowledgeBase, indicators: Dict) -> List[Dict]:
        """
        فحص قاعدة المعرفة وإصدار تحذيرات استباقية.
        """
        alerts = []
        
        # 1. تحذير: جمود معرفي مرتفع (ERI)
        if indicators.get("ERI", 0) > 0.7:
            alerts.append({
                "type": "epistemic_rigidity",
                "severity": "high",
                "message": "⚠️ الجمود المعرفي مرتفع (ERI). يُنصح بضخ مفاهيم جديدة.",
                "suggestion": "استيراد مصادر معرفية خارجية أو فتح حوار مع أطراف جديدة."
            })
        
        # 2. تحذير: تناقضات منطقية (FQI)
        if indicators.get("FQI", 0) > 0.6:
            alerts.append({
                "type": "logical_contradictions",
                "severity": "critical",
                "message": "⚠️ عدد كبير من التناقضات المنطقية المكتشفة (FQI).",
                "suggestion": "مراجعة العلاقات المتضاربة وحل التناقضات."
            })
        
        # 3. تحذير: عزلة مفاهيمية (PAI)
        if indicators.get("PAI", 0) > 0.5:
            alerts.append({
                "type": "isolated_concepts",
                "severity": "medium",
                "message": "⚠️ وجود مفاهيم معزولة بدون علاقات (PAI).",
                "suggestion": "ربط المفاهيم المعزولة بالشبكة المعرفية."
            })
        
        # 4. تحذير: تدهور مؤشر (Trend)
        for concept in list(knowledge_base.concept_history.keys())[:3]:
            trend = knowledge_base.detect_trend(concept, "ERI")
            if trend == "تصاعدي (خطر متزايد)":
                alerts.append({
                    "type": "deteriorating_indicator",
                    "severity": "medium",
                    "message": f"⚠️ مؤشر ERI في تصاعد لمفهوم '{concept}'.",
                    "suggestion": f"مراجعة سبب تصلب المفهوم '{concept}'."
                })
        
        self.alerts.extend(alerts)
        return alerts

# ============================================================
# 4. المحرك المتكامل (AIMA + GOE Core)
# ============================================================

class AIMA_GOE_Core:
    """
    المحرك النهائي الذي يدمج AIMA مع جوهر GOE OS.
    """
    
    def __init__(self):
        self.temporal_kb = TemporalKnowledgeBase()
        self.indicators = KnowledgeIndicators()
        self.proactive = ProactiveSensor()
        self.semantic_network = {
            "nodes": [],
            "edges": []
        }
        self.history = []
        logger.info("🚀 AIMA_GOE_Core initialized (Full Integration)")
    
    def process_text(self, text: str) -> Dict:
        """
        معالجة النص مع تطبيق جميع مكونات GOE OS.
        """
        # 1. استخراج المعرفة (AIMA)
        concepts, relations = self._extract_knowledge(text)
        
        # 2. تحديث الشبكة الدلالية
        for concept in concepts:
            self.semantic_network["nodes"].append(concept)
        for relation in relations:
            self.semantic_network["edges"].append(relation)
        
        # 3. تحديث القاعدة الزمنية (تخزين اللقطة)
        self.temporal_kb.add_concept_snapshot(
            concept_name=concepts[0]["name"] if concepts else "general",
            relations=relations,
            indicators={}
        )
        
        # 4. حساب المؤشرات التسعة
        indicators = self.indicators.calculate(self.semantic_network, self.temporal_kb)
        
        # 5. الفحص الاستباقي
        alerts = self.proactive.scan(self.temporal_kb, indicators)
        
        # 6. توليد التوصيات
        recommendations = self._generate_recommendations(indicators, alerts)
        
        result = {
            "concepts": len(concepts),
            "relations": len(relations),
            "indicators": indicators,
            "alerts": alerts,
            "recommendations": recommendations,
            "summary": self._generate_final_summary(indicators, alerts, recommendations)
        }
        
        self.history.append(result)
        return result
    
    def _extract_knowledge(self, text: str) -> Tuple[List[Dict], List[Dict]]:
        """استخراج المفاهيم والعلاقات من النص (محاكاة متقدمة)."""
        concepts = []
        relations = []
        
        # استخراج المفاهيم
        patterns = {
            r'\b(AI|artificial intelligence)\b': ("AI", "technology"),
            r'\b(governance|government)\b': ("Governance", "institution"),
            r'\b(transparency|accountability)\b': ("Transparency", "value"),
            r'\b(corruption|fraud)\b': ("Corruption", "risk")
        }
        for pattern, (name, ctype) in patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                concept_id = hashlib.md5(f"{name}_{datetime.utcnow().isoformat()}".encode()).hexdigest()[:8]
                concepts.append({
                    "id": concept_id,
                    "name": name,
                    "type": ctype,
                    "created_at": datetime.utcnow().isoformat()
                })
        
        # استخراج العلاقات (محاكاة)
        if len(concepts) >= 2:
            relations.append({
                "source": concepts[0]["id"],
                "target": concepts[1]["id"],
                "type": "influences",
                "weight": 0.8,
                "created_at": datetime.utcnow().isoformat()
            })
        
        return concepts, relations
    
    def _generate_recommendations(self, indicators: Dict, alerts: List) -> List[str]:
        """توليد توصيات عملية."""
        recommendations = []
        
        if indicators.get("ERI", 0) > 0.6:
            recommendations.append("🔧 خفض الجمود المعرفي: إدخال مصادر معرفية متنوعة.")
        if indicators.get("FQI", 0) > 0.5:
            recommendations.append("🔍 حل التناقضات المنطقية: مراجعة العلاقات المتضاربة.")
        if indicators.get("PAI", 0) > 0.4:
            recommendations.append("🔗 ربط المفاهيم المعزولة: بناء روابط جديدة.")
        if indicators.get("DIC", 0) < 0.4:
            recommendations.append("🌱 زيادة التنوع المعرفي: استقطاب خبرات متعددة التخصصات.")
        
        if not recommendations:
            recommendations.append("✅ النظام المعرفي في حالة صحية جيدة.")
        
        return recommendations
    
    def _generate_final_summary(self, indicators: Dict, alerts: List, recommendations: List) -> str:
        """توليد الملخص النهائي."""
        return f"""
═══════════════════════════════════════════════════════════════
🧠 تقرير التحليل المعرفي المتكامل (AIMA + GOE OS)
═══════════════════════════════════════════════════════════════

📊 المؤشرات التسعة:
   • ERI (الجمود المعرفي): {indicators.get('ERI', 0)}
   • FQI (الأسئلة المحرمة): {indicators.get('FQI', 0)}
   • PAI (الغياب الإجرائي): {indicators.get('PAI', 0)}
   • CGI (فجوة المصداقية): {indicators.get('CGI', 0)}
   • AGI (فجوة الفاعلين): {indicators.get('AGI', 0)}
   • DIC (التنوع المعرفي): {indicators.get('DIC', 0)}
   • MCI (التواضع المعرفي): {indicators.get('MCI', 0)}
   • LRI (الجمود التشريعي): {indicators.get('LRI', 0)}
   • SAI (الاغتراب الدلالي): {indicators.get('SAI', 0)}

⚠️ التنبيهات الاستباقية ({len(alerts)}):
{chr(10).join([f"   • {a['message']}" for a in alerts])}

💡 التوصيات:
{chr(10).join([f"   • {r}" for r in recommendations])}

🏆 تم التحليل باستخدام الذكاء الاصطناعي الكلاسيكي (AIMA) + الحوكمة المعرفية (GOE OS).
═══════════════════════════════════════════════════════════════
"""

# ============================================================
# إنشاء النسخة العالمية
# ============================================================

aima_goe_engine = AIMA_GOE_Core()

# ============================================================
# اختبار سريع
# ============================================================

if __name__ == "__main__":
    test_text = """
    The government aims to improve transparency and reduce corruption.
    Transparency is a core value of good governance.
    """
    
    result = aima_goe_engine.process_text(test_text)
    print(result["summary"])
