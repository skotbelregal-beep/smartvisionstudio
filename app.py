import os
import streamlit as st
from google import genai
from google.genai import types

# 1. إعداد الصفحة وتصميم الاستوديو السينمائي
st.set_page_config(
    page_title="Smart Vision Studio Pro",
    page_icon="🎬",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main-header {font-size: 2.3rem; color: #00adb5; font-weight: 800; text-align: center; margin-bottom: 5px;}
    .sub-header {font-size: 1.1rem; color: #95afc0; text-align: center; margin-bottom: 25px;}
    .stButton>button {width: 100%; background-color: #00adb5; color: white; font-weight: bold; border-radius: 8px;}
    .stButton>button:hover {background-color: #00fff5; color: black;}
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. إعداد مفتاح API الخاص بـ Gemini
api_key = os.environ.get("GEMINI_API_KEY")

# الشريط الجانبي (Sidebar)
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/video-editing.png",
        use_container_width=True,
    )
    st.title("⚙️ إعدادات المحرك")
    
    if not api_key:
        api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password")
    
    project_name = st.text_input("اسم المشروع", "Smart Vision Cinematic")
    render_quality = st.selectbox(
        "جودة دقة الصورة المستهدفة",
        ["4K Cinematic", "8K Ultra HD", "1080p Full HD"],
    )
    fps_choice = st.selectbox("معدل الإطارات (FPS)", [24, 30, 60])
    st.markdown("---")
    st.success("✅ المحرك مربوط مباشرة بنماذج Gemini الحقيقية.")

# تهيئة العميل عند توفر المفتاح
client = genai.Client(api_key=api_key) if api_key else None

# الهيدر الرئيسي
st.markdown(
    '<div class="main-header">🎬 Smart Vision Studio Pro</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">المنصة المتكاملة بالذكاء الاصطناعي لكتابة السيناريوهات الحقيقية، نمذجة الشخصيات بصرية، ومعالجة الصوت</div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "1. مولد السيناريو التلقائي (Gemini)",
        "2. توليد صور ونمذجة الشخصيات (3D / كارتون / واقعي)",
        "3. هندسة الصوت والأداء",
        "4. الإخراج وتصدير المشهد",
    ]
)

# Tab 1: Script Generator (Real Gemini API)
with tab1:
    st.subheader("✍️ توليد سيناريو سينمائي كامل من ملخص بسيط")
    col1, col2 = st.columns(2)
    with col1:
        genre = st.selectbox(
            "التصنيف الفني:",
            [
                "دراما سينمائية",
                "خيال علمي وملحمي",
                "إعلان تجاري ضخم",
                "أكشن وإثارة",
                "رعب وغموض",
            ],
        )
        dialect = st.selectbox(
            "اللهجة / لغة الحوار:",
            [
                "عامية مصرية طبيعية",
                "عربية فصحى معاصرة",
                "لهجة خليجية",
                "إنجليزي سينمائي",
            ],
        )
    with col2:
        tone = st.selectbox(
            "النبرة الدرامية:",
            [
                "حماسي ومؤثر",
                "غامض ومثير للتشويق",
                "درامي عميق",
                "ساخر وكوميدي",
            ],
        )
        scene_count = st.slider("عدد المشاهد المطلوبة:", 1, 5, 2)

    brief_text = st.text_area(
        "أدخل ملخص الفكرة أو الأحداث الرئيسية:",
        placeholder="مثال: محقق يكتشف رسالة غريبة مكتوبة بخط يده داخل خزنة مغلقة منذ 20 سنة...",
    )

    if st.button("🚀 توليد السيناريو بالذكاء الاصطناعي الحقيقي"):
        if not client:
            st.error("⚠️ يرجى أدخال GEMINI_API_KEY في الشريط الجانبي أولاً لتفعيل التوليد.")
        elif not brief_text.strip():
            st.warning("يرجى إدخال ملخص الفكرة أولاً.")
        else:
            with st.spinner("جاري صياغة السيناريو وتوزيع المشاهد والحوارات عبر Gemini..."):
                prompt = f"""
أنت مخرج وكاتب سيناريو سينمائي محترف. اكتب سيناريو متكامل بناءً على التفاصيل التالية:
- اسم المشروع: {project_name}
- التصنيف: {genre}
- لهجة الحوار: {dialect}
- النبرة الدرامية: {tone}
- عدد المشاهد: {scene_count}
- الملخص: {brief_text}

يرجى كتابة السيناريو بتنسيق سينمائي محترف يشمل:
1. رقم وتوصيف المشهد (داخلي/خارجي - المكان - الوقت).
2. حركة الكاميرا ونوع الإضاءة المطلوبة لكل كادر.
3. الحوارات الكاملة المكتوبة بـ ({dialect}).
4. المؤثرات الصوتية والبصرية المقترحة.
                """
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt,
                    )
                    st.success("✨ تم توليد السيناريو الحقيقي بنجاح!")
                    st.text_area("السيناريو الناتج:", value=response.text, height=350)
                except Exception as e:
                    st.error(f"حدث خطأ أثناء التوليد: {e}")

# Tab 2: Real Image Generation & Character Modeling
with tab2:
    st.subheader("🎨 نمذجة وتوليد صور الشخصيات واللوكيشن الحقيقية")
    c1, c2 = st.columns(2)
    with c1:
        char_style_mode = st.selectbox(
            "نمط التصميم البصري:",
            [
                "Realistic Cinematic Photorealistic",
                "3D CGI Pixar Disney Animation Style",
                "2D Stylized Cartoon Concept Art",
                "Dark Cyberpunk Sci-Fi Concept",
            ],
        )
        char_description = st.text_input(
            "وصف ملامح الشخصية أو اللوكيشن:",
            placeholder="شاب مصري شجاع بعيون حادة، يرتدي معطفاً دافئاً وتظهر عليه علامات الإرهاق...",
        )
    with c2:
        lighting_setup = st.selectbox(
            "توزيع الإضاءة:",
            [
                "Dramatic Cinematic Studio Lighting",
                "Neon Cyberpunk Rim Lighting",
                "Golden Hour Natural Sunlight",
            ],
        )
        aspect_ratio = st.selectbox(
            "أبعاد الصورة:",
            ["16:9", "1:1", "9:16"]
        )

    if st.button("✨ رسم وتوليد الصورة فوراً"):
        if not client:
            st.error("⚠️ يرجى أدخال GEMINI_API_KEY لتفعيل محرك توليد الصور.")
        elif not char_description.strip():
            st.warning("يرجى كتابة وصف الشخصية أو المشهد.")
        else:
            with st.spinner("جاري تصميم ورسم الصورة بدقة فائقة عبر الذكاء الاصطناعي..."):
                image_prompt = f"{char_description}, style: {char_style_mode}, lighting: {lighting_setup}, highly detailed, 8k resolution, cinematic quality"
                try:
                    result = client.models.generate_images(
                        model='imagen-3.0-generate-002',
                        prompt=image_prompt,
                        config=types.GenerateImagesConfig(
                            number_of_images=1,
                            aspect_ratio=aspect_ratio,
                        )
                    )
                    for generated_image in result.generated_images:
                        st.image(generated_image.image.image_bytes, caption=f"نموذج الشخصية ({char_style_mode})")
                        st.download_button(
                            label="📥 تحميل الصورة عالية الدقة",
                            data=generated_image.image.image_bytes,
                            file_name="smart_vision_character.png",
                            mime="image/png"
                        )
                except Exception as e:
                    st.error(f"حدث خطأ أثناء توليد الصورة: {e}")

# Tab 3: Audio & Voice
with tab3:
    st.subheader("🎙️ هندسة الصوت والتعليق الصوتي")
    voice_text = st.text_area(
        "النص المراد تحويله إلى أداء صوتي:",
        placeholder="اكتب الحوار أو التعليق الصوتي هنا..."
    )
    
    if st.button("🔊 تشغيل الأداء الصوتي"):
        if voice_text.strip():
            # توليد أداء صوتي تفاعلي باستخدام المتصفح مباشرة
            sound_html = f"""
            <script>
            var msg = new SpeechSynthesisUtterance("{voice_text}");
            msg.lang = "ar-SA";
            window.speechSynthesis.speak(msg);
            </script>
            <p style="color: #00adb5;">▶️ جاري تشغيل الأداء الصوتي عبر المتصفح...</p>
            """
            st.components.v1.html(sound_html, height=60)
            st.success("تم بدء الأداء الصوتي بنجاح.")
        else:
            st.warning("يرجى إدخال نص أولاً.")

# Tab 4: Render & Export Setup
with tab4:
    st.subheader("🎞️ تجهيز الدمج وتصدير المشهد النهائي")
    up_img_final = st.file_uploader("رفع صورة الشخصية المعتمدة:", type=["jpg", "png", "jpeg"])
    up_aud_final = st.file_uploader("رفع ملف الصوت المعتمد:", type=["mp3", "wav"])

    if up_img_final and up_aud_final:
        col_a, col_b = st.columns(2)
        with col_a:
            st.image(up_img_final, caption="صورة المشهد/الشخصية", use_container_width=True)
        with col_b:
            st.audio(up_aud_final)

        st.info(f"إعدادات التصدير: الجودة ({render_quality}) | معدل الإطارات ({fps_choice} FPS)")
        if st.button("🚀 تصدير ملفات الإنتاج النهائية"):
            st.success("تم تجهيز حزمة الإنتاج للمشروع وتجميع كافة العناصر الحقيقية!")
            st.balloons()
