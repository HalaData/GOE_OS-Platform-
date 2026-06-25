"""
نظام التحديات اليومية
"""

from typing import Dict, List
from datetime import datetime, timedelta
import random

class ChallengeSystem:
    DAILY_CHALLENGES = {
        "analyze_text": {"name": "📝 حلل نصاً", "description": "قم بتحليل نص باستخدام محرك التشخيص", "points": 10},
        "verify_content": {"name": "✅ تحقق من صحة محتوى", "description": "تحقق من صحة محتوى", "points": 15},
        "create_component": {"name": "🛠️ أنشئ مكوناً", "description": "أنشئ مكوناً جديداً", "points": 25},
        "star_component": {"name": "⭐ أضف نجمة", "description": "أضف نجمة لمكون", "points": 5},
        "fork_component": {"name": "🔀 نسخ مكون", "description": "انسخ مكوناً", "points": 20},
        "diagnose_issue": {"name": "🔍 شخّص مشكلة", "description": "شخّص مشكلة معرفية", "points": 30}
    }
    
    def __init__(self):
        self.user_progress = {}
        self.streak_counter = {}
    
    def get_daily_challenges(self, user_id: str) -> Dict:
        today = datetime.utcnow().date()
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
            self.streak_counter[user_id] = 0
        
        if today not in self.user_progress[user_id]:
            self.user_progress[user_id][today] = self._generate_challenges()
        
        completed = sum(1 for c in self.user_progress[user_id][today] if c.get("completed", False))
        total = len(self.user_progress[user_id][today])
        
        return {
            "status": "success",
            "date": today.isoformat(),
            "challenges": self.user_progress[user_id][today],
            "completed": completed,
            "total": total,
            "progress": round((completed / total) * 100, 1) if total > 0 else 0,
            "streak": self.streak_counter.get(user_id, 0)
        }
    
    def _generate_challenges(self) -> List[Dict]:
        challenges = list(self.DAILY_CHALLENGES.values())
        selected = random.sample(challenges, min(4, len(challenges)))
        for c in selected:
            c["completed"] = False
            c["completed_at"] = None
        return selected
    
    def complete_challenge(self, user_id: str, challenge_name: str) -> Dict:
        today = datetime.utcnow().date()
        if user_id not in self.user_progress or today not in self.user_progress[user_id]:
            return {"status": "error", "message": "No challenges found"}
        
        for challenge in self.user_progress[user_id][today]:
            if challenge["name"] == challenge_name and not challenge.get("completed", False):
                challenge["completed"] = True
                challenge["completed_at"] = datetime.utcnow().isoformat()
                self._update_streak(user_id)
                return {
                    "status": "success",
                    "points_earned": challenge["points"],
                    "challenge": challenge_name
                }
        
        return {"status": "error", "message": "Challenge not found or already completed"}
    
    def _update_streak(self, user_id: str):
        self.streak_counter[user_id] = self.streak_counter.get(user_id, 0) + 1
