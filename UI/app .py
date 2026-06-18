"""
GOE OS - Streamlit Dashboard
واجهة المستخدم الرئيسية للمنصة
"""

import streamlit as st
import requests
import json

# ============================================================
# إعدادات الصفحة
# ============================================================

st.set_page_config(
    page_title="GOE OS Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# API URL
# ============================================================

API_URL = "http://localhost:8000/api/v2"

# ============================================================
# الشريط الجانبي
# ============================================================

with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=GOE+OS", use_column_width=True)
    st.markdown("---")
    st.markdown("### 🧠 GOE OS")
    st.markdown("منصة الحوكمة المعرفية")
    st.markdown("---")
    
    st.markdown("### 📊 الحالة")
    try:
        response = requests.get(f"{API_URL}/status", timeout=2)
        if response.status_code == 200:
            st.success("✅ النظام يعمل")
        else:
            st.warning("⚠️ النظام غير مستجيب")
    except:
        st.error("❌ لا يمكن الاتصال بالخادم")
    
    st.markdown("---")
    st.markdown("### 🔗 الروابط")
    st.markdown("[📚 التوثيق](/docs)")
    st.markdown("[🔍 Swagger](/docs)")

# ============================================================
# الصفحة الرئيسية
# ============================================================

st.title("🧠 GOE OS")
st.markdown("**منصة الحوكمة السيبرنطيقية المعرفية**")
st.markdown("---")

# ============================================================
# التبويبات
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 تشخيص", 
    "📊 مؤشرات", 
    "🚀 توليد", 
    "🔮 استشراف", 
    "⚙️ إعدادات"
])

# ============================================================
# التبويب 1: التشخيص
# ============================================================

