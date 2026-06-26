# ============================================================
# نظام توزيع المهام (بديل مكلف عن AWS/GCP)
# ============================================================

class DistributedTaskQueue:
    """
    قائمة مهام موزعة (محاكاة لـ Celery + Redis ولكن بتكلفة صفر).
    في الإنتاج يمكن استبدالها بـ Redis حقيقي، لكن للبدء نستخدم الملفات.
    """
    def __init__(self, storage_file: str = "task_queue.json"):
        self.storage_file = storage_file
        self.queue = []
        self.workers = {}
        self.results = {}
        self._load_state()

    def _load_state(self):
        """تحميل الحالة من ملف (لتجنب فقدان المهام)."""
        import os
        if os.path.exists(self.storage_file):
            try:
                import json
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.queue = data.get('queue', [])
                    self.results = data.get('results', {})
            except:
                pass

    def _save_state(self):
        """حفظ الحالة إلى ملف."""
        import json
        with open(self.storage_file, 'w') as f:
            json.dump({'queue': self.queue, 'results': self.results}, f)

    def add_task(self, task_type: str, payload: Dict) -> str:
        """إضافة مهمة جديدة إلى قائمة الانتظار."""
        task_id = hashlib.md5(f"{task_type}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:8]
        self.queue.append({
            "id": task_id,
            "type": task_type,
            "payload": payload,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        })
        self._save_state()
        return task_id

    def get_next_task(self) -> Optional[Dict]:
        """استرجاع المهمة التالية (للعاملين)."""
        for task in self.queue:
            if task["status"] == "pending":
                task["status"] = "processing"
                self._save_state()
                return task
        return None

    def complete_task(self, task_id: str, result: Any):
        """تسجيل نتيجة مهمة مكتملة."""
        for task in self.queue:
            if task["id"] == task_id:
                task["status"] = "completed"
                self.results[task_id] = {
                    "result": result,
                    "completed_at": datetime.utcnow().isoformat()
                }
                self._save_state()
                return True
        return False

    def get_result(self, task_id: str) -> Optional[Dict]:
        """استرجاع نتيجة مهمة."""
        return self.results.get(task_id)

    def get_status(self) -> Dict:
        """حالة قائمة الانتظار."""
        return {
            "total": len(self.queue),
            "pending": sum(1 for t in self.queue if t["status"] == "pending"),
            "processing": sum(1 for t in self.queue if t["status"] == "processing"),
            "completed": sum(1 for t in self.queue if t["status"] == "completed"),
            "failed": sum(1 for t in self.queue if t["status"] == "failed")
        }

# إضافة نقطة نهاية API لإدارة المهام (يمكن وضعها في main.py)
# لكننا سنكتفي بتوفير الكود هنا.
