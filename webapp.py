import streamlit as st

# --- Configuration and Styling ---
st.set_page_config(
    page_title="Smart Fertilizer Recommendation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS (unchanged look) ---
st.markdown("""
<style>
    .stApp { background-color: #1f2937; color: #f3f4f6; font-family: 'Inter', sans-serif; }
    .main .block-container { color: #f3f4f6; }
    .stNumberInput > div > div, .stSelectbox > div > div { background-color: #374151; border: 1px solid #4b5563; color: #f3f4f6; border-radius: 0.5rem; }
    .stNumberInput input, .stSelectbox span, .stSelectbox label { color: #f3f4f6 !important; }
    div[data-baseweb="select"] > div:nth-child(2) > div { background-color: #374151 !important; color: #f3f4f6 !important; }
    .header-title { color: #68d391; font-size: 2.5rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem; }
    .stAlert, .stApp h2, .stApp h3 { color: #68d391; }
    .stButton>button { background-color: #48bb78; color: white; font-weight: bold; border-radius: 0.5rem; padding: 0.75rem 1rem; transition: all 0.3s ease; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .stButton>button:hover { background-color: #38a169; transform: scale(1.01); }
    .stAlert { border-radius: 0.5rem; padding: 1rem; }
    .result-title { color: #9ae6b4; font-weight: 700; margin-bottom: 0.3rem; }
    .result-text { color: #d1fae5; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)


# --- Rule-Based Recommendation Logic (unchanged) ---
RECOMMENDATIONS = {
    'N_Low': {'fertilizer': 'Urea & N-Heavy Blend (46-0-0)', 'reason': 'Nitrogen (N) is severely low. Use a high-N fertilizer, especially for foliage-heavy crops.'},
    'P_Low': {'fertilizer': 'Diammonium Phosphate (DAP) or SSP', 'reason': 'Phosphorous (P) is the limiting nutrient. Apply DAP (18-46-0) or Single Super Phosphate for root development.'},
    'K_Low': {'fertilizer': 'Muriate of Potash (MOP) or Potash Sulfate', 'reason': 'Potassium (K) is low. Potash is essential for plant health, water, and disease resistance.'},
    'NPK_Balanced': {'fertilizer': '10-10-10 Universal Mix or Complex Fertilizer', 'reason': 'NPK levels are generally balanced. A complex fertilizer provides maintenance nutrients for overall growth.'},
    'High_NPK': {'fertilizer': 'Balanced Micronutrient Formula & Manure', 'reason': 'Primary nutrients (NPK) are high. Focus on organic manure or micronutrient supplements (e.g., Boron, Zinc).'},
    'Moisture_Low': {'fertilizer': 'Organic Compost & Increased Irrigation', 'reason': 'Moisture is critically low. Focus on organic matter to improve soil water retention before applying chemical fertilizer.'},
    'Moisture_High': {'fertilizer': 'Avoid Soluble Fertilizers & Improve Drainage', 'reason': 'Moisture is high, risking nutrient runoff. Apply granular, slow-release fertilizers sparingly and improve drainage.'}
}

NPK_THRESHOLDS = { 'low': 30, 'high': 60 }

def get_recommendation(N, P, K, M, SoilType, CropType):
    priority_found = False
    if M < 20:
        recommendation_key = 'Moisture_Low'; priority_found = True
    elif M > 80:
        recommendation_key = 'Moisture_High'; priority_found = True

    if not priority_found:
        low_N = N <= NPK_THRESHOLDS['low']; low_P = P <= NPK_THRESHOLDS['low']; low_K = K <= NPK_THRESHOLDS['low']
        high_NPK = N >= NPK_THRESHOLDS['high'] and P >= NPK_THRESHOLDS['high'] and K >= NPK_THRESHOLDS['high']

        if low_N and N <= P and N <= K:
            recommendation_key = 'N_Low'
        elif low_P and P <= N and P <= K:
            recommendation_key = 'P_Low'
        elif low_K and K <= N and K <= P:
            recommendation_key = 'K_Low'
        elif high_NPK:
            recommendation_key = 'High_NPK'
        else:
            recommendation_key = 'NPK_Balanced'

    rec = RECOMMENDATIONS[recommendation_key]
    final_fertilizer = rec['fertilizer']; final_reason = rec['reason']

    # Crop-specific adjustments (must match internal crop_type values)
    if recommendation_key == 'N_Low' and CropType in ['Rice', 'Maize']:
        final_fertilizer = 'High-Grade Urea (46-0-0)'
        final_reason += f" Urea is highly effective for high-demand, grain-producing crops like {CropType}."
    elif recommendation_key == 'K_Low' and CropType in ['Vegetables', 'Cotton']:
        final_fertilizer = 'Sulphate of Potash (SOP) (0-0-50)'
        final_reason += f" SOP provides sulfur, which is beneficial for the quality of fruits and fibers in {CropType}."

    # Soil-specific adjustments
    if recommendation_key == 'P_Low' and SoilType == 'Clayey':
        final_reason += " Caution: Phosphates may be less mobile in heavy clay soils; consider band application."
    elif recommendation_key == 'N_Low' and SoilType == 'Sandy':
        final_reason += " Warning: Sandy soils leach nitrogen quickly. Use slow-release N fertilizer or split applications."
        final_fertilizer = 'Slow-Release N Fertilizer'

    return final_fertilizer, final_reason

MOCK_MODEL_ACCURACIES = [
    {"name": "Decision Tree (Basis for Rules)", "accuracy": 0.985, "color": "green"},
    {"name": "Random Forest Classifier", "accuracy": 0.963, "color": "indigo"},
    {"name": "Support Vector Machine (SVM)", "accuracy": 0.941, "color": "orange"},
    {"name": "K-Nearest Neighbors (KNN)", "accuracy": 0.892, "color": "red"}
]


# --- TRANSLATIONS (English + Easy Kannada) ---
TRANSLATIONS = {
    "English": {
        "title": "🌱 Smart Fertilizer Recommendation",
        "subtitle": "Input your soil and crop conditions to get an optimal fertilizer suggestion.",
        "soil_crop": "Soil & Crop Data",
        "nutrient_title": "Nutrient and Environmental Levels",
        "nitrogen": "Nitrogen (N) - ppm",
        "phosphorous": "Phosphorous (P) - ppm",
        "potassium": "Potassium (K) - ppm",
        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "moisture": "Moisture (%)",
        "soil_type": "Soil Type",
        "crop_type": "Crop Type",
        "get_btn": "Get Fertilizer Recommendation",
        "recommended": "Recommended Fertilizer",
        "recommendation_label": "Recommendation:",
        "helper": "Enter your data and click 'Get Recommendation'.",
        "model_perf": "Model Performance Comparison (Simulated)"
    },
    "Kannada": {
        "title": "🌱 ಸ್ಮಾರ್ಟ್ ಬ Fertilizer ಶಿಫಾರಸು",  # kept short — title can be mostly English + Kannada tag
        "subtitle": "ಉತ್ತಮ ವ್ಯಾಪಕ ಸರಿಯಾದ ಉಲ್ಬಣ ಸಲಹೆಗಾಗಿ ನಿಮ್ಮ ಮಣ್ಣು ಮತ್ತು ಬೆಳೆ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ನಮೂದಿಸಿ.",
        "soil_crop": "ಮಣ್ಣು ಮತ್ತು ಬೆಳೆ ಮಾಹಿತಿ",
        "nutrient_title": "ಸಸ್ಯೋತ್ಪಾದಕ ಮತ್ತು ಹವಾಮಾನ ಮಟ್ಟಗಳು",
        "nitrogen": "ನೈಟ್ರೋಜನ್ (N) - ppm",
        "phosphorous": "ಫಾಸ್ಫರಸ್ (P) - ppm",
        "potassium": "ಪೊಟ್ಯಾಸಿಯಂ (K) - ppm",
        "temperature": "ತಾಪಮಾನ (°C)",
        "humidity": "ಆರ್ದ್ರತೆ (%)",
        "moisture": "ಆರ್ಡ್ರತೆ (%)",
        "soil_type": "ಮಣ್ಣಿನ ಪ್ರಕಾರ",
        "crop_type": "ಬೆಳೆ ಪ್ರಕಾರ",
        "get_btn": "ವೈಶಿಷ್ಟ್ಯ ಶಿಫಾರಸು ಪಡೆವು",
        "recommended": "ಶಿಫಾರಸು ಮಾಡಲಾದ ಉಲ್ಬಣ",
        "recommendation_label": "ಶಿಫಾರಸು:",
        "helper": "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಡೇಟಾವನ್ನು ನಮೂದಿಸಿ ಮತ್ತು 'Get Recommendation' ಕ್ಲಿಕ್ ಮಾಡಿ.",
        "model_perf": "ಮಾದರಿ ಕಾರ್ಯಕ್ಷಮತೆ ಹೋಲಿಕೆ (ನಕಲಿ)"
    }
}

# Soil and crop options:
# Keep internal values in English (so logic comparisons still work), provide translations for display.
SOIL_OPTIONS = [
    ("Loamy", {"en": "Loamy", "kn": "ಲೋಮಿ (Loamy)"}),
    ("Sandy", {"en": "Sandy", "kn": "ಮಣಿಯ (Sandy)"}),
    ("Clayey", {"en": "Clayey", "kn": "ಕ್ಲೇಯ್ ಮಣ್ಣು (Clayey)"}),
    ("Silt", {"en": "Silt", "kn": "ಸಿಡ್ಲ್ (Silt)"}),
    ("Peat", {"en": "Peat", "kn": "ಪೀಟ್ (Peat)"})
]

CROP_OPTIONS = [
    ("Rice", {"en": "Rice", "kn": "ಅನ್ನ (Rice)"}),
    ("Maize", {"en": "Maize", "kn": "ಮಕ್ಕೆಜೋಳ (Maize)"}),
    ("Wheat", {"en": "Wheat", "kn": "ಗೋಧಿ (Wheat)"}),
    ("Millet", {"en": "Millet", "kn": "ಜೋಳ (Millet)"}),
    ("Cotton", {"en": "Cotton", "kn": "ಕಬ್ಬಿಣ (Cotton)"}),
    ("Pulses", {"en": "Pulses", "kn": "ಕಾಳು (Pulses)"}),
    ("Vegetables", {"en": "Vegetables", "kn": " ತರಕಾರಿಗಳು (Vegetables)"})
]

# --- UI: language selector (remember selection) ---
if "ui_lang" not in st.session_state:
    st.session_state["ui_lang"] = "English"

lang = st.sidebar.selectbox("Language / ಭಾಷೆ", ["English", "Kannada"], index=0 if st.session_state["ui_lang"] == "English" else 1)
st.session_state["ui_lang"] = lang

# Convenience alias
tr = TRANSLATIONS[lang]

# --- Page header and layout ---
st.markdown(f"<h1 class='header-title'>{tr['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='text-center text-lg text-gray-400 mb-8'>{tr['subtitle']}</p>", unsafe_allow_html=True)

col_input, col_result = st.columns([2, 1])

with col_input:
    st.header(tr["soil_crop"], divider='green')
    st.subheader(tr["nutrient_title"])

    c1, c2, c3 = st.columns(3)
    with c1:
        N = st.number_input(tr["nitrogen"], value=40, min_value=0, step=5, help=tr["nitrogen"])
    with c2:
        P = st.number_input(tr["phosphorous"], value=50, min_value=0, step=5, help=tr["phosphorous"])
    with c3:
        K = st.number_input(tr["potassium"], value=60, min_value=0, step=5, help=tr["potassium"])

    c4, c5, c6 = st.columns(3)
    with c4:
        T = st.number_input(tr["temperature"], value=25.0, min_value=0.0, max_value=50.0, step=0.5)
    with c5:
        H = st.number_input(tr["humidity"], value=65.0, min_value=0.0, max_value=100.0, step=1.0)
    with c6:
        M = st.number_input(tr["moisture"], value=40.0, min_value=0.0, max_value=100.0, step=1.0)

    st.subheader(tr["soil_type"] + " / " + tr["crop_type"])
    c7, c8 = st.columns(2)

    # Soil Type selectbox: display translated labels, but return internal English value
    soil_display = [opt[1][ 'en' ] if lang == "English" else opt[1]['kn'] for opt in SOIL_OPTIONS]
    soil_values = [opt[0] for opt in SOIL_OPTIONS]
    soil_index_default = 0
    soil_choice_display = c7.selectbox(tr["soil_type"], options=soil_display, index=soil_index_default)
    soil_type = soil_values[soil_display.index(soil_choice_display)]

    # Crop Type selectbox: same technique
    crop_display = [opt[1]['en'] if lang == "English" else opt[1]['kn'] for opt in CROP_OPTIONS]
    crop_values = [opt[0] for opt in CROP_OPTIONS]
    crop_index_default = 0
    crop_choice_display = c8.selectbox(tr["crop_type"], options=crop_display, index=crop_index_default)
    crop_type = crop_values[crop_display.index(crop_choice_display)]

    # Button (translated)
    if st.button(tr["get_btn"], use_container_width=True):
        if any(v is None or v < 0 for v in [N, P, K, T, H, M]):
            # show error in current language
            st.error("Please ensure all numerical inputs are valid and non-negative." if lang == "English" else "ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಸಂಖ್ಯಾತ್ಮಕ ಇನ್ಪುಟ್‌ಗಳು ಸರಿಯಿತೆಂದು ಪರಿಶೀಲಿಸಿ.")
        else:
            fertilizer, reason = get_recommendation(N, P, K, M, soil_type, crop_type)
            st.session_state.result = (fertilizer, reason)

    if 'result' not in st.session_state:
        st.session_state.result = (None, None)

with col_result:
    st.markdown(f"<h2 class='text-xl font-bold text-green-800 mb-4'>{tr['recommended']}</h2>", unsafe_allow_html=True)

    if st.session_state.result[0]:
        fertilizer, reason = st.session_state.result
        st.markdown(f"<div class='result-title'>{tr['recommendation_label']}</div>", unsafe_allow_html=True)
        # show recommendation text plainly (no big green box)
        st.markdown(f"<div class='result-text'><strong>{fertilizer}</strong><br>{reason}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p class='text-lg text-gray-300'>{tr['helper']}</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<h3 class='text-lg font-bold text-green-400 text-center mb-3'>{tr['model_perf']}</h3>", unsafe_allow_html=True)

    for model in MOCK_MODEL_ACCURACIES:
        accuracy_percent = model["accuracy"] * 100
        st.markdown(f"""
        <div class="text-sm" style="margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#cbd5e1;">{model['name']}</span>
                <span style="color:#86efac;">{accuracy_percent:.1f}%</span>
            </div>
            <div style="background-color:#374151; border-radius:999px; height:10px; width:100%;">
                <div style="background-color:#10b981; height:10px; border-radius:999px; width:{accuracy_percent}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
