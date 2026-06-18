"""
GOE OS - Economics & Entrepreneurship Engine
الاقتصاد: نماذج اقتصادية، سلاسل توريد، ريادة الأعمال، توليد أعمال
"""

import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

logger = logging.getLogger("GOE_OS.Economics")

class EconomicsEngine:
    """
    محرك الاقتصاد وريادة الأعمال - نماذج اقتصادية، سلاسل توريد، توليد أعمال
    """
    
    def __init__(self):
        self.forecast_history = []
        self.startup_history = []
        self.business_models = []
        logger.info("✅ Economics Engine initialized")
    
    def forecast(self, data: Dict) -> Dict:
        """التنبؤ الاقتصادي"""
        indicators = data.get("indicators", {})
        months = data.get("months", 6)
        
        inflation = indicators.get("inflation", 5.0)
        gdp_growth = indicators.get("gdp_growth", 2.5)
        unemployment = indicators.get("unemployment", 8.0)
        
        forecast = {
            "inflation_forecast": self._forecast_inflation(inflation, months),
            "gdp_forecast": self._forecast_gdp(gdp_growth, months),
            "unemployment_forecast": self._forecast_unemployment(unemployment, months),
            "confidence_interval": [0.7, 0.9]
        }
        
        result = {
            "status": "success",
            "forecast": forecast,
            "recommendations": self._get_economic_recommendations(forecast),
            "timestamp": datetime.now().isoformat()
        }
        
        self.forecast_history.append(result)
        return result
    
    def _forecast_inflation(self, current: float, months: int) -> List[float]:
        """التنبؤ بالتضخم"""
        return [round(current + (i * 0.2), 1) for i in range(months)]
    
    def _forecast_gdp(self, current: float, months: int) -> List[float]:
        """التنبؤ بالنمو"""
        return [round(current + (i * 0.1), 1) for i in range(months)]
    
    def _forecast_unemployment(self, current: float, months: int) -> List[float]:
        """التنبؤ بالبطالة"""
        return [round(current - (i * 0.1), 1) for i in range(months)]
    
    def _get_economic_recommendations(self, forecast: Dict) -> List[str]:
        """توصيات اقتصادية"""
        recommendations = ["مراقبة التضخم عن كثب", "تنويع مصادر الدخل"]
        if forecast["inflation_forecast"][-1] > 7:
            recommendations.append("رفع أسعار الفائدة تدريجياً")
        return recommendations
    
    def startup_analysis(self, data: Dict) -> Dict:
        """تحليل شركة ناشئة وتوليد خطة عمل"""
        idea = data.get("idea", "")
        market = data.get("market", "local")
        funding = data.get("funding", 50000)
        
        if not idea:
            return {"status": "error", "message": "لا توجد فكرة للتحليل"}
        
        business_plan = self._generate_business_plan(idea, market, funding)
        
        result = {
            "status": "success",
            "business_plan": business_plan,
            "market_analysis": self._analyze_market(market),
            "financial_projection": self._project_finances(funding),
            "recommendations": self._get_startup_recommendations(business_plan),
            "timestamp": datetime.now().isoformat()
        }
        
        self.startup_history.append(result)
        return result
    
    def _generate_business_plan(self, idea: str, market: str, funding: float) -> Dict:
        """توليد خطة عمل"""
        return {
            "name": f"مشروع: {idea[:30]}...",
            "vision": f"الريادة في {market} من خلال {idea[:50]}",
            "mission": f"تقديم حلول مبتكرة تلبي احتياجات السوق",
            "target_market": market,
            "initial_funding": funding,
            "key_activities": ["التطوير", "التسويق", "المبيعات"],
            "revenue_model": self._suggest_revenue_model(idea)
        }
    
    def _suggest_revenue_model(self, idea: str) -> str:
        """اقتراح نموذج إيرادات"""
        if "منصة" in idea:
            return "العمولات والاشتراكات"
        elif "تطبيق" in idea:
            return "الاشتراكات والتراخيص"
        else:
            return "المبيعات المباشرة"
    
    def _analyze_market(self, market: str) -> Dict:
        """تحليل السوق"""
        return {
            "size": "متوسطة",
            "growth": "متنامي",
            "competition": "متوسطة",
            "opportunities": ["طلب متزايد", "فجوات في السوق"],
            "risks": ["منافسة شديدة", "تغيرات سريعة"]
        }
    
    def _project_finances(self, funding: float) -> Dict:
        """التوقعات المالية"""
        return {
            "year_1_revenue": round(funding * 0.8, 0),
            "year_2_revenue": round(funding * 1.5, 0),
            "year_3_revenue": round(funding * 2.5, 0),
            "break_even_months": 18
        }
    
    def _get_startup_recommendations(self, plan: Dict) -> List[str]:
        """توصيات للشركة الناشئة"""
        return [
            "التركيز على السوق المستهدف",
            "بناء فريق قوي",
            "التسويق الرقمي الفعال",
            "مراقبة التدفق النقدي"
        ]
    
    def supply_chain_analysis(self, data: Dict) -> Dict:
        """تحليل سلسلة التوريد"""
        supplier_concentration = data.get("supplier_concentration", 0.5)
        geopolitical_risk = data.get("geopolitical_risk", 0.3)
        inventory_level = data.get("inventory_level", 0.6)
        
        risk_score = (supplier_concentration * 0.3 + geopolitical_risk * 0.3 + (1 - inventory_level) * 0.4)
        
        return {
            "status": "success",
            "risk_score": round(risk_score, 2),
            "risk_level": "high" if risk_score > 0.6 else "medium" if risk_score > 0.4 else "low",
            "recommendations": self._get_supply_chain_recommendations(risk_score),
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_supply_chain_recommendations(self, risk: float) -> List[str]:
        """توصيات سلسلة التوريد"""
        if risk > 0.6:
            return ["تنويع الموردين", "زيادة المخزون الاحتياطي"]
        elif risk > 0.4:
            return ["مراقبة الموردين", "تحسين إدارة المخزون"]
        else:
            return ["الحفاظ على الوضع الحالي"]
