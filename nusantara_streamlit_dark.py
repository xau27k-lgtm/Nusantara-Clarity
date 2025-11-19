import streamlit as st
import pandas as pd
from datetime import datetime

# ===== 1. KONFIGURASI HALAMAN =====
st.set_page_config(
    page_title="Nusantara Clarity",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== 2. DATA LENGKAP =====
risk_data = [
    {"Lokasi": "Jakarta Utara", "Tingkat Risiko": "Tinggi", "Bahaya": "Banjir", "Dampak": "Rp 12.5 M", "Probabilitas": "75%"},
    {"Lokasi": "Surabaya", "Tingkat Risiko": "Sedang", "Bahaya": "Kekeringan", "Dampak": "Rp 8.3 M", "Probabilitas": "45%"},
    {"Lokasi": "Malang", "Tingkat Risiko": "Rendah", "Bahaya": "Longsor", "Dampak": "Rp 3.2 M", "Probabilitas": "20%"},
    {"Lokasi": "Denpasar", "Tingkat Risiko": "Tinggi", "Bahaya": "Banjir", "Dampak": "Rp 9.1 M", "Probabilitas": "60%"},
]

investment_list = [
    {"title": "Sistem Irigasi Tetes AI", "sroi": "5.7x", "cost": "Rp 2.1 M", "status": "Prioritas", "desc": "ROI Tinggi"},
    {"title": "Fortifikasi Infrastruktur", "sroi": "4.2x", "cost": "Rp 5.8 M", "status": "Rekomendasi", "desc": "Jangka Panjang"},
    {"title": "Panel Solar Atap Gudang", "sroi": "3.8x", "cost": "Rp 3.5 M", "status": "Rekomendasi", "desc": "Efisiensi Energi"},
]

alert_list = [
    {"type": "warning", "icon": "⚠️", "text": "<b>Peringatan:</b> Prediksi curah hujan ekstrem area Malang (48 Jam)"},
    {"type": "info", "icon": "ℹ️", "text": "<b>Info:</b> Data satelit Sentinel-2 baru saja diupdate"},
    {"type": "success", "icon": "✅", "text": "<b>Sukses:</b> Laporan TCFD Q4 2025 berhasil dibuat otomatis"},
]

# ===== 3. CSS DARK MODE PREMIUM =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e2e8f0;
    }

    /* Background Utama */
    .stApp { background-color: #0f172a; }
    .block-container { padding-top: 2rem; background-color: #0f172a; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #064e3b !important;
        background-image: linear-gradient(180deg, #065f46 0%, #022c22 100%);
        border-right: 1px solid #059669;
    }
    [data-testid="stSidebarNav"], .stDeployButton { display: none; }

    /* Menu Navigasi */
    [data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child { display: none; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: transparent; padding: 12px 20px; margin-bottom: 8px;
        border-radius: 10px; cursor: pointer; color: #a7f3d0 !important;
        font-weight: 500; font-size: 14px; transition: all 0.3s ease; border: 1px solid transparent;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(16, 185, 129, 0.1); color: white !important;
        transform: translateX(5px); border: 1px solid rgba(16, 185, 129, 0.3);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.2) 0%, transparent 100%) !important;
        color: #34d399 !important; font-weight: 700; border-left: 4px solid #34d399;
    }

    /* Kartu & Alert */
    .card {
        background: #1e293b; padding: 20px; border-radius: 16px;
        border: 1px solid #334155; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px; transition: transform 0.2s;
    }
    .card:hover { border-color: #10b981; transform: translateY(-2px); }
    
    .card-title { color: #94a3b8; font-size: 13px; margin-bottom: 5px; }
    .card-value { color: #f8fafc; font-size: 28px; font-weight: 700; margin: 0; }
    .card-sub { color: #64748b; font-size: 12px; margin-top: 5px; }

    .notification {
        padding: 15px 20px; border-radius: 12px; margin-bottom: 12px;
        border: 1px solid; display: flex; align-items: center; gap: 12px; font-size: 14px;
    }
    
    .notif-warning { border-color: #b45309; background: rgba(245, 158, 11, 0.1); color: #fbbf24; }
    .notif-info { border-color: #1d4ed8; background: rgba(59, 130, 246, 0.1); color: #60a5fa; }
    .notif-success { border-color: #065f46; background: rgba(16, 185, 129, 0.1); color: #34d399; }

</style>
""", unsafe_allow_html=True)

# ===== 4. SIDEBAR =====
with st.sidebar:
    # Header
    st.markdown("""
        <div style="padding: 20px 10px; margin-bottom: 20px; color: white; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <div style="background: #10b981; padding: 8px; border-radius: 8px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19c0-1.7-1.3-3-3-3h-11a4 4 0 1 1 0-8 2.5 2.5 0 0 1 5-2.7 9 9 0 0 1 9.8 2.7"/><path d="M16.2 4a9 9 0 0 0-12.8 15.8"/></svg>
            </div>
            <div>
                <h3 style="margin:0; font-size:16px; font-weight:700; color:white;">Nusantara</h3>
                <p style="margin:0; font-size:10px; color:#6ee7b7; letter-spacing: 1px;">CLARITY AI</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Menu
    selected = st.radio(
        "Menu",
        ["  Overview", "  Kuantifikasi Risiko", "  Optimalisasi Investasi", "  Pemantauan Geografis", "  Pembiayaan Hijau", "  Pelaporan"],
        label_visibility="collapsed"
    )

    # --- PERBAIKAN FOOTER DISINI ---
    # Kita gunakan margin-top agar footer terdorong ke bawah secara natural
    # Bukan position: absolute yang bikin menimpa
    st.markdown("""
        <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); color: #64748b; font-size: 11px;">
            Server: <span style="color:#10b981">● Online</span><br>v2.5 (Full Data)
        </div>
    """, unsafe_allow_html=True)

active_module = selected.strip()

# ===== 5. HEADER =====
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown('<h1 style="color:white; margin-bottom:0;">Dashboard Eksekutif PT. Profitera Team</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#64748b;">Terakhir diperbarui: {datetime.now().strftime("%d %B %Y, %H:%M")} WIB</p>', unsafe_allow_html=True)

with col_h2:
    st.markdown("""
        <div style="display:flex; justify-content:flex-end; align-items:center; gap:15px; height: 100%;">
            <div style="text-align:right; line-height:1.2;">
                <div style="color:white; font-weight:600; font-size:14px;">Admin</div>
                <div style="color:#10b981; font-size:11px;">Profitera</div>
            </div>
            <div style="width:40px; height:40px; background:linear-gradient(135deg, #10b981, #059669); border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-weight:bold; box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);">IN</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ===== 6. KONTEN UTAMA =====
if active_module == "Overview":

    # -- ALERTS --
    for alert in alert_list:
        css_class = f"notif-{alert['type']}"
        st.markdown(f"""
            <div class="notification {css_class}">
                <span>{alert['icon']}</span> {alert['text']}
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -- KPI CARDS --
    c1, c2, c3, c4 = st.columns(4)
    
    def kpi_card(icon, color_bg, color_text, delta, title, value, sub):
        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between;">
                <div style="padding:8px; background:{color_bg}; border-radius:8px; color:{color_text};">{icon}</div>
                <span style="color:{color_text}; font-weight:bold; font-size:12px;">{delta}</span>
            </div>
            <p class="card-title" style="margin-top:10px;">{title}</p>
            <h2 class="card-value">{value}</h2>
            <p class="card-sub">{sub}</p>
        </div>
        """, unsafe_allow_html=True)

    with c1: kpi_card("⚡", "rgba(239, 68, 68, 0.2)", "#f87171", "+15%", "Risiko Finansial", "Rp 450 M", "12 Titik Merah")
    with c2: kpi_card("📈", "rgba(16, 185, 129, 0.2)", "#34d399", "+42%", "Proyeksi SROI", "4.5x", "Social Return")
    with c3: kpi_card("💵", "rgba(59, 130, 246, 0.2)", "#60a5fa", "OPEN", "Dana Hijau", "Rp 15 M", "Siap Cair")
    with c4: kpi_card("🛡️", "rgba(168, 85, 247, 0.2)", "#c084fc", "100%", "Kepatuhan", "TCFD", "Audit Ready")

    # -- TABEL & INVESTASI --
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("### ✵ Peta Risiko Regional")
        df = pd.DataFrame(risk_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

    with col_right:
        st.markdown("### 🗐 Rekomendasi Investasi")
        for inv in investment_list:
            border_color = "#10b981" if inv['status'] == "Prioritas" else "#3b82f6"
            badge_bg = "rgba(16,185,129,0.2)" if inv['status'] == "Prioritas" else "rgba(59,130,246,0.2)"
            badge_text = "#34d399" if inv['status'] == "Prioritas" else "#60a5fa"
            roi_color = "#34d399" if inv['status'] == "Prioritas" else "#60a5fa"
            
            st.markdown(f"""
                <div class="card" style="padding:15px; border-left: 4px solid {border_color}; margin-bottom: 10px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <b style="color:white; font-size: 14px;">{inv['title']}</b>
                        <span style="background:{badge_bg}; color:{badge_text}; padding:2px 8px; border-radius:4px; font-size:10px;">{inv['status'].upper()}</span>
                    </div>
                    <div style="font-size:12px; color:#94a3b8;">
                        Biaya: <b style="color:white;">{inv['cost']}</b> | 
                        ROI: <b style="color:{roi_color};">{inv['sroi']}</b>
                        <div style="margin-top:4px; font-style:italic; opacity:0.7;">{inv['desc']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:400px; text-align:center; border: 2px dashed #334155; border-radius: 20px;">
        <div style="font-size:60px; margin-bottom:20px; filter: grayscale(100%); opacity: 0.5;">🚧</div>
        <h2 style="color:#f8fafc;">Modul {active_module}</h2>
        <p style="color:#64748b;">Fitur ini sedang dikembangkan.</p>
    </div>
    """, unsafe_allow_html=True)