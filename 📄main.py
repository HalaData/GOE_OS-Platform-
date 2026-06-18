"""
GOE OS - Full Platform (Production Ready)
نظام تشغيل الحوكمة المعرفية - الإصدار الكامل الجاهز للإنتاج
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import uvicorn
import json

# ============================================================
# إعداد التسجيل
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("GOE_OS")

# ============================================================
# تحميل المكونات الأساسية
# ============================================================

from core.loader import ComponentLoader
from core.engine import engine

# ============================================================
# دورة حياة التطبيق
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 GOE OS Full Platform starting...")
    logger.info("📦 Loading components...")
    yield
    logger.info("👋 GOE OS shutting down...")

# ============================================================
# التطبيق الرئيسي
# ============================================================

app = FastAPI(
    title="GOE OS - Full Platform",
    description="Knowledge Governance Platform - All Modules",
    version="3.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# تهيئة المحركات الإضافية (تحميل كسول)
# ============================================================

_cybernetic_engine = None
_advanced_risk_engine = None

def get_cybernetic_engine():
    """الحصول على محرك الحوكمة السيبرنطيقية (تحميل عند أول استخدام)"""
    global _cybernetic_engine
    if _cybernetic_engine is None:
        from modules.cybernetic_governance.engine import CyberneticGovernanceEngine
        _cybernetic_engine = CyberneticGovernanceEngine()
        logger.info("✅ Cybernetic Governance Engine loaded")
    return _cybernetic_engine

def get_advanced_risk_engine():
    """الحصول على محرك المخاطر المتقدم (تحميل عند أول استخدام)"""
    global _advanced_risk_engine
    if _advanced_risk_engine is None:
        from modules.entrepreneurship.advanced_risk_engine import AdvancedRiskEngine
        _advanced_risk_engine = AdvancedRiskEngine()
        logger.info("✅ Advanced Risk Engine loaded")
    return _advanced_risk_engine

# ============================================================
# نقاط النهاية العامة
# ============================================================

@app.get("/")
async def root():
    return {
        "name": "GOE OS",
        "version": "3.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "3.0.0", "mode": "full"}

@app.get("/api/v2/status")
async def status():
    return {
        "status": "running",
        "version": "3.0.0",
        "components": list(ComponentLoader.get_all().keys()),
        "uptime": engine.get_status()
    }

# ============================================================
# 1. محرك الحوكمة (Governance)
# ============================================================

@app.post("/api/v2/govern")
async def govern(request: Request):
    """التشخيص الرئيسي للحوكمة المعرفية"""
    data = await request.json()
    gov = ComponentLoader.get_governance()
    if not gov:
        raise HTTPException(status_code=503, detail="Governance engine unavailable")
    return gov.analyze(data)

@app.get("/api/v2/govern/indicators")
async def get_indicators():
    """جميع المؤشرات المتاحة"""
    gov = ComponentLoader.get_governance()
    if not gov:
        raise HTTPException(status_code=503, detail="Governance engine unavailable")
    return gov.get_indicators()

@app.post("/api/v2/govern/indicator/create")
async def create_indicator(request: Request):
    """إنشاء مؤشر جديد"""
    data = await request.json()
    gov = ComponentLoader.get_governance()
    if not gov:
        raise HTTPException(status_code=503, detail="Governance engine unavailable")
    return gov.create_indicator(data)

@app.get("/api/v2/govern/history")
async def get_governance_history(limit: int = 10):
    """سجل التشخيصات السابقة"""
    gov = ComponentLoader.get_governance()
    if not gov:
        raise HTTPException(status_code=503, detail="Governance engine unavailable")
    return gov.get_history(limit)

# ============================================================
# 2. محرك التحليل العميق (Analysis)
# ============================================================

@app.post("/api/v2/analyze")
async def analyze(request: Request):
    """تحليل عميق للنص"""
    data = await request.json()
    analysis = ComponentLoader.get_analysis()
    if not analysis:
        raise HTTPException(status_code=503, detail="Analysis engine unavailable")
    return analysis.analyze(data)

@app.post("/api/v2/analyze/dogmas")
async def analyze_dogmas(request: Request):
    """كشف المسلمات في النص"""
    data = await request.json()
    analysis = ComponentLoader.get_analysis()
    if not analysis:
        raise HTTPException(status_code=503, detail="Analysis engine unavailable")
    return analysis.extract_dogmas(data)

@app.get("/api/v2/analyze/history")
async def get_analysis_history(limit: int = 10):
    analysis = ComponentLoader.get_analysis()
    if not analysis:
        raise HTTPException(status_code=503, detail="Analysis engine unavailable")
    return analysis.get_history(limit)

# ============================================================
# 3. محرك الترجمة والتدويل (i18n)
# ============================================================

@app.post("/api/v2/translate")
async def translate(request: Request):
    """ترجمة نص فورية"""
    data = await request.json()
    translator = ComponentLoader.get_translator()
    if not translator:
        raise HTTPException(status_code=503, detail="Translation engine unavailable")
    return translator.translate(data)

@app.get("/api/v2/translate/languages")
async def get_languages():
    """جميع اللغات المدعومة"""
    translator = ComponentLoader.get_translator()
    if not translator:
        raise HTTPException(status_code=503, detail="Translation engine unavailable")
    return translator.get_languages()

@app.post("/api/v2/translate/file")
async def translate_file(request: Request):
    """ترجمة ملف كبير"""
    data = await request.json()
    translator = ComponentLoader.get_translator()
    if not translator:
        raise HTTPException(status_code=503, detail="Translation engine unavailable")
    return translator.translate_file(data)

@app.post("/api/v2/translate/batch")
async def translate_batch(request: Request):
    """ترجمة دفعية لنصوص متعددة"""
    data = await request.json()
    translator = ComponentLoader.get_translator()
    if not translator:
        raise HTTPException(status_code=503, detail="Translation engine unavailable")
    return translator.translate_batch(data)

# ============================================================
# 4. محرك التوليد (Generation)
# ============================================================

@app.post("/api/v2/generate/code")
async def generate_code(request: Request):
    """توليد كود من وصف طبيعي"""
    data = await request.json()
    generator = ComponentLoader.get_generator()
    if not generator:
        raise HTTPException(status_code=503, detail="Generation engine unavailable")
    return generator.generate_code(data)

@app.post("/api/v2/generate/content")
async def generate_content(request: Request):
    """توليد محتوى (مقال، تقرير)"""
    data = await request.json()
    generator = ComponentLoader.get_generator()
    if not generator:
        raise HTTPException(status_code=503, detail="Generation engine unavailable")
    return generator.generate_content(data)

@app.post("/api/v2/generate/strategy")
async def generate_strategy(request: Request):
    """توليد خطة استراتيجية"""
    data = await request.json()
    generator = ComponentLoader.get_generator()
    if not generator:
        raise HTTPException(status_code=503, detail="Generation engine unavailable")
    return generator.generate_strategy(data)

@app.post("/api/v2/generate/business")
async def generate_business(request: Request):
    """توليد نموذج عمل متكامل"""
    data = await request.json()
    generator = ComponentLoader.get_generator()
    if not generator:
        raise HTTPException(status_code=503, detail="Generation engine unavailable")
    return generator.generate_business(data)

@app.get("/api/v2/generate/history")
async def get_generation_history(limit: int = 10):
    generator = ComponentLoader.get_generator()
    if not generator:
        raise HTTPException(status_code=503, detail="Generation engine unavailable")
    return generator.get_history(limit)

# ============================================================
# 5. القانون الذكي (Law)
# ============================================================

@app.post("/api/v2/law/analyze")
async def law_analyze(request: Request):
    """تحليل نص قانوني واكتشاف الفجوات"""
    data = await request.json()
    law = ComponentLoader.get_law()
    if not law:
        raise HTTPException(status_code=503, detail="Law engine unavailable")
    return law.analyze(data)

@app.post("/api/v2/law/generate")
async def law_generate(request: Request):
    """توليد تشريع جديد لسد الفجوات"""
    data = await request.json()
    law = ComponentLoader.get_law()
    if not law:
        raise HTTPException(status_code=503, detail="Law engine unavailable")
    return law.generate_legislation(data)

@app.post("/api/v2/law/compare")
async def law_compare(request: Request):
    """مقارنة قوانين دولتين"""
    data = await request.json()
    law = ComponentLoader.get_law()
    if not law:
        raise HTTPException(status_code=503, detail="Law engine unavailable")
    return law.compare(data)

@app.post("/api/v2/law/foresight")
async def law_foresight(request: Request):
    """استشراف أثر تشريع مقترح"""
    data = await request.json()
    law = ComponentLoader.get_law()
    if not law:
        raise HTTPException(status_code=503, detail="Law engine unavailable")
    return law.foresight(data)

# ============================================================
# 6. الطب (Medicine)
# ============================================================

@app.post("/api/v2/medicine/diagnose")
async def medicine_diagnose(request: Request):
    """تشخيص طبي مبدئي"""
    data = await request.json()
    med = ComponentLoader.get_medicine()
    if not med:
        raise HTTPException(status_code=503, detail="Medicine engine unavailable")
    return med.diagnose(data)

@app.post("/api/v2/medicine/regenerative")
async def medicine_regenerative(request: Request):
    """تحليل الطب التجديدي والجروح"""
    data = await request.json()
    med = ComponentLoader.get_medicine()
    if not med:
        raise HTTPException(status_code=503, detail="Medicine engine unavailable")
    return med.regenerative_analysis(data)

@app.post("/api/v2/medicine/nutrition")
async def medicine_nutrition(request: Request):
    """تحليل التغذية العلاجية"""
    data = await request.json()
    med = ComponentLoader.get_medicine()
    if not med:
        raise HTTPException(status_code=503, detail="Medicine engine unavailable")
    return med.nutrition_analysis(data)

@app.post("/api/v2/medicine/tooth-regeneration")
async def medicine_tooth_regeneration(request: Request):
    """استشارة نمو أسنان جديدة"""
    data = await request.json()
    med = ComponentLoader.get_medicine()
    if not med:
        raise HTTPException(status_code=503, detail="Medicine engine unavailable")
    return med.tooth_regeneration(data)

# ============================================================
# 7. الزراعة (Agriculture)
# ============================================================

@app.post("/api/v2/agriculture/calendar")
async def agriculture_calendar(request: Request):
    """توليد روزنامة محصولية"""
    data = await request.json()
    agri = ComponentLoader.get_agriculture()
    if not agri:
        raise HTTPException(status_code=503, detail="Agriculture engine unavailable")
    return agri.generate_calendar(data)

@app.post("/api/v2/agriculture/crop/add")
async def agriculture_add_crop(request: Request):
    """إضافة محصول جديد"""
    data = await request.json()
    agri = ComponentLoader.get_agriculture()
    if not agri:
        raise HTTPException(status_code=503, detail="Agriculture engine unavailable")
    return agri.add_crop(data)

@app.post("/api/v2/agriculture/country/add")
async def agriculture_add_country(request: Request):
    """إضافة دولة جديدة"""
    data = await request.json()
    agri = ComponentLoader.get_agriculture()
    if not agri:
        raise HTTPException(status_code=503, detail="Agriculture engine unavailable")
    return agri.add_country(data)

@app.get("/api/v2/agriculture/crops")
async def agriculture_get_crops():
    """جميع المحاصيل"""
    agri = ComponentLoader.get_agriculture()
    if not agri:
        raise HTTPException(status_code=503, detail="Agriculture engine unavailable")
    return agri.get_crops()

@app.get("/api/v2/agriculture/countries")
async def agriculture_get_countries():
    """جميع الدول"""
    agri = ComponentLoader.get_agriculture()
    if not agri:
        raise HTTPException(status_code=503, detail="Agriculture engine unavailable")
    return agri.get_countries()

# ============================================================
# 8. الفيزياء (Physics)
# ============================================================

@app.post("/api/v2/physics/analyze")
async def physics_analyze(request: Request):
    """تحليل فيزيائي عميق"""
    data = await request.json()
    phys = ComponentLoader.get_physics()
    if not phys:
        raise HTTPException(status_code=503, detail="Physics engine unavailable")
    return phys.analyze(data)

@app.post("/api/v2/physics/foresight")
async def physics_foresight(request: Request):
    """استشراف مستقبل الفيزياء"""
    data = await request.json()
    phys = ComponentLoader.get_physics()
    if not phys:
        raise HTTPException(status_code=503, detail="Physics engine unavailable")
    return phys.foresight(data)

@app.post("/api/v2/physics/philosophy")
async def physics_philosophy(request: Request):
    """ربط الفيزياء بالفلسفة"""
    data = await request.json()
    phys = ComponentLoader.get_physics()
    if not phys:
        raise HTTPException(status_code=503, detail="Physics engine unavailable")
    return phys.philosophy_connection(data)

# ============================================================
# 9. الموسيقى (Music)
# ============================================================

@app.post("/api/v2/music/analyze")
async def music_analyze(request: Request):
    """تحليل موسيقي متقدم"""
    data = await request.json()
    music = ComponentLoader.get_music()
    if not music:
        raise HTTPException(status_code=503, detail="Music engine unavailable")
    return music.analyze(data)

@app.post("/api/v2/music/generate")
async def music_generate(request: Request):
    """توليد موسيقى أو لحن"""
    data = await request.json()
    music = ComponentLoader.get_music()
    if not music:
        raise HTTPException(status_code=503, detail="Music engine unavailable")
    return music.generate(data)

@app.post("/api/v2/music/emotion")
async def music_emotion(request: Request):
    """تحليل المشاعر في الموسيقى"""
    data = await request.json()
    music = ComponentLoader.get_music()
    if not music:
        raise HTTPException(status_code=503, detail="Music engine unavailable")
    return music.emotion_analysis(data)

# ============================================================
# 10. الرياضة (Sports)
# ============================================================

@app.post("/api/v2/sports/analyze")
async def sports_analyze(request: Request):
    """تحليل رياضي شامل"""
    data = await request.json()
    sports = ComponentLoader.get_sports()
    if not sports:
        raise HTTPException(status_code=503, detail="Sports engine unavailable")
    return sports.analyze(data)

@app.post("/api/v2/sports/refereeing")
async def sports_refereeing(request: Request):
    """تحليل التحكيم"""
    data = await request.json()
    sports = ComponentLoader.get_sports()
    if not sports:
        raise HTTPException(status_code=503, detail="Sports engine unavailable")
    return sports.refereeing(data)

@app.post("/api/v2/sports/injury-prediction")
async def sports_injury_prediction(request: Request):
    """التنبؤ بالإصابات الرياضية"""
    data = await request.json()
    sports = ComponentLoader.get_sports()
    if not sports:
        raise HTTPException(status_code=503, detail="Sports engine unavailable")
    return sports.injury_prediction(data)

# ============================================================
# 11. الاقتصاد وريادة الأعمال (Economics)
# ============================================================

@app.post("/api/v2/economics/forecast")
async def economics_forecast(request: Request):
    """التنبؤ الاقتصادي"""
    data = await request.json()
    eco = ComponentLoader.get_economics()
    if not eco:
        raise HTTPException(status_code=503, detail="Economics engine unavailable")
    return eco.forecast(data)

@app.post("/api/v2/economics/startup")
async def economics_startup(request: Request):
    """تحليل شركة ناشئة وتوليد خطة عمل"""
    data = await request.json()
    eco = ComponentLoader.get_economics()
    if not eco:
        raise HTTPException(status_code=503, detail="Economics engine unavailable")
    return eco.startup_analysis(data)

@app.post("/api/v2/economics/supply-chain")
async def economics_supply_chain(request: Request):
    """تحليل سلسلة التوريد"""
    data = await request.json()
    eco = ComponentLoader.get_economics()
    if not eco:
        raise HTTPException(status_code=503, detail="Economics engine unavailable")
    return eco.supply_chain_analysis(data)

# ============================================================
# 12. التعليم (Education)
# ============================================================

@app.post("/api/v2/education/analyze")
async def education_analyze(request: Request):
    """تحليل تعليمي شامل"""
    data = await request.json()
    edu = ComponentLoader.get_education()
    if not edu:
        raise HTTPException(status_code=503, detail="Education engine unavailable")
    return edu.analyze(data)

@app.post("/api/v2/education/iep")
async def education_iep(request: Request):
    """توليد خطة تعليمية فردية (IEP)"""
    data = await request.json()
    edu = ComponentLoader.get_education()
    if not edu:
        raise HTTPException(status_code=503, detail="Education engine unavailable")
    return edu.generate_iep(data)

@app.post("/api/v2/education/gamification")
async def education_gamification(request: Request):
    """تحليل التلعيب في التعليم"""
    data = await request.json()
    edu = ComponentLoader.get_education()
    if not edu:
        raise HTTPException(status_code=503, detail="Education engine unavailable")
    return edu.gamification_analysis(data)

# ============================================================
# 13. الاستشراف (Foresight)
# ============================================================

@app.post("/api/v2/foresight/scenarios")
async def foresight_scenarios(request: Request):
    """توليد سيناريوهات غير محدودة"""
    data = await request.json()
    foresight = ComponentLoader.get_foresight()
    if not foresight:
        raise HTTPException(status_code=503, detail="Foresight engine unavailable")
    return foresight.generate_scenarios(data)

@app.post("/api/v2/foresight/wisdom")
async def foresight_wisdom(request: Request):
    """استخلاص الحكمة من الماضي"""
    data = await request.json()
    foresight = ComponentLoader.get_foresight()
    if not foresight:
        raise HTTPException(status_code=503, detail="Foresight engine unavailable")
    return foresight.get_wisdom(data)

@app.post("/api/v2/foresight/impact")
async def foresight_impact(request: Request):
    """استشراف أثر قرار أو تشريع"""
    data = await request.json()
    foresight = ComponentLoader.get_foresight()
    if not foresight:
        raise HTTPException(status_code=503, detail="Foresight engine unavailable")
    return foresight.impact_analysis(data)

# ============================================================
# 14. التخطيط الاستراتيجي (Strategy)
# ============================================================

@app.post("/api/v2/strategy/plan")
async def strategy_plan(request: Request):
    """توليد خطة استراتيجية متكاملة"""
    data = await request.json()
    strategy = ComponentLoader.get_strategy()
    if not strategy:
        raise HTTPException(status_code=503, detail="Strategy engine unavailable")
    return strategy.generate_plan(data)

@app.post("/api/v2/strategy/vision")
async def strategy_vision(request: Request):
    """صياغة رؤية استراتيجية"""
    data = await request.json()
    strategy = ComponentLoader.get_strategy()
    if not strategy:
        raise HTTPException(status_code=503, detail="Strategy engine unavailable")
    return strategy.craft_vision(data)

# ============================================================
# 15. التكامل (Integration)
# ============================================================

@app.post("/api/v2/integration/connect")
async def integration_connect(request: Request):
    """ربط نظام خارجي"""
    data = await request.json()
    integration = ComponentLoader.get_integration()
    if not integration:
        raise HTTPException(status_code=503, detail="Integration engine unavailable")
    return integration.connect(data)

@app.get("/api/v2/integration/status")
async def integration_status():
    """حالة التكاملات"""
    integration = ComponentLoader.get_integration()
    if not integration:
        raise HTTPException(status_code=503, detail="Integration engine unavailable")
    return integration.get_status()

# ============================================================
# 16. الوسائط (Media)
# ============================================================

@app.post("/api/v2/media/transcribe")
async def media_transcribe(request: Request):
    """تفريغ صوتي (Speech-to-Text)"""
    data = await request.json()
    media = ComponentLoader.get_media()
    if not media:
        raise HTTPException(status_code=503, detail="Media engine unavailable")
    return media.transcribe(data)

@app.post("/api/v2/media/translate/video")
async def media_translate_video(request: Request):
    """ترجمة فيديو كامل"""
    data = await request.json()
    media = ComponentLoader.get_media()
    if not media:
        raise HTTPException(status_code=503, detail="Media engine unavailable")
    return media.translate_video(data)

@app.post("/api/v2/media/translate/audio")
async def media_translate_audio(request: Request):
    """ترجمة ملف صوتي"""
    data = await request.json()
    media = ComponentLoader.get_media()
    if not media:
        raise HTTPException(status_code=503, detail="Media engine unavailable")
    return media.translate_audio(data)

# ============================================================
# 17. الإتاحة (Accessibility)
# ============================================================

@app.post("/api/v2/accessibility/set-mode")
async def accessibility_set_mode(request: Request):
    """ضبط وضع الإتاحة (صم، بكم، كفيفين)"""
    data = await request.json()
    access = ComponentLoader.get_accessibility()
    if not access:
        raise HTTPException(status_code=503, detail="Accessibility engine unavailable")
    return access.set_mode(data)

@app.get("/api/v2/accessibility/modes")
async def accessibility_get_modes():
    """جميع أوضاع الإتاحة"""
    access = ComponentLoader.get_accessibility()
    if not access:
        raise HTTPException(status_code=503, detail="Accessibility engine unavailable")
    return access.get_modes()

# ============================================================
# 18. الأطفال (Kids)
# ============================================================

@app.post("/api/v2/kids/game")
async def kids_game(request: Request):
    """بدء لعبة تعليمية للأطفال"""
    data = await request.json()
    kids = ComponentLoader.get_kids()
    if not kids:
        raise HTTPException(status_code=503, detail="Kids engine unavailable")
    return kids.start_game(data)

@app.post("/api/v2/kids/story")
async def kids_story(request: Request):
    """بدء قصة تفاعلية للأطفال"""
    data = await request.json()
    kids = ComponentLoader.get_kids()
    if not kids:
        raise HTTPException(status_code=503, detail="Kids engine unavailable")
    return kids.start_story(data)

@app.get("/api/v2/kids/friend")
async def kids_friend():
    """شخصية مرافقة عشوائية"""
    kids = ComponentLoader.get_kids()
    if not kids:
        raise HTTPException(status_code=503, detail="Kids engine unavailable")
    return kids.get_friend()

# ============================================================
# 19. تمكين المطورين (Empowerment)
# ============================================================

@app.post("/api/v2/empowerment/generate-app")
async def empowerment_generate_app(request: Request):
    """توليد تطبيق من وصف نصي"""
    data = await request.json()
    emp = ComponentLoader.get_empowerment()
    if not emp:
        raise HTTPException(status_code=503, detail="Empowerment engine unavailable")
    return emp.generate_app(data)

@app.post("/api/v2/empowerment/wizard")
async def empowerment_wizard(request: Request):
    """بدء معالج تفاعلي لتوليد التطبيقات"""
    data = await request.json()
    emp = ComponentLoader.get_empowerment()
    if not emp:
        raise HTTPException(status_code=503, detail="Empowerment engine unavailable")
    return emp.start_wizard(data)

# ============================================================
# 20. الوكلاء (Agents)
# ============================================================

@app.post("/api/v2/agents/analyze")
async def agents_analyze(request: Request):
    """تحليل نص بجميع الوكلاء العلميين"""
    data = await request.json()
    agents = ComponentLoader.get_agents()
    if not agents:
        raise HTTPException(status_code=503, detail="Agents engine unavailable")
    return agents.analyze_with_agents(data)

@app.get("/api/v2/agents/list")
async def agents_list():
    """جميع الوكلاء المتاحين"""
    agents = ComponentLoader.get_agents()
    if not agents:
        raise HTTPException(status_code=503, detail="Agents engine unavailable")
    return agents.list_agents()

@app.post("/api/v2/agents/collaborate")
async def agents_collaborate(request: Request):
    """تعاون بين وكيلين"""
    data = await request.json()
    agents = ComponentLoader.get_agents()
    if not agents:
        raise HTTPException(status_code=503, detail="Agents engine unavailable")
    return agents.orchestrate_collaboration(data)

# ============================================================
# 21. الحوكمة السيبرنطيقية (Cybernetic Governance)
# ============================================================

@app.post("/api/v2/governance/observe")
async def observe(request: Request):
    """رصد النظام واكتشاف الثغرات"""
    data = await request.json()
    engine = get_cybernetic_engine()
    return engine.observe(data)

@app.post("/api/v2/governance/diagnose")
async def diagnose(request: Request):
    """تشخيص السبب الجذري للثغرات"""
    data = await request.json()
    engine = get_cybernetic_engine()
    return engine.diagnose(data)

@app.post("/api/v2/governance/remediate")
async def remediate(request: Request):
    """توليد حلول وإصلاح الثغرات"""
    data = await request.json()
    engine = get_cybernetic_engine()
    return engine.remediate(data)

@app.post("/api/v2/governance/proact")
async def proact(request: Request):
    """تطعيم النظام ضد الثغرات المستقبلية"""
    data = await request.json()
    engine = get_cybernetic_engine()
    return engine.proact(data)

@app.post("/api/v2/governance/knowledge")
async def create_knowledge(request: Request):
    """توليد معارف وكتب من عمليات الحوكمة"""
    data = await request.json()
    engine = get_cybernetic_engine()
    return engine.create_knowledge(data)

@app.post("/api/v2/governance/cycle")
async def governance_cycle():
    """تشغيل دورة حوكمة كاملة (رصد → تشخيص → علاج → استباق → معرفي)"""
    engine = get_cybernetic_engine()
    return engine.cycle()

@app.get("/api/v2/governance/history")
async def get_governance_history(limit: int = 10):
    """سجل دورات الحوكمة"""
    engine = get_cybernetic_engine()
    return engine.get_history(limit)

@app.get("/api/v2/governance/status")
async def get_governance_status():
    """حالة الحوكمة"""
    engine = get_cybernetic_engine()
    return engine.get_governance_status()

@app.get("/api/v2/governance/books")
async def get_governance_books():
    """الكتب المولدة من عمليات الحوكمة"""
    engine = get_cybernetic_engine()
    return engine.get_books()

@app.get("/api/v2/governance/protocols")
async def get_governance_protocols():
    """البروتوكولات المناعية"""
    engine = get_cybernetic_engine()
    return engine.get_protocols()

@app.get("/api/v2/governance/indicators")
async def get_governance_indicators():
    """المؤشرات الجديدة المولدة"""
    engine = get_cybernetic_engine()
    return engine.get_indicators()

@app.get("/api/v2/governance/knowledge-base")
async def get_knowledge_base():
    """قاعدة المعرفة الكاملة"""
    engine = get_cybernetic_engine()
    return engine.get_knowledge_base()

# ============================================================
# 22. مولد السيناريوهات غير المحدود (Unlimited Scenarios)
# ============================================================

@app.post("/api/v2/governance/scenarios/generate")
async def generate_unlimited_scenarios(request: Request):
    """توليد سيناريوهات غير محدودة (عدد قابل للتحديد)"""
    data = await request.json()
    fix = data.get("fix", {})
    vulnerability = data.get("vulnerability", {})
    count = data.get("count", 10)
    engine = get_cybernetic_engine()
    return engine.generate_unlimited_scenarios(fix, vulnerability, count)

@app.get("/api/v2/governance/scenarios/statistics")
async def get_scenario_statistics():
    """إحصائيات السيناريوهات المولدة"""
    engine = get_cybernetic_engine()
    return engine.get_scenario_statistics()

@app.get("/api/v2/governance/scenarios/{scenario_id}")
async def get_scenario_by_id(scenario_id: str):
    """بحث عن سيناريو بالمعرف"""
    engine = get_cybernetic_engine()
    scenario = engine.get_scenario_by_id(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return scenario

# ============================================================
# 23. تحليل المخاطر المتقدم للشركات الناشئة (Advanced Risk)
# ============================================================

@app.post("/api/v2/risk/market-demand")
async def analyze_market_demand(request: Request):
    """تحليل الاحتياج السوقي المتقدم"""
    data = await request.json()
    engine = get_advanced_risk_engine()
    return engine.analyze_market_demand(data)

@app.post("/api/v2/risk/cash-flow")
async def predict_cash_flow(request: Request):
    """التنبؤ بالتدفق النقدي"""
    data = await request.json()
    engine = get_advanced_risk_engine()
    return engine.predict_cash_flow(data)

@app.post("/api/v2/risk/team")
async def analyze_team(request: Request):
    """تحليل ديناميكيات الفريق"""
    data = await request.json()
    engine = get_advanced_risk_engine()
    return engine.analyze_team(data)

@app.post("/api/v2/risk/pivot")
async def analyze_pivot(request: Request):
    """تحليل فرص تعديل المسار"""
    data = await request.json()
    engine = get_advanced_risk_engine()
    return engine.analyze_pivot_opportunity(data)

@app.post("/api/v2/risk/legal")
async def analyze_legal(request: Request):
    """تحليل المخاطر القانونية"""
    data = await request.json()
    engine = get_advanced_risk_engine()
    return engine.analyze_legal_risks(data)

@app.post("/api/v2/risk/network")
async def analyze_network(request: Request):
    """تحليل العلاقات والشراكات"""
    data = await request.json()
    engine = get_advanced_risk_engine()
    return engine.analyze_network(data)

@app.post("/api/v2/risk/comprehensive")
async def comprehensive_risk_report(request: Request):
    """تقرير مخاطر شامل مع احتمالية النجاح"""
    data = await request.json()
    engine = get_advanced_risk_engine()
    return engine.comprehensive_risk_report(data)

# ============================================================
# المحرك الرئيسي
# ============================================================

@app.get("/api/v2/engine/status")
async def engine_status():
    """حالة المحرك الرئيسي"""
    return engine.get_status()

@app.post("/api/v2/engine/component/load")
async def engine_load_component(request: Request):
    """تحميل مكون يدوياً"""
    data = await request.json()
    name = data.get("name")
    module_path = data.get("module_path")
    class_name = data.get("class_name")
    
    if not all([name, module_path, class_name]):
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    component = ComponentLoader.get(name, module_path, class_name)
    if not component:
        raise HTTPException(status_code=500, detail=f"Failed to load component: {name}")
    
    return {"status": "loaded", "name": name}

# ============================================================
# التشغيل
# ============================================================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
