import streamlit as st
from datetime import datetime
import pandas as pd

# ===== KONFIGURASI HALAMAN =====
st.set_page_config(
    page_title="Nusantara Clarity",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== INITIALIZE SESSION STATE =====
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = True
if 'active_module' not in st.session_state:
    st.session_state.active_module = "Overview"

# ===== CUSTOM CSS DENGAN SIDEBAR TOGGLE =====
sidebar_state = "expanded" if st.session_state.sidebar_open else "collapsed"

st.markdown(f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{display: none;}}
    
    /* Remove Default Padding */
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }}
    
    /* Main Container Background */
    .main {{
        background: linear-gradient(to bottom right, #f8fafc, #eff6ff) !important;
    }}
    
    /* ========== SIDEBAR TOGGLE ANIMATION ========== */
    [data-testid="stSidebar"] {{
        background: linear-gradient(to bottom, #059669, #0d9488) !important;
        transition: all 0.3s ease-in-out !important;
        {f'width: 0px !important; min-width: 0px !important;' if sidebar_state == 'collapsed' else 'width: 21rem !important; min-width: 21rem !important;'}
        overflow: hidden !important;
    }}
    
    [data-testid="stSidebar"] > div:first-child {{
        background: transparent !important;
        {f'opacity: 0;' if sidebar_state == 'collapsed' else 'opacity: 1;'}
        transition: opacity 0.2s ease-in-out;
    }}
    
    /* Sidebar Content */
    [data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    /* Sidebar Logo */
    .sidebar-logo {{
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        padding: 0 1rem;
    }}
    
    .sidebar-logo h1 {{
        color: white !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }}
    
    /* ========== HEADER WITH TOGGLE BUTTON ========== */
    .header-container {{
        display: flex;
        align-items: center;
        gap: 1rem;
        background: white;
        padding: 1rem 2rem;
        border-radius: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #e2e8f0;
    }}
    
    .toggle-button {{
        background: transparent;
        border: none;
        padding: 0.5rem;
        border-radius: 0.5rem;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
        color: #1e293b;
        font-size: 1.5rem;
    }}
    
    .toggle-button:hover {{
        background: #f1f5f9;
    }}
    
    .header-content {{
        flex: 1;
    }}
    
    .header-title {{
        font-size: 1.875rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        line-height: 1.2;
    }}
    
    .header-subtitle {{
        font-size: 0.875rem;
        color: #64748b;
        margin-top: 0.5rem;
    }}
    
    .header-actions {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}
    
    .notification-btn {{
        position: relative;
        background: transparent;
        border: none;
        padding: 0.5rem;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 1.5rem;
    }}
    
    .notification-btn:hover {{
        background: #f1f5f9;
    }}
    
    .notification-badge {{
        position: absolute;
        top: 0.25rem;
        right: 0.25rem;
        width: 0.5rem;
        height: 0.5rem;
        background: #ef4444;
        border-radius: 50%;
    }}
    
    .user-avatar {{
        width: 2.5rem;
        height: 2.5rem;
        background: linear-gradient(to bottom right, #6ee7b7, #0d9488);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.875rem;
    }}
    
    /* ========== MODULE NAVIGATION CARDS ========== */
    .module-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }}
    
    .module-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 2px solid #e2e8f0;
        cursor: pointer;
        transition: all 0.3s;
        text-align: center;
    }}
    
    .module-card:hover {{
        border-color: #059669;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.15);
        transform: translateY(-2px);
    }}
    
    .module-card.active {{
        border-color: #059669;
        background: linear-gradient(135deg, #f0fdf4 0%, #d1fae5 100%);
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.15);
    }}
    
    .module-icon {{
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }}
    
    .module-name {{
        font-size: 0.875rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0;
    }}
    
    /* ========== ALERT BOXES ========== */
    .alert-box {{
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 0.875rem;
        font-weight: 500;
        border-left: 4px solid;
    }}
    
    .alert-warning {{
        background-color: #fffbeb;
        border-color: #f59e0b;
        color: #78350f;
    }}
    
    .alert-info {{
        background-color: #eff6ff;
        border-color: #3b82f6;
        color: #1e40af;
    }}
    
    .alert-success {{
        background-color: #f0fdf4;
        border-color: #10b981;
        color: #065f46;
    }}
    
    /* ========== METRIC CARDS FIX ========== */
    div[data-testid="stMetric"] {{
        background: white !important;
        padding: 1.5rem !important;
        border-radius: 1rem !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s !important;
    }}
    
    div[data-testid="stMetric"]:hover {{
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-2px);
    }}
    
    div[data-testid="stMetric"] label {{
        font-size: 0.875rem !important;
        color: #64748b !important;
        font-weight: 500 !important;
    }}
    
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        font-size: 1.875rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }}
    
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] {{
        font-size: 0.875rem !important;
        font-weight: 600 !important;
    }}
    
    /* Icon Containers */
    .metric-icon {{
        padding: 0.75rem;
        border-radius: 0.75rem;
        width: fit-content;
        margin-bottom: 1rem;
        font-size: 1.5rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }}
    
    /* ========== TABLE STYLING ========== */
    .stDataFrame {{
        background: white !important;
        border-radius: 1rem !important;
        overflow: hidden !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid #e2e8f0 !important;
    }}
    
    [data-testid="stDataFrame"] > div {{
        border-radius: 1rem !important;
    }}
    
    /* ========== SECTION HEADERS ========== */
    .section-header {{
        font-size: 1.25rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        margin-top: 2rem;
    }}
    
    /* ========== INVESTMENT CARDS ========== */
    .investment-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        transition: all 0.3s;
    }}
    
    .investment-card:hover {{
        border-color: #6ee7b7;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }}
    
    .investment-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }}
    
    .investment-title {{
        font-size: 1rem;
        font-weight: 600;
        color: #1e293b;
    }}
    
    .investment-text {{
        color: #64748b;
        font-size: 0.75rem;
    }}
    
    .investment-value {{
        color: #1e293b;
        font-size: 1.125rem;
        font-weight: 700;
    }}
    
    .badge {{
        padding: 0.375rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }}
    
    .badge-priority {{
        background-color: #d1fae5;
        color: #065f46;
    }}
    
    .badge-recommended {{
        background-color: #dbeafe;
        color: #1e40af;
    }}
    
    /* ========== EMPTY STATE ========== */
    .empty-state {{
        background: white;
        padding: 4rem 3rem;
        border-radius: 1rem;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    
    .empty-state-icon {{
        background: #f1f5f9;
        width: 6rem;
        height: 6rem;
        border-radius: 50%;
        margin: 0 auto 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        color: #94a3b8;
    }}
    
    .empty-state-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.75rem;
    }}
    
    .empty-state-text {{
        color: #64748b;
        max-width: 28rem;
        margin: 0 auto;
        line-height: 1.6;
    }}
    
    /* Hide default Streamlit button */
    button[kind="header"] {{
        display: none !important;
    }}
    
    /* ========== DARK MODE ========== */
    @media (prefers-color-scheme: dark) {{
        .main {{
            background: linear-gradient(to bottom right, #0f172a, #1e293b) !important;
        }}
        
        [data-testid="stSidebar"] {{
            background: linear-gradient(to bottom, #047857, #0f766e) !important;
        }}
        
        .header-container {{
            background: #1e293b !important;
            border-bottom-color: #334155 !important;
        }}
        
        .header-title {{
            color: #f1f5f9 !important;
        }}
        
        .header-subtitle {{
            color: #94a3b8 !important;
        }}
        
        .toggle-button {{
            color: #f1f5f9 !important;
        }}
        
        .toggle-button:hover {{
            background: #334155 !important;
        }}
        
        .notification-btn {{
            color: #f1f5f9 !important;
        }}
        
        .notification-btn:hover {{
            background: #334155 !important;
        }}
        
        .module-card {{
            background: #1e293b !important;
            border-color: #334155 !important;
        }}
        
        .module-card:hover {{
            border-color: #10b981 !important;
        }}
        
        .module-card.active {{
            border-color: #10b981 !important;
            background: linear-gradient(135deg, #1e293b 0%, #0f766e 100%) !important;
        }}
        
        .module-name {{
            color: #f1f5f9 !important;
        }}
        
        .alert-warning {{
            background-color: rgba(251, 191, 36, 0.1) !important;
            color: #fcd34d !important;
        }}
        
        .alert-info {{
            background-color: rgba(59, 130, 246, 0.1) !important;
            color: #93c5fd !important;
        }}
        
        .alert-success {{
            background-color: rgba(16, 185, 129, 0.1) !important;
            color: #6ee7b7 !important;
        }}
        
        div[data-testid="stMetric"] {{
            background: #1e293b !important;
            border-color: #334155 !important;
        }}
        
        div[data-testid="stMetric"]:hover {{
            border-color: #475569 !important;
        }}
        
        div[data-testid="stMetric"] label {{
            color: #94a3b8 !important;
        }}
        
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            color: #f1f5f9 !important;
        }}
        
        .stDataFrame {{
            background: #1e293b !important;
            border-color: #334155 !important;
        }}
        
        .section-header {{
            color: #f1f5f9 !important;
        }}
        
        .investment-card {{
            background: #1e293b !important;
            border-color: #334155 !important;
        }}
        
        .investment-card:hover {{
            border-color: #10b981 !important;
        }}
        
        .investment-title {{
            color: #f1f5f9 !important;
        }}
        
        .investment-text {{
            color: #94a3b8 !important;
        }}
        
        .investment-value {{
            color: #f1f5f9 !important;
        }}
        
        .badge-priority {{
            background-color: rgba(16, 185, 129, 0.2) !important;
            color: #6ee7b7 !important;
        }}
        
        .badge-recommended {{
            background-color: rgba(59, 130, 246, 0.2) !important;
            color: #93c5fd !important;
        }}
        
        .empty-state {{
            background: #1e293b !important;
            border-color: #334155 !important;
        }}
        
        .empty-state-icon {{
            background: #334155 !important;
            color: #64748b !important;
        }}
        
        .empty-state-title {{
            color: #f1f5f9 !important;
        }}
        
        .empty-state-text {{
            color: #94a3b8 !important;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ===== DATA =====
risk_data = [
    {"Lokasi": "Jakarta", "Tingkat Risiko": "Tinggi", "Jenis Bahaya": "Banjir", "Dampak Finansial": "Rp 12.5 M", "Probabilitas": "75%"},
    {"Lokasi": "Surabaya", "Tingkat Risiko": "Sedang", "Jenis Bahaya": "Kekeringan", "Dampak Finansial": "Rp 8.3 M", "Probabilitas": "45%"},
    {"Lokasi": "Bandung", "Tingkat Risiko": "Rendah", "Jenis Bahaya": "Longsor", "Dampak Finansial": "Rp 3.2 M", "Probabilitas": "20%"},
]

investment_recommendations = [
    {"title": "Sistem Irigasi Tetes", "sroi": "5.7x", "cost": "Rp 2.1 M", "timeline": "6 bulan", "status": "Prioritas"},
    {"title": "Fortifikasi Infrastruktur", "sroi": "4.2x", "cost": "Rp 5.8 M", "timeline": "12 bulan", "status": "Direkomendasikan"},
    {"title": "Panel Solar Atap", "sroi": "3.8x", "cost": "Rp 3.5 M", "timeline": "8 bulan", "status": "Direkomendasikan"},
]

alerts = [
    {"type": "warning", "message": "⚠️ Prediksi curah hujan tinggi dalam 48 jam - Area Jakarta"},
    {"type": "info", "message": "ℹ️ Data satelit terbaru tersedia untuk analisis"},
    {"type": "success", "message": "✓ Laporan TCFD Q3 2024 berhasil dibuat"},
]

modules = [
    {"id": "Overview", "name": "Overview", "icon": "⌕"},
    {"id": "Kuantifikasi Risiko", "name": "Kuantifikasi Risiko", "icon": "!"},
    {"id": "Optimalisasi Investasi", "name": "Optimalisasi Investasi", "icon": "$"},
    {"id": "Pemantauan Geografis", "name": "Pemantauan Geografis", "icon": "🗺"},
    {"id": "Pembiayaan Hijau", "name": "Pembiayaan Hijau", "icon": "⬀"},
    {"id": "Pelaporan", "name": "Pelaporan", "icon": "✉"},
]

# ===== SIDEBAR (Hidden by default, controlled by toggle) =====
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo">
            <span style="font-size: 2rem;">☁</span>
            <h1>Nusantara Clarity</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Menu Navigasi")
    st.markdown("---")
    
    for module in modules:
        if st.button(f"{module['icon']} {module['name']}", key=f"sidebar_{module['id']}", use_container_width=True):
            st.session_state.active_module = module['id']
            st.rerun()

# ===== HEADER WITH TOGGLE =====
col_toggle, col_header, col_notif, col_avatar = st.columns([0.5, 8, 0.5, 0.5])

with col_toggle:
    if st.button("☰" if st.session_state.sidebar_open else "☰", key="toggle_sidebar", help="Toggle Sidebar"):
        st.session_state.sidebar_open = not st.session_state.sidebar_open
        st.rerun()

with col_header:
    st.markdown(f"""
        <div class="header-content">
            <h2 class="header-title">Dashboard PT. Infrastruktur Nusantara</h2>
            <p class="header-subtitle">Terakhir diperbarui: {datetime.now().strftime("%d %B %Y, %H:%M")} WIB</p>
        </div>
    """, unsafe_allow_html=True)

with col_notif:
    st.markdown("""
        <div class="notification-btn">
            🔔
            <span class="notification-badge"></span>
        </div>
    """, unsafe_allow_html=True)

with col_avatar:
    st.markdown("""
        <div class="user-avatar">IN</div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== MODULE NAVIGATION CARDS =====
st.markdown('<div class="module-grid">', unsafe_allow_html=True)

cols = st.columns(6)
for idx, module in enumerate(modules):
    with cols[idx]:
        active_class = "active" if st.session_state.active_module == module['id'] else ""
        if st.button(
            f"{module['icon']}\n\n{module['name']}", 
            key=f"module_{module['id']}", 
            use_container_width=True,
            type="primary" if active_class else "secondary"
        ):
            st.session_state.active_module = module['id']
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ===== ALERTS =====
for alert in alerts:
    alert_class = f"alert-{alert['type']}"
    st.markdown(f"""
        <div class="alert-box {alert_class}">
            {alert['message']}
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== CONTENT BERDASARKAN ACTIVE MODULE =====
if st.session_state.active_module == "Overview":
    # Metric Cards dengan Icon
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-icon" style="background: #fee2e2;">
                <span style="font-size: 1.5rem;">!</span>
            </div>
        """, unsafe_allow_html=True)
        st.metric(
            label="Total Risiko Teridentifikasi",
            value="Rp 450 M",
            delta="+15%",
            delta_color="inverse"
        )
        st.caption("12 lokasi berisiko tinggi")
    
    with col2:
        st.markdown("""
            <div class="metric-icon" style="background: #d1fae5;">
                <span style="font-size: 1.5rem;">📈</span>
            </div>
        """, unsafe_allow_html=True)
        st.metric(
            label="Proyeksi SROI",
            value="4.5x",
            delta="+42%"
        )
        st.caption("Dari 8 rekomendasi investasi")
    
    with col3:
        st.markdown("""
            <div class="metric-icon" style="background: #dbeafe;">
                <span style="font-size: 1.5rem;">💵</span>
            </div>
        """, unsafe_allow_html=True)
        st.metric(
            label="Akses Pembiayaan Hijau",
            value="Rp 15 M",
            delta="Tersedia"
        )
        st.caption("3 instrumen tersedia")
    
    with col4:
        st.markdown("""
            <div class="metric-icon" style="background: #e9d5ff;">
                <span style="font-size: 1.5rem;">✓</span>
            </div>
        """, unsafe_allow_html=True)
        st.metric(
            label="Status Kepatuhan",
            value="TCFD",
            delta="100%"
        )
        st.caption("Laporan otomatis siap")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Risk Assessment Table
    st.markdown('<h3 class="section-header">Penilaian Risiko Iklim</h3>', unsafe_allow_html=True)
    
    df_risk = pd.DataFrame(risk_data)
    
    st.dataframe(
        df_risk,
        use_container_width=True,
        hide_index=True,
        height=200
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Investment Recommendations
    st.markdown('<h3 class="section-header">Rekomendasi Investasi Adaptasi</h3>', unsafe_allow_html=True)
    
    for inv in investment_recommendations:
        badge_class = "badge-priority" if inv["status"] == "Prioritas" else "badge-recommended"
        
        st.markdown(f"""
            <div class="investment-card">
                <div class="investment-header">
                    <span class="investment-title">{inv['title']}</span>
                    <span class="badge {badge_class}">{inv['status']}</span>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">
                    <div>
                        <p class="investment-text" style="margin-bottom: 0.25rem;">SROI</p>
                        <p style="font-size: 1.125rem; font-weight: 700; color: #059669; margin: 0;">{inv['sroi']}</p>
                    </div>
                    <div>
                        <p class="investment-text" style="margin-bottom: 0.25rem;">Biaya</p>
                        <p class="investment-value" style="margin: 0;">{inv['cost']}</p>
                    </div>
                    <div>
                        <p class="investment-text" style="margin-bottom: 0.25rem;">Timeline</p>
                        <p class="investment-value" style="margin: 0;">{inv['timeline']}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

else:
    # Empty State untuk modul lainnya
    module_icons = {
        "Kuantifikasi Risiko": "!",
        "Optimalisasi Investasi": "$",
        "Pemantauan Geografis": "🗺",
        "Pembiayaan Hijau": "↗",
        "Pelaporan": "✉"
    }
    
    icon = module_icons.get(st.session_state.active_module, "📊")
    
    st.markdown(f"""
        <div class="empty-state">
            <div class="empty-state-icon">{icon}</div>
            <h3 class="empty-state-title">{st.session_state.active_module}</h3>
            <p class="empty-state-text">
                Modul ini sedang dalam pengembangan. Konten lengkap akan tersedia dalam versi produk minimum.
            </p>
        </div>
    """, unsafe_allow_html=True)