"""
GOE OS - Pytest Configuration
"""

import pytest
import sys
import os
from pathlib import Path

# إضافة مسار المشروع إلى sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def sample_text():
    """نص عينة للاختبار"""
    return "هذا هو النص الذي سيتم تحليله بواسطة GOE OS. يحتوي على كلمات مفتاحية مثل invited و consulted و promised."

@pytest.fixture
def sample_code():
    """كود عينة للاختبار"""
    return """
def process_input(user_input):
    result = eval(user_input)
    return result

def secure_function(data):
    return data
"""

@pytest.fixture
def sample_vulnerability():
    """ثغرة عينة للاختبار"""
    return {
        "type": "code_injection",
        "description": "استخدام eval() خطر",
        "severity": "critical",
        "location": "eval() في السطر 2"
    }

@pytest.fixture
def sample_governance_request():
    """طلب حوكمة عينة"""
    return {
        "text": "هذه السياسة تم إعدادها دون تشاور مع المجتمعات المحلية.",
        "domain": "law",
        "consent_given": True
    }
