import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ======================================================================================
# KONFIGURASI HALAMAN
# ======================================================================================
st.set_page_config(
    page_title="Dashboard Clustering Hadist",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================================================
# CSS & GAYA TAMPILAN MODERN (Dengan Auto Dark/Light Mode)
# ======================================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --text-color-primary: #1a202c;
        --text-color-secondary: #4a5568;
        --bg-color-primary: #f7fafc;
        --bg-color-secondary: #edf2f7;
        --glass-bg: rgba(255, 255, 255, 0.6);
        --glass-border: rgba(200, 200, 200, 0.3);
        --shadow-light: 0 4px 12px rgba(0, 0, 0, 0.05);
        --shadow-medium: 0 8px 25px rgba(0, 0, 0, 0.08);
        --gradient-main: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    }

    [data-theme="dark"] {
        --text-color-primary: #e2e8f0;
        --text-color-secondary: #a0aec0;
        --bg-color-primary: #1a202c;
        --bg-color-secondary: #2d3748;
        --glass-bg: rgba(45, 55, 72, 0.5);
        --glass-border: rgba(255, 255, 255, 0.1);
        --shadow-light: 0 4px 12px rgba(0, 0, 0, 0.2);
        --shadow-medium: 0 8px 25px rgba(0, 0, 0, 0.3);
    }

    * {
        font-family: 'Inter', sans-serif;
        color: var(--text-color-primary);
    }

    .stApp {
        background-color: var(--bg-color-primary);
        transition: background-color 0.3s ease, color 0.3s ease;
    }

    /* Sembunyikan elemen bawaan Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    
    /* Atur padding container utama */
    .block-container {
        padding: 2rem 3rem 3rem 3rem !important;
    }

    /* Kartu Kaca (Glassmorphism) */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-light);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-medium);
        border-color: rgba(102, 126, 234, 0.5);
    }

    /* Hero Header */
    .hero-header {
        background: var(--gradient-main);
        padding: 4rem 2rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        text-align: center;
        color: white;
    }
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: white;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
        color: white;
        margin-top: -1rem;
    }

    /* Kartu Metrik */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: var(--bg-color-secondary);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        transition: all 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: scale(1.05);
    }
    .metric-label {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text-color-secondary);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
    }

    /* Kartu Hadist */
    .hadith-card {
        background: var(--bg-color-secondary);
        border-left: 5px solid var(--primary-color);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    .hadith-card:hover {
        box-shadow: var(--shadow-light);
        transform: translateX(4px);
    }
    .hadith-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .hadith-meta {
        font-size: 0.85rem;
        color: var(--text-color-secondary);
        margin-bottom: 1rem;
    }
    .hadith-content {
        color: var(--text-color-secondary);
        line-height: 1.6;
    }
    .search-highlight {
        background-color: #f093fb;
        background-image: linear-gradient(315deg, #f093fb 0%, #f5576c 74%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    [data-theme="dark"] .search-highlight {
        background-color: #f093fb;
        background-image: linear-gradient(315deg, #f093fb 0%, #f5576c 74%);
    }

    /* Sidebar */
    .css-1d391kg {
        background: var(--bg-color-secondary);
        border-right: 1px solid var(--glass-border);
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: 600;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--glass-border);
    }

    /* Tombol dan Input */
    .stButton > button {
        background: var(--gradient-main);
        border: none;
        border-radius: 12px;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-light);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-medium);
        filter: brightness(1.1);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background: none;
        padding-left: 20px;
        padding-right: 20px;
        border-radius: 8px;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
    }
    .stTabs [aria-selected="true"] p {
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ======================================================================================
# JAVASCRIPT UNTUK DETEKSI TEMA OTOMATIS
# ======================================================================================
# Script ini akan mengubah atribut data-theme pada body berdasarkan preferensi sistem pengguna
st.components.v1.html("""
<script>
const streamlitDoc = window.parent.document;

function setTheme(theme) {
    const body = streamlitDoc.querySelector('body');
    if (theme === 'dark') {
        body.setAttribute('data-theme', 'dark');
    } else {
        body.removeAttribute('data-theme');
    }
}

const darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)");

// Set tema awal berdasarkan preferensi sistem
setTheme(darkThemeMq.matches ? 'dark' : 'light');

// Tambahkan listener untuk mengubah tema jika preferensi sistem berubah
darkThemeMq.addEventListener('change', (e) => {
    setTheme(e.matches ? 'dark' : 'light');
});
</script>
""", height=0)


# ======================================================================================
# FUNGSI-FUNGSI UTAMA
# ======================================================================================

@st.cache_data
def load_data():
    """Memuat data dari file CSV dengan penanganan error."""
    try:
        df = pd.read_csv('hadits_with_topics.csv')
        # Pastikan kolom yang dibutuhkan ada
        required_cols = ['Perawi', 'Terjemahan', 'topic']
        if not all(col in df.columns for col in required_cols):
            st.error(f"❌ File CSV harus memiliki kolom: {', '.join(required_cols)}")
            return None
        return df
    except FileNotFoundError:
        st.error("❌ File 'hadits_with_topics.csv' tidak ditemukan! Pastikan file berada di direktori yang sama.")
        return None
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memuat data: {e}")
        return None

def create_hero_section(df):
    """Membuat bagian hero header dengan statistik utama."""
    total_hadits = len(df)
    # Asumsi topik -1 adalah outlier/tidak terkluster
    total_topics = df[df['topic'] != -1]['topic'].nunique()
    clustered = len(df[df['topic'] != -1])
    
    st.markdown(f"""
    <div class="hero-header">
        <h1 class="hero-title">Dashboard Analisis Hadist</h1>
        <p class="hero-subtitle">Mengelompokkan dan Menganalisis Ribuan Hadist Menggunakan Machine Learning</p>
    </div>
    
    <div class="metric-grid">
        <div class="metric-card">
            <p class="metric-label">Total Hadist</p>
            <p class="metric-value">{total_hadits:,}</p>
        </div>
        <div class="metric-card">
            <p class="metric-label">Topik Teridentifikasi</p>
            <p class="metric-value">{total_topics}</p>
        </div>
        <div class="metric-card">
            <p class="metric-label">Hadist Terkluster</p>
            <p class="metric-value">{clustered:,}</p>
        </div>
         <div class="metric-card">
            <p class="metric-label">Perawi Unik</p>
            <p class="metric-value">{df['Perawi'].nunique():,}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_main_dashboard(df):
    """Menampilkan halaman dasbor utama."""
    st.markdown("## 📖 Tinjauan Umum")
    
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("#### 📊 Distribusi Hadist per Topik")
        topic_counts = df[df['topic'] != -1]['topic'].value_counts().nlargest(10)
        if not topic_counts.empty:
            fig = px.bar(
                topic_counts,
                x=topic_counts.index,
                y=topic_counts.values,
                labels={'x': 'Nomor Topik', 'y': 'Jumlah Hadist'},
                color_discrete_sequence=[st.get_option("theme.primaryColor")]
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(type='category')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Tidak ada data topik untuk ditampilkan.")
            
    with col2:
        st.markdown("#### 👥 Distribusi Perawi")
        top_perawi = df['Perawi'].value_counts().nlargest(10)
        if not top_perawi.empty:
            fig = px.pie(
                top_perawi,
                values=top_perawi.values,
                names=top_perawi.index,
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Plasma_r
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Tidak ada data perawi untuk ditampilkan.")

    st.markdown("---")
    st.markdown("### 📜 Contoh Hadist dari Topik Populer")
    top_topics = df[df['topic'] != -1]['topic'].value_counts().nlargest(3).index
    for topic_id in top_topics:
        sample_hadith = df[df['topic'] == topic_id].iloc[0]
        with st.container():
            st.markdown(f"""
            <div class="hadith-card">
                <p class="hadith-title">Topik {int(topic_id)}</p>
                <p class="hadith-meta">Diriwayatkan oleh: <strong>{sample_hadith['Perawi']}</strong></p>
                <p class="hadith-content">"{sample_hadith['Terjemahan'][:300]}..."</p>
            </div>
            """, unsafe_allow_html=True)

def show_search_page(df):
    """Menampilkan halaman pencarian hadist."""
    st.markdown("## 🔍 Pencarian & Eksplorasi Hadist")

    search_type = st.radio(
        "Cari Berdasarkan:",
        ["Kata Kunci", "Topik", "Perawi"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown('<hr style="margin-top: -0.5rem; margin-bottom: 1rem;">', unsafe_allow_html=True)
    
    if search_type == "Kata Kunci":
        search_query = st.text_input("Masukkan kata kunci pencarian:", placeholder="Contoh: shalat, puasa, zakat...")
        if search_query:
            mask = df['Terjemahan'].str.contains(search_query, case=False, na=False)
            results = df[mask]
            st.info(f"Ditemukan {len(results)} hadist yang cocok.")
            
            for _, row in results.head(20).iterrows():
                highlighted_text = row['Terjemahan'].replace(
                    search_query, f'<span class="search-highlight">{search_query}</span>'
                )
                st.markdown(f"""
                <div class="hadith-card">
                    <p class="hadith-meta"><strong>Perawi:</strong> {row['Perawi']} | <strong>Topik:</strong> {int(row['topic'])}</p>
                    <p class="hadith-content">{highlighted_text}</p>
                </div>
                """, unsafe_allow_html=True)

    elif search_type == "Topik":
        available_topics = sorted([t for t in df['topic'].unique() if t != -1])
        selected_topic = st.selectbox("Pilih Topik:", available_topics)
        if selected_topic is not None:
            results = df[df['topic'] == selected_topic]
            st.info(f"Menampilkan {len(results)} hadist dari Topik {selected_topic}.")
            for _, row in results.head(20).iterrows():
                st.markdown(f"""
                <div class="hadith-card">
                    <p class="hadith-meta"><strong>Perawi:</strong> {row['Perawi']}</p>
                    <p class="hadith-content">{row['Terjemahan']}</p>
                </div>
                """, unsafe_allow_html=True)

    elif search_type == "Perawi":
        available_perawi = sorted(df['Perawi'].unique())
        selected_perawi = st.selectbox("Pilih Perawi:", available_perawi)
        if selected_perawi:
            results = df[df['Perawi'] == selected_perawi]
            st.info(f"Menampilkan {len(results)} hadist dari {selected_perawi}.")
            for _, row in results.head(20).iterrows():
                st.markdown(f"""
                <div class="hadith-card">
                    <p class="hadith-meta"><strong>Topik:</strong> {int(row['topic'])}</p>
                    <p class="hadith-content">{row['Terjemahan']}</p>
                </div>
                """, unsafe_allow_html=True)

def show_analysis_page(df):
    """Menampilkan halaman analisis data mendalam."""
    st.markdown("## 📈 Analisis Mendalam")
    
    tab1, tab2, tab3 = st.tabs(["Distribusi Topik", "Analisis Perawi", "Statistik Kluster"])

    with tab1:
        st.markdown("### Sebaran Hadist di Seluruh Topik")
        topic_counts = df[df['topic'] != -1]['topic'].value_counts()
        fig = px.histogram(
            x=topic_counts.values,
            nbins=20,
            title="Distribusi Ukuran Topik (Jumlah Hadist per Topik)",
            labels={'x': 'Jumlah Hadist dalam Topik', 'y': 'Frekuensi (Jumlah Topik)'},
            color_discrete_sequence=[st.get_option("theme.primaryColor")]
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"Rata-rata terdapat **{topic_counts.mean():.1f}** hadist per topik, dengan topik terbesar berisi **{topic_counts.max()}** hadist dan yang terkecil **{topic_counts.min()}** hadist.")


    with tab2:
        st.markdown("### Keragaman Perawi Antar Topik")
        perawi_per_topic = df[df['topic'] != -1].groupby('topic')['Perawi'].nunique()
        fig = px.scatter(
            x=perawi_per_topic.index,
            y=perawi_per_topic.values,
            size=perawi_per_topic.values,
            color=perawi_per_topic.values,
            color_continuous_scale='Plasma',
            title="Keragaman Perawi per Topik",
            labels={'x': 'Nomor Topik', 'y': 'Jumlah Perawi Unik', 'color': 'Jumlah Perawi Unik'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(type='category')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("Setiap titik merepresentasikan sebuah topik. Ukuran dan warna titik menunjukkan jumlah perawi unik yang hadistnya ada di dalam topik tersebut.")

    with tab3:
        st.markdown("### Statistik Detail Kluster")
        topic_stats = df[df['topic'] != -1].groupby('topic').agg(
            jumlah_hadist=('Terjemahan', 'count'),
            jumlah_perawi=('Perawi', 'nunique')
        ).reset_index()
        
        # Kode yang Direkomendasikan
        try:
            # Coba tampilkan dengan gradasi warna
            st.dataframe(
                topic_stats.style.background_gradient(cmap='viridis'),
                use_container_width=True
            )
        except ImportError:
            # Jika matplotlib tidak ada, tampilkan tabel biasa
            st.warning("Matplotlib tidak terinstal. Menampilkan tabel tanpa pewarnaan gradien.")
            st.dataframe(topic_stats, use_container_width=True)
        st.info("Tabel di atas menunjukkan jumlah hadist dan jumlah perawi unik untuk setiap topik yang berhasil diidentifikasi.")


# ======================================================================================
# FUNGSI MAIN()
# ======================================================================================

def main():
    """Fungsi utama untuk menjalankan aplikasi Streamlit."""
    df = load_data()
    if df is None:
        st.warning("Silakan unggah atau perbaiki file data untuk melanjutkan.")
        st.stop()
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown('<p class="sidebar-header">🧭 Navigasi</p>', unsafe_allow_html=True)
        page = st.radio(
            "Pilih Halaman:",
            ["🏠 Dasbor Utama", "🔍 Pencarian", "📈 Analisis"],
            label_visibility="collapsed"
        )
        st.markdown("---")
        st.markdown("#### ℹ️ Tentang Aplikasi")
        st.info(
            "Aplikasi ini menggunakan model clustering untuk mengelompokkan hadist berdasarkan "
            "kemiripan teks terjemahannya. Tujuannya adalah untuk membantu analisis dan "
            "eksplorasi koleksi hadist dalam jumlah besar."
        )

    # Hero Section - Tampil di semua halaman
    create_hero_section(df)

    # Page Routing
    if page == "🏠 Dasbor Utama":
        show_main_dashboard(df)
    elif page == "🔍 Pencarian":
        show_search_page(df)
    elif page == "📈 Analisis":
        show_analysis_page(df)

if __name__ == "__main__":
    main()