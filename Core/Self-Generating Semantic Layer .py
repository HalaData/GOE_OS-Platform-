"""
GOE OS - محرك الخريطة الدلالية الذاتية (Self-Generating Semantic Layer)
يربط المصطلحات عبر التخصصات تلقائياً بناءً على تفاعلات المستخدم والمستندات.
"""

import hashlib
import json
import re
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Set, Tuple
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
        logger.info("🧠 Semantic Mapper initialized (Zero-cost Knowledge Graph)")

    def process_text(self, text: str, domain: str):
        """
        معالجة نص جديد واستخراج العلاقات الدلالية تلقائياً.
        """
        # 1. استخراج المصطلحات المفتاحية (أساسية)
        terms = self._extract_key_terms(text)
        if not terms:
            return

        # 2. تحديث تردد المصطلحات
        for term in terms:
            self.term_frequency[term] += 1

        # 3. ربط المصطلحات ببعضها (العلاقات الدلالية)
        for i, term_i in enumerate(terms):
            for j, term_j in enumerate(terms):
                if i != j and self._are_related(term_i, term_j, text):
                    self.term_graph[term_i].add(term_j)
                    self.term_graph[term_j].add(term_i)

        # 4. ربط المجال بالمصطلحات
        if domain:
            self.domain_connections[domain].extend(terms)
            self.domain_connections[domain] = list(set(self.domain_connections[domain]))

        logger.info(f"🔗 Processed {len(terms)} terms in domain: {domain}")

    def _extract_key_terms(self, text: str) -> List[str]:
        """استخراج المصطلحات المفتاحية (بسيطة وفعالة)."""
        # تنظيف النص
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        words = clean_text.split()
        
        # استبعاد الكلمات الشائعة (Stopwords)
        stopwords = {"و", "في", "من", "إلى", "على", "عن", "مع", "أن", "هذا", "هذه"}
        key_terms = [w for w in words if len(w) > 3 and w not in stopwords]
        
        # أخذ المصطلحات الأكثر تكراراً (الثلاثي الأكثر شيوعاً)
        if len(key_terms) > 10:
            # استخراج العبارات الثنائية (Bigrams) البسيطة كمرادفات
            bigrams = [" ".join(key_terms[i:i+2]) for i in range(len(key_terms)-1)]
            key_terms.extend(bigrams)
        
        return list(set(key_terms[:20]))  # حد أقصى 20 مصطلحاً لتجنب التضخم

    def _are_related(self, term_a: str, term_b: str, context: str) -> bool:
        """تحديد ما إذا كان مصطلحان مرتبطان (محاكاة بسيطة)."""
        # إذا ظهرا معاً في نفس الجملة
        sentences = re.split(r'[.!?]', context)
        for sent in sentences:
            if term_a in sent and term_b in sent:
                return True
        return False

    def get_domain_terms(self, domain: str) -> List[str]:
        """استرجاع المصطلحات المرتبطة بمجال معين."""
        return self.domain_connections.get(domain, [])

    def get_term_connections(self, term: str) -> List[str]:
        """استرجاع المصطلحات المرتبطة بمصطلح معين."""
        return list(self.term_graph.get(term, set()))

    def get_cross_domain_bridges(self) -> List[Tuple[str, str]]:
        """اكتشاف الروابط بين المجالات (المناطق المعرفية المشتركة)."""
        bridges = []
        domains = list(self.domain_connections.keys())
        for i in range(len(domains)):
            for j in range(i+1, len(domains)):
                d1, d2 = domains[i], domains[j]
                common_terms = set(self.domain_connections[d1]) & set(self.domain_connections[d2])
                if common_terms:
                    bridges.append((d1, d2, list(common_terms)[:5]))  # 5 روابط كحد أقصى
        return bridges
