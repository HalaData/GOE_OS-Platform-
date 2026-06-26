# إضافة داخل class SelfOrchestrator (أو في ملف منفصل)

class DistributedTaskQueue:
    """
    قائمة مهام موزعة (محاكاة لـ Celery + Redis ولكن بتكلفة صفر).
    في الإنتاج يمكن استبدالها بـ Redis حقيقي، لكن للبدء نستخدم الملفات.
    """
    def __init__(self):
        self.queue = []
        self.workers = {}
        self.results = {}

    def add_task(self, task_type: str, payload: Dict) -> str:
        task_id = hashlib.md5(f"{task_type}{datetime.utcnow().isoformat()}".encode()).hexdigest()[:8]
        self.queue.append({
            "id": task_id,
            "type": task_type,
            "payload": payload,
            "status": "pending"
        })
        return task_id

    def process_queue(self):
        """معالجة المهام (في الخلفية) دون الحاجة إلى AWS."""
        # محاكاة: في الواقع يمكن تشغيل هذا كـ Thread منفصل
        for task in self.queue:
            if task["status"] == "pending":
                # محاكاة المعالجة
                task["status"] = "completed"
                self.results[task["id"]] = {"result": f"Processed {task['type']}"}
        return self.results
