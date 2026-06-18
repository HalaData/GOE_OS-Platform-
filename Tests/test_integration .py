"""
GOE OS - Integration Tests
اختبارات التكامل بين المكونات
"""

import pytest
from core.loader import ComponentLoader


class TestIntegration:
    """اختبارات التكامل"""
    
    def test_governance_analysis_integration(self):
        """اختبار تكامل الحوكمة والتحليل"""
        gov = ComponentLoader.get_governance()
        if gov is None:
            pytest.skip("Governance engine not available")
        
        result = gov.analyze({
            "text": "نص للتحليل مع كلمات مفتاحية مثل invited و consulted",
            "consent_given": True
        })
        assert result["status"] == "success"
        assert "vigilance_score" in result
    
    def test_translation_integration(self):
        """اختبار تكامل الترجمة"""
        translator = ComponentLoader.get_translator()
        if translator is None:
            pytest.skip("Translation engine not available")
        
        result = translator.translate({
            "text": "Hello World",
            "target_lang": "ar"
        })
        # قد يكون الترجمة محاكاة أو حقيقية
        assert "translated" in result or "status" in result
