"""
GOE OS - نظام المجتمع (Community Module)
يدير التفاعلات الاجتماعية، نظام السمعة، التحديات، المرشدين، والخبراء.
"""

import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

# ============================================================
# 1. نظام السمعة والتأثير (Reputation System)
# ============================================================

class ReputationSystem:
    """
    نظام السمعة والتأثير - مستوحى من GitHub Stars و Forks
    """
    
    def __init__(self):
        self.users = {}
        self.components = {}
        self.activity_log = []
    
    def add_user(self, user_id: str, name: str) -> Dict:
        """إضافة مستخدم جديد"""
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
        logger.info(f"✅ User {user_id} added to reputation system")
        return {"status": "success", "user": self.users[user_id]}
    
    def star_component(self, user_id: str, component_id: str) -> Dict:
        """إضافة نجمة لمكون"""
        if user_id not in self.users:
            return {"status": "error", "message": "User not found"}
        
        if component_id not in self.components:
            self.components[component_id] = {"stars": 0, "forks": 0, "uses": 0, "contributors": []}
        
        self.components[component_id]["stars"] += 1
        self.users[user_id]["stars_given"] += 1
        self.users[user_id]["reputation"] += 5
        self._check_badges(user_id)
        
        logger.info(f"⭐ {user_id} starred {component_id}")
        return {"status": "success", "component": component_id, "stars": self.components[component_id]["stars"]}
    
    def fork_component(self, user_id: str, component_id: str) -> Dict:
        """نسخ مكون"""
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
        
        logger.info(f"🔀 {user_id} forked {component_id}")
        return {"status": "success", "component": component_id, "forks": self.components[component_id]["forks"]}
    
    def use_component(self, user_id: str, component_id: str) -> Dict:
        """استخدام مكون في مشروع"""
        if user_id not in self.users:
            return {"status": "error", "message": "User not found"}
        
        if component_id not in self.components:
            self.components[component_id] = {"stars": 0, "forks": 0, "uses": 0, "contributors": []}
        
        self.components[component_id]["uses"] += 1
        self.users[user_id]["reputation"] += 2
        
        logger.info(f"📦 {user_id} used {component_id}")
        return {"status": "success", "component": component_id, "uses": self.components[component_id]["uses"]}
    
    def _check_badges(self, user_id: str):
        """منح شارات تلقائياً عند تحقيق إنجازات"""
        user = self.users[user_id]
        badges = []
        
        if user["reputation"] >= 50:
            badges.append("🏅 مبتكر")
        if user["reputation"] >= 100:
            badges.append("🌟 نجم")
        if user["reputation"] >= 500:
            badges.append("👑 قائد")
        if user["contributions"] >= 10:
            badges.append("🤝 مساهم فعال")
        if user["forks_created"] >= 5:
            badges.append("🔀 مبدع")
        if user["stars_given"] >= 20:
            badges.append("⭐ داعم")
        
        user["badges"] = list(set(badges))
    
    def get_user_profile(self, user_id: str) -> Dict:
        """الحصول على ملف المستخدم"""
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
        if reputation >= 500:
            return "👑 خبير حوكمة"
        elif reputation >= 200:
            return "🌟 باحث متقدم"
        elif reputation >= 50:
            return "📚 باحث مبتدئ"
        else:
            return "🔍 مستكشف"
    
    def get_component_stats(self, component_id: str) -> Dict:
        """الحصول على إحصائيات مكون"""
        if component_id not in self.components:
            return {"status": "error", "message": "Component not found"}
        
        return {"status": "success", "stats": self.components[component_id]}

# ============================================================
# 2. نظام التحديات اليومية (Challenges System)
# ============================================================

