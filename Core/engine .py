"""
GOE OS - Core Engine (Singleton)
المحرك الرئيسي للمنصة - يدير جميع المكونات بشكل مرن
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger("GOE_OS.Engine")

class GOEEngine:
    """
    المحرك الرئيسي للمنصة - يوفر واجهة موحدة لجميع المكونات
    """
    
    _instance = None
    _executor = ThreadPoolExecutor(max_workers=4)
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._components = {}
        self._startup_time = datetime.now()
        self._request_count = 0
        logger.info("🚀 GOE Engine initialized")
    
    def register_component(self, name: str, component: Any) -> None:
        """تسجيل مكون في المحرك"""
        self._components[name] = component
        logger.info(f"✅ Component registered: {name}")
    
    def get_component(self, name: str) -> Optional[Any]:
        """الحصول على مكون"""
        return self._components.get(name)
    
    def get_status(self) -> Dict:
        """حالة المحرك"""
        uptime = (datetime.now() - self._startup_time).total_seconds()
        return {
            "status": "running",
            "components": list(self._components.keys()),
            "components_count": len(self._components),
            "uptime_seconds": round(uptime, 2),
            "uptime_hours": round(uptime / 3600, 2),
            "started_at": self._startup_time.isoformat(),
            "request_count": self._request_count
        }
    
    def increment_requests(self) -> None:
        """زيادة عدد الطلبات"""
        self._request_count += 1

# ============================================================
# إنشاء نسخة واحدة من المحرك (Singleton)
# ============================================================

engine = GOEEngine()
