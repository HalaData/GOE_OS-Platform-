# تشغيل جميع الاختبارات
pytest tests/

# تشغيل اختبارات محددة
pytest tests/test_core.py

# تشغيل مع تقرير التغطية
pytest --cov=core --cov=modules tests/

# تشغيل اختبارات سريعة فقط
pytest -m "not slow"
