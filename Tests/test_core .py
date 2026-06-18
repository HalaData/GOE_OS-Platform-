"""
GOE OS - Core Component Tests
اختبارات المكونات الأساسية
"""

import pytest
from core.engine import engine
from core.loader import ComponentLoader
from core.utils import SimpleCache, hash_text, clean_text, merge_dicts


class TestEngine:
    """اختبارات محرك GOE الرئيسي"""
    
    def test_engine_singleton(self):
        """اختبار أن المحرك هو Singleton"""
        e1 = engine
        e2 = engine
        assert e1 is e2
    
    def test_engine_status(self):
        """اختبار حالة المحرك"""
        status = engine.get_status()
        assert status["status"] == "running"
        assert "components" in status
        assert "uptime_seconds" in status


class TestComponentLoader:
    """اختبارات محمل المكونات"""
    
    def test_loader_get_component(self):
        """اختبار تحميل مكون"""
        # محاولة تحميل مكون غير موجود
        component = ComponentLoader.get("non_existent", "non_existent.module", "NonExistentClass")
        assert component is None
    
    def test_loader_get_all(self):
        """اختبار الحصول على جميع المكونات المحملة"""
        components = ComponentLoader.get_all()
        assert isinstance(components, dict)
    
    def test_loader_clear(self):
        """اختبار مسح المكونات"""
        ComponentLoader.clear()
        assert len(ComponentLoader.get_all()) == 0


class TestUtils:
    """اختبارات الدوال المساعدة"""
    
    def test_cache(self):
        """اختبار التخزين المؤقت"""
        cache = SimpleCache(max_size=2)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        assert cache.get("key1") == "value1"
        assert cache.size() == 2
    
    def test_cache_overflow(self):
        """اختبار تجاوز سعة التخزين المؤقت"""
        cache = SimpleCache(max_size=2)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        assert cache.size() == 2
        assert cache.get("key1") is None
    
    def test_hash_text(self):
        """اختبار تجزئة النص"""
        h1 = hash_text("test")
        h2 = hash_text("test")
        assert h1 == h2
        assert len(h1) == 32
    
    def test_clean_text(self):
        """اختبار تنظيف النص"""
        text = "  هذا  نص   مع  مسافات  "
        cleaned = clean_text(text)
        assert cleaned == "هذا نص مع مسافات"
    
    def test_merge_dicts(self):
        """اختبار دمج القواميس"""
        dict1 = {"a": 1, "b": 2}
        dict2 = {"b": 3, "c": 4}
        merged = merge_dicts(dict1, dict2)
        assert merged["a"] == 1
        assert merged["b"] == 3
        assert merged["c"] == 4
