"""
GOE OS - Advanced Risk Engine Tests
اختبارات محرك المخاطر المتقدم
"""

import pytest
from modules.entrepreneurship.advanced_risk_engine import AdvancedRiskEngine


class TestAdvancedRisk:
    """اختبارات محرك المخاطر المتقدم"""
    
    def test_risk_init(self):
        """اختبار تهيئة المحرك"""
        engine = AdvancedRiskEngine()
        assert engine is not None
        assert hasattr(engine, 'risk_models')
        assert hasattr(engine, 'analysis_history')
    
    def test_market_demand_analysis(self):
        """اختبار تحليل الطلب السوقي"""
        engine = AdvancedRiskEngine()
        result = engine.analyze_market_demand({
            "social_media": ["منتج رائع", "بحاجة لهذا المنتج"],
            "competitors": [{"name": "منافس 1"}],
            "surveys": [{"interest": 0.8}]
        })
        assert "proactive_demand_index" in result
        assert "recommendation" in result
    
    def test_cash_flow_prediction(self):
        """اختبار التنبؤ بالتدفق النقدي"""
        engine = AdvancedRiskEngine()
        result = engine.predict_cash_flow({
            "current_cash": 100000,
            "monthly_burn": 20000,
            "revenue_growth": 0.05
        })
        assert "predictions" in result
        assert "burn_rate" in result
        assert "cash_warning" in result
    
    def test_team_analysis(self):
        """اختبار تحليل الفريق"""
        engine = AdvancedRiskEngine()
        result = engine.analyze_team({
            "members": [
                {"name": "عضو 1", "role": "مطور"},
                {"name": "عضو 2", "role": "مسوق"}
            ],
            "conflicts": []
        })
        assert "team_cohesion_index" in result
        assert "recommendations" in result
    
    def test_comprehensive_risk_report(self):
        """اختبار التقرير الشامل للمخاطر"""
        engine = AdvancedRiskEngine()
        result = engine.comprehensive_risk_report({
            "market": {"social_media": ["test"]},
            "financial": {"current_cash": 50000},
            "team": {"members": [{"name": "test"}]},
            "business": {},
            "legal": {"contracts": []},
            "network": {"partners": []}
        })
        assert "success_probability" in result
        assert "failure_probability" in result
        assert "recommendations" in result
