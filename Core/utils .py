"""
GOE OS - Unified Utilities
دوال مساعدة موحدة للمنصة بأكملها
"""

import hashlib
import json
import re
import time
from typing import Dict, List, Any, Optional, Union
from functools import lru_cache
from datetime import datetime

# ============================================================
# 1. التخزين المؤقت (Simple Cache)
# ============================================================

class SimpleCache:
    """تخزين مؤقت بسيط في الذاكرة مع LRU"""
    
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size
        self._access_order: List[str] = []
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            # تحديث ترتيب الوصول
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)
            return self._cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        if len(self._cache) >= self._max_size:
            # حذف الأقدم
            oldest = self._access_order.pop(0)
            del self._cache[oldest]
        self._cache[key] = value
        self._access_order.append(key)
    
    def clear(self) -> None:
        self._cache.clear()
        self._access_order.clear()
    
    def size(self) -> int:
        return len(self._cache)
    
    def keys(self) -> List[str]:
        return list(self._cache.keys())

# تخزين مؤقت عالمي
global_cache = SimpleCache(500)

# ============================================================
# 2. دوال التجزئة (Hashing)
# ============================================================

def hash_text(text: str) -> str:
    """تجزئة النص باستخدام MD5"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def hash_json(data: Union[Dict, List]) -> str:
    """تجزئة البيانات كـ JSON"""
    return hashlib.md5(json.dumps(data, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()

def hash_bytes(data: bytes) -> str:
    """تجزئة البيانات الثنائية"""
    return hashlib.md5(data).hexdigest()

def hash_file_path(file_path: str) -> str:
    """تجزئة مسار الملف"""
    return hashlib.md5(file_path.encode('utf-8')).hexdigest()

# ============================================================
# 3. تنسيق الوقت (Time Formatting)
# ============================================================

def current_timestamp() -> str:
    """الوقت الحالي بصيغة ISO"""
    return datetime.utcnow().isoformat() + "Z"

def current_date() -> str:
    """التاريخ الحالي"""
    return datetime.utcnow().strftime("%Y-%m-%d")

def format_time_seconds(seconds: float) -> str:
    """تنسيق الثواني إلى (HH:MM:SS)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def format_time_srt(seconds: float) -> str:
    """تنسيق الثواني بصيغة SRT (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

# ============================================================
# 4. معالجة النصوص (Text Processing)
# ============================================================

def clean_text(text: str) -> str:
    """تنظيف النص من المسافات الزائدة والأحرف الخاصة"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """اختصار النص الطويل"""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def extract_keywords(text: str, count: int = 5) -> List[str]:
    """استخراج الكلمات المفتاحية من النص"""
    if not text:
        return []
    words = re.findall(r'\b\w{3,}\b', text.lower())
    from collections import Counter
    return [w for w, _ in Counter(words).most_common(count)]

def is_arabic_text(text: str) -> bool:
    """التحقق مما إذا كان النص عربياً"""
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    return bool(arabic_pattern.search(text))

# ============================================================
# 5. دمج القواميس (Dictionary Operations)
# ============================================================

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """دمج قواميس (سطحية)"""
    result = dict1.copy()
    result.update(dict2)
    return result

def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """دمج عميق للقواميس المتداخلة"""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def safe_get(data: Dict, path: str, default: Any = None) -> Any:
    """الحصول على قيمة من قاموس باستخدام مسار نقطي (مثل: 'a.b.c')"""
    keys = path.split('.')
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

# ============================================================
# 6. التحقق من الصحة (Validation)
# ============================================================

def is_valid_email(email: str) -> bool:
    """التحقق من صحة البريد الإلكتروني"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_valid_url(url: str) -> bool:
    """التحقق من صحة الرابط"""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))

def is_valid_uuid(uuid_str: str) -> bool:
    """التحقق من صحة UUID"""
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(pattern, uuid_str.lower()))

# ============================================================
# 7. تنسيق الحجم (Size Formatting)
# ============================================================

def format_size(bytes_count: int) -> str:
    """تنسيق حجم الملف بوحدات مناسبة"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.1f} PB"

def format_duration(seconds: int) -> str:
    """تنسيق المدة الزمنية"""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)

# ============================================================
# 8. توليد المعرفات (ID Generation)
# ============================================================

def generate_id(prefix: str = "", length: int = 8) -> str:
    """توليد معرف فريد"""
    import random
    import string
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{prefix}{random_str}" if prefix else random_str

def generate_uuid() -> str:
    """توليد UUID"""
    import uuid
    return str(uuid.uuid4())
