"""
GOE OS - Interactive Wizard
معالج تفاعلي لتوجيه المستخدمين في بناء التطبيقات

جميع الحقوق محفوظة © 2024 GOE OS
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger("GOE_OS.Wizard")

class Wizard:
    """
    معالج تفاعلي - يوجه المستخدم خطوة بخطوة لبناء تطبيقه
    """
    
    def __init__(self):
        self.sessions = {}
        self.flows = self._init_flows()
        logger.info("✅ Wizard initialized")
    
    def _init_flows(self) -> Dict:
        """تهيئة تدفقات المعالج"""
        return {
            "app_creation": {
                "steps": [
                    {
                        "id": "app_type",
                        "question": "ما هو نوع التطبيق الذي تريد بناءه؟",
                        "type": "choice",
                        "options": [
                            {"id": "analysis", "label": "📊 تحليل نصوص"},
                            {"id": "generation", "label": "🚀 توليد محتوى"},
                            {"id": "foresight", "label": "🔮 استشراف"},
                            {"id": "governance", "label": "🧠 حوكمة معرفية"}
                        ]
                    },
                    {
                        "id": "domain",
                        "question": "اختر المجال:",
                        "type": "choice",
                        "options": [
                            {"id": "general", "label": "📌 عام"},
                            {"id": "law", "label": "⚖️ قانون"},
                            {"id": "medicine", "label": "🏥 طب"},
                            {"id": "agriculture", "label": "🌾 زراعة"},
                            {"id": "education", "label": "📚 تعليم"}
                        ]
                    },
                    {
                        "id": "features",
                        "question": "اختر الميزات التي تريدها (اختر 2-4):",
                        "type": "multi_choice",
                        "options": [
                            {"id": "reports", "label": "📄 تقارير"},
                            {"id": "dashboard", "label": "📊 لوحة تحكم"},
                            {"id": "integration", "label": "🔗 تكامل"},
                            {"id": "notifications", "label": "🔔 إشعارات"},
                            {"id": "multilingual", "label": "🌐 لغات متعددة"}
                        ]
                    },
                    {
                        "id": "name",
                        "question": "ما هو اسم تطبيقك؟",
                        "type": "text",
                        "placeholder": "أدخل اسم التطبيق..."
                    },
                    {
                        "id": "description",
                        "question": "اكتب وصفاً لتطبيقك:",
                        "type": "text_area",
                        "placeholder": "وصف مختصر لتطبيقك..."
                    }
                ]
            }
        }
    
    def start_session(self, user_id: str, flow_id: str = "app_creation") -> Dict:
        """بدء جلسة معالج جديدة"""
        flow = self.flows.get(flow_id)
        if not flow:
            return {"status": "error", "message": "التدفق غير موجود"}
        
        session = {
            "user_id": user_id,
            "flow_id": flow_id,
            "current_step": 0,
            "answers": {},
            "started_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.sessions[f"{user_id}_{flow_id}"] = session
        
        return self.get_next_step(user_id, flow_id)
    
    def get_next_step(self, user_id: str, flow_id: str) -> Dict:
        """الحصول على الخطوة التالية في المعالج"""
        session_key = f"{user_id}_{flow_id}"
        session = self.sessions.get(session_key)
        
        if not session:
            return {"status": "error", "message": "الجلسة غير موجودة"}
        
        flow = self.flows.get(flow_id)
        if not flow:
            return {"status": "error", "message": "التدفق غير موجود"}
        
        current_step = session["current_step"]
        steps = flow["steps"]
        
        if current_step >= len(steps):
            return self.complete_session(user_id, flow_id)
        
        step = steps[current_step]
        
        return {
            "status": "success",
            "step_index": current_step,
            "total_steps": len(steps),
            "step": step,
            "progress": round(current_step / len(steps) * 100, 1)
        }
    
    def submit_answer(self, user_id: str, flow_id: str, answer: Any) -> Dict:
        """تقديم إجابة في المعالج"""
        session_key = f"{user_id}_{flow_id}"
        session = self.sessions.get(session_key)
        
        if not session:
            return {"status": "error", "message": "الجلسة غير موجودة"}
        
        flow = self.flows.get(flow_id)
        if not flow:
            return {"status": "error", "message": "التدفق غير موجود"}
        
        current_step = session["current_step"]
        steps = flow["steps"]
        
        if current_step >= len(steps):
            return self.complete_session(user_id, flow_id)
        
        step = steps[current_step]
        session["answers"][step["id"]] = answer
        session["current_step"] += 1
        
        return self.get_next_step(user_id, flow_id)
    
    def complete_session(self, user_id: str, flow_id: str) -> Dict:
        """إكمال جلسة المعالج"""
        session_key = f"{user_id}_{flow_id}"
        session = self.sessions.get(session_key)
        
        if not session:
            return {"status": "error", "message": "الجلسة غير موجودة"}
        
        session["status"] = "completed"
        session["completed_at"] = datetime.now().isoformat()
        
        return {
            "status": "success",
            "message": "🎉 تم إكمال المعالج بنجاح",
            "answers": session["answers"],
            "next_steps": self._generate_next_steps(session["answers"])
        }
    
    def _generate_next_steps(self, answers: Dict) -> List[str]:
        """توليد الخطوات التالية بناءً على الإجابات"""
        steps = []
        
        if answers.get("app_type"):
            steps.append(f"ابدأ في بناء تطبيق {answers['app_type']}")
        
        if answers.get("domain"):
            steps.append(f"ركز على مجال {answers['domain']}")
        
        features = answers.get("features", [])
        if features:
            steps.append(f"أضف الميزات: {', '.join(features)}")
        
        return steps
    
    def get_session_status(self, user_id: str, flow_id: str) -> Dict:
        """حالة جلسة المعالج"""
        session_key = f"{user_id}_{flow_id}"
        session = self.sessions.get(session_key)
        
        if not session:
            return {"status": "not_found", "message": "الجلسة غير موجودة"}
        
        return {
            "status": session["status"],
            "current_step": session["current_step"],
            "answers": session["answers"],
            "started_at": session["started_at"]
        }
