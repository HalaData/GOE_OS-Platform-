"""
السيلان المعرفي - Cognitive Fluidity
المعرفة كسائل يتدفق ويتشكل حسب السياق
"""

from typing import Dict, List, Any
import random
import logging

logger = logging.getLogger(__name__)

class CognitiveFluidityEngine:
    """
    المعرفة ليست جامدة، بل سائل يتشكل حسب الحاوية (السياق).
    """
    
    def __init__(self):
        self.knowledge_streams = []
    
    def simplify(self, knowledge: Dict) -> Dict:
        """تبسيط المعرفة للمبتدئين."""
        simplified = {
            "title": knowledge.get("title", "معرفة"),
            "summary": knowledge.get("summary", knowledge.get("content", ""))[:200],
            "key_points": knowledge.get("key_points", [])[:3],
            "complexity": 0.2,
            "audience": "beginner"
        }
        return simplified
    
    def complexify(self, knowledge: Dict) -> Dict:
        """تعقيد المعرفة للخبراء."""
        complexified = {
            "title": knowledge.get("title", "معرفة متقدمة"),
            "full_content": knowledge.get("content", ""),
            "detailed_analysis": knowledge.get("analysis", {}),
            "references": knowledge.get("references", []),
            "complexity": 0.9,
            "audience": "expert"
        }
        return complexified
    
    def condense(self, knowledge: Dict) -> Dict:
        """تكثيف المعرفة للحالات العاجلة."""
        condensed = {
            "title": knowledge.get("title", "خلاصة"),
            "one_liner": knowledge.get("summary", knowledge.get("content", ""))[:100],
            "action_items": knowledge.get("action_items", []),
            "urgency_score": 0.9,
            "complexity": 0.3
        }
        return condensed
    
    def expand(self, knowledge: Dict) -> Dict:
        """توسيع المعرفة للدراسة المتعمقة."""
        expanded = {
            "title": knowledge.get("title", "دراسة معمقة"),
            "full_content": knowledge.get("content", ""),
            "related_topics": knowledge.get("related", []),
            "case_studies": knowledge.get("case_studies", []),
            "exercises": knowledge.get("exercises", []),
            "complexity": 0.7,
            "audience": "researcher"
        }
        return expanded
    
    def fluidize_knowledge(self, knowledge: Dict, context: Dict) -> Dict:
        """إعادة تشكيل المعرفة حسب السياق."""
        audience = context.get("audience", "general")
        urgency = context.get("urgency", "normal")
        
        if audience == "beginner":
            result = self.simplify(knowledge)
        elif audience == "expert":
            result = self.complexify(knowledge)
        elif urgency == "high":
            result = self.condense(knowledge)
        elif context.get("depth") == "deep":
            result = self.expand(knowledge)
        else:
            result = knowledge.copy()
        
        result["fluidity_version"] = random.randint(1000, 9999)
        result["context_applied"] = audience if audience != "general" else urgency
        
        self.knowledge_streams.append({
            "original": knowledge.get("title", "unknown"),
            "transformed": result.get("title", result.get("one_liner", "transformed")),
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return result
