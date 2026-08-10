import streamlit as st
import requests
import re
import base64

API_URL = "https://trustlens-j0su.onrender.com"

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TrustLens | Digital Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(59, 130, 246, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(139, 92, 246, 0.10),
                transparent 30%
            ),
            #07111f;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* ---------- HEADER ---------- */

    .brand {
        text-align: center;
        margin-top: 15px;
    }

    .brand-icon {
        font-size: 52px;
        margin-bottom: 5px;
    }

    .brand-title {
        font-size: 48px;
        font-weight: 800;
        letter-spacing: -2px;
        color: #ffffff;
        margin: 0;
    }

    .brand-title span {
        color: #60a5fa;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 18px;
        margin-top: 8px;
    }

    .hero-text {
        text-align: center;
        color: #cbd5e1;
        font-size: 16px;
        max-width: 700px;
        margin: 18px auto 35px auto;
        line-height: 1.6;
    }

    /* ---------- CARDS ---------- */

    .feature-card {
        background: rgba(15, 30, 50, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 18px;
        padding: 26px;
        min-height: 230px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.22);
        transition: 0.2s ease;
    }

    .feature-card:hover {
        border-color: rgba(96, 165, 250, 0.45);
        transform: translateY(-2px);
    }

    .feature-icon {
        font-size: 34px;
        margin-bottom: 8px;
    }

    .feature-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 7px;
    }

    .feature-description {
        color: #94a3b8;
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 18px;
    }

    /* ---------- ANALYSIS CARD ---------- */

    .analysis-card {
        background: rgba(15, 30, 50, 0.9);
        border: 1px solid rgba(96, 165, 250, 0.20);
        border-radius: 20px;
        padding: 28px;
        margin-top: 30px;
        box-shadow: 0 15px 45px rgba(0,0,0,0.25);
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #94a3b8;
        margin-bottom: 22px;
    }

    /* ---------- TRUST SCORE ---------- */

    .score-box {
        text-align: center;
        padding: 18px;
        border-radius: 15px;
        background: rgba(2, 8, 23, 0.45);
        border: 1px solid rgba(148,163,184,0.12);
    }

    .score-number {
        font-size: 42px;
        font-weight: 800;
        color: #ffffff;
    }

    .score-label {
        color: #94a3b8;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ---------- INFO STRIP ---------- */

    .info-card {
        background: rgba(15, 30, 50, 0.72);
        border: 1px solid rgba(148,163,184,0.13);
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        min-height: 150px;
    }

    .info-icon {
        font-size: 30px;
    }

    .info-title {
        color: #ffffff;
        font-weight: 700;
        margin-top: 8px;
    }

    .info-text {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 5px;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid rgba(148,163,184,0.10);
    }

    /* ---------- STREAMLIT BUTTONS ---------- */

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid rgba(96,165,250,0.35);
        background: linear-gradient(
            135deg,
            #2563eb,
            #4f46e5
        );
        color: white;
        font-weight: 700;
        min-height: 44px;
    }

    div.stButton > button:hover {
        border-color: #93c5fd;
        color: white;
    }

    /* ---------- INPUT ---------- */

    div[data-baseweb="input"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">🛡️</div>
        <div class="brand-title">
            Trust<span>Lens</span>
        </div>
        <div class="brand-subtitle">
            Your AI-powered digital safety companion
        </div>
    </div>

    <div class="hero-text">
        Detect suspicious links, messages and QR codes
        before they put your personal information at risk.
        TrustLens combines machine learning with security
        intelligence to help you make safer decisions online.
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FEATURE CARDS
# =========================================================

col1, col2, col3 = st.columns(3, gap="large")

# ---------------------------------------------------------
# LINK CARD
# ---------------------------------------------------------

with col1:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔗</div>
            <div class="feature-title">Scan a Link</div>
            <div class="feature-description">
                Check a suspicious website URL for phishing,
                unsafe domains and security risks.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    link_url = st.text_input(
        "Website URL",
        placeholder="https://example.com",
        key="link_input",
        label_visibility="collapsed"
    )

    analyze_link = st.button(
        "🔍 Analyze Link",
        key="analyze_link",
        use_container_width=True
    )

# ---------------------------------------------------------
# MESSAGE CARD
# ---------------------------------------------------------

with col2:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-title">Check a Message</div>
            <div class="feature-description">
                Paste a suspicious SMS, email or chat message
                and find links that may be unsafe.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    message = st.text_area(
        "Message",
        placeholder="Paste a suspicious message here...",
        key="message_input",
        height=100,
        label_visibility="collapsed"
    )

    check_message = st.button(
        "💬 Check Message",
        key="check_message",
        use_container_width=True
    )

# ---------------------------------------------------------
# QR CARD
# ---------------------------------------------------------

with col3:

    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📷</div>
            <div class="feature-title">Scan QR Code</div>
            <div class="feature-description">
                Upload a QR-code image and inspect the
                destination before opening it.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    qr_file = st.file_uploader(
        "Upload QR image",
        type=["png", "jpg", "jpeg"],
        key="qr_upload",
        label_visibility="collapsed"
    )

    scan_qr = st.button(
        "📷 Scan QR Code",
        key="scan_qr",
        use_container_width=True
    )

# =========================================================
# LINK ANALYSIS
# =========================================================

if analyze_link:

    if not link_url.strip():

        st.warning("Please enter a website URL.")
        st.stop()

    try:

        with st.spinner("🔎 Analyzing URL..."):

            response = requests.post(
    f"{API_URL}/analyze",
    json={"url": link_url.strip()},
    timeout=30
)

        if response.status_code != 200:

            st.error(
                f"Backend error: {response.status_code}"
            )
            st.stop()

        result = response.json()

        st.markdown(
            '<div class="analysis-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">🔎 Analysis Result</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-subtitle">'
            'TrustLens security assessment'
            '</div>',
            unsafe_allow_html=True
        )

        st.code(
            result.get("url", link_url),
            language=None
        )

        # -----------------------------
        # Risk + Score
        # -----------------------------

        risk = result.get("risk", "Unknown")
        score = result.get("trust_score", 0)

        result_col1, result_col2 = st.columns(2)

        with result_col1:

            if risk == "High":

                st.error("🔴 HIGH RISK")

            elif risk == "Medium":

                st.warning("🟠 MEDIUM RISK")

            else:

                st.success("🟢 LOW RISK")

        with result_col2:

            st.markdown(
                f"""
                <div class="score-box">
                    <div class="score-label">
                        Trust Score
                    </div>
                    <div class="score-number">
                        {score}/100
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.progress(
            max(0, min(score, 100)) / 100
        )

        # -----------------------------
        # ML
        # -----------------------------

        st.markdown("### 🤖 AI / ML Assessment")

        ml1, ml2 = st.columns(2)

        prediction = result.get(
            "ml_prediction",
            "Not available"
        )

        probability = result.get(
            "ml_phishing_probability",
            0
        )

        with ml1:

            if prediction == "Phishing":

                st.error(
                    f"🚨 ML Model: {prediction}"
                )

            else:

                st.success(
                    f"✅ ML Model: {prediction}"
                )

        with ml2:

            st.metric(
                "🎯 Phishing Probability",
                f"{probability}%"
            )

        # -----------------------------
        # Security findings
        # -----------------------------

        st.markdown("### ⚠️ Security Findings")

        reasons = result.get(
            "reasons",
            []
        )

        if reasons:

            for reason in reasons:

                st.warning(
                    f"⚠️ {reason}"
                )

        else:

            st.success(
                "✅ No major security issues detected."
            )

        # -----------------------------
        # Final recommendation
        # -----------------------------

        st.markdown("### 💡 TrustLens Recommendation")

        if risk == "High":

            st.error(
                "Avoid entering passwords, payment details "
                "or other sensitive information on this website."
            )

        elif risk == "Medium":

            st.warning(
                "Proceed carefully and verify the website "
                "before sharing sensitive information."
            )

        else:

            st.success(
                "No major security indicators were detected. "
                "Continue using normal online safety practices."
            )

        st.markdown("</div>", unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ TrustLens backend is not running."
        )

        st.info(
            "Start FastAPI with: "
            "`uvicorn backend.main:app --reload`"
        )

    except requests.exceptions.Timeout:

        st.error(
            "⏱️ The analysis request timed out."
        )

    except Exception as e:

        st.error(
            f"Unexpected error: {e}"
        )

# =========================================================
# MESSAGE ANALYSIS
# =========================================================

if check_message:

    if not message.strip():

        st.warning("Please paste a message first.")
        st.stop()

    urls = re.findall(
        r'https?://[^\s]+',
        message
    )

    st.markdown("### 💬 Message Analysis")

    if not urls:

        st.info(
            "No HTTP/HTTPS links were detected in this message."
        )

    else:

        st.write(
            f"🔎 Found **{len(urls)} link(s)** in the message."
        )

        for found_url in urls:

            clean_url = found_url.rstrip(
                ".,!?;:)"
            )

            try:

                response = requests.post(
    f"{API_URL}/analyze",
    json={"url": clean_url},
    timeout=30
)

                if response.status_code == 200:

                    result = response.json()

                    risk = result.get(
                        "risk",
                        "Unknown"
                    )

                    score = result.get(
                        "trust_score",
                        0
                    )

                    if risk == "High":

                        st.error(
                            f"🔴 High Risk — {clean_url}"
                        )

                    elif risk == "Medium":

                        st.warning(
                            f"🟠 Medium Risk — {clean_url}"
                        )

                    else:

                        st.success(
                            f"🟢 Low Risk — {clean_url}"
                        )

                    st.write(
                        f"Trust Score: **{score}/100**"
                    )

            except Exception:

                st.error(
                    f"Could not analyze {clean_url}"
                )

# =========================================================
# QR CODE
# =========================================================

if scan_qr:

    if qr_file is None:

        st.warning(
            "Please upload a QR-code image first."
        )

    else:

        st.info(
            "📷 QR upload interface is ready. "
            "QR decoding will be connected next."
        )

        st.image(
            qr_file,
            caption="Uploaded QR Code",
            width=250
        )

# =========================================================
# HOW TRUSTLENS WORKS
# =========================================================

st.markdown("## 🛡️ How TrustLens Protects You")

info1, info2, info3, info4 = st.columns(4)

with info1:

    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">🔎</div>
            <div class="info-title">Detect</div>
            <div class="info-text">
                Identify suspicious URL characteristics
                and security signals.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with info2:

    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">🤖</div>
            <div class="info-title">Analyze</div>
            <div class="info-text">
                Use machine learning to identify
                phishing patterns.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with info3:

    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">🛡️</div>
            <div class="info-title">Assess</div>
            <div class="info-text">
                Combine AI predictions with
                deterministic security rules.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with info4:

    st.markdown(
        """
        <div class="info-card">
            <div class="info-icon">⚠️</div>
            <div class="info-title">Protect</div>
            <div class="info-text">
                Explain the risk and help users
                make safer decisions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🛡️ TrustLens &nbsp;•&nbsp;
        AI-assisted digital safety platform
        <br><br>
        Stay alert. Verify before you click.
    </div>
    """,
    unsafe_allow_html=True
)