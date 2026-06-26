"""
GOE OS - محرك الخريطة الدلالية الذاتية (Self-Generating Semantic Layer)
يربط المصطلحات عبر التخصصات تلقائياً بناءً على تفاعلات المستخدم والمستندات.
"""

import hashlib
import json
import re
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Set, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class SemanticMapper:
    """
    يبني خريطة معرفية ديناميكية دون الحاجة إلى بنية تحتية ضخمة.
    """

    def __init__(self):
        self.term_graph: Dict[str, Set[str]] = defaultdict(set)  # مصطلح -> مصطلحات مرتبطة
        self.domain_connections: Dict[str, List[str]] = defaultdict(list)  # مجال -> مصطلحات رئيسية
        self.term_frequency: Dict[str, int] = defaultdict(int)
        self.term_cooccurrence: Dict[Tuple[str, str], int] = defaultdict(int)  # تكرار ظهور مصطلحين معاً
        self.processed_docs = 0
        logger.info("🧠 Semantic Mapper initialized (Zero-cost Knowledge Graph)")

    def process_text(self, text: str, domain: str, doc_id: Optional[str] = None):
        """
        معالجة نص جديد واستخراج العلاقات الدلالية تلقائياً.
        """
        if not text or len(text) < 20:
            return

        self.processed_docs += 1
        
        # 1. استخراج المصطلحات المفتاحية
        terms = self._extract_key_terms(text)
        if len(terms) < 2:
            return

        # 2. تحديث تردد المصطلحات
        for term in terms:
            self.term_frequency[term] += 1

        # 3. تحديث التكرار المشترك (Co-occurrence)
        for i, term_i in enumerate(terms):
            for j, term_j in enumerate(terms):
                if i < j:
                    pair = tuple(sorted([term_i, term_j]))
                    self.term_cooccurrence[pair] += 1

        # 4. بناء العلاقات الدلالية (بناءً على التكرار المشترك)
        for (a, b), count in list(self.term_cooccurrence.items()):
            if count > 2:  # عتبة بسيطة
                self.term_graph[a].add(b)
                self.term_graph[b].add(a)

        # 5. ربط المجال بالمصطلحات
        if domain:
            self.domain_connections[domain].extend(terms)
            # إزالة المكررات والحفاظ على الترتيب
            self.domain_connections[domain] = list(dict.fromkeys(self.domain_connections[domain]))

        logger.info(f"🔗 Processed {len(terms)} terms in domain: {domain} (total docs: {self.processed_docs})")

    def _extract_key_terms(self, text: str) -> List[str]:
        """استخراج المصطلحات المفتاحية (بسيطة وفعالة)."""
        # تنظيف النص
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        words = clean_text.split()
        
        # استبعاد الكلمات الشائعة (Stopwords)
        stopwords = {"و", "في", "من", "إلى", "على", "عن", "مع", "أن", "هذا", "هذه", "ذلك", "لكن", "إذا", "ثم", "بين", "حيث", "كان", "قد", "لا", "ما", "كل", "بعض"}
        key_terms = [w for w in words if len(w) > 2 and w not in stopwords]
        
        # استخراج العبارات الثنائية (Bigrams) كمرادفات محتملة
        bigrams = []
        for i in range(len(key_terms)-1):
            if len(key_terms[i]) > 2 and len(key_terms[i+1]) > 2:
                bigrams.append(f"{key_terms[i]} {key_terms[i+1]}")
        
        # دمج الكلمات والعبارات الثنائية
        all_terms = key_terms + bigrams
        
        # اختيار المصطلحات الأكثر تكراراً (حد أقصى 30)
        if len(all_terms) > 30:
            # بسيط: أخذ أول 30 أو استخدام Counter
            term_counts = Counter(all_terms)
            all_terms = [t for t, _ in term_counts.most_common(30)]
        
        return list(set(all_terms))

    def get_domain_terms(self, domain: str) -> List[str]:
        """استرجاع المصطلحات المرتبطة بمجال معين."""
        return self.domain_connections.get(domain, [])

    def get_term_connections(self, term: str) -> List[str]:
        """استرجاع المصطلحات المرتبطة بمصطلح معين."""
        return list(self.term_graph.get(term, set()))

    def get_cross_domain_bridges(self) -> List[Tuple[str, str, List[str]]]:
        """اكتشاف الروابط بين المجالات (المناطق المعرفية المشتركة)."""
        bridges = []
        domains = list(self.domain_connections.keys())
        for i in range(len(domains)):
            for j in range(i+1, len(domains)):
                d1, d2 = domains[i], domains[j]
                set1 = set(self.domain_connections[d1])
                set2 = set(self.domain_connections[d2])
                common_terms = set1 & set2
                if common_terms:
                    bridges.append((d1, d2, list(common_terms)[:5]))  # 5 روابط كحد أقصى
        return bridges

    def get_top_terms(self, limit: int = 20) -> List[Tuple[str, int]]:
        """المصطلحات الأكثر شيوعاً في النظام."""
        return sorted(self.term_frequency.items(), key=lambda x: x[1], reverse=True)[:limit]

    def get_semantic_density(self) -> float:
        """كثافة العلاقات الدلالية (متوسط عدد الروابط لكل مصطلح)."""
        if not self.term_graph:
            return 0.0
        total_edges = sum(len(v) for v in self.term_graph.values())
        total_nodes = len(self.term_graph)
        return total_edges / total_nodes if total_nodes > 0 else 0.0

    def export_graph(self) -> Dict:
        """تصدير الرسم البياني الدلالي كـ JSON."""
        return {
            "nodes": list(self.term_graph.keys()),
            "edges": [(k, list(v)) for k, v in self.term_graph.items()],
            "domain_connections": dict(self.domain_connections),
            "term_frequency": dict(self.term_frequency)
        }
