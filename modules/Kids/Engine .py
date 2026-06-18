"""
GOE OS - Kids Engine
منصة الأطفال: ألعاب تعليمية، قصص تفاعلية، شخصيات مرافقة
"""

import logging
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

logger = logging.getLogger("GOE_OS.Kids")

class KidsEngine:
    """
    محرك الأطفال - ألعاب تعليمية، قصص، شخصيات
    """
    
    FRIENDS = [
        {"name": "جوي", "emoji": "🦊", "color": "#FF6B35", "personality": "مرح ومغامر"},
        {"name": "إيلي", "emoji": "🐘", "color": "#6C5CE7", "personality": "حكيم وصبور"},
        {"name": "زوزو", "emoji": "🐝", "color": "#FDCB6E", "personality": "نشيط ومجتهد"},
        {"name": "ليلو", "emoji": "🦁", "color": "#E17055", "personality": "شجاع وقائد"},
        {"name": "نورا", "emoji": "🦋", "color": "#00CEC9", "personality": "لطيفة ومبدعة"}
    ]
    
    GAMES = [
        {"id": "word_hunt", "name": "🔍 صيد الكلمات", "age": "6-10", "type": "reading"},
        {"id": "story_builder", "name": "📖 باني القصص", "age": "7-12", "type": "creative"},
        {"id": "color_analyzer", "name": "🎨 محلل الألوان", "age": "4-8", "type": "art"},
        {"id": "music_maker", "name": "🎵 صانع الموسيقى", "age": "5-10", "type": "music"}
    ]
    
    STORIES = [
        {"id": "story_1", "title": "مغامرة جوي في الغابة", "age": "4-8"},
        {"id": "story_2", "title": "رحلة إيلي إلى النجوم", "age": "5-10"}
    ]
    
    def __init__(self):
        self.game_sessions = {}
        self.story_sessions = {}
        self.rewards = {}
        logger.info("✅ Kids Engine initialized")
    
    def start_game(self, data: Dict) -> Dict:
        """بدء لعبة تعليمية للأطفال"""
        user_id = data.get("user_id", "")
        game_id = data.get("game_id", "")
        age = data.get("age", 7)
        
        if not game_id:
            games = self._get_available_games(age)
            if games:
                game_id = games[0]["id"]
            else:
                return {"status": "error", "message": "لا توجد ألعاب مناسبة"}
        
        session_id = hashlib.md5(f"{user_id}{game_id}{datetime.now()}".encode()).hexdigest()[:8]
        
        session = {
            "id": session_id,
            "user_id": user_id,
            "game_id": game_id,
            "score": 0,
            "stars": 0,
            "started_at": datetime.now().isoformat()
        }
        
        self.game_sessions[session_id] = session
        
        game = self._get_game(game_id)
        
        return {
            "status": "success",
            "session": session,
            "game": game,
            "friend": self.get_friend()
        }
    
    def _get_available_games(self, age: int) -> List[Dict]:
        """الألعاب المناسبة للعمر"""
        available = []
        for game in self.GAMES:
            age_range = game["age"].split("-")
            if int(age_range[0]) <= age <= int(age_range[1]):
                available.append(game)
        return available
    
    def _get_game(self, game_id: str) -> Optional[Dict]:
        """الحصول على لعبة بالمعرف"""
        for game in self.GAMES:
            if game["id"] == game_id:
                return game
        return None
    
    def start_story(self, data: Dict) -> Dict:
        """بدء قصة تفاعلية للأطفال"""
        user_id = data.get("user_id", "")
        story_id = data.get("story_id", "")
        
        if not story_id:
            return {"status": "error", "message": "معرف القصة مطلوب"}
        
        story = self._get_story(story_id)
        if not story:
            return {"status": "error", "message": "القصة غير موجودة"}
        
        session_key = f"{user_id}_{story_id}"
        self.story_sessions[session_key] = {
            "user_id": user_id,
            "story_id": story_id,
            "current_page": 0,
            "started_at": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "story": story,
            "page": story["pages"][0] if story.get("pages") else {"text": "بداية القصة"}
        }
    
    def _get_story(self, story_id: str) -> Optional[Dict]:
        """الحصول على قصة بالمعرف"""
        for story in self.STORIES:
            if story["id"] == story_id:
                # إضافة صفحات افتراضية
                story["pages"] = [
                    {"page": 1, "text": f"كان {story['title']} يوماً جميلاً..."},
                    {"page": 2, "text": "وفجأة حدث شيء مميز..."}
                ]
                return story
        return None
    
    def get_friend(self) -> Dict:
        """شخصية مرافقة عشوائية"""
        return random.choice(self.FRIENDS)
    
    def complete_game(self, session_id: str, score: int) -> Dict:
        """إكمال لعبة"""
        session = self.game_sessions.get(session_id)
        if not session:
            return {"status": "error", "message": "الجلسة غير موجودة"}
        
        session["score"] = score
        session["completed_at"] = datetime.now().isoformat()
        
        stars = 3 if score >= 90 else 2 if score >= 70 else 1 if score >= 50 else 0
        session["stars"] = stars
        
        reward = self._calculate_reward(session["user_id"], stars)
        
        return {
            "status": "success",
            "session": session,
            "stars_earned": stars,
            "reward": reward,
            "message": self._get_encouragement(stars)
        }
    
    def _calculate_reward(self, user_id: str, stars: int) -> Dict:
        """حساب المكافأة"""
        if user_id not in self.rewards:
            self.rewards[user_id] = {"stars": 0, "level": 1}
        
        self.rewards[user_id]["stars"] += stars
        
        # تحديث المستوى
        total_stars = self.rewards[user_id]["stars"]
        level = min(5, total_stars // 10 + 1)
        self.rewards[user_id]["level"] = level
        
        return {
            "stars": stars,
            "total_stars": total_stars,
            "level": level,
            "next_level_stars": level * 10
        }
    
    def _get_encouragement(self, stars: int) -> str:
        """رسالة تشجيعية"""
        messages = {
            3: "🌟 ممتاز! أنت رائع جداً!",
            2: "⭐ جيد جداً! استمر في التحسن!",
            1: "👍 عمل جيد! حاول مرة أخرى!",
            0: "💪 لا تستسلم! المحاولة القادمة أفضل!"
        }
        return messages.get(stars, "🌟 أحسنت!")