class ChallengeSystem:
    """نظام التحديات اليومية"""
    
    DAILY_CHALLENGES = {
        "analyze_text": {"name": "📝 حلل نصاً", "description": "قم بتحليل نص باستخدام محرك التشخيص", "points": 10},
        "verify_content": {"name": "✅ تحقق من صحة محتوى", "description": "تحقق من صحة محتوى في مكتبة المعرفة", "points": 15},
        "create_component": {"name": "🛠️ أنشئ مكوناً", "description": "أنشئ مكوناً جديداً للمنصة", "points": 25},
        "star_component": {"name": "⭐ أضف نجمة", "description": "أضف نجمة لمكون من مكونات الآخرين", "points": 5},
        "fork_component": {"name": "🔀 نسخ مكون", "description": "انسخ مكوناً وعدّله", "points": 20},
        "diagnose_issue": {"name": "🔍 شخّص مشكلة", "description": "شخّص مشكلة معرفية باستخدام المؤشرات التسعة", "points": 30}
    }
    
    def __init__(self):
        self.user_progress = {}
        self.streak_counter = {}
    
    def get_daily_challenges(self, user_id: str) -> Dict:
        """الحصول على التحديات اليومية للمستخدم"""
        today = datetime.utcnow().date()
        
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
            self.streak_counter[user_id] = 0
        
        if today not in self.user_progress[user_id]:
            self.user_progress[user_id][today] = self._generate_challenges(user_id)
        
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
    
    def _generate_challenges(self, user_id: str) -> List[Dict]:
        """توليد تحديات عشوائية لليوم مع مراعاة مستوى المستخدم"""
        import random
        challenges = list(self.DAILY_CHALLENGES.values())
        selected = random.sample(challenges, min(4, len(challenges)))
        for c in selected:
            c["completed"] = False
            c["completed_at"] = None
        return selected
    
    def complete_challenge(self, user_id: str, challenge_name: str) -> Dict:
        """تسجيل إكمال تحدي"""
        today = datetime.utcnow().date()
        
        if user_id not in self.user_progress or today not in self.user_progress[user_id]:
            return {"status": "error", "message": "No challenges found for today"}
        
        for challenge in self.user_progress[user_id][today]:
            if challenge["name"] == challenge_name and not challenge.get("completed", False):
                challenge["completed"] = True
                challenge["completed_at"] = datetime.utcnow().isoformat()
                self._update_streak(user_id)
                
                logger.info(f"🎯 {user_id} completed challenge: {challenge_name}")
                return {
                    "status": "success",
                    "points_earned": challenge["points"],
                    "challenge": challenge_name
                }
        
        return {"status": "error", "message": "Challenge not found or already completed"}
    
    def _update_streak(self, user_id: str):
        """تحديث سلسلة الإنجازات اليومية"""
        if user_id not in self.streak_counter:
            self.streak_counter[user_id] = 0
        self.streak_counter[user_id] += 1

# ============================================================
# 3. نظام المرشدين (Mentors System)
# ============================================================

