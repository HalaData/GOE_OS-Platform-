"""
نظام السمعة والتأثير
"""

from typing import Dict, List
from datetime import datetime

class ReputationSystem:
    def __init__(self):
        self.users = {}
        self.components = {}
    
    def add_user(self, user_id: str, name: str) -> Dict:
        if user_id in self.users:
            return {"status": "error", "message": "User already exists"}
        
        self.users[user_id] = {
            "name": name,
            "reputation": 0,
            "contributions": 0,
            "badges": [],
            "stars_given": 0,
            "forks_created": 0,
            "joined_at": datetime.utcnow().isoformat()
        }
        return {"status": "success", "user": self.users[user_id]}
    
    def star_component(self, user_id: str, component_id: str) -> Dict:
        if user_id not in self.users:
            return {"status": "error", "message": "User not found"}
        
        if component_id not in self.components:
            self.components[component_id] = {"stars": 0, "forks": 0, "uses": 0, "contributors": []}
        
        self.components[component_id]["stars"] += 1
        self.users[user_id]["stars_given"] += 1
        self.users[user_id]["reputation"] += 5
        self._check_badges(user_id)
        return {"status": "success", "component": component_id, "stars": self.components[component_id]["stars"]}
    
    def fork_component(self, user_id: str, component_id: str) -> Dict:
        if user_id not in self.users:
            return {"status": "error", "message": "User not found"}
        
        if component_id not in self.components:
            self.components[component_id] = {"stars": 0, "forks": 0, "uses": 0, "contributors": []}
        
        self.components[component_id]["forks"] += 1
        self.components[component_id]["contributors"].append(user_id)
        self.users[user_id]["forks_created"] += 1
        self.users[user_id]["reputation"] += 10
        self.users[user_id]["contributions"] += 1
        self._check_badges(user_id)
        return {"status": "success", "component": component_id, "forks": self.components[component_id]["forks"]}
    
    def use_component(self, user_id: str, component_id: str) -> Dict:
        if user_id not in self.users:
            return {"status": "error", "message": "User not found"}
        
        if component_id not in self.components:
            self.components[component_id] = {"stars": 0, "forks": 0, "uses": 0, "contributors": []}
        
        self.components[component_id]["uses"] += 1
        self.users[user_id]["reputation"] += 2
        return {"status": "success", "component": component_id, "uses": self.components[component_id]["uses"]}
    
    def _check_badges(self, user_id: str):
        user = self.users[user_id]
        badges = []
        if user["reputation"] >= 50: badges.append("🏅 مبتكر")
        if user["reputation"] >= 100: badges.append("🌟 نجم")
        if user["reputation"] >= 500: badges.append("👑 قائد")
        if user["contributions"] >= 10: badges.append("🤝 مساهم فعال")
        if user["forks_created"] >= 5: badges.append("🔀 مبدع")
        if user["stars_given"] >= 20: badges.append("⭐ داعم")
        user["badges"] = list(set(badges))
    
    def get_user_profile(self, user_id: str) -> Dict:
        if user_id not in self.users:
            return {"status": "error", "message": "User not found"}
        
        user = self.users[user_id]
        return {
            "status": "success",
            "user": {
                "name": user["name"],
                "reputation": user["reputation"],
                "badges": user["badges"],
                "contributions": user["contributions"],
                "stars_given": user["stars_given"],
                "forks_created": user["forks_created"],
                "joined_at": user["joined_at"],
                "rank": self._calculate_user_rank(user["reputation"])
            }
        }
    
    def _calculate_user_rank(self, reputation: int) -> str:
        if reputation >= 500: return "👑 خبير حوكمة"
        elif reputation >= 200: return "🌟 باحث متقدم"
        elif reputation >= 50: return "📚 باحث مبتدئ"
        else: return "🔍 مستكشف"
