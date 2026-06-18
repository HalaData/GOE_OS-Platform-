"""
GOE OS - Governance Module Tests
اختبارات وحدة الحوكمة
"""

import pytest
from modules.governance.engine import GovernanceEngine


class TestGovernanceEngine:
    """اختبارات محرك الحوكمة"""
    
    def test_governance_init(self):
        """اختبار تهيئة محرك الحوكمة"""
        gov = GovernanceEngine()
        assert gov is not None
        assert hasattr(gov, 'indicators')
        assert hasattr(gov, 'analysis_history')
    
    def test_governance_analyze_without_consent(self):
        """اختبار التحليل بدون موافقة"""
        gov = GovernanceEngine()
        result = gov.analyze({"text": "نص للتحليل", "consent_given": False})
        assert result["status"] == "consent_required"
    
    def test_governance_analyze_with_consent(self, sample_governance_request):
        """اختبار التحليل مع الموافقة"""
        gov = GovernanceEngine()
        result = gov.analyze(sample_governance_request)
        assert result["status"] == "success"
        assert "vigilance_score" in result
        assert "indicators" in result
    
    def test_governance_get_indicators(self):
        """اختبار الحصول على المؤشرات"""
        gov = GovernanceEngine()
        indicators = gov.get_indicators()
        assert isinstance(indicators, dict)
    
    def test_governance_create_indicator(self):
        """اختبار إنشاء مؤشر جديد"""
        gov = GovernanceEngine()
        result = gov.create_indicator({
            "id": "TEST_IND",
            "name": "مؤشر اختبار",
            "question": "سؤال اختبار",
            "threshold": 0.5
        })
        assert result["status"] == "created"
        assert "TEST_IND" in gov.indicators
