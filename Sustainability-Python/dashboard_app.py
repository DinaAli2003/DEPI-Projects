import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import warnings

# Ignore Matplotlib and Seaborn warnings related to styles
warnings.filterwarnings("ignore")

# ====================================================================
# ⚠️ STREAMLIT PAGE CONFIGURATION (MUST BE FIRST STREAMLIT COMMAND)
# ====================================================================
st.set_page_config(
    page_title="Sustainability Dashboard", 
    layout="wide",
    page_icon="🌱",
    initial_sidebar_state="expanded"
) 

# ====================================================================
# REVOLUTIONARY CSS STYLING - GUARANTEED CONTAINMENT
# ====================================================================
def apply_custom_css():
    st.markdown("""
    <style>
    /* Complete background - consistent green theme */
    .stApp {
        background: linear-gradient(135deg, #F0F9F0 0%, #E8F5E8 50%, #F0F9F0 100%) !important;
    }
    
    /* Remove all white containers and ensure consistent background */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        background: transparent !important;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #1B5E20 0%, #388E3C 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(27, 94, 32, 0.3);
    }
    
    /* KPI metrics styling - enhanced green cards */
    [data-testid="stMetricValue"] {
        color: #1B5E20 !important;
        font-weight: bold !important;
        font-size: 1.5rem !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #2E7D32 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 100%) !important;
        padding: 15px !important;
        border-radius: 12px !important;
        border-left: 5px solid #4CAF50 !important;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2) !important;
        margin: 5px !important;
        height: 120px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }
    
    /* Tab styling - complete green theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #C8E6C9 !important;
        border-radius: 8px 8px 0px 0px;
        padding: 12px 20px;
        font-weight: 600;
        color: #1B5E20 !important;
        border: 1px solid #A5D6A7;
        margin: 0 2px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%) !important;
        color: white !important;
        border-bottom: 3px solid #1B5E20;
    }
    
    /* REVOLUTIONARY CHART CONTAINMENT SYSTEM */
    .chart-container {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FDF8 100%) !important;
        padding: 25px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(27, 94, 32, 0.15) !important;
        border: 1px solid #C8E6C9 !important;
        margin-bottom: 25px !important;
        transition: transform 0.2s ease !important;
        height: 500px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
        overflow: visible !important;
    }
    
    .chart-container:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(27, 94, 32, 0.2) !important;
    }
    
    /* FORCE CHART TO STAY INSIDE CONTAINER */
    .chart-container > .element-container {
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
    }
    
    .chart-container .stPyplot {
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
    }
    
    .chart-container .stPyplot figure {
        width: 95% !important;
        height: 95% !important;
        margin: 0 auto !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .chart-container .stPyplot canvas {
        max-width: 100% !important;
        max-height: 100% !important;
        object-fit: contain !important;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
        color: #1B5E20;
    }
    
    /* Footer styling */
    .footer {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-top: 2rem;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%) !important;
    }
    
    .stSidebar label, .stSidebar p, .stSidebar div, .stSidebar span {
        color: #FFFFFF !important;
    }
    
    .filter-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Ensure columns work properly */
    [data-testid="column"] {
        padding: 10px !important;
    }
    
    /* Remove any default margins/padding that might separate containers */
    div[data-testid="stVerticalBlock"] > div {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Apply the custom CSS
apply_custom_css()

# ====================================================================
# 0. Helper Functions and Data Loading
# ====================================================================
@st.cache_data
def load_raw_data():
    try:
        df = pd.read_csv('Sustainability-Python/Sustainability_Raw_Data.csv')
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
        if 'certification' in df.columns:
            df['certification'] = df['certification'].fillna('None').astype(str)
        return df
    except FileNotFoundError:
        st.error("❌ Error: 'Sustainability_Raw_Data.csv' not found.")
        return pd.DataFrame() 
    except Exception as e:
        st.error(f"❌ An error occurred during data loading: {e}")
        return pd.DataFrame() 

def safe_kpi_calc(series, func, rounding=2):
    """Calculates KPI safely, returning 'N/A' on error or empty data."""
    if series.empty or not pd.api.types.is_numeric_dtype(series):
        return "N/A"
    try:
        result = func(series.dropna())
        if isinstance(result, (int, float)):
            return round(result, rounding)
        return "N/A"
    except Exception:
        return "N/A"

# ====================================================================
# 1. VISUALIZATION FUNCTIONS WITH GUARANTEED CONTAINMENT
# ====================================================================

# Set global green color palette
GREEN_PALETTE = ['#1B5E20', '#2E7D32', '#388E3C', '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7']
sns.set_palette(GREEN_PALETTE)

def create_contained_figure(df, title, func, figsize=(7, 5)):
    """Create figures that are guaranteed to stay in their containers"""
    if df.empty: 
        return None
    try:
        # Create figure with optimal size for containers
        fig, ax = plt.subplots(figsize=figsize)
        
        # Set transparent background
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        
        # Apply the plotting function
        func(fig, ax, df) 
        
        # Professional styling
        ax.set_title(title, fontsize=16, color='#1B5E20', fontweight='bold', pad=15)
        ax.set_xlabel(ax.get_xlabel(), fontsize=12, color='#2E7D32', fontweight='600')
        ax.set_ylabel(ax.get_ylabel(), fontsize=12, color='#2E7D32', fontweight='600')
        ax.tick_params(colors='#388E3C', labelsize=10)
        
        for spine in ax.spines.values():
            spine.set_color('#4CAF50')
            spine.set_linewidth(1.5)
            
        ax.grid(True, alpha=0.2, color='#C8E6C9')
        
        # Ultra-tight layout for perfect container fit
        plt.tight_layout(pad=3.0)
        return fig
    except Exception as e:
        st.error(f"Chart error: {e}")
        return None

# Plotting functions
def plot_top_brands(df_brands): 
    def plot_func(fig, ax, df):
        colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
        bars = ax.bar(df["brand_name"], df["sustainability_rating"], color=colors, 
                      edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
        
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{bar.get_height():.2f}', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1B5E20')
        
        ax.set_xlabel("Brand Name", fontsize=12, fontweight='600')
        ax.set_ylabel("Sustainability Rating", fontsize=12, fontweight='600')
        ax.set_xticklabels(df["brand_name"], rotation=45, ha='right', fontsize=10)
        ax.set_ylim(0, df["sustainability_rating"].max() * 1.15)
    
    return create_contained_figure(df_brands, "Top 10 Sustainable Brands", plot_func, figsize=(8, 5))

def plot_top_product_lines(df_categories): 
    def plot_func(fig, ax, df):
        colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
        bars = ax.bar(df["product_line"], df["sustainability_rating"], 
                      color=colors, edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
        
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{bar.get_height():.2f}', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1B5E20')
        
        ax.set_xlabel("Product Line", fontsize=12, fontweight='600')
        ax.set_ylabel("Sustainability Rating", fontsize=12, fontweight='600')
        ax.set_xticklabels(df["product_line"], rotation=45, ha='right', fontsize=10)
        ax.set_ylim(0, df["sustainability_rating"].max() * 1.15)
    
    return create_contained_figure(df_categories, "Top 5 Sustainable Product Lines", plot_func, figsize=(7, 5))

def plot_top_countries(df_countries):
    def plot_func(fig, ax, df):
        colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
        bars = ax.bar(df["country_name"], df["sustainability_rating"], 
                      color=colors, edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
        
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f"{bar.get_height():.2f}", 
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1B5E20')
        
        ax.set_xlabel("Country", fontsize=12, fontweight='600')
        ax.set_ylabel("Sustainability Rating", fontsize=12, fontweight='600')
        ax.set_xticklabels(df["country_name"], rotation=45, ha='right', fontsize=10)
        ax.set_ylim(0, df["sustainability_rating"].max() * 1.15)
    
    return create_contained_figure(df_countries, "Top 5 Countries by Sustainability", plot_func, figsize=(7, 5))

def plot_time_improvement(df_time_avg): 
    def plot_func(fig, ax, df):
        sns.lineplot(data=df, x='year', y='avg_rating', marker='o', color='#2E7D32', 
                    linewidth=3, markersize=8, ax=ax, markerfacecolor='#1B5E20')
        
        for x, y in zip(df['year'], df['avg_rating']):
            ax.text(x, y + 0.005, f"{y:.2f}", ha='center', fontsize=10, fontweight='bold', color='#1B5E20')
        
        ax.set_xlabel("Year", fontsize=12, fontweight='600')
        ax.set_ylabel("Average Sustainability Rating", fontsize=12, fontweight='600')
        ax.set_xticks(df['year'])
        ax.grid(True, alpha=0.3, color='#C8E6C9')
        ax.set_ylim(df['avg_rating'].min() * 0.95, df['avg_rating'].max() * 1.05)
    
    return create_contained_figure(df_time_avg, "Sustainability Trend Over Years", plot_func, figsize=(7, 5))

# ====================================================================
# 2. STREAMLIT APP WITH GUARANTEED CHART CONTAINMENT
# ====================================================================

def main():
    # Load Data
    df = load_raw_data()
    if df.empty:
        return

    # Header
    st.markdown("""
    <div class="main-header">
        <div style="text-align: center;">
            <h1 style="margin: 0; font-size: 2.8rem; color: white;">🌱 Sustainability Analytics Dashboard</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.3rem; opacity: 0.95;">Comprehensive Environmental Impact & Sustainable Performance Tracking</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Filters
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #1B5E20 0%, #388E3C 100%); 
                padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; text-align: center;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">📊 Dashboard Filters</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
    df_filtered = df.copy()
    
    # Simple filters
    if 'country_name' in df.columns:
        countries = st.sidebar.multiselect("🌍 Select Countries:", options=sorted(df['country_name'].unique()))
        if countries:
            df_filtered = df_filtered[df_filtered['country_name'].isin(countries)]
    
    if 'year' in df.columns:
        years = st.sidebar.multiselect("📅 Select Years:", options=sorted(df['year'].unique()))
        if years:
            df_filtered = df_filtered[df_filtered['year'].isin(years)]
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Data summary
    st.sidebar.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px;">
        <h4 style="color: white; margin: 0 0 10px 0;">📈 Data Summary</h4>
        <p style="color: #E8F5E8; margin: 5px 0;">Total Records: <strong>{len(df_filtered):,}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Use filtered data or fallback
    df_to_use = df_filtered if not df_filtered.empty else df

    # Calculate insights
    df_top_brands = pd.DataFrame()
    if 'brand_name' in df_to_use.columns and 'sustainability_rating' in df_to_use.columns and not df_to_use.empty:
        df_top_brands = (
            df_to_use.groupby("brand_name")["sustainability_rating"].mean().round(2).reset_index()
            .sort_values(by="sustainability_rating", ascending=False).head(10))

    df_top_categories = pd.DataFrame()
    if 'product_line' in df_to_use.columns and 'sustainability_rating' in df_to_use.columns and not df_to_use.empty:
        df_top_categories = (
            df_to_use.groupby("product_line")["sustainability_rating"].mean().round(2).reset_index()
            .sort_values(by="sustainability_rating", ascending=False).head(5))

    df_top_countries = pd.DataFrame()
    if 'country_name' in df_to_use.columns and 'sustainability_rating' in df_to_use.columns and not df_to_use.empty:
        df_top_countries = (
            df_to_use.groupby("country_name")["sustainability_rating"].mean().round(2).reset_index()
            .sort_values(by="sustainability_rating", ascending=False).head(5))

    df_avg_time = pd.DataFrame()
    if 'year' in df_to_use.columns and 'sustainability_rating' in df_to_use.columns and not df_to_use.empty:
        df_avg_time = df_to_use.groupby('year')['sustainability_rating'].mean().reset_index(name='avg_rating')

    # KPIs
    st.markdown('<div class="section-header"><h3>📊 Key Performance Indicators</h3></div>', unsafe_allow_html=True)
    
    avg_price = safe_kpi_calc(df_to_use.get('average_price', pd.Series()), np.mean)
    avg_rating = safe_kpi_calc(df_to_use.get('sustainability_rating', pd.Series()), np.mean)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Average Price", f"{avg_price:,.2f}" if isinstance(avg_price, (int, float)) else avg_price)
    with col2:
        st.metric("📈 Avg Sustainability", f"{avg_rating:.2f}" if isinstance(avg_rating, (int, float)) else avg_rating)
    with col3:
        st.metric("📊 Total Records", f"{len(df_to_use):,}")
    with col4:
        st.metric("🌍 Countries", len(df_to_use['country_name'].unique()) if 'country_name' in df_to_use.columns else "N/A")
    
    st.markdown("---")

    # Tabs with GUARANTEED CONTAINMENT
    tab1, tab2, tab3 = st.tabs(["🏆 Top Performance", "🌍 Geographic Analysis", "📈 Trends Over Time"])
    
    # REVOLUTIONARY DISPLAY FUNCTION - GUARANTEES CONTAINMENT
    def display_chart_guaranteed(fig, col=None):
        """Display chart with 100% guaranteed container containment"""
        if fig is not None:
            if col:
                with col:
                    # Create container and immediately put chart inside
                    container_html = """
                    <div class="chart-container">
                    """
                    st.markdown(container_html, unsafe_allow_html=True)
                    st.pyplot(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            else:
                # Create container and immediately put chart inside
                container_html = """
                <div class="chart-container">
                """
                st.markdown(container_html, unsafe_allow_html=True)
                st.pyplot(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # Tab 1: Top Performance
    with tab1:
        st.markdown('<div class="section-header"><h3>🏆 Top Sustainable Performers</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # These charts WILL stay in their containers
        top_brands_chart = plot_top_brands(df_top_brands)
        top_categories_chart = plot_top_product_lines(df_top_categories)
        
        if top_brands_chart is not None:
            display_chart_guaranteed(top_brands_chart, col1)
        
        if top_categories_chart is not None:
            display_chart_guaranteed(top_categories_chart, col2)

    # Tab 2: Geographic Analysis
    with tab2:
        st.markdown('<div class="section-header"><h3>🌍 Geographic Sustainability Analysis</h3></div>', unsafe_allow_html=True)
        
        countries_chart = plot_top_countries(df_top_countries)
        if countries_chart is not None:
            display_chart_guaranteed(countries_chart)

    # Tab 3: Trends
    with tab3:
        st.markdown('<div class="section-header"><h3>📈 Sustainability Trends Over Time</h3></div>', unsafe_allow_html=True)
        
        time_chart = plot_time_improvement(df_avg_time)
        if time_chart is not None:
            display_chart_guaranteed(time_chart)

    # Footer
    st.markdown("""
    <div class="footer">
        <h4 style="margin: 0; color: white;">🌍 Sustainability Analytics Dashboard</h4>
        <p style="margin: 5px 0 0 0; color: #E8F5E8;">Driving Sustainable Business Decisions • Powered by Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
