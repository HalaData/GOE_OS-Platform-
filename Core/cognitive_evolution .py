# ============================================================
# 6. أنواع السلوك الإضافية (Behavioral Types)
# ============================================================

class BehavioralTypes:
    """
    تعريف الأنماط السلوكية الستة (الداروينية + 5 أنماط جديدة).
    """
    DARWINIAN = "darwinian"          # البقاء للأصلح
    HOMEOSTATIC = "homeostatic"      # الحفاظ على التوازن
    RESONANT = "resonant"            # التوافق الاجتماعي
    HERMENEUTIC = "hermeneutic"      # التفسير العميق
    TRANSCENDENT = "transcendent"    # التجاوز والإبداع
    PATTERN = "pattern"              # التعرف على الأنماط

# ============================================================
# 7. كاشف الأنماط السلوكية المتقدم (Advanced Behavioral Detector)
# ============================================================

class BehavioralDetector:
    """
    يكتشف الأنماط السلوكية الستة في النصوص وسلوكيات الوكلاء.
    """

    @staticmethod
    def detect_darwinian(text: str) -> Dict:
        """كشف السلوك الدارويني (البقاء للأصلح)."""
        indicators = ["منافسة", "بقاء", "أصلح", "تكيف", "انتقاء"]
        matches = [w for w in indicators if w in text]
        return {
            "type": BehavioralTypes.DARWINIAN,
            "score": len(matches) / len(indicators),
            "indicators": matches,
            "description": "سلوك يركز على المنافسة والبقاء للأصلح."
        }

    @staticmethod
    def detect_homeostatic(text: str) -> Dict:
        """كشف السلوك التوافقي (الحفاظ على التوازن)."""
        indicators = ["استقرار", "توازن", "تجنب", "مخاطرة", "عدم تغيير"]
        matches = [w for w in indicators if w in text]
        return {
            "type": BehavioralTypes.HOMEOSTATIC,
            "score": len(matches) / len(indicators),
            "indicators": matches,
            "description": "سلوك يسعى للحفاظ على التوازن وتجنب المخاطر."
        }

    @staticmethod
    def detect_resonant(text: str) -> Dict:
        """كشف السلوك الرنيني (التوافق الاجتماعي)."""
        indicators = ["معظم", "اتجاه عام", "يتبع", "على خطى", "كما يفعل الآخرون"]
        matches = [w for w in indicators if w in text]
        return {
            "type": BehavioralTypes.RESONANT,
            "score": len(matches) / len(indicators),
            "indicators": matches,
            "description": "سلوك يتبع الجماعة ويتوافق مع الاتجاه العام."
        }

    @staticmethod
    def detect_hermeneutic(text: str) -> Dict:
        """كشف السلوك التفسيري (بناء المعنى)."""
        indicators = ["سبب", "معنى", "يروي", "قصة", "خلفية", "سياق"]
        matches = [w for w in indicators if w in text]
        return {
            "type": BehavioralTypes.HERMENEUTIC,
            "score": len(matches) / len(indicators),
            "indicators": matches,
            "description": "سلوك يسعى لفهم المعنى والتفسير العميق."
        }

    @staticmethod
    def detect_transcendent(text: str) -> Dict:
        """كشف السلوك التجاوزي (الإبداع والابتكار)."""
        indicators = ["جديد", "مبتكر", "تخيل", "استكشاف", "غير مألوف"]
        matches = [w for w in indicators if w in text]
        return {
            "type": BehavioralTypes.TRANSCENDENT,
            "score": len(matches) / len(indicators),
            "indicators": matches,
            "description": "سلوك يبحث عن الإبداع والتجاوز والاستكشاف."
        }

    @staticmethod
    def detect_pattern(text: str) -> Dict:
        """كشف السلوك الأنماطي (التعرف على الأنماط)."""
        indicators = ["دائماً", "أبداً", "يتكرر", "نمط", "عادةً"]
        matches = [w for w in indicators if w in text]
        return {
            "type": BehavioralTypes.PATTERN,
            "score": len(matches) / len(indicators),
            "indicators": matches,
            "description": "سلوك يبحث عن الأنماط المتكررة ويتنبأ بناءً عليها."
        }

    @staticmethod
    def analyze_behavior(text: str) -> List[Dict]:
        """تحليل النص لاكتشاف جميع الأنماط السلوكية."""
        detectors = [
            BehavioralDetector.detect_darwinian,
            BehavioralDetector.detect_homeostatic,
            BehavioralDetector.detect_resonant,
            BehavioralDetector.detect_hermeneutic,
            BehavioralDetector.detect_transcendent,
            BehavioralDetector.detect_pattern
        ]

        results = []
        for detector in detectors:
            result = detector(text)
            results.append(result)

        return results