class GovernanceMentorSystem:
    """نظام مرشد الحوكمة"""
    
    def __init__(self):
        self.mentors = {}
        self.mentorships = {}
        self.mentor_ratings = {}
    
    def apply_for_mentorship(self, user_id: str, reputation: int, contributions: int) -> Dict:
        """تقديم طلب ليصبح المستخدم مرشداً"""
        if reputation < 200:
            return {"status": "error", "message": "تحتاج إلى 200 نقطة سمعة على الأقل"}
        if contributions < 10:
            return {"status": "error", "message": "تحتاج إلى 10 مساهمات على الأقل"}
        
        if user_id in self.mentors:
            return {"status": "error", "message": "Already a mentor"}
        
        self.mentors[user_id] = {
            "mentees": [],
            "total_mentees": 0,
            "success_rate": 0,
            "joined_at": datetime.utcnow().isoformat(),
            "status": "active",
            "rating": 0,
            "total_ratings": 0
        }
        
        logger.info(f"✅ {user_id} became a mentor")
        return {"status": "success", "message": "تم قبولك كمرشد للحوكمة"}
    
    def request_mentorship(self, mentee_id: str, mentor_id: str) -> Dict:
        """طلب التوجيه من مرشد معين"""
        if mentor_id not in self.mentors:
            return {"status": "error", "message": "Mentor not found"}
        
        mentorship_id = f"mentorship_{mentor_id}_{mentee_id}_{int(datetime.utcnow().timestamp())}"
        self.mentorships[mentorship_id] = {
            "mentor": mentor_id,
            "mentee": mentee_id,
            "status": "pending",
            "requested_at": datetime.utcnow().isoformat(),
            "accepted_at": None,
            "completed_at": None,
            "sessions": 0
        }
        
        self.mentors[mentor_id]["mentees"].append(mentee_id)
        self.mentors[mentor_id]["total_mentees"] += 1
        
        logger.info(f"📩 {mentee_id} requested mentorship from {mentor_id}")
        return {"status": "pending", "mentorship_id": mentorship_id}
    
    def accept_mentorship(self, mentorship_id: str, mentor_id: str) -> Dict:
        """قبول طلب التوجيه"""
        if mentorship_id not in self.mentorships:
            return {"status": "error", "message": "Mentorship request not found"}
        
        mentorship = self.mentorships[mentorship_id]
        if mentorship["mentor"] != mentor_id:
            return {"status": "error", "message": "Unauthorized"}
        
        mentorship["status"] = "active"
        mentorship["accepted_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"✅ {mentor_id} accepted mentorship of {mentorship['mentee']}")
        return {"status": "active", "mentorship": mentorship}
    
    def complete_mentorship_session(self, mentorship_id: str, mentee_feedback: str, rating: int = 5) -> Dict:
        """إكمال جلسة توجيه مع تقييم"""
        if mentorship_id not in self.mentorships:
            return {"status": "error", "message": "Mentorship not found"}
        
        mentorship = self.mentorships[mentorship_id]
        mentorship["sessions"] += 1
        mentorship["last_session"] = datetime.utcnow().isoformat()
        mentorship["feedback"] = mentee_feedback
        
        # تحديث تقييم المرشد
        mentor_id = mentorship["mentor"]
        if mentor_id not in self.mentor_ratings:
            self.mentor_ratings[mentor_id] = {"total": 0, "count": 0}
        self.mentor_ratings[mentor_id]["total"] += rating
        self.mentor_ratings[mentor_id]["count"] += 1
        self.mentors[mentor_id]["rating"] = round(self.mentor_ratings[mentor_id]["total"] / self.mentor_ratings[mentor_id]["count"], 1)
        self.mentors[mentor_id]["total_ratings"] = self.mentor_ratings[mentor_id]["count"]
        
        logger.info(f"✅ Completed mentorship session: {mentorship_id}")
        return {
            "status": "success",
            "sessions": mentorship["sessions"],
            "rating": self.mentors[mentor_id]["rating"]
        }
    
    def get_mentor_leaderboard(self) -> List[Dict]:
        """لوحة متصدرين المرشدين حسب التقييم وعدد المستفيدين"""
        sorted_mentors = sorted(
            self.mentors.items(),
            key=lambda x: (x[1]["rating"], x[1]["total_mentees"]),
            reverse=True
        )
        return [
            {
                "user_id": user_id,
                "mentees": data["total_mentees"],
                "success_rate": data.get("success_rate", 0),
                "rating": data.get("rating", 0),
                "rank": i + 1
            }
            for i, (user_id, data) in enumerate(sorted_mentors[:10])
        ]

# ============================================================
# 4. نظام خبراء المجتمع (Domain Expert System)
# ============================================================

class DomainExpertSystem:
    """
    نظام إدارة خبراء المجالات - بديل عن التعاقد مع مستشارين مدفوعين.
    """
    
    def __init__(self):
        self.experts = {}  # user_id -> expert_data
        self.proposals = []  # اقتراحات معرفية جديدة
        self.votes = {}  # proposal_id -> votes
        self.accepted_knowledge = []  # المعرفة المقبولة
        self.expert_requests = []  # طلبات الخبرة المعلقة
    
    def register_expert(self, user_id: str, domain: str, credentials: Dict) -> str:
        """تسجيل خبير في مجال معين."""
        if user_id in self.experts:
            return "❌ Already registered"
        
        self.experts[user_id] = {
            "domain": domain,
            "credentials": credentials,
            "joined_at": datetime.utcnow().isoformat(),
            "proposals_count": 0,
            "approval_rate": 0.0,
            "status": "pending"  # pending, active, suspended
        }
        
        # إضافة طلب خبرة للتصويت المجتمعي
        self.expert_requests.append({
            "user_id": user_id,
            "domain": domain,
            "credentials": credentials,
            "created_at": datetime.utcnow().isoformat(),
            "votes": {"approve": 0, "reject": 0}
        })
        
        logger.info(f"🧑‍🔬 Expert registration request: {user_id} for {domain}")
        return f"✅ Expert registration submitted for approval"
    
    def vote_expert(self, user_id: str, voter_id: str, approve: bool) -> str:
        """التصويت على طلب خبرة."""
        for req in self.expert_requests:
            if req["user_id"] == user_id:
                if voter_id in req.get("voters", []):
                    return "❌ Already voted"
                
                if "voters" not in req:
                    req["voters"] = []
                req["voters"].append(voter_id)
                
                if approve:
                    req["votes"]["approve"] += 1
                else:
                    req["votes"]["reject"] += 1
                
                # إذا تجاوز عدد الموافقات 5، يتم قبول الخبير
                if req["votes"]["approve"] > 5:
                    self.experts[user_id]["status"] = "active"
                    req["status"] = "approved"
                    logger.info(f"✅ Expert {user_id} approved by community")
                    return "✅ Expert approved!"
                
                return "🗳️ Vote recorded"
        
        return "❌ Expert request not found"
    
    def propose_knowledge(self, expert_id: str, domain: str, knowledge: Dict) -> str:
        """اقتراح معرفة جديدة من خبير."""
        if expert_id not in self.experts:
            return "❌ Expert not found"
        if self.experts[expert_id]["status"] != "active":
            return "❌ Expert not active"
        
        proposal_id = hashlib.md5(f"{expert_id}{domain}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:8]
        self.proposals.append({
            "id": proposal_id,
            "expert": expert_id,
            "domain": domain,
            "knowledge": knowledge,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        })
        self.experts[expert_id]["proposals_count"] += 1
        
        logger.info(f"📝 Knowledge proposal from {expert_id}: {knowledge.get('title', 'Untitled')}")
        return proposal_id
    
    def vote_knowledge(self, proposal_id: str, voter_id: str, approve: bool) -> str:
        """التصويت على اقتراح معرفي."""
        proposal = None
        for p in self.proposals:
            if p["id"] == proposal_id:
                proposal = p
                break
        if not proposal:
            return "❌ Proposal not found"
        if proposal["expert"] == voter_id:
            return "❌ Cannot vote on your own proposal"
        
        if proposal_id not in self.votes:
            self.votes[proposal_id] = {"approve": 0, "reject": 0, "voters": set()}
        
        if voter_id in self.votes[proposal_id]["voters"]:
            return "❌ Already voted"
        
        self.votes[proposal_id]["voters"].add(voter_id)
        if approve:
            self.votes[proposal_id]["approve"] += 1
        else:
            self.votes[proposal_id]["reject"] += 1
        
        # إذا تجاوز عدد الموافقات 5، يُقبل الاقتراح
        if self.votes[proposal_id]["approve"] > 5:
            proposal["status"] = "approved"
            self.accepted_knowledge.append({
                "proposal_id": proposal_id,
                "domain": proposal["domain"],
                "knowledge": proposal["knowledge"],
                "approved_at": datetime.utcnow().isoformat()
            })
            # تحديث معدل قبول الخبير
            expert_id = proposal["expert"]
            total = self.experts[expert_id]["proposals_count"]
            approved = sum(1 for p in self.proposals if p["expert"] == expert_id and p["status"] == "approved")
            self.experts[expert_id]["approval_rate"] = approved / total if total > 0 else 0
            return "✅ Knowledge proposal approved!"
        
        return "🗳️ Vote recorded"
    
    def get_pending_proposals(self) -> List[Dict]:
        """الحصول على جميع الاقتراحات المعلقة."""
        return [p for p in self.proposals if p["status"] == "pending"]
    
    def get_accepted_knowledge(self) -> List[Dict]:
        """الحصول على المعرفة المقبولة."""
        return self.accepted_knowledge
    
    def get_experts(self) -> Dict:
        """الحصول على قائمة الخبراء المسجلين."""
        return self.experts

# ============================================================
# 5. نقاط النهاية API (FastAPI)
# ============================================================

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v2/community", tags=["Community"])

_reputation = None
_challenges = None
_mentors = None
_experts = None

def get_reputation():
    global _reputation
    if _reputation is None:
        _reputation = ReputationSystem()
    return _reputation

def get_challenges():
    global _challenges
    if _challenges is None:
        _challenges = ChallengeSystem()
    return _challenges

def get_mentors():
    global _mentors
    if _mentors is None:
        _mentors = GovernanceMentorSystem()
    return _mentors

def get_experts():
    global _experts
    if _experts is None:
        _experts = DomainExpertSystem()
    return _experts

# ============================================================
# سمعة (Reputation)
# ============================================================

@router.post("/reputation/user")
async def create_user(user_id: str, name: str):
    rep = get_reputation()
    return rep.add_user(user_id, name)

@router.post("/reputation/star")
async def star_component(user_id: str, component_id: str):
    rep = get_reputation()
    return rep.star_component(user_id, component_id)

@router.post("/reputation/fork")
async def fork_component(user_id: str, component_id: str):
    rep = get_reputation()
    return rep.fork_component(user_id, component_id)

@router.get("/reputation/profile/{user_id}")
async def get_user_profile(user_id: str):
    rep = get_reputation()
    return rep.get_user_profile(user_id)

@router.get("/reputation/component/{component_id}")
async def get_component_stats(component_id: str):
    rep = get_reputation()
    return rep.get_component_stats(component_id)

# ============================================================
# تحديات (Challenges)
# ============================================================

@router.get("/challenges/{user_id}")
async def get_challenges(user_id: str):
    chal = get_challenges()
    return chal.get_daily_challenges(user_id)

@router.post("/challenges/complete")
async def complete_challenge(user_id: str, challenge_name: str):
    chal = get_challenges()
    return chal.complete_challenge(user_id, challenge_name)

# ============================================================
# مرشدين (Mentors)
# ============================================================

@router.post("/mentors/apply")
async def apply_mentor(user_id: str, reputation: int, contributions: int):
    mentor = get_mentors()
    return mentor.apply_for_mentorship(user_id, reputation, contributions)

@router.post("/mentors/request")
async def request_mentorship(mentee_id: str, mentor_id: str):
    mentor = get_mentors()
    return mentor.request_mentorship(mentee_id, mentor_id)

@router.post("/mentors/accept")
async def accept_mentorship(mentorship_id: str, mentor_id: str):
    mentor = get_mentors()
    return mentor.accept_mentorship(mentorship_id, mentor_id)

@router.post("/mentors/complete-session")
async def complete_mentorship_session(mentorship_id: str, mentee_feedback: str, rating: int = 5):
    mentor = get_mentors()
    return mentor.complete_mentorship_session(mentorship_id, mentee_feedback, rating)

@router.get("/mentors/leaderboard")
async def mentor_leaderboard():
    mentor = get_mentors()
    return {"leaderboard": mentor.get_mentor_leaderboard()}

# ============================================================
# خبراء (Experts)
# ============================================================

@router.post("/experts/register")
async def register_expert(user_id: str, domain: str, credentials: Dict):
    expert = get_experts()
    return {"message": expert.register_expert(user_id, domain, credentials)}

@router.post("/experts/vote")
async def vote_expert(user_id: str, voter_id: str, approve: bool):
    expert = get_experts()
    return {"message": expert.vote_expert(user_id, voter_id, approve)}

@router.post("/experts/propose")
async def propose_knowledge(expert_id: str, domain: str, knowledge: Dict):
    expert = get_experts()
    proposal_id = expert.propose_knowledge(expert_id, domain, knowledge)
    return {"proposal_id": proposal_id}

@router.post("/experts/vote-knowledge")
async def vote_knowledge(proposal_id: str, voter_id: str, approve: bool):
    expert = get_experts()
    return {"message": expert.vote_knowledge(proposal_id, voter_id, approve)}

@router.get("/experts/pending")
async def get_pending_proposals():
    expert = get_experts()
    return {"proposals": expert.get_pending_proposals()}

@router.get("/experts/accepted")
async def get_accepted_knowledge():
    expert = get_experts()
    return {"knowledge": expert.get_accepted_knowledge()}

@router.get("/experts/list")
async def list_experts():
    expert = get_experts()
    return {"experts": expert.get_experts()}

# ============================================================
# إنشاء النسخة العالمية (للاستخدام الداخلي)
# ============================================================

reputation = get_reputation()
challenges = get_challenges()
mentors = get_mentors()
experts = get_experts()
