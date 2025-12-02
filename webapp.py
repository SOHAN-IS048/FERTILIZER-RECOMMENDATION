import streamlit as st

# --- Configuration and Styling ---
st.set_page_config(
    page_title="Smart Fertilizer Recommendation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a clean, professional look (mimicking Tailwind classes where necessary)
st.markdown("""
<style>
    /* *** START OF DARK MODE CHANGES ***
    */
    .stApp {
        background-color: #1f2937; /* Dark Gray background (Slate-800) */
        color: #f3f4f6; /* Light text color (Gray-100) */
        font-family: 'Inter', sans-serif;
    }

    /* Style for Streamlit's main content area background */
    .main .block-container {
        color: #f3f4f6; /* Ensure text remains light in the content block */
    }
    
    /* Input Field Styling (number_input, selectbox) */
    .stNumberInput > div > div, .stSelectbox > div > div {
        background-color: #374151; /* Medium Dark Gray for input fields (Slate-700) */
        border: 1px solid #4b5563; /* Darker border */
        color: #f3f4f6; /* Light text inside input fields */
        border-radius: 0.5rem;
    }
    
    /* Ensure the text inside the input fields is visible (Light Gray) */
    .stNumberInput input, .stSelectbox span, .stSelectbox label {
        color: #f3f4f6 !important;
    }
    /* Set the background of the selectbox options dropdown to dark */
    div[data-baseweb="select"] > div:nth-child(2) > div {
        background-color: #374151 !important;
        color: #f3f4f6 !important;
    }

    /* Titles and Header text */
    .header-title {
        color: #68d391; /* Light Green for title */
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Component Headers (e.g., "Soil & Crop Data") */
    .stAlert, .stApp h2, .stApp h3 {
        color: #68d391; /* Light Green for sub-headers */
    }
    
    /* --- END OF DARK MODE CHANGES --- */

    .stButton>button {
        background-color: #48bb78; /* Green-600 */
        color: white;
        font-weight: bold;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.06);
    }
    .stButton>button:hover {
        background-color: #38a169; /* Green-700 */
        transform: scale(1.01);
    }
    
    .stAlert {
        border-radius: 0.5rem;
        padding: 1rem;
    }
    .result-box {
        border: 2px solid #68d391; /* Green-300 */
        background-color: #064e3b; /* Dark Green for results */
        color: #f0fff4; /* Light text in results */
        padding: 2rem;
        border-radius: 0.5rem;
        text-align: center;
        min-height: 250px;
    }
    .result-box .text-xl, .result-box .text-2xl {
        color: #bcf5d4; /* Lighter green for results text */
    }
</style>
""", unsafe_allow_html=True)


# --- Rule-Based Recommendation Logic (Translated from JavaScript) ---

RECOMMENDATIONS = {
    'N_Low': {'fertilizer': 'Urea & N-Heavy Blend (46-0-0)', 'reason': 'Nitrogen (N) is severely low. Use a high-N fertilizer, especially for foliage-heavy crops.'},
    'P_Low': {'fertilizer': 'Diammonium Phosphate (DAP) or SSP', 'reason': 'Phosphorous (P) is the limiting nutrient. Apply DAP (18-46-0) or Single Super Phosphate for root development.'},
    'K_Low': {'fertilizer': 'Muriate of Potash (MOP) or Potash Sulfate', 'reason': 'Potassium (K) is low. Potash is essential for plant health, water, and disease resistance.'},
    'NPK_Balanced': {'fertilizer': '10-10-10 Universal Mix or Complex Fertilizer', 'reason': 'NPK levels are generally balanced. A complex fertilizer provides maintenance nutrients for overall growth.'},
    'High_NPK': {'fertilizer': 'Balanced Micronutrient Formula & Manure', 'reason': 'Primary nutrients (NPK) are high. Focus on organic manure or micronutrient supplements (e.g., Boron, Zinc).'},
    'Moisture_Low': {'fertilizer': 'Organic Compost & Increased Irrigation', 'reason': 'Moisture is critically low. Focus on organic matter to improve soil water retention before applying chemical fertilizer.'},
    'Moisture_High': {'fertilizer': 'Avoid Soluble Fertilizers & Improve Drainage', 'reason': 'Moisture is high, risking nutrient runoff. Apply granular, slow-release fertilizers sparingly and improve drainage.'}
}

NPK_THRESHOLDS = {
    'low': 30,
    'high': 60,
}

# --- Function to get Recommendation ---
def get_recommendation(N, P, K, M, SoilType, CropType):
    """Calculates fertilizer recommendation based on rule-based logic."""
    
    # 1. Check for severe moisture issues first
    priority_found = False
    if M < 20:
        recommendation_key = 'Moisture_Low'
        priority_found = True
    elif M > 80:
        recommendation_key = 'Moisture_High'
        priority_found = True
    
    # 2. If no severe moisture issue, check NPK levels for nutrient deficiency
    if not priority_found:
        low_N = N <= NPK_THRESHOLDS['low']
        low_P = P <= NPK_THRESHOLDS['low']
        low_K = K <= NPK_THRESHOLDS['low']
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

    # 3. Customize recommendation based on Crop/Soil (Secondary Logic)
    rec = RECOMMENDATIONS[recommendation_key]
    final_fertilizer = rec['fertilizer']
    final_reason = rec['reason']

    # Crop-specific adjustments
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

# --- Model Accuracy Data (for display) ---
MOCK_MODEL_ACCURACIES = [
    {"name": "Decision Tree (Basis for Rules)", "accuracy": 0.985, "color": "green"},
    {"name": "Random Forest Classifier", "accuracy": 0.963, "color": "indigo"},
    {"name": "Support Vector Machine (SVM)", "accuracy": 0.941, "color": "orange"},
    {"name": "K-Nearest Neighbors (KNN)", "accuracy": 0.892, "color": "red"}
]


# --- Streamlit UI Layout ---

st.markdown("<h1 class='header-title'>🌱 Smart Fertilizer Recommendation</h1>", unsafe_allow_html=True)
st.markdown("<p class='text-center text-lg text-gray-400 mb-8'>Input your soil and crop conditions to get an optimal fertilizer suggestion.</p>", unsafe_allow_html=True)

# --- LANGUAGE SELECTOR (added, does not alter app logic/content) ---
# This replicates the simple dropdown appearance in your screenshot.
if "ui_lang" not in st.session_state:
    st.session_state["ui_lang"] = "Kannada"  # default shown in screenshot

st.sidebar.markdown("### Language / ಭಾಷೆ")
st.session_state["ui_lang"] = st.sidebar.selectbox("", ["Kannada", "English"], index=0 if st.session_state["ui_lang"] == "Kannada" else 1)

# Use columns for the two main panels
col_input, col_result = st.columns([2, 1])

with col_input:
    st.header("Soil & Crop Data", divider='green')
    
    # Numerical Inputs (Grid Layout - 3 columns)
    st.subheader("Nutrient and Environmental Levels")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        N = st.number_input("Nitrogen (N) - ppm", value=40, min_value=0, step=5, help="Concentration of Nitrogen in the soil.")
    with c2:
        P = st.number_input("Phosphorous (P) - ppm", value=50, min_value=0, step=5, help="Concentration of Phosphorous in the soil.")
    with c3:
        K = st.number_input("Potassium (K) - ppm", value=60, min_value=0, step=5, help="Concentration of Potassium in the soil.")

    c4, c5, c6 = st.columns(3)

    with c4:
        T = st.number_input("Temperature (°C)", value=25.0, min_value=0.0, max_value=50.0, step=0.5)
    with c5:
        H = st.number_input("Humidity (%)", value=65.0, min_value=0.0, max_value=100.0, step=1.0)
    with c6:
        M = st.number_input("Moisture (%)", value=40.0, min_value=0.0, max_value=100.0, step=1.0)

    # Categorical Inputs (2 columns)
    st.subheader("Soil and Crop Type")
    c7, c8 = st.columns(2)
    
    with c7:
        soil_type = st.selectbox(
            "Soil Type",
            ('Loamy', 'Sandy', 'Clayey', 'Silt', 'Peat'),
            index=0
        )
    
    with c8:
        crop_type = st.selectbox(
            "Crop Type",
            ('Rice', 'Maize', 'Wheat', 'Millet', 'Cotton', 'Pulses', 'Vegetables'),
            index=0
        )

    # Recommendation Button
    if st.button("Get Fertilizer Recommendation", use_container_width=True):
        if any(v is None or v < 0 for v in [N, P, K, T, H, M]):
            st.error("Please ensure all numerical inputs are valid and non-negative.")
        else:
            # Calculate and store the result in session state
            fertilizer, reason = get_recommendation(N, P, K, M, soil_type, crop_type)
            st.session_state.result = (fertilizer, reason)
    
    # Initialize session state if not present
    if 'result' not in st.session_state:
        st.session_state.result = (None, None)

with col_result:
    st.markdown("<div class='result-box'>", unsafe_allow_html=True)
    st.markdown("<h2 class='text-xl font-bold text-green-800 mb-4'>Recommended Fertilizer</h2>", unsafe_allow_html=True)

    if st.session_state.result[0]:
        # Display the successful recommendation
        fertilizer, reason = st.session_state.result
        
        st.markdown(f"""
        <svg class="w-12 h-12 text-green-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <p class='text-2xl font-extrabold text-green-200 mb-2'>{fertilizer}</p>
        <p class='text-sm text-green-300'>{reason}</p>
        """, unsafe_allow_html=True)
    else:
        # Display the initial message WITHOUT the large decorative SVG (removed)
        st.markdown("""
        <p class='text-lg text-gray-300'>Enter your data and click 'Get Recommendation'.</p>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model Performance Comparison
    st.markdown("<h3 class='text-lg font-bold text-green-400 text-center mb-3'>Model Performance Comparison (Simulated)</h3>", unsafe_allow_html=True)
    
    for model in MOCK_MODEL_ACCURACIES:
        accuracy_percent = model["accuracy"] * 100
        # Updated text colors for dark mode visibility
        st.markdown(f"""
        <div class="text-sm">
            <div class="flex justify-between mb-1">
                <span class="font-medium text-gray-300">{model['name']}</span>
                <span class="font-semibold text-green-300">{accuracy_percent:.1f}%</span>
            </div>
            <div class="w-full bg-gray-600 rounded-full h-2.5">
                <div class="h-2.5 rounded-full" style="background-color: #10b981; width: {accuracy_percent}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
