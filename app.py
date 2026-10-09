import os
import re
import time
import subprocess
import importlib
from pathlib import Path
import streamlit as st
import downloader

# Ensure downloader module is reloaded
importlib.reload(downloader)

# Page Configuration
st.set_page_config(
    page_title="YouTube Medya İndirici",
    page_icon="📥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom High-End Cinematic Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Typography & Deep Cinematic Atmosphere */
    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #F1F5F9;
    }

    /* Preserve Icon Fonts & Prevent Overlapping Ligatures */
    [data-testid="stIconMaterial"], 
    .material-symbols-rounded, 
    .material-icons, 
    [class*="material-symbols"], 
    [data-testid="stExpanderToggleIcon"],
    summary svg,
    summary span[class*="st-"] {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        font-style: normal !important;
        font-weight: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
    }
    
    .stApp {
        background: 
            radial-gradient(ellipse 90% 50% at 50% -15%, rgba(239, 68, 68, 0.12), transparent),
            radial-gradient(circle at 100% 90%, rgba(99, 102, 241, 0.07), transparent 45%),
            radial-gradient(circle at 0% 50%, rgba(16, 185, 129, 0.04), transparent 40%),
            linear-gradient(180deg, #07090e 0%, #0a0d16 50%, #07090e 100%) !important;
        background-attachment: fixed !important;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.025em;
        color: #FFFFFF !important;
    }

    /* Main Container Spacing */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 4rem;
        max-width: 820px;
    }

    /* Cinematic Hero Container */
    .hero-container {
        text-align: center;
        padding: 2.2rem 1.8rem 2rem 1.8rem;
        background: radial-gradient(circle at 50% 0%, rgba(255, 30, 68, 0.16) 0%, rgba(15, 20, 32, 0.85) 80%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        margin-bottom: 1.8rem;
        box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(18px);
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 30, 68, 0.12);
        color: #FF5A79;
        border: 1px solid rgba(255, 30, 68, 0.3);
        padding: 6px 16px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        box-shadow: 0 0 20px rgba(255, 30, 68, 0.2);
    }

    .hero-badge::before {
        content: "";
        width: 7px;
        height: 7px;
        background: #FF3366;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #FF3366;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 30%, #FFA8B6 70%, #FF1E44 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.6rem;
        line-height: 1.15;
    }

    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        font-weight: 400;
        line-height: 1.5;
        max-width: 580px;
        margin: 0 auto;
    }

    /* Soft-Edged Modern Input Styling */
    div[data-testid="stTextInput"] input {
        border-radius: 16px !important;
        background: rgba(14, 19, 31, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #F8FAFC !important;
        padding: 0.85rem 1.2rem !important;
        font-size: 0.98rem !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.25s ease !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #FF2A55 !important;
        box-shadow: 0 0 0 3px rgba(255, 42, 85, 0.22), inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        background: rgba(18, 24, 38, 0.95) !important;
    }

    div[data-testid="stTextInput"] label {
        font-weight: 600 !important;
        color: #E2E8F0 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.4rem !important;
    }

    /* Soft Rounded Action Buttons */
    div.stButton > button {
        border-radius: 16px !important;
        font-weight: 600 !important;
        font-size: 0.96rem !important;
        padding: 0.72rem 1.4rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: #E2E8F0 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25) !important;
    }

    div.stButton > button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.22) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.35) !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FF1E44 0%, #E1062B 55%, #A7001E 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 8px 25px -4px rgba(255, 30, 68, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    }

    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 12px 32px -4px rgba(255, 30, 68, 0.65) !important;
        transform: translateY(-2px) scale(1.005) !important;
    }

    /* Custom Border Containers (Cards) */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.video-preview-anchor) {
        background: linear-gradient(160deg, rgba(20, 26, 42, 0.75) 0%, rgba(11, 15, 25, 0.85) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        border-radius: 24px !important;
        box-shadow: 0 18px 40px -10px rgba(0, 0, 0, 0.65) !important;
        padding: 1.4rem !important;
        backdrop-filter: blur(18px) !important;
        margin-top: 0.8rem !important;
        margin-bottom: 1.2rem !important;
    }

    /* === DEDICATED SUCCESS CARD CONTAINER === */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.success-card-anchor) {
        background: linear-gradient(165deg, rgba(14, 25, 35, 0.92) 0%, rgba(8, 14, 23, 0.98) 100%) !important;
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
        border-radius: 26px !important;
        box-shadow: 0 25px 55px -12px rgba(0, 0, 0, 0.85), 0 0 35px -5px rgba(16, 185, 129, 0.22) !important;
        padding: 1.8rem 1.6rem !important;
        backdrop-filter: blur(22px) !important;
        margin-top: 1.4rem !important;
        margin-bottom: 1.6rem !important;
        animation: fadeInCard 0.4s ease-out forwards;
    }

    @keyframes fadeInCard {
        from {
            opacity: 0;
            transform: translateY(10px) scale(0.98);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    /* Success Card Header Badge */
    .success-header-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 6px 15px;
        border-radius: 999px;
        font-size: 0.84rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.9rem;
    }

    .success-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.3;
        margin-bottom: 0.4rem;
    }

    /* THE GREEN DOWNLOAD BUTTON */
    div[data-testid="stDownloadButton"] > button {
        width: 100% !important;
        background: linear-gradient(135deg, #10B981 0%, #059669 60%, #047857 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        padding: 0.95rem 1.6rem !important;
        border-radius: 18px !important;
        box-shadow: 0 10px 30px -4px rgba(16, 185, 129, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-top: 0.6rem !important;
        margin-bottom: 1rem !important;
    }

    div[data-testid="stDownloadButton"] > button:hover {
        background: linear-gradient(135deg, #34D399 0%, #10B981 60%, #059669 100%) !important;
        box-shadow: 0 14px 38px -4px rgba(16, 185, 129, 0.65) !important;
        transform: translateY(-2px) !important;
        color: #FFFFFF !important;
    }

    /* Player Container Sub-card */
    .player-subcard {
        background: rgba(0, 0, 0, 0.35);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 18px;
        padding: 1.1rem;
        margin-top: 0.6rem;
        margin-bottom: 1rem;
    }

    .player-label {
        font-size: 0.88rem;
        font-weight: 600;
        color: #CBD5E1;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Audio / Video Elements Customization */
    audio {
        width: 100% !important;
        border-radius: 14px !important;
        outline: none !important;
        filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.3));
    }

    video {
        width: 100% !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4) !important;
    }

    /* File Path Sub-box */
    .filepath-box {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 0.9rem 1.1rem;
        margin-top: 0.5rem;
    }

    .filepath-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #94A3B8;
        word-break: break-all;
        line-height: 1.4;
    }

    /* Badges */
    .badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.09);
        color: #E2E8F0;
        padding: 5px 12px;
        border-radius: 10px;
        font-size: 0.82rem;
        font-weight: 500;
    }

    .badge-emerald {
        background: rgba(16, 185, 129, 0.12) !important;
        border-color: rgba(16, 185, 129, 0.3) !important;
        color: #6EE7B7 !important;
        font-weight: 600 !important;
    }

    /* Radio Group (Format selector) */
    div[data-testid="stRadio"] > label {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        margin-bottom: 0.6rem !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 10px !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.09) !important;
        padding: 14px 18px !important;
        border-radius: 16px !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
    }

    /* Force all text inside radio labels to be bright white */
    div[data-testid="stRadio"] div[role="radiogroup"] > label p,
    div[data-testid="stRadio"] div[role="radiogroup"] > label span,
    div[data-testid="stRadio"] div[role="radiogroup"] > label div {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        font-size: 0.98rem !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(255, 30, 68, 0.08) !important;
        border-color: rgba(255, 30, 68, 0.45) !important;
        transform: translateY(-1px);
    }

    /* Highlight Active/Selected Radio Option */
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, rgba(255, 30, 68, 0.16) 0%, rgba(22, 28, 44, 0.85) 100%) !important;
        border-color: rgba(255, 30, 68, 0.6) !important;
        box-shadow: 0 0 20px rgba(255, 30, 68, 0.22) !important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Streamlit Alert Boxes (st.info, st.warning, st.success, st.error) */
    div[data-testid="stAlert"] {
        border-radius: 18px !important;
        backdrop-filter: blur(14px) !important;
        padding: 1.1rem 1.3rem !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.9rem !important;
        background: linear-gradient(135deg, rgba(14, 30, 58, 0.92) 0%, rgba(9, 18, 36, 0.96) 100%) !important;
        border: 1px solid rgba(59, 130, 246, 0.4) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45), 0 0 15px rgba(59, 130, 246, 0.15) !important;
    }

    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] div,
    div[data-testid="stAlert"] span {
        color: #E0F2FE !important;
        font-size: 0.96rem !important;
        line-height: 1.55 !important;
    }

    div[data-testid="stAlert"] strong {
        color: #93C5FD !important;
        font-weight: 700 !important;
    }

    div[data-testid="stAlert"] svg,
    div[data-testid="stAlert"] [data-testid="stIconMaterial"] {
        color: #60A5FA !important;
        filter: drop-shadow(0 0 6px rgba(96, 165, 250, 0.6)) !important;
    }

    /* Checkbox Styling */
    div[data-testid="stCheckbox"] {
        margin-top: 0.6rem !important;
        margin-bottom: 0.6rem !important;
    }

    div[data-testid="stCheckbox"] label span p {
        font-size: 0.98rem !important;
        font-weight: 600 !important;
        color: #F8FAFC !important;
    }

    /* Section Cut Sub-card */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.section-cut-card-anchor) {
        background: rgba(14, 20, 32, 0.75) !important;
        border: 1px dashed rgba(255, 30, 68, 0.45) !important;
        border-radius: 18px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
    }

    /* Metrics Box */
    .metrics-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.035);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 12px 10px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
    }

    .metric-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    .metric-label {
        font-size: 0.74rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 2px;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF1E44, #FF758C, #10B981) !important;
        border-radius: 999px !important;
    }

    /* History Item Cards */
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.history-item-anchor) {
        background: rgba(14, 20, 32, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px !important;
        padding: 0.9rem 1.2rem !important;
        margin-bottom: 0.6rem !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.25s ease !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.history-item-anchor):hover {
        background: rgba(18, 26, 42, 0.9) !important;
        border-color: rgba(255, 255, 255, 0.16) !important;
        transform: translateY(-1px) !important;
    }

    /* Expander Safeguard Styling */
    details[data-testid="stExpander"] {
        background: rgba(14, 20, 32, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
        margin-bottom: 0.8rem !important;
        overflow: hidden !important;
    }

    details[data-testid="stExpander"] summary {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        padding: 0.85rem 1.2rem !important;
    }

    details[data-testid="stExpander"] summary svg,
    details[data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"] {
        flex-shrink: 0 !important;
        margin-right: 10px !important;
    }

    details[data-testid="stExpander"] summary p,
    details[data-testid="stExpander"] summary span {
        margin: 0 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #F1F5F9 !important;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        color: #64748B;
        font-size: 0.85rem;
        margin-top: 3.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        padding-top: 1.5rem;
    }

    /* Hide standard Streamlit header and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "video_info" not in st.session_state:
    st.session_state.video_info = None
if "current_url" not in st.session_state:
    st.session_state.current_url = ""
if "download_result" not in st.session_state:
    st.session_state.download_result = None
if "history" not in st.session_state:
    st.session_state.history = []

# Hero Header
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">yt-dlp & FFmpeg Entegre</div>
    <div class="hero-title">YouTube Medya İndirici</div>
    <div class="hero-subtitle">En yüksek kalitede stüdyo sesleri (320 kbps MP3) ve kristal netliğinde videolar (MP4) saniyeler içinde hazır.</div>
</div>
""", unsafe_allow_html=True)

# URL Input Section
url_input_col, btn_col = st.columns([4, 1.2], vertical_alignment="bottom")

with url_input_col:
    youtube_url = st.text_input(
        "YouTube Video veya Shorts Bağlantısı",
        value=st.session_state.current_url,
        placeholder="https://www.youtube.com/watch?v=... veya https://youtu.be/...",
        key="url_field",
        help="İndirmek istediğiniz YouTube linkini buraya yapıştırın."
    )

with btn_col:
    fetch_clicked = st.button("🔍 Getir", use_container_width=True, type="primary")

# Quick Action Buttons
col_sample, col_clear = st.columns([1, 1])
with col_sample:
    if st.button("🎲 Örnek Link Dene", use_container_width=True):
        st.session_state.current_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        st.session_state.video_info = None
        st.session_state.download_result = None
        st.rerun()
        
with col_clear:
    if st.button("🗑️ Temizle", use_container_width=True):
        st.session_state.current_url = ""
        st.session_state.video_info = None
        st.session_state.download_result = None
        st.rerun()

# Logic when URL is submitted or fetched
active_url = youtube_url.strip()

if (fetch_clicked or (active_url and active_url != st.session_state.current_url)) and active_url:
    st.session_state.current_url = active_url
    st.session_state.download_result = None
    
    if not ("youtube.com" in active_url or "youtu.be" in active_url):
        st.warning("⚠️ Lütfen geçerli bir YouTube veya Shorts bağlantısı girin.")
    else:
        with st.spinner("⏳ Video bilgileri taranıyor..."):
            try:
                info = downloader.get_video_info(active_url)
                st.session_state.video_info = info
            except Exception as e:
                st.session_state.video_info = None
                st.error(f"❌ Video bilgileri alınamadı: {str(e)}")

# Display Video Card & Download Options if Info Available
if st.session_state.video_info:
    info = st.session_state.video_info

    # Video Info Container
    with st.container(border=True):
        st.markdown('<div class="video-preview-anchor"></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([1.5, 2.5], vertical_alignment="top")
        with c1:
            if info.get('thumbnail'):
                st.image(info['thumbnail'], use_container_width=True)
        with c2:
            st.markdown(f"<div style='font-size:1.2rem; font-weight:700; color:#F8FAFC; line-height:1.35; margin-bottom:8px;'>{info['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:10px;">
                <span class="badge-pill">👤 {info['channel']}</span>
                <span class="badge-pill">⏱️ {info['duration_formatted']}</span>
                <span class="badge-pill">👁️ {info['views_formatted']}</span>
                <span class="badge-pill badge-emerald">🎬 {info['best_resolution']}</span>
            </div>
            """, unsafe_allow_html=True)

            if info.get('description'):
                st.caption(info['description'])

    # Format Option Selection
    st.markdown("<div style='margin-top:1.2rem; margin-bottom:0.4rem; font-size:1.05rem; font-weight:700;'>🎯 İndirme Formatını Belirleyin</div>", unsafe_allow_html=True)
    
    format_choice = st.radio(
        label="Format Seçeneği",
        options=[
            "Sadece Ses (En Yüksek Kalite MP3)",
            "Video (En Yüksek Kalite MP4)"
        ],
        index=0,
        label_visibility="collapsed",
        key="selected_format"
    )

    # Format Details Pill
    if format_choice == "Sadece Ses (En Yüksek Kalite MP3)":
        st.info("🎵 **Ses Modu:** En yüksek kalitedeki ses parçası ayıklanıp 320 kbps stüdyo kalitesinde MP3 formatına dönüştürülecektir.")
        mode_key = "audio"
    else:
        st.info(f"🎬 **Video Modu:** En yüksek çözünürlükteki görüntü ({info['best_resolution']}) ile kristal ses akışı MP4 formatında kayıpsız birleştirilecektir.")
        mode_key = "video"

    # Specific Range Download Feature
    cut_section = st.checkbox("✂️ Belirli Bir Aralığı İndir", value=False, key="cut_section")
    start_time_val = ""
    end_time_val = ""

    if cut_section:
        with st.container(border=True):
            st.markdown('<div class="section-cut-card-anchor"></div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:6px;">
                <span style="font-size:0.92rem; font-weight:700; color:#F8FAFC;">⏱️ Kesme Zaman Aralığı (FFmpeg Hassas Kesim)</span>
                <span style="font-size:0.78rem; color:#94A3B8;">Toplam Süre: {info['duration_formatted']}</span>
            </div>
            """, unsafe_allow_html=True)
            col_start, col_end = st.columns(2)
            with col_start:
                start_time_val = st.text_input(
                    "Başlangıç Zamanı",
                    placeholder="00:00:10 veya 10",
                    help="Örn: 00:01:15 veya sadece saniye (75). Boş bırakılırsa en baştan başlar.",
                    key="cut_start_input"
                )
            with col_end:
                end_time_val = st.text_input(
                    "Bitiş Zamanı",
                    placeholder="00:01:30 veya 90",
                    help="Örn: 00:02:45 veya sadece saniye (165). Boş bırakılırsa videonun sonuna kadar indirir.",
                    key="cut_end_input"
                )

    # Action Button
    start_download = st.button("🚀 İndirmeyi Başlat", type="primary", use_container_width=True)

    if start_download:
        # Validate section times if enabled
        validation_error = None
        if cut_section:
            try:
                s_sec = downloader.parse_time_to_seconds(start_time_val) if start_time_val.strip() else None
                e_sec = downloader.parse_time_to_seconds(end_time_val) if end_time_val.strip() else None
                if s_sec is not None and e_sec is not None and s_sec >= e_sec:
                    validation_error = f"Başlangıç zamanı ({start_time_val}), bitiş zamanından ({end_time_val}) küçük olmalıdır."
            except Exception as ve:
                validation_error = str(ve)

        if validation_error:
            st.error(f"⚠️ {validation_error}")
        else:
            st.session_state.download_result = None
            
            progress_bar = st.progress(0, text="İndirme hazırlanıyor...")
            metrics_placeholder = st.empty()
            status_box = st.empty()

            def progress_callback(data):
                status = data.get('status')
                if status == 'downloading':
                    percent = data.get('percent', 0.0)
                    progress_bar.progress(int(percent), text=f"İndiriliyor: %{percent:.1f}")
                    
                    speed_str = data.get('speed_str', '')
                    eta_str = data.get('eta_str', '')
                    total_b = data.get('total_bytes', 0)
                    downloaded_b = data.get('downloaded_bytes', 0)
                    
                    metrics_placeholder.markdown(f"""
                    <div class="metrics-container">
                        <div class="metric-card">
                            <div class="metric-value">{speed_str}</div>
                            <div class="metric-label">İndirme Hızı</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{downloader.format_filesize(downloaded_b)} / {downloader.format_filesize(total_b)}</div>
                            <div class="metric-label">Boyut</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{eta_str}</div>
                            <div class="metric-label">Kalan Süre</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                elif status == 'processing':
                    progress_bar.progress(100, text="FFmpeg ile En Yüksek Kaliteye Dönüştürülüyor...")
                    status_box.info("⚙️ FFmpeg aralığı hassas şekilde kesiyor ve dönüştürüyor, lütfen bekleyin...")

            try:
                with st.spinner("İşlem yürütülüyor..."):
                    result = downloader.download_media(
                        url=st.session_state.current_url,
                        download_mode=mode_key,
                        output_folder="downloads",
                        progress_callback=progress_callback,
                        start_time=start_time_val.strip() if (cut_section and start_time_val.strip()) else None,
                        end_time=end_time_val.strip() if (cut_section and end_time_val.strip()) else None,
                    )
                
                progress_bar.progress(100, text="Tamamlandı! 🎉")
                time.sleep(0.4)
                status_box.empty()
                metrics_placeholder.empty()
                st.session_state.download_result = result
                
                # Save into history
                if result not in st.session_state.history:
                    st.session_state.history.insert(0, result)

                st.balloons()

            except Exception as e:
                progress_bar.empty()
                metrics_placeholder.empty()
                status_box.empty()
                st.error(f"❌ İndirme sırasında bir hata oluştu: {str(e)}")

# ========================================================
# SLEEK SHADED SUCCESS CARD CONTAINER
# ========================================================
if st.session_state.download_result:
    res = st.session_state.download_result
    file_path = res.get('file_path')

    if file_path and os.path.exists(file_path):
        with st.container(border=True):
            st.markdown('<div class="success-card-anchor"></div>', unsafe_allow_html=True)
            
            # Card Header with Emerald Status
            cut_sec_badge = f'<span class="badge-pill" style="border-color:rgba(245,158,11,0.4); color:#FCD34D;">✂️ Bölüm: {res["section"]}</span>' if res.get("is_cut") else ''
            success_hdr = (
                f'<div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">'
                f'<div><div class="success-header-badge">✨ İndirme ve Kodlama Başarılı</div>'
                f'<div class="success-title">{res["title"]}</div></div>'
                f'<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:4px;">'
                f'<span class="badge-pill badge-emerald">{"🎵 MP3 (320 kbps)" if res["format"] == "MP3" else "🎬 MP4 (Orijinal)"}</span>'
                f'{cut_sec_badge}'
                f'<span class="badge-pill">💾 {res["file_size_formatted"]}</span>'
                f'</div></div>'
            )
            st.markdown(success_hdr, unsafe_allow_html=True)

            # Read file bytes for download
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            mime_type = "audio/mpeg" if res['format'] == "MP3" else "video/mp4"

            # Prominent Soft Green Download Button
            st.download_button(
                label=f"💾 {res['file_name']} İndir ({res['file_size_formatted']})",
                data=file_bytes,
                file_name=res['file_name'],
                mime=mime_type,
                use_container_width=True
            )

            # Media Preview Sub-card
            st.markdown(f"""
            <div class="player-subcard">
                <div class="player-label">
                    {'🎧 Ses Önizlemesi (Doğrudan Dinleyin):' if res['format'] == 'MP3' else '🎬 Video Önizlemesi (Doğrudan İzleyin):'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if res['format'] == "MP3":
                st.audio(file_bytes, format="audio/mp3")
            else:
                st.video(file_bytes, format="video/mp4")

            # Local Filepath & Open Folder Sub-card (Desktop) vs Web Hint (Cloud)
            is_local_desktop = (os.name == 'nt') and not os.environ.get("STREAMLIT_SHARING_HOST")

            if is_local_desktop:
                st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                c_path, c_open = st.columns([3.2, 1.2], vertical_alignment="center")
                with c_path:
                    abs_fpath = os.path.abspath(file_path)
                    st.markdown(
                        f'<div class="filepath-box"><span style="font-size:1.2rem;">📁</span>'
                        f'<div><div style="font-size:0.75rem; text-transform:uppercase; color:#64748B; font-weight:700; letter-spacing:0.04em;">Yerel Kayıt Konumu</div>'
                        f'<div class="filepath-text">{abs_fpath}</div></div></div>',
                        unsafe_allow_html=True
                    )
                with c_open:
                    if st.button("📂 Klasörü Aç", key="btn_open_downloads_folder", use_container_width=True):
                        try:
                            downloads_dir = os.path.abspath("downloads")
                            os.makedirs(downloads_dir, exist_ok=True)
                            target_item = os.path.abspath(file_path) if (file_path and os.path.exists(file_path)) else downloads_dir
                            
                            # Open folder and highlight the downloaded file in Windows Explorer
                            if target_item != downloads_dir:
                                subprocess.Popen(f'explorer /select,"{target_item}"')
                            else:
                                subprocess.Popen(f'explorer "{downloads_dir}"')
                                
                            st.toast("📂 Klasör açıldı!", icon="📂")
                        except Exception as ex:
                            st.error(f"Klasör açılamadı: {ex}")
            else:
                st.markdown("""
                <div style="margin-top: 10px; padding: 12px 16px; background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.22); border-radius: 12px; font-size: 0.88rem; color: #6EE7B7; display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 1.2rem;">💡</span>
                    <span>Dosyayı telefonunuza veya bilgisayarınıza kaydetmek için yukarıdaki <b>yeşil indirme butonuna</b> tıklayabilirsiniz.</span>
                </div>
                """, unsafe_allow_html=True)

# Download History Section
if st.session_state.history:
    st.markdown("<div style='height: 1.8rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 1.15rem; font-weight: 700; color: #E2E8F0; margin-bottom: 0.8rem; display:flex; align-items:center; gap:8px;'><span>📜</span> <span>Bu Oturumda İndirilenler</span></div>", unsafe_allow_html=True)
    for idx, item in enumerate(st.session_state.history):
        if os.path.exists(item['file_path']):
            with st.container(border=True):
                st.markdown('<div class="history-item-anchor"></div>', unsafe_allow_html=True)
                col_info, col_action = st.columns([3.4, 1.2], vertical_alignment="center")
                
                is_mp3 = item['format'] == 'MP3'
                media_icon = "🎵" if is_mp3 else "🎬"
                badge_type = "badge-emerald" if is_mp3 else "badge-pill"
                cut_badge = f'<span class="badge-pill" style="font-size:0.75rem; padding:2px 8px; border-color:rgba(245,158,11,0.4); color:#FCD34D;">✂️ {item["section"]}</span>' if item.get("is_cut") else ''
                
                with col_info:
                    hist_html = (
                        f'<div style="display:flex; align-items:center; gap:12px;">'
                        f'<div style="font-size:1.6rem; line-height:1; flex-shrink:0;">{media_icon}</div>'
                        f'<div style="min-width:0; overflow:hidden;">'
                        f'<div style="font-size:0.96rem; font-weight:700; color:#F8FAFC; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{item["title"]}</div>'
                        f'<div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:5px; align-items:center;">'
                        f'<span class="badge-pill {badge_type}" style="font-size:0.75rem; padding:2px 8px;">{item["format"]}</span>'
                        f'{cut_badge}'
                        f'<span class="badge-pill" style="font-size:0.75rem; padding:2px 8px;">{item["file_size_formatted"]}</span>'
                        f'<span style="font-size:0.78rem; color:#64748B; font-family:\'JetBrains Mono\',monospace;">{item["file_name"][:28]}...</span>'
                        f'</div></div></div>'
                    )
                    st.markdown(hist_html, unsafe_allow_html=True)
                    
                with col_action:
                    with open(item['file_path'], "rb") as f_hist:
                        hist_bytes = f_hist.read()
                    st.download_button(
                        label="💾 Tekrar İndir",
                        data=hist_bytes,
                        file_name=item['file_name'],
                        mime="audio/mpeg" if is_mp3 else "video/mp4",
                        key=f"hist_dl_{idx}",
                        use_container_width=True
                    )

# Footer
st.markdown("""
<div class="app-footer">
    YouTube Medya İndirici • yt-dlp & Streamlit ile güçlendirilmiştir • 2026
</div>
""", unsafe_allow_html=True)
