import re
import html

import streamlit as st

from workflow import build_workflow


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TripWise AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# TRUSTED HTML RENDERER
# =========================================================

def render_html(content):
    """Render app-owned HTML/CSS without exposing HTML tags as text."""
    if hasattr(st, "html"):
        st.html(content)
    else:
        st.markdown(content, unsafe_allow_html=True)


# =========================================================
# CUSTOM CSS
# =========================================================

render_html(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 5% 10%, rgba(59,130,246,.13), transparent 28%),
            radial-gradient(circle at 95% 18%, rgba(236,72,153,.12), transparent 30%),
            radial-gradient(circle at 50% 100%, rgba(16,185,129,.08), transparent 32%),
            #f7f9fc;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 1.4rem;
        padding-bottom: 4rem;
    }

    /* ---------- HERO ---------- */
    .hero {
        position: relative;
        min-height: 220px;
        padding: 2.2rem 3rem;
        border-radius: 28px;
        background: linear-gradient(110deg, #4f46e5 0%, #7c3aed 38%, #ec4899 70%, #ff9f43 100%);
        color: white;
        margin: .8rem auto 2rem auto;
        border: 2px solid rgba(255,255,255,.55);
        box-shadow: 0 22px 55px rgba(79,70,229,.24), 0 0 0 1px rgba(79,70,229,.08);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    .hero:before {
        content: "✈";
        position: absolute;
        left: 7%;
        top: 25px;
        font-size: 72px;
        opacity: .16;
        transform: rotate(-18deg);
    }
    .hero:after {
        content: "☀   ☁        ✈";
        position: absolute;
        right: 5%;
        bottom: 18px;
        font-size: 44px;
        letter-spacing: 18px;
        opacity: .17;
    }
    .hero h1 {
        position: relative;
        z-index: 2;
        font-size: 3.25rem !important;
        line-height: 1.05 !important;
        font-weight: 850 !important;
        margin: 0 !important;
        letter-spacing: -.8px;
        color: #fff !important;
        text-shadow: 0 3px 18px rgba(0,0,0,.15);
    }
    .hero p {
        position: relative;
        z-index: 2;
        font-size: 1.15rem !important;
        margin: .65rem 0 0 !important;
        color: rgba(255,255,255,.94) !important;
    }

    /* ---------- FORM SHELL ---------- */
    .form-shell {
        background: rgba(255,255,255,.92);
        border: 1px solid rgba(226,232,240,.9);
        border-radius: 26px;
        padding: 1.55rem 1.7rem 1.7rem;
        box-shadow: 0 18px 45px rgba(15,23,42,.08);
        margin-bottom: 1.5rem;
    }
    .section-heading {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: .2rem 0 1.25rem;
        color: #172554;
        font-size: 1.55rem;
        font-weight: 800;
    }
    .section-subtitle {
        margin: -1rem 0 1.25rem 43px;
        color: #64748b;
        font-size: .94rem;
    }

    /* ---------- COLORFUL INPUT HEADERS ---------- */
    .field-card {
        border-radius: 17px;
        overflow: hidden;
        margin-bottom: .55rem;
        border: 1px solid rgba(148,163,184,.16);
        box-shadow: 0 8px 22px rgba(15,23,42,.05);
    }
    .field-head {
        color: white;
        padding: .72rem 1rem;
        font-weight: 800;
        font-size: .98rem;
        letter-spacing: .05px;
    }
    .field-head span { margin-right: 7px; }
    .blue .field-head { background: linear-gradient(100deg,#2563eb,#93b4ff); }
    .purple .field-head { background: linear-gradient(100deg,#7c3aed,#e8a5f2); }
    .green .field-head { background: linear-gradient(100deg,#10b981,#8ee8c2); }
    .orange .field-head { background: linear-gradient(100deg,#f59e0b,#ffd77b); }
    .pink .field-head { background: linear-gradient(100deg,#ec4899,#f9a8c8); }
    .cyan .field-head { background: linear-gradient(100deg,#06b6d4,#9be8f4); }

    /* Streamlit widgets under our custom field headers */
    .field-widget { margin-top: -1px; }
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #fff !important;
        border-radius: 0 0 14px 14px !important;
        border-color: #e2e8f0 !important;
        min-height: 43px;
    }
    div[data-testid="stTextInput"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label {
        display: none !important;
    }
    div[data-testid="stTextInput"] > div,
    div[data-testid="stNumberInput"] > div,
    div[data-testid="stSelectbox"] > div {
        border-radius: 0 0 14px 14px;
    }
    div[data-testid="stTextInput"],
    div[data-testid="stNumberInput"],
    div[data-testid="stSelectbox"] { margin-top: -1px; }

    /* ---------- INTERESTS ---------- */
    .interest-box {
        margin-top: 1.15rem;
        padding: 1.15rem 1.25rem 1rem;
        border-radius: 19px;
        background: linear-gradient(135deg,#fff 0%,#faf7ff 100%);
        border: 1px solid #ede9fe;
        box-shadow: 0 8px 22px rgba(15,23,42,.04);
    }
    .interest-title { font-size: 1.3rem; font-weight: 800; color: #172554; }
    .interest-sub { color:#64748b; font-size:.9rem; margin-top:.2rem; }
    div[data-testid="stMultiSelect"] label { display:none !important; }
    div[data-testid="stMultiSelect"] > div > div {
        border-radius: 14px !important;
        border-color: #e2e8f0 !important;
        background: #fff !important;
        min-height: 52px;
    }
    div[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    /* ---------- BUTTON ---------- */
    div.stButton > button {
        min-height: 58px;
        border: 0 !important;
        border-radius: 15px !important;
        font-size: 1.08rem !important;
        font-weight: 850 !important;
        color: white !important;
        background: linear-gradient(100deg,#f72585 0%,#ff4d4d 50%,#ff9f1c 100%) !important;
        box-shadow: 0 12px 28px rgba(244,63,94,.23);
        transition: transform .15s ease, box-shadow .15s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 34px rgba(244,63,94,.30);
    }

    /* ---------- RESULTS ---------- */
    .section-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #172554;
        margin-top: 1.8rem;
        margin-bottom: .9rem;
    }
    .info-card,.place-card,.itinerary-card {
        padding: 1.25rem;
        border-radius: 18px;
        background: white;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 24px rgba(15,23,42,.06);
    }
    .info-card { min-height: 105px; }
    .place-card { min-height: 130px; }
    .itinerary-card { margin-bottom: 1rem; }
    .info-label { color:#64748b; font-size:.82rem; margin-bottom:.35rem; }
    .info-value { color:#0f172a; font-size:1.25rem; font-weight:750; }
    .footer { text-align:center; color:#64748b; font-size:.85rem; margin-top:3rem; padding-bottom:2rem; }
    </style>
    """,
)

# =========================================================
# BASIC HELPERS
# =========================================================

def get_value(obj, key, default=None):
    if obj is None:
        return default

    if isinstance(obj, dict):
        return obj.get(key, default)

    return getattr(obj, key, default)


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return int(default)


def format_pkr(value):
    number = safe_float(value, 0)
    return f"PKR {number:,.0f}"


def get_research_value(research, key, default=None):
    if research is None:
        return default

    if isinstance(research, dict):
        return research.get(key, default)

    return getattr(research, key, default)


def normalize_places(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    return []


# =========================================================
# STRONG AI OUTPUT CLEANER
# =========================================================

def clean_ai_output(text):
    """
    Cleans AI-generated output.

    Removes:
    - HTML tags
    - CSS
    - JavaScript
    - code fences
    - localhost links
    - SVG links
    - HTML attribute lines

    It does NOT affect our own Streamlit HTML/CSS.
    """

    if not text:
        return ""

    text = str(text)

    # -----------------------------------------------------
    # Decode HTML entities
    # -----------------------------------------------------

    for _ in range(3):
        text = html.unescape(text)

    # -----------------------------------------------------
    # Remove HTML blocks
    # -----------------------------------------------------

    text = re.sub(
        r"<style\b[^>]*>.*?</style>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    text = re.sub(
        r"<script\b[^>]*>.*?</script>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    # -----------------------------------------------------
    # Remove normal HTML tags
    # -----------------------------------------------------

    text = re.sub(
        r"<[^>\n]+>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # -----------------------------------------------------
    # Remove escaped HTML-looking text
    # -----------------------------------------------------

    text = re.sub(
        r"\\+<[^>\n]+>",
        "",
        text,
    )

    # -----------------------------------------------------
    # Remove markdown code fences
    # -----------------------------------------------------

    text = re.sub(
        r"```(?:html|css|javascript|js|markdown|md|text|python)?",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = text.replace("```", "")

    # -----------------------------------------------------
    # Remove localhost markdown links
    # -----------------------------------------------------

    text = re.sub(
        r"\[([^\]]*)\]\(\s*https?://localhost:[^)]+\)",
        r"\1",
        text,
        flags=re.IGNORECASE,
    )

    # -----------------------------------------------------
    # Remove SVG links
    # -----------------------------------------------------

    text = re.sub(
        r"\[svg\]\([^)]+\)",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # -----------------------------------------------------
    # Remove standalone HTML attribute lines
    # -----------------------------------------------------

    cleaned_lines = []

    for line in text.splitlines():

        stripped = line.strip()
        lower = stripped.lower()

        if not stripped:
            cleaned_lines.append("")
            continue

        # HTML attributes
        if re.match(
            r"^(style|class|id|href|src)\s*=",
            lower,
        ):
            continue

        # CSS properties
        if re.match(
            r"^(margin|padding|color|display|font|background|"
            r"border|box|text|width|height|position|"
            r"align|justify|overflow)[-\w]*\s*:",
            lower,
        ):
            continue

        cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # -----------------------------------------------------
    # Remove remaining HTML-like lines
    # -----------------------------------------------------

    text = re.sub(
        r"^\s*\\?<?/?[A-Za-z][^>\n]*>\s*$",
        "",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )

    # -----------------------------------------------------
    # Remove excessive blank lines
    # -----------------------------------------------------

    text = re.sub(
        r"\n[ \t]*\n[ \t]*\n+",
        "\n\n",
        text,
    )

    return text.strip()


# =========================================================
# EXTRACT ONLY THE REAL ITINERARY
# =========================================================

def extract_itinerary(text):
    """
    Extract only:

        Day 1
        Day 2
        Day 3
        ...

    from the AI response.

    Dashboard HTML, budget HTML, weather HTML,
    places HTML etc. are ignored.
    """

    if not text:
        return ""

    text = str(text)

    # -----------------------------------------------------
    # Decode HTML entities
    # -----------------------------------------------------

    for _ in range(3):
        text = html.unescape(text)

    # -----------------------------------------------------
    # Remove code fences
    # -----------------------------------------------------

    text = re.sub(
        r"```(?:html|markdown|md|text|python)?",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = text.replace("```", "")

    # -----------------------------------------------------
    # Remove SVG links
    # -----------------------------------------------------

    text = re.sub(
        r"\[svg\]\([^)]+\)",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # -----------------------------------------------------
    # Find first Day 1
    # -----------------------------------------------------

    day_match = re.search(
        r"(?im)^\s*(?:#{1,6}\s*)?(?:\*\*)?\s*Day\s+1\b[^\n]*",
        text,
    )

    if not day_match:

        # Sometimes AI places Day 1 in the middle
        day_match = re.search(
            r"(?i)(?:#{1,6}\s*)?(?:\*\*)?\s*Day\s+1\b",
            text,
        )

    if not day_match:
        return ""

    # -----------------------------------------------------
    # Keep only from Day 1 onward
    # -----------------------------------------------------

    text = text[day_match.start():]

    # -----------------------------------------------------
    # Stop before verification / notes
    # -----------------------------------------------------

    stop_patterns = [
        r"(?im)^\s*\*?\*?Important Verification\s*:?.*$",
        r"(?im)^\s*\*?\*?Important Notes\s*:?.*$",
        r"(?im)^\s*⚠️\s*\*?\*?Important Notes\s*:?.*$",
        r"(?im)^\s*\*?\*?Verification\s*:?.*$",
    ]

    for pattern in stop_patterns:

        match = re.search(
            pattern,
            text,
        )

        if match:
            text = text[:match.start()]

    # -----------------------------------------------------
    # Strong cleanup
    # -----------------------------------------------------

    text = clean_ai_output(text)

    # -----------------------------------------------------
    # Remove localhost links again
    # -----------------------------------------------------

    text = re.sub(
        r"\[([^\]]*)\]\(\s*https?://localhost:[^)]+\)",
        r"\1",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\[svg\]\([^)]+\)",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # -----------------------------------------------------
    # Remove remaining HTML
    # -----------------------------------------------------

    text = re.sub(
        r"<[^>\n]+>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\\+<[^>\n]+>",
        "",
        text,
    )

    # -----------------------------------------------------
    # Remove excessive blank lines
    # -----------------------------------------------------

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


# =========================================================
# MAIN HERO
# =========================================================

render_html(
    """
    <div class="hero">
        <h1>✈️ TripWise AI</h1>
        <p>Your Smart Travel Planner</p>
    </div>
    """,
)

# =========================================================
# TRIP FORM
# =========================================================

render_html(
    """
    <div class="form-shell">
        <div class="section-heading">🧭 <span>Plan Your Journey</span></div>
        <div class="section-subtitle">Tell us your travel preferences and we'll create the perfect plan for you.</div>
    </div>
    """,
)

# Starting point + destination
col1, col2 = st.columns(2, gap="large")

with col1:
    render_html('<div class="field-card blue"><div class="field-head"><span>📍</span>Starting Point</div></div>')
    origin = st.text_input("Starting point", placeholder="e.g. Lahore", label_visibility="collapsed")

with col2:
    render_html('<div class="field-card purple"><div class="field-head"><span>📍</span>Destination</div></div>')
    destination = st.text_input("Destination", placeholder="e.g. Murree", label_visibility="collapsed")

# Duration + travelers + budget + transport
c1, c2, c3, c4 = st.columns(4, gap="medium")

with c1:
    render_html('<div class="field-card green"><div class="field-head"><span>📅</span>Trip Duration (Days)</div></div>')
    days_input = st.number_input("Trip duration", min_value=1, max_value=30, value=3, step=1, label_visibility="collapsed")

with c2:
    render_html('<div class="field-card orange"><div class="field-head"><span>👥</span>Travelers</div></div>')
    travelers_input = st.number_input("Travelers", min_value=1, max_value=20, value=2, step=1, label_visibility="collapsed")

with c3:
    render_html('<div class="field-card pink"><div class="field-head"><span>💰</span>Total Budget (PKR)</div></div>')
    budget_input = st.number_input("Total budget (PKR)", min_value=1000, max_value=10000000, value=25000, step=1000, label_visibility="collapsed")

with c4:
    render_html('<div class="field-card cyan"><div class="field-head"><span>🚗</span>Preferred Transport</div></div>')
    transport_input = st.selectbox("Preferred transport", ["Public transport", "Private car", "Rental car", "Any"], label_visibility="collapsed")

# Interests
render_html(
    """
    <div class="interest-box">
        <div class="interest-title">❤️ Your Interests</div>
        <div class="interest-sub">Select what you want from the trip</div>
    </div>
    """,
)

interests_input = st.multiselect(
    "Select what you want from the trip",
    ["Nature", "Sightseeing", "Peaceful places", "Adventure", "Food", "Historical places", "Shopping", "Photography"],
    default=["Nature", "Sightseeing", "Peaceful places"],
    label_visibility="collapsed",
)

render_html("<div style='height:12px'></div>")

plan_button = st.button("🚀 Create My Trip Plan", type="primary", use_container_width=True)

# =========================================================
# WORKFLOW EXECUTION
# =========================================================

if plan_button:

    if not origin.strip():

        st.error(
            "Please enter your starting location."
        )

    elif not destination.strip():

        st.error(
            "Please enter your destination."
        )

    elif not interests_input:

        st.error(
            "Please select at least one interest."
        )

    else:

        user_request = f"""
I want to travel from {origin} to {destination}

for {days_input} days.

Total budget: {budget_input} PKR.

Number of travelers: {travelers_input}.

My interests are:

{", ".join(interests_input)}.

Preferred transport:

{transport_input.lower()}.
"""

        with st.spinner(
            "✈️ TripWise AI is researching your trip..."
        ):

            try:

                workflow = build_workflow()

                result = workflow.invoke(
                    {
                        "user_request": user_request
                    }
                )

                st.session_state["trip_result"] = result
                st.session_state["trip_created"] = True

            except Exception as error:

                st.error(
                    "Something went wrong while creating your trip."
                )

                st.exception(error)


# =========================================================
# RESULTS DASHBOARD
# =========================================================

if "trip_result" in st.session_state:

    result = st.session_state["trip_result"]

    st.success(
        "✅ Trip plan created successfully!"
    )


    # =====================================================
    # GET DATA
    # =====================================================

    trip = result.get("trip")

    budget_data = result.get(
        "budget",
        {},
    )

    research_data = result.get(
        "research",
        {},
    )

    final_itinerary = result.get(
        "final_itinerary",
        "",
    )


    # =====================================================
    # SAFETY CHECK
    # =====================================================

    if trip is None:

        st.error(
            "Trip information was not returned by the workflow."
        )

        st.stop()


    # =====================================================
    # TRIP VALUES
    # =====================================================

    origin_value = get_value(
        trip,
        "origin",
        origin,
    )

    destination_value = get_value(
        trip,
        "destination",
        destination,
    )

    days_value = get_value(
        trip,
        "days",
        days_input,
    )

    travelers_value = get_value(
        trip,
        "travelers",
        travelers_input,
    )

    budget_value = get_value(
        trip,
        "budget",
        budget_input,
    )

    transport_value = get_value(
        trip,
        "transport_preference",
        transport_input,
    )

    trip_interests = get_value(
        trip,
        "interests",
        interests_input,
    )


    budget_number = safe_float(
        budget_value,
        budget_input,
    )

    days_number = max(
        safe_int(
            days_value,
            days_input,
        ),
        1,
    )

    travelers_number = max(
        safe_int(
            travelers_value,
            travelers_input,
        ),
        1,
    )


    # =====================================================
    # RESULT HERO
    # =====================================================

    st.markdown("---")

    render_html(
        f"""
        <div class="hero">

            <h1>
                📍 {html.escape(str(origin_value))}
                →
                {html.escape(str(destination_value))}
            </h1>

            <p>
                {days_number} days ·
                {travelers_number} travelers ·
                {format_pkr(budget_number)}
            </p>

        </div>
        """,
    )


    # =====================================================
    # TRIP OVERVIEW
    # =====================================================

    render_html(
        '<div class="section-title">📊 Trip Overview</div>',
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "👥 Travelers",
            travelers_number,
        )


    with c2:

        st.metric(
            "📅 Duration",
            f"{days_number} Days",
        )


    with c3:

        st.metric(
            "💰 Total Budget",
            format_pkr(budget_number),
        )


    with c4:

        st.metric(
            "🚌 Transport",
            str(transport_value).title(),
        )


    # =====================================================
    # BUDGET OVERVIEW
    # =====================================================

    render_html(
        '<div class="section-title">💰 Budget Overview</div>',
    )


    if not isinstance(
        budget_data,
        dict,
    ):
        budget_data = {}


    default_per_person = (
        budget_number / travelers_number
    )

    default_per_day = (
        budget_number / days_number
    )

    default_per_person_day = (
        budget_number
        / travelers_number
        / days_number
    )


    budget_per_person = safe_float(
        budget_data.get(
            "budget_per_person",
            default_per_person,
        ),
        default_per_person,
    )


    budget_per_day = safe_float(
        budget_data.get(
            "budget_per_day",
            default_per_day,
        ),
        default_per_day,
    )


    budget_per_person_per_day = safe_float(
        budget_data.get(
            "budget_per_person_per_day",
            default_per_person_day,
        ),
        default_per_person_day,
    )


    b1, b2, b3 = st.columns(3)


    with b1:

        render_html(
            f"""
            <div class="info-card">

                <div class="info-label">
                    Budget Per Person
                </div>

                <div class="info-value">
                    {format_pkr(budget_per_person)}
                </div>

            </div>
            """,
                )


    with b2:

        render_html(
            f"""
            <div class="info-card">

                <div class="info-label">
                    Budget Per Day
                </div>

                <div class="info-value">
                    {format_pkr(budget_per_day)}
                </div>

            </div>
            """,
                )


    with b3:

        render_html(
            f"""
            <div class="info-card">

                <div class="info-label">
                    Per Person / Day
                </div>

                <div class="info-value">
                    {format_pkr(budget_per_person_per_day)}
                </div>

            </div>
            """,
                )


    # =====================================================
    # INTERESTS
    # =====================================================

    render_html(
        '<div class="section-title">❤️ Your Interests</div>',
    )


    if trip_interests:

        if isinstance(
            trip_interests,
            (list, tuple),
        ):

            interest_text = " · ".join(
                str(item).title()
                for item in trip_interests
            )

        else:

            interest_text = str(
                trip_interests
            )

        st.info(
            f"Trip personalized around: {interest_text}"
        )


    # =====================================================
    # DESTINATION
    # =====================================================

    location_data = get_research_value(
        research_data,
        "location",
        {},
    )


    if location_data:

        render_html(
            '<div class="section-title">📍 Destination</div>',
                )


        location_name = get_research_value(
            location_data,
            "name",
            destination_value,
        )


        country_name = get_research_value(
            location_data,
            "country",
            "Pakistan",
        )


        latitude = get_research_value(
            location_data,
            "latitude",
            None,
        )


        longitude = get_research_value(
            location_data,
            "longitude",
            None,
        )


        location_cols = st.columns(3)


        with location_cols[0]:

            st.metric(
                "Destination",
                location_name,
            )


        with location_cols[1]:

            st.metric(
                "Country",
                country_name,
            )


        with location_cols[2]:

            if (
                latitude is not None
                and longitude is not None
            ):

                st.metric(
                    "Coordinates",
                    f"{safe_float(latitude):.4f}, "
                    f"{safe_float(longitude):.4f}",
                )


    # =====================================================
    # WEATHER
    # =====================================================

    render_html(
        '<div class="section-title">🌦️ Weather Forecast</div>',
    )


    weather_data = get_research_value(
        research_data,
        "weather",
        {},
    )


    daily = get_research_value(
        weather_data,
        "daily",
        {},
    )


    if isinstance(
        daily,
        dict,
    ):

        weather_dates = daily.get(
            "time",
            [],
        )

        max_temps = daily.get(
            "temperature_2m_max",
            [],
        )

        min_temps = daily.get(
            "temperature_2m_min",
            [],
        )

        rain_probability = daily.get(
            "precipitation_probability_max",
            [],
        )


        if weather_dates:

            weather_cols = st.columns(
                min(
                    len(weather_dates),
                    4,
                )
            )


            for index, date in enumerate(
                weather_dates
            ):

                if index >= len(weather_cols):
                    break


                max_temp = (
                    max_temps[index]
                    if index < len(max_temps)
                    else "N/A"
                )


                min_temp = (
                    min_temps[index]
                    if index < len(min_temps)
                    else "N/A"
                )


                rain = (
                    rain_probability[index]
                    if index < len(rain_probability)
                    else "N/A"
                )


                with weather_cols[index]:

                    render_html(
                        f"""
                        <div class="info-card">

                            <div class="info-label">
                                📅 {date}
                            </div>

                            <div class="info-value">
                                🌡️ {max_temp}°C
                                / {min_temp}°C
                            </div>

                            <div style="
                                margin-top:8px;
                                color:#64748b;
                            ">
                                🌧️ Rain chance: {rain}%
                            </div>

                        </div>
                        """,
                                        )

        else:

            st.info(
                "Weather data is not available."
            )

    else:

        st.info(
            "Weather data is not available."
        )


    # =====================================================
    # PLACES FOUND
    # =====================================================

    places_data = normalize_places(
        get_research_value(
            research_data,
            "places",
            [],
        )
    )


    render_html(
        '<div class="section-title">📍 Places Found</div>',
    )


    if places_data:

        display_places = places_data[:12]

        place_cols = st.columns(3)


        for index, place in enumerate(
            display_places
        ):

            place_name = get_value(
                place,
                "name",
                "Unknown place",
            )


            place_type = get_value(
                place,
                "type",
                "Place",
            )


            place_lat = get_value(
                place,
                "latitude",
                None,
            )


            place_lon = get_value(
                place,
                "longitude",
                None,
            )


            coordinates = ""


            if (
                place_lat is not None
                and place_lon is not None
            ):

                coordinates = (
                    f"{safe_float(place_lat):.4f}, "
                    f"{safe_float(place_lon):.4f}"
                )


            with place_cols[index % 3]:

                render_html(
                    f"""
                    <div class="place-card">

                        <div class="info-label">
                            📍 {html.escape(
                                str(place_type)
                                .replace("_", " ")
                                .title()
                            )}
                        </div>

                        <div class="info-value">
                            {html.escape(str(place_name))}
                        </div>

                        <div style="
                            margin-top:8px;
                            color:#64748b;
                            font-size:0.85rem;
                        ">
                            {coordinates}
                        </div>

                    </div>
                    """,
                                )

    else:

        st.info(
            "No places were found."
        )


    # =====================================================
    # ITINERARY
    # =====================================================

    render_html(
        '<div class="section-title">🗺️ Your Personalized Itinerary</div>',
    )


    cleaned_itinerary = extract_itinerary(
        final_itinerary
    )


    if not cleaned_itinerary:

        st.warning(
            "No itinerary was returned."
        )

    else:

        # -------------------------------------------------
        # Split by Day headings
        # -------------------------------------------------

        day_pattern = (
            r"(?im)"
            r"(?=^\s*(?:#{1,6}\s*)?"
            r"(?:\*\*)?\s*Day\s+\d+\b)"
        )


        day_sections = re.split(
            day_pattern,
            cleaned_itinerary,
        )


        day_sections = [
            section.strip()
            for section in day_sections
            if section.strip()
        ]


        # -------------------------------------------------
        # Display days
        # -------------------------------------------------

        displayed_days = 0


        for day_content in day_sections:

            day_match = re.search(
                r"(?i)Day\s+(\d+)",
                day_content,
            )


            if not day_match:
                continue


            day_number = int(
                day_match.group(1)
            )


            # Don't show days beyond user's request

            if day_number > days_number:
                continue


            # -------------------------------------------------
            # Remove Day heading
            # -------------------------------------------------

            clean_content = re.sub(
                r"^\s*(?:#{1,6}\s*)?"
                r"(?:\*\*)?\s*Day\s+\d+\b"
                r"(?:\*\*)?\s*:?[^\n]*\n?",
                "",
                day_content,
                count=1,
                flags=re.IGNORECASE,
            ).strip()


            # -------------------------------------------------
            # Remove localhost / SVG
            # -------------------------------------------------

            clean_content = re.sub(
                r"\[svg\]\([^)]+\)",
                "",
                clean_content,
                flags=re.IGNORECASE,
            )


            clean_content = re.sub(
                r"\[([^\]]*)\]\(\s*https?://localhost:[^)]+\)",
                r"\1",
                clean_content,
                flags=re.IGNORECASE,
            )


            # -------------------------------------------------
            # Final cleanup
            # -------------------------------------------------

            clean_content = clean_ai_output(
                clean_content
            )


            if not clean_content:
                continue


            displayed_days += 1


            # -------------------------------------------------
            # Day container
            # -------------------------------------------------

            with st.container(border=True):

                st.markdown(
                    f"### 🗓️ Day {day_number}"
                )

                st.markdown(
                    clean_content,
                    unsafe_allow_html=False,
                )


        if displayed_days == 0:

            st.warning(
                "No readable itinerary days were returned."
            )


    # =====================================================
    # IMPORTANT NOTES
    # =====================================================

    render_html(
        '<div class="section-title">⚠️ Important Notes</div>',
    )


    verification_items = [

        "Confirm transport schedule and fare before travelling.",

        "Check the latest weather before outdoor activities.",

        "Confirm hotel or guest house availability and price.",

        "Check attraction opening hours and entry fees.",

        "Keep some extra money for unexpected expenses.",

    ]


    for item in verification_items:

        st.markdown(
            f"- {item}"
        )


    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    render_html(
        "<br>",
    )


    action_col1, action_col2 = st.columns(2)


    with action_col1:

        if st.button(
            "🔄 Plan Another Trip",
            use_container_width=True,
        ):

            st.session_state.pop(
                "trip_result",
                None,
            )

            st.session_state.pop(
                "trip_created",
                None,
            )

            st.rerun()


    with action_col2:

        if st.button(
            "⬆️ Back to Trip Form",
            use_container_width=True,
        ):

            st.session_state.pop(
                "trip_result",
                None,
            )

            st.session_state.pop(
                "trip_created",
                None,
            )

            st.rerun()


# =========================================================
# FOOTER
# =========================================================

render_html(
    """
    <div class="footer">

        TripWise AI · Intelligent travel planning powered by AI

        <br>

        Always verify live prices, schedules,
        weather and local conditions before travelling.

    </div>
    """,
)