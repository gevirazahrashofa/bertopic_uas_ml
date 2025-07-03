import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Dashboard Clustering Hadist",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .hadith-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #2E86AB;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    .stSelectbox > div > div {
        background-color: #f0f2f6;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load preprocessed data"""
    try:
        df = pd.read_csv('hadits_with_topics.csv')
        return df
    except FileNotFoundError:
        st.error("❌ File 'hadits_with_topics.csv' tidak ditemukan!")
        return None

def main():
    st.markdown('<h1 class="main-header">📚 Dashboard Clustering Hadist</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigasi")
    page = st.sidebar.radio(
        "Pilih Halaman:",
        ["📊 Dashboard Utama", "🔍 Pencarian Hadist", "📈 Visualisasi Data"]
    )
    
    if page == "📊 Dashboard Utama":
        show_main_dashboard(df)
    elif page == "🔍 Pencarian Hadist":
        show_search_page(df)
    elif page == "📈 Visualisasi Data":
        show_visualization_page(df)

def show_main_dashboard(df):
    """Main dashboard with key metrics and overview"""
    st.header("📊 Ringkasan Data")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_hadits = len(df)
    total_topics = len(df['topic'].unique()) - (1 if -1 in df['topic'].unique() else 0)
    clustered = len(df[df['topic'] != -1])
    success_rate = (clustered / total_hadits) * 100
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📚 Total Hadist</h3>
            <h2>{total_hadits:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏷️ Jumlah Topik</h3>
            <h2>{total_topics}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ Terkluster</h3>
            <h2>{clustered:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈 Tingkat Sukses</h3>
            <h2>{success_rate:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sample hadits from top topics
    st.subheader("📖 Contoh Hadist dari Topik Teratas")
    top_topic = df['topic'].value_counts().index[0]
    sample_hadits = df[df['topic'] == top_topic].head(3)
    
    for idx, row in sample_hadits.iterrows():
        st.markdown(f"""
        <div class="hadith-card">
            <h4>📝 Hadist dari Topik {row['topic']}</h4>
            <p><strong>Perawi:</strong> {row['Perawi']}</p>
            <p><strong>Terjemahan:</strong> {row['Terjemahan'][:200]}...</p>
        </div>
        """, unsafe_allow_html=True)

def show_search_page(df):
    """Search functionality"""
    st.header("🔍 Pencarian Hadist")
    
    # Search options
    search_type = st.selectbox(
        "Pilih jenis pencarian:",
        ["🔤 Kata Kunci", "🏷️ Topik", "👤 Perawi"]
    )
    
    if search_type == "🔤 Kata Kunci":
        search_query = st.text_input("🔍 Masukkan kata kunci:", placeholder="Contoh: shalat, puasa, zakat")
        
        if search_query:
            # Search in text
            mask = df['Terjemahan'].str.contains(search_query, case=False, na=False)
            results = df[mask]
            
            st.success(f"✅ Ditemukan {len(results)} hadist yang mengandung '{search_query}'")
            
            if len(results) > 0:
                # Show results with pagination
                results_per_page = 5
                total_pages = (len(results) - 1) // results_per_page + 1
                
                if total_pages > 1:
                    page_num = st.selectbox("Pilih halaman:", range(1, total_pages + 1))
                    start_idx = (page_num - 1) * results_per_page
                    end_idx = start_idx + results_per_page
                    page_results = results.iloc[start_idx:end_idx]
                else:
                    page_results = results.head(results_per_page)
                
                for idx, row in page_results.iterrows():
                    st.markdown(f"""
                    <div class="hadith-card">
                        <h4>📝 Hadist #{idx + 1} - Topik {row['topic']}</h4>
                        <p><strong>Perawi:</strong> {row['Perawi']}</p>
                        <p><strong>Terjemahan:</strong> {row['Terjemahan']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif search_type == "🏷️ Topik":
        available_topics = sorted([t for t in df['topic'].unique() if t != -1])
        selected_topic = st.selectbox("Pilih topik:", available_topics)
        
        if selected_topic is not None:
            results = df[df['topic'] == selected_topic]
            st.success(f"✅ Ditemukan {len(results)} hadist dalam topik {selected_topic}")
            
            # Show sample results
            for idx, row in results.head(5).iterrows():
                st.markdown(f"""
                <div class="hadith-card">
                    <h4>📝 Hadist #{idx + 1}</h4>
                    <p><strong>Perawi:</strong> {row['Perawi']}</p>
                    <p><strong>Terjemahan:</strong> {row['Terjemahan']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif search_type == "👤 Perawi":
        available_perawi = sorted(df['Perawi'].unique())
        selected_perawi = st.selectbox("Pilih perawi:", available_perawi)
        
        if selected_perawi:
            results = df[df['Perawi'] == selected_perawi]
            st.success(f"✅ Ditemukan {len(results)} hadist dari {selected_perawi}")
            
            # Show sample results
            for idx, row in results.head(5).iterrows():
                st.markdown(f"""
                <div class="hadith-card">
                    <h4>📝 Hadist #{idx + 1} - Topik {row['topic']}</h4>
                    <p><strong>Terjemahan:</strong> {row['Terjemahan']}</p>
                </div>
                """, unsafe_allow_html=True)

def show_visualization_page(df):
    """Data visualization page"""
    st.header("📈 Visualisasi Data")
    
    # Topic distribution
    st.subheader("📊 Analisis Distribusi Topik")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Topic size histogram
        topic_counts = df['topic'].value_counts()
        topic_sizes = [count for topic, count in topic_counts.items() if topic != -1]
        
        fig = px.histogram(
            x=topic_sizes,
            nbins=15,
            title="Distribusi Ukuran Topik",
            labels={'x': 'Ukuran Topik (Jumlah Hadist)', 'y': 'Frekuensi'},
            color_discrete_sequence=['#2E86AB']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top perawi
        top_perawi = df['Perawi'].value_counts().head(10)
        
        fig = px.bar(
            x=top_perawi.values,
            y=top_perawi.index,
            orientation='h',
            title="Top 10 Perawi dengan Hadist Terbanyak",
            color=top_perawi.values,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Interactive scatter plot
    st.subheader("🎯 Analisis Clustering")
    
    # Create scatter plot of topics vs hadith count
    topic_stats = df.groupby('topic').agg({
        'Terjemahan': 'count',
        'Perawi': 'nunique'
    }).rename(columns={'Terjemahan': 'jumlah_hadist', 'Perawi': 'jumlah_perawi'})
    
    fig = px.scatter(
        topic_stats,
        x='jumlah_hadist',
        y='jumlah_perawi',
        title="Hubungan Jumlah Hadist dan Jumlah Perawi per Topik",
        labels={'jumlah_hadist': 'Jumlah Hadist', 'jumlah_perawi': 'Jumlah Perawi'},
        color='jumlah_hadist',
        size='jumlah_hadist',
        hover_data=['jumlah_hadist', 'jumlah_perawi']
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics
    st.subheader("📊 Statistik Ringkasan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Rata-rata Hadist per Topik", f"{topic_stats['jumlah_hadist'].mean():.1f}")
    
    with col2:
        st.metric("Topik Terbesar", f"{topic_stats['jumlah_hadist'].max()} hadist")
    
    with col3:
        st.metric("Topik Terkecil", f"{topic_stats['jumlah_hadist'].min()} hadist")

if __name__ == "__main__":
    main()