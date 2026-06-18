"""
GOE OS - Accessibility Engine
الإتاحة الشاملة: للصم، البكم، الكفيفين
"""

import logging
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger("GOE_OS.Accessibility")

class AccessibilityEngine:
    """
    محرك الإتاحة - دعم الصم، البكم، الكفيفين
    """
    
    def __init__(self):
        self.user_modes = {}
        self.accessibility_history = []
        logger.info("✅ Accessibility Engine initialized")
    
    def set_mode(self, data: Dict) -> Dict:
        """ضبط وضع الإتاحة"""
        user_id = data.get("user_id", "")
        mode = data.get("mode", "none")
        
        if mode not in ["deaf", "mute", "blind", "none"]:
            return {"status": "error", "message": "وضع غير معروف"}
        
        self.user_modes[user_id] = {
            "mode": mode,
            "set_at": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "user_id": user_id,
            "mode": mode,
            "features": self._get_features(mode)
        }
    
    def _get_features(self, mode: str) -> List[str]:
        """ميزات وضع الإتاحة"""
        features = {
            "deaf": ["ترجمة لغة إشارة", "نصوص مساعدة", "إشعارات بصرية"],
            "mute": ["تحويل النص لكلام", "لوحة تواصل", "جمل سريعة"],
            "blind": ["قراءة الشاشة", "أوامر صوتية", "وصف الصور"],
            "none": []
        }
        return features.get(mode, [])
    
    def get_modes(self) -> Dict:
        """جميع أوضاع الإتاحة"""
        return {
            "deaf": {"name": "وضع الصم", "icon": "🦻", "features": self._get_features("deaf")},
            "mute": {"name": "وضع البكم", "icon": "💬", "features": self._get_features("mute")},
            "blind": {"name": "وضع الكفيفين", "icon": "👁️", "features": self._get_features("blind")}
        }
    
    def get_user_mode(self, user_id: str) -> Dict:
        """وضع المستخدم الحالي"""
        if user_id in self.user_modes:
            return self.user_modes[user_id]
        return {"mode": "none"}
    
    def process_content(self, data: Dict) -> Dict:
        """معالجة المحتوى حسب وضع الإتاحة"""
        user_id = data.get("user_id", "")
        content = data.get("content", "")
        
        mode = self.get_user_mode(user_id).get("mode", "none")
        
        processed = {
            "original": content,
            "mode": mode,
            "processed": self._apply_mode(content, mode)
        }
        
        self.accessibility_history.append(processed)
        return processed
    
    def _apply_mode(self, content: str, mode: str) -> Dict:
        """تطبيق وضع الإتاحة على المحتوى"""
        if mode == "deaf":
            return {
                "captions": content,
                "sign_language": f"ترجمة لغة إشارة لـ: {content[:30]}...",
                "visual_alerts": "إشعار بصري"
            }
        elif mode == "mute":
            return {
                "tts": f"تحويل إلى كلام: {content[:30]}...",
                "quick_phrases": ["مرحباً", "شكراً", "أحتاج مساعدة"]
            }
        elif mode == "blind":
            return {
                "screen_reader": f"قراءة: {content[:50]}...",
                "voice_commands": ["التالي", "السابق", "قراءة"]
            }
        else:
            return {"text": content}
