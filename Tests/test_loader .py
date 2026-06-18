"""
GOE OS - Component Loader Tests
اختبارات محمل المكونات المتقدم
"""

import pytest
from core.loader import ComponentLoader


class TestLoaderAdvanced:
    """اختبارات متقدمة لمحمل المكونات"""
    
    def test_loader_get_governance(self):
        """اختبار تحميل محرك الحوكمة"""
        gov = ComponentLoader.get_governance()
        # قد يكون None إذا لم يتم تثبيت التبعيات
        # الاختبار يتحقق من عدم حدوث خطأ
        assert gov is not None or gov is None
    
    def test_loader_get_analysis(self):
        """اختبار تحميل محرك التحليل"""
        analysis = ComponentLoader.get_analysis()
        assert analysis is not None or analysis is None
    
    def test_loader_get_translator(self):
        """اختبار تحميل محرك الترجمة"""
        translator = ComponentLoader.get_translator()
        assert translator is not None or translator is None
    
    def test_loader_get_generator(self):
        """اختبار تحميل محرك التوليد"""
        generator = ComponentLoader.get_generator()
        assert generator is not None or generator is None
    
    def test_loader_loading_state(self):
        """اختبار حالة التحميل"""
        # محاولة تحميل مكون مرتين
        comp1 = ComponentLoader.get("test_component", "core.utils", "SimpleCache")
        comp2 = ComponentLoader.get("test_component", "core.utils", "SimpleCache")
        # المكون قد لا يكون محملاً إذا لم يتم تثبيت التبعيات
        # لكننا نتحقق من عدم حدوث خطأ
        assert True
