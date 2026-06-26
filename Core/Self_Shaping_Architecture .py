"""
التشكيل الذاتي - Self-Shaping Architecture
الوحدات تعيد تشكيل نفسها، تندمج، أو تخلق وحدات جديدة حسب السياق
"""

from typing import Dict, List, Any
from datetime import datetime
import random
import hashlib
import logging

logger = logging.getLogger(__name__)

class SelfShapingEngine:
    """
    هندسة معمارية تتشكل ذاتياً: وحدات تتكيف، تندمج، أو تولد جديدة.
    """
    
    def __init__(self):
        self.unit_history = []
        self.knowledge_gaps = []
    
    def reform_unit(self, unit: Dict) -> Dict:
        """إعادة تشكيل وحدة غير مستخدمة."""
        reformed = unit.copy()
        reformed["reformed_at"] = datetime.utcnow().isoformat()
        reformed["version"] = f"{float(unit.get('version', 1.0)) + 0.1:.1f}"
        reformed["status"] = "reformed"
        reformed["description"] = f"تم إعادة تشكيل: {unit.get('name', 'unnamed')}"
        logger.info(f"🔄 Unit reformed: {unit.get('id', 'unknown')}")
        return reformed
    
    def merge_units(self, unit_a: Dict, unit_b: Dict) -> Dict:
        """دمج وحدتين متشابهتين."""
        merged = {
            "id": hashlib.md5(f"{unit_a.get('id')}_{unit_b.get('id')}".encode()).hexdigest()[:8],
            "name": f"{unit_a.get('name', '')}_{unit_b.get('name', '')}",
            "type": "merged",
            "capabilities": list(set(unit_a.get("capabilities", []) + unit_b.get("capabilities", []))),
            "version": max(float(unit_a.get("version", 1.0)), float(unit_b.get("version", 1.0))),
            "created_at": datetime.utcnow().isoformat(),
            "merged_from": [unit_a.get("id"), unit_b.get("id")]
        }
        logger.info(f"🔗 Units merged: {unit_a.get('id')} + {unit_b.get('id')} -> {merged['id']}")
        return merged
    
    def create_unit_for_gap(self, gap: Dict) -> Dict:
        """خلق وحدة جديدة لسد فجوة معرفية."""
        new_unit = {
            "id": hashlib.md5(f"{gap.get('description')}_{datetime.utcnow().timestamp()}".encode()).hexdigest()[:8],
            "name": f"gap_solver_{gap.get('id', 'unknown')}",
            "type": "generated",
            "purpose": gap.get("description", "سد فجوة معرفية"),
            "capabilities": gap.get("required_capabilities", ["analysis", "synthesis"]),
            "version": 1.0,
            "created_at": datetime.utcnow().isoformat(),
            "status": "active"
        }
        logger.info(f"🧬 New unit created for gap: {gap.get('description', 'unknown')}")
        return new_unit
    
    def detect_knowledge_gaps(self, current_units: List[Dict], usage_data: Dict) -> List[Dict]:
        """كشف الفجوات المعرفية بناءً على استخدام الوحدات."""
        gaps = []
        
        # كشف الفجوات: إذا كانت هناك مواضيع غير مغطاة
        topics = set()
        for unit in current_units:
            topics.update(unit.get("capabilities", []))
        
        required_topics = {"analysis", "synthesis", "prediction", "diagnosis", "remediation"}
        missing_topics = required_topics - topics
        
        for topic in missing_topics:
            gaps.append({
                "id": hashlib.md5(topic.encode()).hexdigest()[:6],
                "description": f"فجوة في قدرة {topic}",
                "required_capabilities": [topic, "processing", "integration"],
                "severity": "high" if topic in ["analysis", "diagnosis"] else "medium"
            })
        
        self.knowledge_gaps.extend(gaps)
        return gaps
    
    def shape_architecture(self, current_units: List[Dict], usage_data: Dict) -> List[Dict]:
        """الدورة الكاملة للتشكيل الذاتي."""
        new_units = []
        
        # 1. إعادة تشكيل الوحدات غير المستخدمة
        for unit in current_units:
            if usage_data.get(unit["id"], 0) < 10:
                reformed = self.reform_unit(unit)
                new_units.append(reformed)
            else:
                new_units.append(unit)
        
        # 2. دمج الوحدات المتشابهة
        # محاكاة: إذا كان هناك وحدتان متشابهتان، ندمجهما
        if len(new_units) > 5 and random.random() > 0.5:
            merged = self.merge_units(new_units[0], new_units[1])
            new_units = [merged] + new_units[2:]
        
        # 3. كشف الفجوات وإنشاء وحدات جديدة
        gaps = self.detect_knowledge_gaps(new_units, usage_data)
        for gap in gaps[:2]:  # حد أقصى وحدتين جديدتين
            new_unit = self.create_unit_for_gap(gap)
            new_units.append(new_unit)
        
        logger.info(f"🏗️ Architecture shaped: {len(current_units)} -> {len(new_units)} units")
        return new_units
