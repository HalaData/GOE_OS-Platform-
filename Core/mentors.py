"""
نظام مرشد الحوكمة
"""

from typing import Dict, List
from datetime import datetime

class GovernanceMentorSystem:
    def __init__(self):
        self.mentors = {}
        self.mentorships = {}
        self.mentor_ratings = {}
    
    def apply_for_mentorship(self, user_id: str, reputation: int, contributions: int) -> Dict:
        if reputation < 200:
            return {"status": "error", "message": "تحتاج إلى 200 نقطة سمعة"}
        if contributions < 10:
            return {"status": "error", "message": "تحتاج إلى 10 مساهمات"}
        
        if user_id in self.mentors:
            return {"status": "error", "message": "Already a mentor"}
        
        self.mentors[user_id] = {
            "mentees": [],
            "total_mentees": 0,
            "success_rate": 0,
            "joined_at": datetime.utcnow().isoformat(),
            "status": "active",
            "rating": 0
        }
        return {"status": "success", "message": "تم قبولك كمرشد"}
    
    def request_mentorship(self, mentee_id: str, mentor_id: str) -> Dict:
        if mentor_id not in self.mentors:
            return {"status": "error", "message": "Mentor not found"}
        
        mentorship_id = f"mentorship_{mentor_id}_{mentee_id}_{int(datetime.utcnow().timestamp())}"
        self.mentorships[mentorship_id] = {
            "mentor": mentor_id,
            "mentee": mentee_id,
            "status": "pending",
            "requested_at": datetime.utcnow().isoformat()
        }
        self.mentors[mentor_id]["mentees"].append(mentee_id)
        self.mentors[mentor_id]["total_mentees"] += 1
        return {"status": "pending", "mentorship_id": mentorship_id}
    
    def get_mentor_leaderboard(self) -> List[Dict]:
        sorted_mentors = sorted(
            self.mentors.items(),
            key=lambda x: (x[1].get("rating", 0), x[1]["total_mentees"]),
            reverse=True
        )
        return [
            {
                "user_id": user_id,
                "mentees": data["total_mentees"],
                "rating": data.get("rating", 0),
                "rank": i + 1
            }
            for i, (user_id, data) in enumerate(sorted_mentors[:10])
        ]
