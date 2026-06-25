"""
AgriOS - الروزنامات الإضافية
تكملة للروزنامات اللانهائية (الأبقار، الصمغ العربي، الأغنام، النحل، الأسماك، الأخشاب)
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

# ============================================================
# 1. روزنامة الأبقار (Cattle Calendar)
# ============================================================

class CattleInfiniteCalendar:
    """
    روزنامة غير نهائية لإنتاج الأبقار (حليب، لحم)
    """
    
    def __init__(self):
        self.breeds = {
            "dairy": {"name": "أبقار حلاب", "cycle_days": 305, "milk": 20},
            "beef": {"name": "أبقار لحم", "cycle_days": 365, "weight": 600}
        }
    
    def generate_infinite_calendar(self, breed_type: str, start_date: str, farm_data: Dict) -> Dict:
        breed = self.breeds.get(breed_type, self.breeds["dairy"])
        start_date_obj = datetime.fromisoformat(start_date)
        
        days = []
        current_date = start_date_obj
        
        phases = [
            {"phase": "فترة الحمل المبكر", "days": 90, "tasks": ["فحص الحمل", "تحسين التغذية", "مراقبة الصحة"]},
            {"phase": "فترة الحمل المتوسط", "days": 90, "tasks": ["تغذية متوازنة", "تمارين خفيفة", "تحضير للولادة"]},
            {"phase": "فترة الحمل المتأخر", "days": 90, "tasks": ["تغذية عالية الطاقة", "تحضير مكان الولادة", "مراقبة يومية"]},
            {"phase": "الولادة وفترة ما بعدها", "days": 35, "tasks": ["مساعدة الولادة", "رعاية العجل", "بداية الحلب"]},
            {"phase": "فترة الحلب", "days": 220, "tasks": ["حلب يومي", "تغذية مكثفة", "مراقبة الصحة"]},
            {"phase": "فترة الجفاف", "days": 60, "tasks": ["إيقاف الحلب", "تغذية جافة", "التحضير للحمل القادم"]}
        ]
        
        day_count = 0
        
        for cycle in range(2):
            for phase in phases:
                for day in range(phase["days"]):
                    day_count += 1
                    days.append({
                        "day": day_count,
                        "date": current_date.strftime("%Y-%m-%d"),
                        "phase": phase["phase"],
                        "tasks": phase["tasks"],
                        "cycle": cycle + 1,
                        "is_critical": phase["phase"] in ["الولادة وفترة ما بعدها", "فترة الحلب"],
                        "milk_production": self._get_milk_production(phase, day, breed),
                        "recommendation": self._get_cattle_recommendation(phase, day)
                    })
                    current_date += timedelta(days=1)
        
        return {
            "breed": breed["name"],
            "start_date": start_date,
            "total_days": len(days),
            "calendar": days,
            "forecast": self._get_cattle_forecast(day_count, breed),
            "infinite": True,
            "can_expand": True
        }
    
    def _get_milk_production(self, phase: Dict, day: int, breed: Dict) -> float:
        if phase["phase"] == "فترة الحلب":
            return round(breed["milk"] * (0.8 + 0.2 * (day / 220)), 1)
        return 0
    
    def _get_cattle_recommendation(self, phase: Dict, day: int) -> str:
        if phase["phase"] == "الولادة وفترة ما بعدها":
            return "⚠️ أيام حرجة: جهز مكان الولادة، تأكد من وجود طبيب بيطري"
        elif phase["phase"] == "فترة الحلب":
            return "🥛 حلب مرتين يومياً، مراقبة صحة الضرع"
        else:
            return "📋 استمر في التغذية والمتابعة المنتظمة"
    
    def _get_cattle_forecast(self, total_days: int, breed: Dict) -> Dict:
        return {
            "total_milk": round(total_days * breed.get("milk", 20) * 0.5, 1) if "dairy" in breed["name"] else 0,
            "calves_produced": round(total_days / 365, 0),
            "total_feed": round(total_days * 15, 1)
        }

# ============================================================
# 2. روزنامة الصمغ العربي (Gum Arabic Calendar)
# ============================================================

class GumArabicInfiniteCalendar:
    """
    روزنامة غير نهائية لإنتاج الصمغ العربي
    """
    
    def __init__(self):
        self.tree_types = {
            "hashab": {"name": "هشاب", "yield": 0.8, "peak_years": (5, 20)},
            "talh": {"name": "طلح", "yield": 0.5, "peak_years": (8, 25)}
        }
    
    def generate_infinite_calendar(self, tree_type: str, start_date: str, tree_data: Dict) -> Dict:
        tree = self.tree_types.get(tree_type, self.tree_types["hashab"])
        start_date_obj = datetime.fromisoformat(start_date)
        
        days = []
        current_date = start_date_obj
        
        phases = [
            {"phase": "تحضير الأشجار", "days": 30, "tasks": ["تنظيف قاعدة الشجرة", "إزالة الأغصان الجافة", "فحص الصحة"]},
            {"phase": "عملية التبكيت", "days": 15, "tasks": ["عمل 2-3 جروح في الجذع", "مراقبة تسرب الصمغ"]},
            {"phase": "جمع الصمغ الأول", "days": 10, "tasks": ["جمع الصمغ بعد 30 يوم", "تحديد الجودة"]},
            {"phase": "إعادة التبكيت", "days": 15, "tasks": ["إعادة عملية التبكيت", "جمع الصمغ الثاني"]},
            {"phase": "جمع الصمغ الثاني", "days": 15, "tasks": ["جمع الصمغ الثاني", "تصنيف الجودة"]},
            {"phase": "فترة الراحة", "days": 90, "tasks": ["راحة الأشجار", "مراقبة النمو", "تحضير للموسم القادم"]}
        ]
        
        day_count = 0
        
        for season in range(4):
            for phase in phases:
                for day in range(phase["days"]):
                    day_count += 1
                    days.append({
                        "day": day_count,
                        "date": current_date.strftime("%Y-%m-%d"),
                        "season": season + 1,
                        "phase": phase["phase"],
                        "tasks": phase["tasks"],
                        "expected_yield": self._get_yield_forecast(season, tree, day_count),
                        "quality": self._get_quality_forecast(season, day_count),
                        "recommendation": self._get_gum_recommendation(phase, season)
                    })
                    current_date += timedelta(days=1)
        
        return {
            "tree_type": tree["name"],
            "start_date": start_date,
            "total_days": len(days),
            "calendar": days,
            "forecast": self._get_gum_forecast(day_count, tree),
            "infinite": True,
            "sustainable": True
        }
    
    def _get_yield_forecast(self, season: int, tree: Dict, day: int) -> float:
        base_yield = tree["yield"]
        peak_factor = 1.0 if season < 2 else 0.6
        return round(base_yield * peak_factor * random.uniform(0.8, 1.2), 2)
    
    def _get_quality_forecast(self, season: int, day: int) -> str:
        if season == 0:
            return "جودة عالية"
        elif season == 1:
            return "جودة متوسطة"
        else:
            return "جودة منخفضة"
    
    def _get_gum_recommendation(self, phase: Dict, season: int) -> str:
        if phase["phase"] == "عملية التبكيت":
            return f"⚠️ موسم {season+1}: تبكيت عميق 3 جروح في كل شجرة"
        elif phase["phase"] == "جمع الصمغ الأول":
            return f"📦 موسم {season+1}: جمع الصمغ بعد 30 يوم، تصنيف حسب اللون"
        else:
            return "📋 استمر في الممارسات المستدامة"
    
    def _get_gum_forecast(self, total_days: int, tree: Dict) -> Dict:
        return {
            "total_yield": round(total_days * tree["yield"] * 0.1, 1),
            "quality_high": round(total_days * 0.3, 0),
            "quality_medium": round(total_days * 0.4, 0),
            "quality_low": round(total_days * 0.3, 0)
        }

# ============================================================
# 3. روزنامة الأغنام والماعز (Sheep & Goats Calendar)
# ============================================================

class SheepGoatInfiniteCalendar:
    """
    روزنامة غير نهائية لإنتاج الأغنام والماعز
    """
    
    def __init__(self):
        self.types = {
            "sheep": {"name": "أغنام", "gestation": 150, "lambing_interval": 180},
            "goats": {"name": "ماعز", "gestation": 150, "lambing_interval": 180}
        }
    
    def generate_infinite_calendar(self, animal_type: str, start_date: str, farm_data: Dict) -> Dict:
        animal = self.types.get(animal_type, self.types["sheep"])
        start_date_obj = datetime.fromisoformat(start_date)
        
        days = []
        current_date = start_date_obj
        
        phases = [
            {"phase": "فترة التزاوج", "days": 30, "tasks": ["اختيار الذكور", "مراقبة التزاوج", "تغذية محسنة"]},
            {"phase": "فترة الحمل المبكر", "days": 60, "tasks": ["تغذية متوازنة", "مراقبة الصحة", "فصل الذكور"]},
            {"phase": "فترة الحمل المتأخر", "days": 60, "tasks": ["تغذية عالية الطاقة", "تحضير مكان الولادة", "مراقبة يومية"]},
            {"phase": "الولادة ورعاية الصغار", "days": 30, "tasks": ["مساعدة الولادة", "رعاية الصغار", "تحصين"]},
            {"phase": "فترة الرضاعة", "days": 60, "tasks": ["تغذية الأمهات", "مراقبة النمو", "فطام تدريجي"]},
            {"phase": "فترة الراحة", "days": 30, "tasks": ["راحة القطيع", "مراقبة الصحة", "تحضير للموسم القادم"]}
        ]
        
        day_count = 0
        
        for cycle in range(3):
            for phase in phases:
                for day in range(phase["days"]):
                    day_count += 1
                    days.append({
                        "day": day_count,
                        "date": current_date.strftime("%Y-%m-%d"),
                        "phase": phase["phase"],
                        "tasks": phase["tasks"],
                        "cycle": cycle + 1,
                        "is_critical": phase["phase"] in ["الولادة ورعاية الصغار", "فترة التزاوج"],
                        "expected_offspring": self._get_offspring_forecast(phase, animal),
                        "recommendation": self._get_sheep_recommendation(phase, day)
                    })
                    current_date += timedelta(days=1)
        
        return {
            "animal_type": animal["name"],
            "start_date": start_date,
            "total_days": len(days),
            "calendar": days,
            "forecast": self._get_sheep_forecast(day_count, animal),
            "infinite": True
        }
    
    def _get_offspring_forecast(self, phase: Dict, animal: Dict) -> str:
        if phase["phase"] == "الولادة ورعاية الصغار":
            return f"{random.randint(1, 3)} صغار"
        return "لا يوجد"
    
    def _get_sheep_recommendation(self, phase: Dict, day: int) -> str:
        if phase["phase"] == "فترة التزاوج":
            return "⚠️ موسم التزاوج: اختر الذكور المناسبة"
        elif phase["phase"] == "الولادة ورعاية الصغار":
            return "🤱 أيام حرجة: جهز مكان الولادة، نظف الصغار"
        else:
            return "📋 استمر في التغذية والمتابعة"
    
    def _get_sheep_forecast(self, total_days: int, animal: Dict) -> Dict:
        return {
            "total_offspring": round(total_days / 180 * 2, 0),
            "total_feed": round(total_days * 2, 1),
            "mortality_rate": round(random.uniform(5, 15), 1)
        }

# ============================================================
# 4. روزنامة النحل (Bees Calendar)
# ============================================================

class BeesInfiniteCalendar:
    """
    روزنامة غير نهائية لإنتاج العسل
    """
    
    def __init__(self):
        self.hive_types = {
            "modern": {"name": "خلايا حديثة", "yield": 25},
            "traditional": {"name": "خلايا تقليدية", "yield": 12}
        }
    
    def generate_infinite_calendar(self, hive_type: str, start_date: str, farm_data: Dict) -> Dict:
        hive = self.hive_types.get(hive_type, self.hive_types["modern"])
        start_date_obj = datetime.fromisoformat(start_date)
        
        days = []
        current_date = start_date_obj
        
        phases = [
            {"phase": "تحضير الخلايا", "days": 20, "tasks": ["تنظيف الخلايا", "فحص الملكة", "تجهيز الغذاء"]},
            {"phase": "موسم الرحيق", "days": 60, "tasks": ["مراقبة الخلايا", "إضافة براويز", "جمع العسل"]},
            {"phase": "تكاثر النحل", "days": 30, "tasks": ["مراقبة التكاثر", "تقسيم الخلايا", "تجهيز خلايا جديدة"]},
            {"phase": "موسم الجفاف", "days": 40, "tasks": ["توفير الماء", "تغذية صناعية", "مراقبة الأمراض"]},
            {"phase": "فترة الراحة", "days": 30, "tasks": ["فحص صحي", "علاج الأمراض", "تحضير لموسم جديد"]}
        ]
        
        day_count = 0
        
        for cycle in range(2):
            for phase in phases:
                for day in range(phase["days"]):
                    day_count += 1
                    days.append({
                        "day": day_count,
                        "date": current_date.strftime("%Y-%m-%d"),
                        "phase": phase["phase"],
                        "tasks": phase["tasks"],
                        "cycle": cycle + 1,
                        "expected_honey": self._get_honey_forecast(phase, hive),
                        "recommendation": self._get_bees_recommendation(phase, day)
                    })
                    current_date += timedelta(days=1)
        
        return {
            "hive_type": hive["name"],
            "start_date": start_date,
            "total_days": len(days),
            "calendar": days,
            "forecast": self._get_bees_forecast(day_count, hive),
            "infinite": True
        }
    
    def _get_honey_forecast(self, phase: Dict, hive: Dict) -> float:
        if phase["phase"] == "موسم الرحيق":
            return round(hive["yield"] * random.uniform(0.3, 0.7), 1)
        return 0
    
    def _get_bees_recommendation(self, phase: Dict, day: int) -> str:
        if phase["phase"] == "موسم الرحيق":
            return "🍯 مراقبة الخلايا يومياً، جمع العسل عند اكتمال الإطارات"
        elif phase["phase"] == "موسم الجفاف":
            return "💧 توفير الماء للنحل، تغذية صناعية عند الحاجة"
        else:
            return "📋 استمر في الفحص الدوري"
    
    def _get_bees_forecast(self, total_days: int, hive: Dict) -> Dict:
        return {
            "total_honey": round(total_days * 0.1, 1),
            "hive_expansion": round(total_days / 60, 0),
            "queen_health": round(random.uniform(70, 95), 1)
        }

# ============================================================
# 5. روزنامة الأسماك (Fish Calendar)
# ============================================================

class FishInfiniteCalendar:
    """
    روزنامة غير نهائية للاستزراع السمكي
    """
    
    def __init__(self):
        self.fish_types = {
            "tilapia": {"name": "بلطي", "cycle_days": 180, "weight": 0.8},
            "catfish": {"name": "قرموط", "cycle_days": 240, "weight": 1.2},
            "carp": {"name": "مبني", "cycle_days": 210, "weight": 1.0}
        }
    
    def generate_infinite_calendar(self, fish_type: str, start_date: str, farm_data: Dict) -> Dict:
        fish = self.fish_types.get(fish_type, self.fish_types["tilapia"])
        start_date_obj = datetime.fromisoformat(start_date)
        
        days = []
        current_date = start_date_obj
        
        phases = [
            {"phase": "تحضير الأحواض", "days": 15, "tasks": ["تنظيف الأحواض", "ضبط جودة الماء", "تجهيز التهوية"]},
            {"phase": "استقبال الزريعة", "days": 5, "tasks": ["استقبال الزريعة", "فحص الصحة", "تغذية بدائية"]},
            {"phase": "النمو المبكر", "days": 45, "tasks": ["تغذية مرتين يومياً", "مراقبة جودة الماء", "فحص دوري"]},
            {"phase": "النمو المتوسط", "days": 60, "tasks": ["تغذية 3 مرات يومياً", "مراقبة النمو", "تغيير الماء"]},
            {"phase": "النمو المتأخر", "days": 50, "tasks": ["تغذية عالية البروتين", "مراقبة الصحة", "تحضير للحصاد"]},
            {"phase": "الحصاد", "days": 5, "tasks": ["صيد الأسماك", "تصنيف حسب الوزن", "تسويق"]}
        ]
        
        day_count = 0
        
        for cycle in range(2):
            for phase in phases:
                for day in range(phase["days"]):
                    day_count += 1
                    days.append({
                        "day": day_count,
                        "date": current_date.strftime("%Y-%m-%d"),
                        "phase": phase["phase"],
                        "tasks": phase["tasks"],
                        "cycle": cycle + 1,
                        "expected_weight": self._get_weight_forecast(phase, day, fish),
                        "water_quality": self._get_water_quality(phase, day),
                        "recommendation": self._get_fish_recommendation(phase, day)
                    })
                    current_date += timedelta(days=1)
        
        return {
            "fish_type": fish["name"],
            "start_date": start_date,
            "total_days": len(days),
            "calendar": days,
            "forecast": self._get_fish_forecast(day_count, fish),
            "infinite": True
        }
    
    def _get_weight_forecast(self, phase: Dict, day: int, fish: Dict) -> float:
        if phase["phase"] == "الحصاد":
            return fish["weight"]
        return round(fish["weight"] * (day / fish["cycle_days"]) * 0.8, 2)
    
    def _get_water_quality(self, phase: Dict, day: int) -> str:
        if day % 15 == 0:
            return "جيدة" if random.random() > 0.2 else "تحتاج تحسين"
        return "جيدة"
    
    def _get_fish_recommendation(self, phase: Dict, day: int) -> str:
        if phase["phase"] == "استقبال الزريعة":
            return "⚠️ أيام حساسة: تأكد من درجة الحرارة 26-28 درجة مئوية"
        elif phase["phase"] == "الحصاد":
            return "🐟 وزن متوقع {:.1f} كغم".format(random.uniform(0.7, 1.0))
        else:
            return "📋 استمر في التغذية والمراقبة"
    
    def _get_fish_forecast(self, total_days: int, fish: Dict) -> Dict:
        return {
            "total_weight": round(total_days * 0.005, 1),
            "survival_rate": round(random.uniform(70, 90), 1),
            "total_feed": round(total_days * 0.1, 1)
        }

# ============================================================
# 6. المحرك الرئيسي للروزنامات الإضافية
# ============================================================

class AdditionalCalendarEngine:
    """
    المحرك الرئيسي لتوليد جميع الروزنامات الإضافية
    """
    
    def __init__(self):
        self.calendars = {
            "cattle": CattleInfiniteCalendar(),
            "gum_arabic": GumArabicInfiniteCalendar(),
            "sheep_goat": SheepGoatInfiniteCalendar(),
            "bees": BeesInfiniteCalendar(),
            "fish": FishInfiniteCalendar()
        }
    
    def generate(self, calendar_type: str, start_date: str, farm_data: Dict) -> Dict:
        if calendar_type in self.calendars:
            return self.calendars[calendar_type].generate_infinite_calendar(
                farm_data.get("subtype", "dairy"),
                start_date,
                farm_data
            )
        else:
            return {"error": f"Unknown calendar type: {calendar_type}"}

# ============================================================
# 7. نقاط النهاية API
# ============================================================

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v2/agriculture/additional-calendars", tags=["AgriOS Additional Calendars"])

_calendar_engine = None

def get_calendar_engine() -> AdditionalCalendarEngine:
    global _calendar_engine
    if _calendar_engine is None:
        _calendar_engine = AdditionalCalendarEngine()
    return _calendar_engine

@router.post("/generate/{calendar_type}")
async def generate_calendar(calendar_type: str, start_date: str, farm_data: Dict):
    """توليد روزنامة غير نهائية"""
    engine = get_calendar_engine()
    result = engine.generate(calendar_type, start_date, farm_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/types")
async def get_calendar_types():
    """أنواع الروزنامات المتاحة"""
    return {
        "types": [
            {"id": "cattle", "name": "أبقار", "subtypes": ["dairy", "beef"]},
            {"id": "gum_arabic", "name": "صمغ عربي", "subtypes": ["hashab", "talh"]},
            {"id": "sheep_goat", "name": "أغنام وماعز", "subtypes": ["sheep", "goats"]},
            {"id": "bees", "name": "نحل", "subtypes": ["modern", "traditional"]},
            {"id": "fish", "name": "أسماك", "subtypes": ["tilapia", "catfish", "carp"]}
        ]
    }