# ============================================================
# 8. دمج الأنماط السلوكية مع محرك التطور المعرفي
# ============================================================

class CognitiveEvolutionEngine:
    # ... الكود السابق ...

    def __init__(self):
        # ... الكود السابق ...
        self.behavioral_detector = BehavioralDetector()
        self.behavioral_history: Dict[str, List] = defaultdict(list)  # agent_id -> behavioral_results
        logger.info("🧠 Cognitive Evolution Engine initialized with 6 behavioral models.")

    def analyze_behavioral_profile(self, agent_id: str, text: str) -> Dict:
        """
        تحليل السلوك المتعدد الأبعاد لوكيل معين بناءً على نص.
        """
        results = self.behavioral_detector.analyze_behavior(text)
        self.behavioral_history[agent_id].append({
            "timestamp": datetime.utcnow().isoformat(),
            "results": results
        })

        # 1. حساب الميول السلوكية العامة
        scores = {r["type"]: r["score"] for r in results}
        primary_behavior = max(scores, key=scores.get)

        # 2. استخراج المورثات المعرفية من الأنماط السلوكية
        genes = []
        for result in results:
            if result["score"] > 0.5:
                gene = KnowledgeGene(
                    id=hashlib.md5(f"{agent_id}_{result['type']}_{datetime.utcnow().isoformat()}".encode()).hexdigest()[:16],
                    name=f"Behavior_{result['type']}",
                    description=result["description"],
                    type=result["type"],
                    source_agent_id=agent_id,
                    fitness_score=result["score"]
                )
                genes.append(gene)

        # 3. تسجيل المورثات الجديدة
        for gene in genes:
            self.extractor.gene_registry[gene.id] = gene
            self.agent_knowledge[agent_id].append(gene.id)

        return {
            "agent_id": agent_id,
            "behavioral_profile": scores,
            "primary_behavior": primary_behavior,
            "behavioral_complexity": self._calculate_behavioral_complexity(results),
            "genes_discovered": [g.id for g in genes],
            "timestamp": datetime.utcnow().isoformat()
        }

    def _calculate_behavioral_complexity(self, results: List[Dict]) -> float:
        """
        حساب تعقيد المزيج السلوكي (مدى تنوع الأنماط المكتشفة).
        """
        active_behaviors = [r for r in results if r["score"] > 0.5]
        if not active_behaviors:
            return 0.0
        return len(active_behaviors) / len(results)

    def get_behavioral_history(self, agent_id: str, limit: int = 10) -> List[Dict]:
        """استرجاع التاريخ السلوكي لوكيل معين."""
        return self.behavioral_history.get(agent_id, [])[-limit:]

# ============================================================
# 9. نقاط النهاية الجديدة (API)
# ============================================================

@router.post("/agent/analyze-behavior")
async def analyze_agent_behavior(agent_id: str, text: str):
    """تحليل النمط السلوكي لوكيل معين."""
    engine = get_engine()
    return engine.analyze_behavioral_profile(agent_id, text)

@router.get("/agent/behavioral-history/{agent_id}")
async def get_behavioral_history(agent_id: str, limit: int = 10):
    """استرجاع التاريخ السلوكي لوكيل معين."""
    engine = get_engine()
    return {"history": engine.get_behavioral_history(agent_id, limit)}

@router.get("/behavioral-types")
async def get_behavioral_types():
    """جميع الأنماط السلوكية المتاحة."""
    return {
        "types": [
            {"id": "darwinian", "name": "الدارويني", "description": "البقاء للأصلح"},
            {"id": "homeostatic", "name": "التوافقي", "description": "الحفاظ على التوازن"},
            {"id": "resonant", "name": "الرنيني", "description": "التوافق الاجتماعي"},
            {"id": "hermeneutic", "name": "التفسيري", "description": "بناء المعنى العميق"},
            {"id": "transcendent", "name": "التجاوزي", "description": "الإبداع والاستكشاف"},
            {"id": "pattern", "name": "الأنماطي", "description": "التعرف على الأنماط والتوقع"}
        ]
    }
