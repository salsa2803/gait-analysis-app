import streamlit as st
import extra_streamlit_components as stx
import json
import os
import base64
from datetime import datetime, timedelta

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Gait Analysis App",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. DATABASE PENGGUNA (FILE JSON)
# ==========================================
USER_FILE = "users.json"

def load_users():
    """Membaca data akun dari file JSON"""
    if not os.path.exists(USER_FILE):
        default_users = {
            "salsa": {
                "password": "123",
                "name": "Aulia Salsa",
                "email": "aulia.salsa@gmail.com",
                "role": "Researcher / User",
                "avatar": ""
            }
        }
        with open(USER_FILE, "w") as f:
            json.dump(default_users, f, indent=4)
        return default_users
    
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Menyimpan data akun baru/update ke JSON"""
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

users_db = load_users()

# Data Dummy untuk Tabel Riwayat Analisis
RIWAYAT_DATA = [
    {"tanggal": "12 Juni 2026 • 10:30", "nama": "gait_pasien_01.mp4", "status": "NORMAL", "akurasi": "92%", "durasi": "10.45 detik"},
    {"tanggal": "10 Juni 2026 • 14:20", "nama": "gait_pasien_02.mp4", "status": "ABNORMAL", "akurasi": "78%", "durasi": "12.20 detik"},
    {"tanggal": "08 Juni 2026 • 09:15", "nama": "gait_pasien_03.mp4", "status": "NORMAL", "akurasi": "90%", "durasi": "09.87 detik"},
    {"tanggal": "05 Juni 2026 • 16:45", "nama": "gait_pasien_04.mp4", "status": "ABNORMAL", "akurasi": "65%", "durasi": "11.30 detik"},
    {"tanggal": "02 Juni 2026 • 11:10", "nama": "gait_pasien_05.mp4", "status": "NORMAL", "akurasi": "88%", "durasi": "10.15 detik"},
]

# ==========================================
# 3. MANAJEMEN SESSION STATE & COOKIE
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

try:
    cookie_manager = stx.CookieManager(key="gait_cookie_mgr")
    saved_session = cookie_manager.get("gait_user_session")
    if saved_session and saved_session in users_db and not st.session_state.logged_in:
        st.session_state.logged_in = True
        st.session_state.username = saved_session
except Exception:
    cookie_manager = None


# ==========================================
# 4. HALAMAN AUTENTIKASI (SIGN IN / SIGN UP)
# ==========================================
def show_auth_page():
    st.markdown("""
        <style>
        header, footer {visibility: hidden;}
        .stApp { background-color: #F8FAFC !important; }

        .stTextInput input {
            border-radius: 12px !important;
            border: 1.5px solid #67E8F9 !important;
            padding: 12px 16px !important;
            background-color: #FFFFFF !important;
            color: #1E293B !important;
            box-shadow: 0px 4px 10px rgba(103, 232, 249, 0.15) !important;
        }
        
        .stTextInput input:focus {
            border-color: #06B6D4 !important;
            box-shadow: 0px 0px 12px rgba(6, 182, 212, 0.3) !important;
        }

        .stTextInput label {
            color: #475569 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
        }

        button[key="btn_signin"] {
            background-color: #F472B6 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 12px !important;
            font-weight: 600 !important;
            box-shadow: 0px 6px 15px rgba(244, 114, 182, 0.4) !important;
        }

        button[key="btn_signup"] {
            background-color: #8B5CF6 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            padding: 12px !important;
            font-weight: 600 !important;
            box-shadow: 0px 6px 15px rgba(139, 92, 246, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 0.8, 1])
    
    with col2:
        st.write("")
        st.write("")
        
        st.markdown("""
            <div style="background: white; padding: 25px 20px 15px 20px; border-radius: 24px; box-shadow: 0px 10px 25px rgba(0,0,0,0.05); text-align: center; margin-bottom: 25px;">
                <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                    <svg width="60" height="60" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="50" cy="50" r="45" stroke="#F472B6" stroke-width="4" stroke-dasharray="200" stroke-dashoffset="40"/>
                        <path d="M50 25 C53 25 55 27 55 30 C55 33 53 35 50 35 C47 35 45 33 45 30 C45 27 47 25 50 25 Z" fill="#1E1B4B"/>
                        <path d="M48 37 L54 48 L46 62 L52 75" stroke="#1E1B4B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M52 45 L42 55 L38 68" stroke="#1E1B4B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                        <circle cx="46" cy="62" r="3" fill="#F472B6"/>
                        <circle cx="52" cy="45" r="3" fill="#8B5CF6"/>
                        <path d="M20 50 Q 30 45, 40 50 T 60 50 T 80 50" stroke="#F472B6" stroke-width="2" fill="none" opacity="0.5"/>
                    </svg>
                </div>
                <h4 style="margin: 0; color: #1E293B; font-weight: 700; font-size: 16px;">Gait Analysis</h4>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            input_identity = st.text_input("Email / Username", placeholder="Masukkan Email Anda").strip()
            password = st.text_input("Password", type="password", placeholder="••••••••").strip()
            
            st.write("")
            if st.button("Sign In", key="btn_signin", use_container_width=True):
                if not input_identity or not password:
                    st.warning("Mohon isi Email/Username dan Password!")
                else:
                    user_found = None
                    for u, val in users_db.items():
                        match_user = (u.lower() == input_identity.lower())
                        match_email = (val.get("email", "").lower() == input_identity.lower())
                        match_pass = (val.get("password") == password)
                        
                        if (match_user or match_email) and match_pass:
                            user_found = u
                            break
                    
                    if user_found:
                        st.session_state.logged_in = True
                        st.session_state.username = user_found
                        
                        if cookie_manager:
                            try:
                                cookie_manager.set(
                                    cookie="gait_user_session", 
                                    val=user_found, 
                                    key="set_session_cookie", 
                                    expires_at=datetime.now() + timedelta(days=30)
                                )
                            except Exception:
                                pass
                        st.success("Berhasil masuk!")
                        st.rerun()
                    else:
                        st.error("Email/Username atau Password tidak cocok!")

            st.markdown("<p style='text-align: center; color: #64748B; font-size: 12px; margin-top: 15px; margin-bottom: 5px;'>Don't have an account? Register</p>", unsafe_allow_html=True)
            if st.button("Sign Up", key="btn_signup", use_container_width=True):
                st.session_state.auth_mode = "register"
                st.rerun()

        else:
            name = st.text_input("Nama Lengkap", placeholder="Masukkan Nama Lengkap").strip()
            email = st.text_input("Email", placeholder="Masukkan Email Anda").strip()
            password = st.text_input("Password", type="password", placeholder="••••••••").strip()
            
            st.write("")
            if st.button("Sign Up", key="btn_signup", use_container_width=True):
                if not name or not email or not password:
                    st.warning("Semua kolom wajib diisi!")
                else:
                    username_gen = email.split("@")[0].lower()
                    
                    is_exist = any(
                        u.lower() == username_gen or val.get("email", "").lower() == email.lower()
                        for u, val in users_db.items()
                    )
                    
                    if is_exist:
                        st.error("Email/Username sudah terdaftar! Silakan Sign In.")
                    else:
                        users_db[username_gen] = {
                            "password": password,
                            "name": name,
                            "email": email,
                            "role": "Researcher / User",
                            "avatar": ""
                        }
                        save_users(users_db)
                        st.success("Akun berhasil dibuat! Silakan Sign In.")
                        st.session_state.auth_mode = "login"
                        st.rerun()

            st.markdown("<p style='text-align: center; color: #64748B; font-size: 12px; margin-top: 15px; margin-bottom: 5px;'>Already have an account?</p>", unsafe_allow_html=True)
            if st.button("Sign In", key="btn_signin", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()


# ==========================================
# 5. APLIKASI UTAMA (DASHBOARD & HALAMAN UTAMA)
# ==========================================
def show_main_app():
    current_user = users_db.get(st.session_state.username, {
        "name": "Salsa", "email": "salsa@gmail.com", "role": "Researcher / User", "avatar": ""
    })
    first_name = current_user["name"].split()[0]
    initials = "".join([n[0].upper() for n in current_user["name"].split()[:2]]) or "US"
    user_avatar = current_user.get("avatar", "")

    st.markdown("""
        <style>
        .stApp { background-color: #F8FAFC !important; }
        [data-testid="stSidebar"] { 
            background-color: #FFFFFF !important; 
            border-right: 1px solid #E2E8F0 !important; 
        }
        
        h1, h2, h3, h4, h5, h6, p, span, label, div { color: #1E293B !important; }
        .stCaption, caption { color: #64748B !important; }
        
        .user-name-text {
            color: #1E293B !important;
            font-size: 13px !important;
            font-weight: 700 !important;
        }
        .user-role-text {
            color: #64748B !important;
            font-size: 11px !important;
        }

        div[data-testid="stSidebar"] button[key="btn_logout"] {
            background-color: #FEE2E2 !important;
            color: #EF4444 !important;
            border: 1px solid #FCA5A5 !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
        }
        div[data-testid="stSidebar"] button[key="btn_logout"]:hover {
            background-color: #FCA5A5 !important;
            color: #B91C1C !important;
        }

        div[data-testid="stCameraInput"] video { transform: scaleX(1) !important; }

        .desktop-card {
            background: white !important;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.03);
            border: 1px solid #F1F5F9;
        }
        
        .status-badge-normal {
            background-color: #DCFCE7; color: #15803D !important; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 11px;
        }
        .status-badge-abnormal {
            background-color: #FEE2E2; color: #B91C1C !important; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 11px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- SIDEBAR NAVIGASI ---
    with st.sidebar:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px; padding: 5px 0;">
                <div style="width: 32px; height: 32px; border-radius: 50%; border: 2px solid #F472B6; display: flex; align-items: center; justify-content: center;">🏃</div>
                <h3 style="margin:0; font-size: 16px; font-weight: 700; color: #1E293B;">Gait Analysis</h3>
            </div>
        """, unsafe_allow_html=True)
        st.write("---")

        menu_options = ["Dashboard", "Rekam Video", "Riwayat", "Laporan", "Profil"]
        default_index = menu_options.index(st.session_state.current_page) if st.session_state.current_page in menu_options else 0
        
        selected_menu = st.radio("Menu Utama", menu_options, index=default_index, label_visibility="collapsed")
        st.session_state.current_page = selected_menu
        
        st.write("---")
        
        if user_avatar:
            avatar_html = f'<img src="data:image/png;base64,{user_avatar}" style="width: 38px; height: 38px; border-radius: 50%; object-fit: cover;">'
        else:
            avatar_html = f'<div style="background: #8B5CF6; color: white !important; width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold;">{initials}</div>'

        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                {avatar_html}
                <div>
                    <div class="user-name-text">{current_user['name']}</div>
                    <div class="user-role-text">{current_user['role']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Logout", key="btn_logout", use_container_width=True):
            if cookie_manager:
                try:
                    cookie_manager.delete("gait_user_session", key="del_session_cookie")
                except Exception:
                    pass
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

    # --- HALAMAN 1: DASHBOARD ---
    if st.session_state.current_page == "Dashboard":
        col_t, col_i = st.columns([4, 1])
        with col_t:
            st.markdown(f"## Halo, {first_name} 👋")
            st.caption("Selamat Datang di Gait Analysis !!")
        with col_i:
            st.markdown("<div style='text-align: right; font-size: 24px;'>🔔</div>", unsafe_allow_html=True)

        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="desktop-card" style="text-align:center;"><span style="color:#64748B; font-size:12px; font-weight:600;">Total Analisis</span><h2 style="margin:5px 0;">25</h2></div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="desktop-card" style="text-align:center;"><span style="color:#64748B; font-size:12px; font-weight:600;">Gait Normal</span><h2 style="margin:5px 0; color:#16A34A !important;">18</h2></div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="desktop-card" style="text-align:center;"><span style="color:#64748B; font-size:12px; font-weight:600;">Gait Abnormal</span><h2 style="margin:5px 0; color:#DC2626 !important;">7</h2></div>', unsafe_allow_html=True)

        st.write("")
        st.markdown("<h4 style='font-size: 15px; font-weight: 600; color: #475569;'>Menu Utama</h4>", unsafe_allow_html=True)
        
        with st.container(border=True):
            col_m1, col_m2 = st.columns([4, 1])
            with col_m1:
                st.markdown("**Mulai Analisis Gait**")
                st.caption("Rekam video untuk memulai analisis pola berjalan")
            with col_m2:
                if st.button("🎥 Rekam >", type="primary", use_container_width=True):
                    st.session_state.current_page = "Rekam Video"
                    st.rerun()

        sub_c1, sub_c2 = st.columns(2)
        with sub_c1:
            with st.container(border=True):
                st.markdown("**📋 Riwayat Analisis**")
                st.caption("Lihat daftar riwayat rekaman")
                if st.button("Buka Riwayat", key="btn_to_riwayat", use_container_width=True):
                    st.session_state.current_page = "Riwayat"
                    st.rerun()
        with sub_c2:
            with st.container(border=True):
                st.markdown("**📊 Laporan**")
                st.caption("Lihat laporan hasil pengukuran")
                if st.button("Buka Laporan", key="btn_to_laporan", use_container_width=True):
                    st.session_state.current_page = "Laporan"
                    st.rerun()

    # --- HALAMAN 2: REKAM VIDEO ---
    elif st.session_state.current_page == "Rekam Video":
        st.title("📹 Rekam / Upload Video Pasien")
        st.caption("Ambil rekaman dari kamera atau upload file video dari komputer.")
        
        tab1, tab2 = st.tabs(["🎥 Rekam via Kamera", "📁 Upload File Video"])
        
        with tab1:
            col_cam, col_setting = st.columns([2.5, 1])
            with col_cam:
                with st.container(border=True):
                    st.subheader("Preview Kamera")
                    picture = st.camera_input("Ambil Frame / Foto Pasien")
                    if picture:
                        st.image(picture, caption="Frame Terrekam (Posisi Normal)", use_column_width=True)
                        st.success("Frame berhasil diambil!")
            with col_setting:
                with st.container(border=True):
                    st.subheader("Pengaturan Kamera")
                    st.selectbox("Sumber Kamera", ["Integrated Camera (Webcam)", "Kamera Eksternal USB"])
                    st.slider("Durasi Perekaman (Detik)", 5, 60, 15)

        with tab2:
            with st.container(border=True):
                st.subheader("Upload Video Analisis")
                uploaded_video = st.file_uploader("Pilih file video (.mp4, .avi, .mov)", type=["mp4", "avi", "mov"])
                if uploaded_video is not None:
                    st.success(f"File '{uploaded_video.name}' berhasil di-upload!")
                    st.video(uploaded_video)

    # --- HALAMAN 3: RIWAYAT ---
    elif st.session_state.current_page == "Riwayat":
        st.title("📋 Riwayat Analisis Gait")
        st.caption("Daftar seluruh rekaman dan hasil analisis pola berjalan pasien.")

        col_search, col_filter = st.columns([3, 1])
        with col_search:
            search_query = st.text_input("🔍 Cari File Video", placeholder="Ketik nama file...").lower()
        with col_filter:
            status_filter = st.selectbox("Filter Status", ["Semua", "NORMAL", "ABNORMAL"])

        st.write("")
        with st.container(border=True):
            for item in RIWAYAT_DATA:
                if search_query and search_query not in item["nama"].lower():
                    continue
                if status_filter != "Semua" and item["status"] != status_filter:
                    continue

                col_icon, col_info, col_stat, col_act = st.columns([0.5, 3, 1.5, 1])
                with col_icon:
                    st.markdown("<div style='font-size:24px; text-align:center;'>📹</div>", unsafe_allow_html=True)
                with col_info:
                    st.markdown(f"**{item['nama']}**")
                    st.caption(f"{item['tanggal']} • Durasi: {item['durasi']}")
                with col_stat:
                    badge_class = "status-badge-normal" if item["status"] == "NORMAL" else "status-badge-abnormal"
                    st.markdown(f"""
                        <div style="display:flex; align-items:center; gap:8px; height:100%;">
                            <span class="{badge_class}">{item['status']}</span>
                            <b style="font-size:13px;">{item['akurasi']}</b>
                        </div>
                    """, unsafe_allow_html=True)
                with col_act:
                    if st.button("Detail", key=f"btn_{item['nama']}", use_container_width=True):
                        st.session_state.current_page = "Laporan"
                        st.rerun()

    # --- HALAMAN 4: LAPORAN ---
    elif st.session_state.current_page == "Laporan":
        st.title("📊 Laporan Analisis Gait")
        st.caption("Ringkasan detail hasil pengukuran parameter pola berjalan.")
        
        with st.container(border=True):
            st.subheader("Hasil Analisis: NORMAL (Akurasi 92%)")
            st.write("---")
            c_l1, c_l2, c_l3 = st.columns(3)
            c_l1.metric("Step Length", "54.2 cm")
            c_l2.metric("Stride Length", "112.8 cm")
            c_l3.metric("Cadence", "92 step/min")
            
            st.write("")
            st.download_button("📥 Unduh Laporan PDF", data="Detail Laporan Gait Analysis", file_name="laporan_gait.pdf")

    # --- HALAMAN 5: PROFIL ---
    elif st.session_state.current_page == "Profil":
        st.title("👤 Profil Pengguna")
        st.caption("Kelola identitas akun, keamanan kata sandi, dan foto profil Anda.")

        col_p1, col_p2 = st.columns([1, 2])
        
        with col_p1:
            with st.container(border=True):
                if user_avatar:
                    st.markdown(f"""
                        <div style="text-align: center; padding: 10px 0;">
                            <img src="data:image/png;base64,{user_avatar}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 3px solid #8B5CF6; margin-bottom: 10px;">
                            <h3 style="margin: 0; font-size: 18px;">{current_user['name']}</h3>
                            <p style="color: #64748B; font-size: 13px; margin-top: 2px;">{current_user['role']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style="text-align: center; padding: 10px 0;">
                            <div style="background: #8B5CF6; color: white !important; width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: bold; margin: 0 auto 10px auto;">
                                {initials}
                            </div>
                            <h3 style="margin: 0; font-size: 18px;">{current_user['name']}</h3>
                            <p style="color: #64748B; font-size: 13px; margin-top: 2px;">{current_user['role']}</p>
                        </div>
                    """, unsafe_allow_html=True)

                st.write("---")
                st.write(f"**Username:** `{st.session_state.username}`")
                st.write(f"**Email:** {current_user['email']}")

        with col_p2:
            with st.container(border=True):
                # 1. Edit Informasi Profil
                st.subheader("Edit Informasi Profil")
                edit_name = st.text_input("Nama Lengkap", value=current_user["name"])
                edit_email = st.text_input("Email", value=current_user["email"])
                
                # 2. Ubah Password
                st.write("---")
                st.subheader("Ubah Password")
                edit_pass = st.text_input("Password Baru (Biarkan kosong jika tidak diubah)", type="password")
                
                # 3. Ganti Foto Profil
                st.write("---")
                st.subheader("Ganti Foto Profil")
                uploaded_img = st.file_uploader("Pilih file gambar (.jpg, .png, .jpeg)", type=["jpg", "png", "jpeg"])
                
                if uploaded_img is not None:
                    st.image(uploaded_img, caption="Preview Foto Baru", width=120)
                    st.info("💡 Klik tombol **💾 Simpan Perubahan Profil** di bawah untuk menerapkan foto ini.")
                
                # 4. Tombol Simpan Perubahan
                st.write("")
                if st.button("💾 Simpan Perubahan Profil", type="primary", use_container_width=True):
                    users_db[st.session_state.username]["name"] = edit_name
                    users_db[st.session_state.username]["email"] = edit_email
                    
                    if edit_pass.strip() != "":
                        users_db[st.session_state.username]["password"] = edit_pass
                    
                    if uploaded_img is not None:
                        bytes_data = uploaded_img.getvalue()
                        base64_str = base64.b64encode(bytes_data).decode()
                        users_db[st.session_state.username]["avatar"] = base64_str
                    
                    save_users(users_db)
                    st.success("Profil & Foto berhasil disimpan!")
                    st.rerun()


# ==========================================
# 6. KONTROL ALUR APLIKASI
# ==========================================
if not st.session_state.logged_in:
    show_auth_page()
else:
    show_main_app()