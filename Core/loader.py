"""
GOE OS - Lazy Component Loader (Advanced)
محمل المكونات الكسول المتقدم - تحميل عند الطلب مع تخزين مؤقت ومعالجة الأخطاء
"""

import logging
import importlib
from typing import Dict, Any, Optional, Callable
from functools import wraps
import time

logger = logging.getLogger("GOE_OS.Loader")

# ============================================================
# ديكوراتور لتتبع وقت التحميل
# ============================================================

def timed_load(func: Callable) -> Callable:
    """تتبع وقت تحميل المكونات"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        if elapsed > 0.5:
            logger.info(f"⏱️ Load time for {func.__name__}: {elapsed:.2f}s")
        return result
    return wrapper

# ============================================================
# المحمل الرئيسي
# ============================================================

class ComponentLoader:
    """
    محمل المكونات المتقدم - تحميل كسول مع:
    - تخزين مؤقت (Caching)
    - معالجة الأخطاء المتقدمة
    - تتبع وقت التحميل
    - إدارة التبعيات
    - إعادة التحميل الديناميكي
    """
    
    _components: Dict[str, Any] = {}
    _loading: Dict[str, bool] = {}
    _load_times: Dict[str, float] = {}
    _retry_count: Dict[str, int] = {}
    _dependencies: Dict[str, list] = {}
    
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0  # ثواني
    
    @classmethod
    @timed_load
    def get(cls, name: str, module_path: str, class_name: str, 
            retry: bool = True, dependencies: list = None) -> Optional[Any]:
        """
        تحميل مكون عند أول طلب فقط مع إعادة محاولة تلقائية
        
        Args:
            name: اسم المكون (مفتاح للتخزين)
            module_path: مسار الوحدة النمطية (مثل: 'modules.governance.engine')
            class_name: اسم الكلاس (مثل: 'GovernanceEngine')
            retry: إعادة المحاولة عند الفشل
            dependencies: قائمة بأسماء المكونات التي يعتمد عليها
        
        Returns:
            نسخة من المكون المحمل، أو None في حالة الفشل
        """
        # التحقق من التبعيات
        if dependencies:
            for dep in dependencies:
                if dep not in cls._components:
                    logger.warning(f"⚠️ Dependency '{dep}' not loaded for '{name}'")
                    # محاولة تحميل التبعية تلقائياً
                    cls._load_dependency(dep)
        
        # إذا كان المكون محملاً بالفعل
        if name in cls._components:
            return cls._components[name]
        
        # منع التحميل المتزامن المتكرر
        if cls._loading.get(name, False):
            logger.warning(f"⏳ Component '{name}' is already loading")
            return None
        
        cls._loading[name] = True
        
        try:
            # محاولة استيراد الوحدة
            module = importlib.import_module(module_path)
            
            # التحقق من وجود الكلاس
            if not hasattr(module, class_name):
                logger.error(f"❌ Class '{class_name}' not found in '{module_path}'")
                return None
            
            # إنشاء نسخة من المكون
            component_class = getattr(module, class_name)
            
            # محاولة إنشاء المكون مع تمرير المعاملات إذا كانت موجودة
            try:
                component = component_class()
            except TypeError:
                # بعض المكونات قد تتطلب معاملات إضافية
                component = component_class()
            
            # تخزين المكون
            cls._components[name] = component
            cls._load_times[name] = time.time()
            cls._retry_count[name] = 0
            
            logger.info(f"✅ Component loaded: {name} (from {module_path}.{class_name})")
            return component
            
        except ImportError as e:
            logger.error(f"❌ Import error for '{name}': {e}")
            if retry and cls._retry_count.get(name, 0) < cls.MAX_RETRIES:
                cls._retry_count[name] = cls._retry_count.get(name, 0) + 1
                logger.info(f"🔄 Retrying '{name}' ({cls._retry_count[name]}/{cls.MAX_RETRIES})...")
                time.sleep(cls.RETRY_DELAY)
                return cls.get(name, module_path, class_name, retry, dependencies)
            return None
            
        except AttributeError as e:
            logger.error(f"❌ Attribute error for '{name}': {e}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to load component '{name}': {e}")
            return None
            
        finally:
            cls._loading[name] = False
    
    @classmethod
    def _load_dependency(cls, dep_name: str):
        """محاولة تحميل تبعية مفقودة"""
        dep_map = {
            "governance": ("modules.governance.engine", "GovernanceEngine"),
            "analysis": ("modules.analysis.engine", "AnalysisEngine"),
            "translator": ("modules.i18n.engine", "TranslatorEngine"),
            "generator": ("modules.generation.engine", "GenerationEngine"),
            "law": ("modules.law.engine", "LawEngine"),
            "medicine": ("modules.medicine.engine", "MedicineEngine"),
            "agriculture": ("modules.agriculture.engine", "AgricultureEngine"),
            "physics": ("modules.physics.engine", "PhysicsEngine"),
            "music": ("modules.music.engine", "MusicEngine"),
            "sports": ("modules.sports.engine", "SportsEngine"),
            "economics": ("modules.economics.engine", "EconomicsEngine"),
            "education": ("modules.education.engine", "EducationEngine"),
            "foresight": ("modules.foresight.engine", "ForesightEngine"),
            "strategy": ("modules.strategy.engine", "StrategyEngine"),
            "integration": ("modules.integration.engine", "IntegrationEngine"),
            "media": ("modules.media.engine", "MediaEngine"),
            "accessibility": ("modules.accessibility.engine", "AccessibilityEngine"),
            "kids": ("modules.kids.engine", "KidsEngine"),
            "empowerment": ("modules.empowerment.engine", "EmpowermentEngine"),
            "agents": ("modules.agents.engine", "AgentsEngine"),
            "cybernetic_governance": ("modules.cybernetic_governance.engine", "CyberneticGovernanceEngine"),
        }
        
        if dep_name in dep_map:
            module_path, class_name = dep_map[dep_name]
            cls.get(dep_name, module_path, class_name, retry=False)
    
    # ============================================================
    # دوال مساعدة لتحميل المكونات الشائعة (مع التبعيات)
    # ============================================================
    
    @classmethod
    def get_governance(cls):
        return cls.get("governance", "modules.governance.engine", "GovernanceEngine")
    
    @classmethod
    def get_analysis(cls):
        return cls.get("analysis", "modules.analysis.engine", "AnalysisEngine")
    
    @classmethod
    def get_translator(cls):
        return cls.get("translator", "modules.i18n.engine", "TranslatorEngine")
    
    @classmethod
    def get_generator(cls):
        return cls.get("generator", "modules.generation.engine", "GenerationEngine")
    
    @classmethod
    def get_law(cls):
        return cls.get("law", "modules.law.engine", "LawEngine")
    
    @classmethod
    def get_medicine(cls):
        return cls.get("medicine", "modules.medicine.engine", "MedicineEngine")
    
    @classmethod
    def get_agriculture(cls):
        return cls.get("agriculture", "modules.agriculture.engine", "AgricultureEngine")
    
    @classmethod
    def get_physics(cls):
        return cls.get("physics", "modules.physics.engine", "PhysicsEngine")
    
    @classmethod
    def get_music(cls):
        return cls.get("music", "modules.music.engine", "MusicEngine")
    
    @classmethod
    def get_sports(cls):
        return cls.get("sports", "modules.sports.engine", "SportsEngine")
    
    @classmethod
    def get_economics(cls):
        return cls.get("economics", "modules.economics.engine", "EconomicsEngine")
    
    @classmethod
    def get_education(cls):
        return cls.get("education", "modules.education.engine", "EducationEngine")
    
    @classmethod
    def get_foresight(cls):
        return cls.get("foresight", "modules.foresight.engine", "ForesightEngine")
    
    @classmethod
    def get_strategy(cls):
        return cls.get("strategy", "modules.strategy.engine", "StrategyEngine")
    
    @classmethod
    def get_integration(cls):
        return cls.get("integration", "modules.integration.engine", "IntegrationEngine")
    
    @classmethod
    def get_media(cls):
        return cls.get("media", "modules.media.engine", "MediaEngine")
    
    @classmethod
    def get_accessibility(cls):
        return cls.get("accessibility", "modules.accessibility.engine", "AccessibilityEngine")
    
    @classmethod
    def get_kids(cls):
        return cls.get("kids", "modules.kids.engine", "KidsEngine")
    
    @classmethod
    def get_empowerment(cls):
        return cls.get("empowerment", "modules.empowerment.engine", "EmpowermentEngine")
    
    @classmethod
    def get_agents(cls):
        return cls.get("agents", "modules.agents.engine", "AgentsEngine")
    
    @classmethod
    def get_cybernetic_governance(cls):
        return cls.get("cybernetic_governance", "modules.cybernetic_governance.engine", "CyberneticGovernanceEngine")
    
    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        """جميع المكونات المحملة"""
        return cls._components.copy()
    
    @classmethod
    def get_load_times(cls) -> Dict[str, float]:
        """أوقات تحميل المكونات"""
        return cls._load_times.copy()
    
    @classmethod
    def clear(cls):
        """مسح جميع المكونات (لإعادة التحميل)"""
        cls._components.clear()
        cls._loading.clear()
        cls._load_times.clear()
        cls._retry_count.clear()
        logger.info("🔄 All components cleared")
    
    @classmethod
    def reload(cls, name: str):
        """إعادة تحميل مكون محدد"""
        if name in cls._components:
            cls._components.pop(name)
            cls._loading.pop(name, None)
            cls._load_times.pop(name, None)
            logger.info(f"🔄 Component '{name}' cleared for reload")
            return True
        return False
    
    @classmethod
    def is_loaded(cls, name: str) -> bool:
        """التحقق من تحميل مكون"""
        return name in cls._components
    
    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """حالة المحمل"""
        return {
            "loaded_components": list(cls._components.keys()),
            "total_loaded": len(cls._components),
            "loading_in_progress": list(cls._loading.keys()),
            "load_times": {k: f"{v:.2f}s" for k, v in cls._load_times.items()},
        }

# ============================================================
# نسخة وحيدة (Singleton) للمحمل
# ============================================================

loader = ComponentLoader