with tab1:
    st.subheader("📝 التشخيص المعرفي")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        text = st.text_area(
            "أدخل النص للتحليل:",
            height=200,
            placeholder="الصق النص هنا..."
        )
    
    with col2:
        domain = st.selectbox(
            "المجال",
            ["general", "law", "medicine", "agriculture", "education", "sports", "music"]
        )
        depth = st.selectbox(
            "العمق",
            ["rapid", "standard", "deep"]
        )
        consent = st.checkbox("أوافق على التشخيص")
    
    if st.button("🔍 تشخيص", type="primary", use_container_width=True):
        if not text:
            st.warning("⚠️ الرجاء إدخال النص")
        elif not consent:
            st.warning("⚠️ يجب الموافقة على التشخيص")
        else:
            with st.spinner("جاري التشخيص..."):
                try:
                    response = requests.post(
                        f"{API_URL}/govern",
                        json={
                            "text": text,
                            "domain": domain,
                            "depth": depth,
                            "consent_given": True
                        },
                        timeout=30
                    )
                    data = response.json()
                    
                    if response.status_code == 200:
                        st.success(f"✅ درجة اليقظة: {data.get('vigilance_score', 0)}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("درجة اليقظة", f"{data.get('vigilance_score', 0)}%")
                            st.metric("عدد المؤشرات", len(data.get('indicators', {})))
                        
                        with col2:
                            st.metric("الأسئلة المحرمة", len(data.get('forbidden_questions', [])))
                            st.metric("المسلمات", len(data.get('dogmas', [])))
                        
                        with st.expander("📋 التشخيص الكامل", expanded=True):
                            st.json(data)
                    else:
                        st.error(f"❌ خطأ: {data.get('message', 'غير معروف')}")
                except requests.exceptions.Timeout:
                    st.error("⏰ انتهى الوقت. حاول مرة أخرى")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

# ============================================================
# التبويب 2: المؤشرات
# ============================================================

with tab2:
    st.subheader("📊 المؤشرات المعرفية")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        indicator_text = st.text_area(
            "أدخل نصاً لتحليل المؤشرات:",
            height=150,
            placeholder="الصق النص هنا..."
        )
    
    with col2:
        st.markdown("**المؤشرات المتاحة**")
        try:
            response = requests.get(f"{API_URL}/govern/indicators", timeout=5)
            if response.status_code == 200:
                indicators = response.json()
                for key, value in indicators.items():
                    st.markdown(f"- **{key}**: {value.get('name', '')}")
            else:
                st.warning("لا يمكن تحميل المؤشرات")
        except:
            st.warning("⚠️ لا يمكن الاتصال بالخادم")
    
    if st.button("📊 تحليل المؤشرات", type="primary"):
        if not indicator_text:
            st.warning("⚠️ الرجاء إدخال النص")
        else:
            with st.spinner("جاري التحليل..."):
                try:
                    response = requests.post(
                        f"{API_URL}/govern",
                        json={
                            "text": indicator_text,
                            "domain": "general",
                            "consent_given": True
                        },
                        timeout=30
                    )
                    data = response.json()
                    
                    if response.status_code == 200:
                        st.success("✅ تم تحليل المؤشرات")
                        
                        # عرض المؤشرات كبطاقات
                        cols = st.columns(3)
                        for idx, (key, value) in enumerate(data.get('indicators', {}).items()):
                            with cols[idx % 3]:
                                score = value.get('score', 0)
                                threshold = value.get('threshold', 0.7)
                                color = "🟢" if score < threshold else "🔴" if score > threshold * 1.2 else "🟡"
                                st.metric(
                                    f"{color} {key}",
                                    f"{score:.2f}",
                                    f"العتبة: {threshold}"
                                )
                    else:
                        st.error(f"❌ خطأ: {data.get('message', 'غير معروف')}")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

# ============================================================
# التبويب 3: التوليد
# ============================================================

with tab3:
    st.subheader("🚀 توليد المحتوى")
    
    generation_type = st.selectbox(
        "نوع التوليد",
        ["code", "content", "strategy", "business"]
    )
    
    description = st.text_area(
        "وصف المحتوى المطلوب:",
        height=100,
        placeholder="أدخل وصفاً لما تريد توليده..."
    )
    
    if st.button("🚀 توليد", type="primary"):
        if not description:
            st.warning("⚠️ الرجاء إدخال وصف")
        else:
            with st.spinner("جاري التوليد..."):
                try:
                    response = requests.post(
                        f"{API_URL}/generate/{generation_type}",
                        json={"description": description},
                        timeout=30
                    )
                    data = response.json()
                    
                    if response.status_code == 200:
                        st.success("✅ تم التوليد بنجاح")
                        
                        if generation_type == "code":
                            st.code(data.get('code', ''), language='python')
                        else:
                            st.json(data)
                    else:
                        st.error(f"❌ خطأ: {data.get('message', 'غير معروف')}")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

# ============================================================
# التبويب 4: الاستشراف
# ============================================================

with tab4:
    st.subheader("🔮 الاستشراف")
    
    col1, col2 = st.columns(2)
    
    with col1:
        domain_foresight = st.text_input("المجال", placeholder="أدخل المجال...")
        count = st.number_input("عدد السيناريوهات", min_value=1, max_value=20, value=5)
    
    with col2:
        st.info("🔮 سيناريوهات مستقبلية")
        st.markdown("""
        سيتم توليد سيناريوهات متعددة بناءً على:
        - **الأبعاد**: الأداء، الأمن، التكلفة، الوقت
        - **الأنماط**: متفائل، واقعي، متشائم، هجين
        - **الاحتمالات**: محاكاة مونت كارلو
        """)
    
    if st.button("🔮 توليد السيناريوهات", type="primary"):
        if not domain_foresight:
            st.warning("⚠️ الرجاء إدخال المجال")
        else:
            with st.spinner("جاري توليد السيناريوهات..."):
                try:
                    response = requests.post(
                        f"{API_URL}/foresight/scenarios",
                        json={"domain": domain_foresight, "count": count},
                        timeout=30
                    )
                    data = response.json()
                    
                    if response.status_code == 200:
                        st.success(f"✅ تم توليد {len(data.get('scenarios', []))} سيناريو")
                        
                        for i, scenario in enumerate(data.get('scenarios', []), 1):
                            with st.expander(f"📊 السيناريو {i}: {scenario.get('name', '')}"):
                                st.json(scenario)
                    else:
                        st.error(f"❌ خطأ: {data.get('message', 'غير معروف')}")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

# ============================================================
# التبويب 5: الإعدادات
# ============================================================

with tab5:
    st.subheader("⚙️ إعدادات المنصة")
    
    st.markdown("### 🌐 اللغات")
    try:
        response = requests.get(f"{API_URL}/translate/languages", timeout=5)
        if response.status_code == 200:
            languages = response.json()
            st.write(f"عدد اللغات المدعومة: {len(languages)}")
            st.json(list(languages.keys())[:10])
    except:
        st.warning("⚠️ لا يمكن تحميل اللغات")
    
    st.markdown("---")
    
    st.markdown("### 🔗 التكاملات")
    try:
        response = requests.get(f"{API_URL}/integration/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            st.metric("عدد التكاملات", data.get('total_connections', 0))
    except:
        st.warning("⚠️ لا يمكن تحميل التكاملات")
    
    st.markdown("---")
    
    st.markdown("### 🧠 حالة المحرك")
    try:
        response = requests.get(f"{API_URL}/engine/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            col1, col2, col3 = st.columns(3)
            col1.metric("المكونات", data.get('components_count', 0))
            col2.metric("وقت التشغيل", f"{data.get('uptime_hours', 0):.1f} ساعة")
            col3.metric("الطلبات", data.get('request_count', 0))
    except:
        st.warning("⚠️ لا يمكن تحميل حالة المحرك")
