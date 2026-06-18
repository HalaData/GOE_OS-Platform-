"""
GOE OS - Lazy Component Loader
تحميل كسول للمكونات الثقيلة (Lazy Loading)
"""

import logging
import importlib
from typing import Dict, Any, Optional

logger = logging.getLogger("GOE_OS.Loader")

class ComponentLoader:
    """
    محمل المكونات - تحميل كسول (عند الطلب فقط)
    """
    
    _components: Dict[str, Any] = {}
    _loading: Dict[str, bool] = {}
    
    @classmethod
    def get(cls, name: str, module_path: str, class_name: str) -> Optional[Any]:
        """
        تحميل مكون عند أول طلب فقط
        """
        # إذا كان المكون محملاً بالفعل
        if name in cls._components:
            return cls._components[name]
        
        # منع التحميل المتزامن المتكرر
        if cls._loading.get(name, False):
            logger.warning(f"Component '{name}' is already loading")
            return None
        
        cls._loading[name] = True
        
        try:
            module = importlib.import_module(module_path)
            component = getattr(module, class_name)()
            cls._components[name] = component
            logger.info(f"✅ Component loaded: {name}")
            return component
        except ImportError as e:
            logger.error(f"Import error for '{name}': {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to load component '{name}': {e}")
            return None
        finally:
            cls._loading[name] = False
    
    # ============================================================
    # دوال مساعدة لتحميل المكونات الشائعة
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
    def clear(cls):
        """مسح جميع المكونات (لإعادة التحميل)"""
        cls._components.clear()
        cls._loading.clear()
        logger.info("🔄 All components cleared")
