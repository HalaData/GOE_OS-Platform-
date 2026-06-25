"""
المحرك التلقائي - يكتشف المكونات الجديدة ويحملها تلقائياً
"""

import os
import importlib
import inspect
from fastapi import APIRouter, FastAPI
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AutoLoader:
    def __init__(self, app: FastAPI, base_path: str = "core", prefix: str = "/api/v2"):
        self.app = app
        self.base_path = base_path
        self.prefix = prefix
        self.loaded_modules = {}
        self.watch_folders = [base_path, "modules", "execution"]
    
    def discover_and_load(self, folders: List[str] = None) -> Dict:
        if folders is None:
            folders = self.watch_folders
        
        results = {}
        for folder in folders:
            if os.path.exists(folder):
                results[folder] = self._scan_folder(folder)
            else:
                logger.warning(f"⚠️ المجلد {folder} غير موجود")
                results[folder] = {"status": "not_found", "modules": []}
        
        return results
    
    def _scan_folder(self, folder: str) -> Dict:
        modules = []
        for file in os.listdir(folder):
            if file.endswith(".py") and not file.startswith("__") and not file.startswith("auto"):
                module_name = file[:-3]
                try:
                    module = importlib.import_module(f"{folder}.{module_name}")
                    classes = self._extract_classes(module)
                    
                    if classes:
                        router = self._generate_router(module_name, classes, folder)
                        if router:
                            self.app.include_router(router, prefix=f"{self.prefix}/{module_name}")
                            modules.append({
                                "name": module_name,
                                "classes": classes,
                                "status": "loaded",
                                "endpoints": self._get_endpoints(router)
                            })
                except Exception as e:
                    logger.error(f"❌ فشل تحميل {module_name}: {e}")
                    modules.append({"name": module_name, "error": str(e), "status": "failed"})
        
        return {"modules": modules, "count": len(modules)}
    
    def _extract_classes(self, module) -> List[str]:
        classes = []
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module.__name__:
                if name not in ["BaseModel", "FastAPI", "APIRouter"]:
                    classes.append(name)
        return classes
    
    def _generate_router(self, module_name: str, classes: List[str], folder: str):
        try:
            router = APIRouter(tags=[module_name])
            module = importlib.import_module(f"{folder}.{module_name}")
            
            for class_name in classes:
                if class_name in ["__init__"]:
                    continue
                cls = getattr(module, class_name)
                methods = inspect.getmembers(cls, inspect.isfunction)
                for method_name, method in methods:
                    if not method_name.startswith("_") and method_name not in ["__init__"]:
                        self._add_endpoint(router, class_name, method_name, method)
            
            return router
        except Exception as e:
            logger.error(f"❌ فشل توليد نقاط النهاية: {e}")
            return None
    
    def _add_endpoint(self, router: APIRouter, class_name: str, method_name: str, method):
        endpoint_name = f"{class_name.lower()}_{method_name}"
        method_type = "POST" if method_name in ["analyze", "predict", "generate", "create", "calculate", "simulate", "run"] else "GET"
        
        if method_type == "POST":
            router.add_api_route(
                f"/{endpoint_name}",
                self._create_handler(class_name, method_name),
                methods=["POST"],
                name=endpoint_name,
                tags=[class_name.lower()]
            )
        else:
            router.add_api_route(
                f"/{endpoint_name}",
                self._create_handler(class_name, method_name),
                methods=["GET"],
                name=endpoint_name,
                tags=[class_name.lower()]
            )
    
    def _create_handler(self, class_name: str, method_name: str):
        async def handler(request: Dict = None):
            return {
                "status": "success",
                "module": class_name,
                "method": method_name,
                "data": request or {},
                "timestamp": datetime.now().isoformat()
            }
        return handler
    
    def _get_endpoints(self, router: APIRouter) -> List[str]:
        return [route.path for route in router.routes]
