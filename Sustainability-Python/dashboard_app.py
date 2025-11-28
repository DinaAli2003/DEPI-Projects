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
# SIMPLIFIED CSS - FOCUSED ON CHART CONTAINMENT
# ====================================================================
def apply_custom_css():
    st.markdown("""
    <style>
    /* Clean background */
    .stApp {
        background: linear-gradient(135deg, #F0F9F0 0%, #E8F5E8 50%, #F0F9F0 100%);
    }
    
    /* Remove default padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        background: transparent;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
    }
    
    .stSidebar label, .stSidebar p, .stSidebar div, .stSidebar span {
        color: #FFFFFF !important;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1B5E20 0%, #388E3C 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(27, 94, 32, 0.3);
    }
    
    /* KPI metrics styling */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 100%);
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
        margin: 5px;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab"] {
        background-color: #C8E6C9;
        border-radius: 8px 8px 0px 0px;
        padding: 12px 20px;
        font-weight: 600;
        color: #1B5E20;
        border: 1px solid #A5D6A7;
        margin: 0 2px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%);
        color: white;
        border-bottom: 3px solid #1B5E20;
    }
    
    /* PERFECT CHART CONTAINMENT - SIMPLIFIED APPROACH */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #C8E6C9;
        box-shadow: 0 4px 12px rgba(27, 94, 32, 0.15);
        margin-bottom: 20px;
        position: relative;
    }
    
    .chart-title {
        font-size: 16px;
        font-weight: bold;
        color: #1B5E20;
        margin-bottom: 15px;
        text-align: center;
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
    
    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-top: 2rem;
    }
    
    /* Filter section */
    .filter-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Apply the custom CSS
apply_custom_css()

# ====================================================================
# 0. Helper Functions and Data Loading (Initial Data Prep)
# ====================================================================
@st.cache_data
def load_raw_data():
    try:
        df = pd.read_csv('Sustainability-Python/Sustainability_Raw_Data.csv')
        # Standardize column names for safe processing
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('[^a-z0-9_]', '', regex=True)
        # Ensure 'year' is numeric and handle potential errors
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)
            
        if 'certification' in df.columns:
            df['certification'] = df['certification'].fillna('None').astype(str)

        return df
    except FileNotFoundError:
        st.error("❌ Error: 'Sustainability_Raw_Data.csv' not found. Please ensure it's in the same folder.")
        return pd.DataFrame() 
    except Exception as e:
        st.error(f"❌ An error occurred during data loading: {e}")
        return pd.DataFrame() 

# --- Helper Function for Safe KPI Calculation ---
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
# 1. SIMPLIFIED VISUALIZATION FUNCTIONS (FIXED CONTAINMENT)
# ====================================================================

# Set global green color palette
GREEN_PALETTE = ['#1B5E20', '#2E7D32', '#388E3C', '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7']
sns.set_palette(GREEN_PALETTE)

def create_chart_figure(title, plotting_function, data, figsize=(6, 4)):
    """Simplified figure creation with proper containment"""
    if data.empty: 
        return None
    try:
        # Create figure with tight layout
        fig, ax = plt.subplots(figsize=figsize)
        
        # Apply the plotting function
        plotting_function(ax, data)
        
        # Professional styling
        ax.set_title(title, fontsize=14, color='#1B5E20', fontweight='bold', pad=12)
        ax.grid(True, alpha=0.2, color='#C8E6C9')
        
        # Tight layout for perfect fit
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Chart error: {e}")
        return None

# Simplified plotting functions
def plot_top_brands(ax, df):
    colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
    bars = ax.bar(df["brand_name"], df["sustainability_rating"], color=colors, 
                  edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
    
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{bar.get_height():.2f}', 
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1B5E20')
    
    ax.set_xlabel("Brand Name", fontsize=11, fontweight='600')
    ax.set_ylabel("Sustainability Rating", fontsize=11, fontweight='600')
    rotation_angle = 45 if max([len(str(label)) for label in df["brand_name"]]) > 8 else 30
    ax.set_xticklabels(df["brand_name"], rotation=rotation_angle, ha='right', fontsize=9)
    ax.set_ylim(0, df["sustainability_rating"].max() * 1.15)

def plot_top_product_lines(ax, df):
    colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
    bars = ax.bar(df["product_line"], df["sustainability_rating"], 
                  color=colors, edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
    
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{bar.get_height():.2f}', 
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1B5E20')
    
    ax.set_xlabel("Product Line", fontsize=11, fontweight='600')
    ax.set_ylabel("Sustainability Rating", fontsize=11, fontweight='600')
    rotation_angle = 45 if max([len(str(label)) for label in df["product_line"]]) > 10 else 30
    ax.set_xticklabels(df["product_line"], rotation=rotation_angle, ha='right', fontsize=10)
    ax.set_ylim(0, df["sustainability_rating"].max() * 1.15)

def plot_top_countries(ax, df):
    colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
    bars = ax.bar(df["country_name"], df["sustainability_rating"], 
                  color=colors, edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
    
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f"{bar.get_height():.2f}", 
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1B5E20')
    
    ax.set_xlabel("Country", fontsize=11, fontweight='600')
    ax.set_ylabel("Sustainability Rating", fontsize=11, fontweight='600')
    ax.set_xticklabels(df["country_name"], rotation=25, ha='right', fontsize=10)
    ax.set_ylim(0, df["sustainability_rating"].max() * 1.15)

def plot_certifications_per_product(ax, df):
    colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
    bars = ax.bar(df['product_line'], df['num_certification'], color=colors, 
                  edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
    
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, str(int(bar.get_height())), 
                ha='center', va='bottom', fontsize=9, color='#1B5E20', fontweight='bold')
    
    ax.set_xlabel('Product Line', fontsize=11, fontweight='600')
    ax.set_ylabel('Number of Certifications', fontsize=11, fontweight='600')
    ax.tick_params(axis='x', rotation=30, labelsize=9)

def plot_environmental_metrics(ax, df):
    sns.barplot(data=df, x='product_line', y='Average Value', hue='Metric', 
               palette=['#1B5E20', '#388E3C', '#4CAF50'], ax=ax, alpha=0.9)
    
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f', label_type='edge', fontsize=8, 
                     color='#1B5E20', fontweight='bold', padding=3)
    
    ax.set_xlabel('Product Line', fontsize=11, fontweight='600')
    ax.set_ylabel('Average Value', fontsize=11, fontweight='600')
    ax.tick_params(axis='x', rotation=30, labelsize=9)
    ax.legend(title='Environmental Metric', title_fontsize=10, fontsize=9)

def plot_time_improvement(ax, df):
    sns.lineplot(data=df, x='year', y='avg_rating', marker='o', color='#2E7D32', 
                linewidth=3, markersize=8, ax=ax, markerfacecolor='#1B5E20')
    
    for x, y in zip(df['year'], df['avg_rating']):
        ax.text(x, y + 0.005, f"{y:.2f}", ha='center', fontsize=9, fontweight='bold', 
                color='#1B5E20')
    
    ax.set_xlabel("Year", fontsize=11, fontweight='600')
    ax.set_ylabel("Average Sustainability Rating", fontsize=11, fontweight='600')
    ax.set_xticks(df['year'])
    ax.tick_params(axis='x', rotation=0, labelsize=10)
    ax.grid(True, alpha=0.3, color='#C8E6C9')
    ax.set_ylim(df['avg_rating'].min() * 0.95, df['avg_rating'].max() * 1.05)

def plot_audience_sustainability(ax, df):
    colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
    bars = sns.barplot(data=df, x='target_audience', y='sustainability_rating', 
                       palette=colors, ax=ax, alpha=0.9)
    
    for index, row in df.iterrows():
        ax.text(index, row['sustainability_rating'] + 0.008, f"{row['sustainability_rating']:.3f}", 
                ha='center', fontsize=9, fontweight='bold', color='#1B5E20')
    
    ax.set_xlabel('Target Audience', fontsize=11, fontweight='600')
    ax.set_ylabel('Sustainability Rating', fontsize=11, fontweight='600')
    ax.tick_params(axis='x', rotation=15, labelsize=9)

def plot_material_status(df_material_sus):
    if df_material_sus.empty or len(df_material_sus) < 2:
        return None
        
    fig, ax = plt.subplots(figsize=(5, 4))
    colors = GREEN_PALETTE[:len(df_material_sus)]
    
    wedges, texts, autotexts = ax.pie(df_material_sus['sustainability_rating'], 
                           labels=df_material_sus['material_status'], 
                           autopct='%1.1f%%',
                           startangle=90, colors=colors)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Sustainability by Material Status', fontsize=13, color='#1B5E20', fontweight='bold')
    plt.tight_layout()
    return fig

def plot_eco_friendly_counts(eco_counts_series):
    if eco_counts_series.empty or len(eco_counts_series) < 2: 
        return None

    fig, ax = plt.subplots(figsize=(5, 4))
    colors = ['#A5D6A7', '#1B5E20'][:len(eco_counts_series)]
    labels = ['Non Eco-friendly', 'Eco-friendly'][:len(eco_counts_series)]
    
    wedges, texts, autotexts = ax.pie(eco_counts_series.values, 
           labels=labels, 
           autopct='%1.1f%%', 
           colors=colors, 
           startangle=90)
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title("Eco-friendly Manufacturing", fontsize=13, color='#1B5E20', fontweight='bold')
    plt.tight_layout()
    return fig

def plot_price_vs_sustainability(ax, df):
    sns.scatterplot(data=df, x="average_price", y="sustainability_rating", 
                   hue="brand_category", palette=GREEN_PALETTE, alpha=0.8, s=80, 
                   edgecolor="white", linewidth=1, ax=ax)
    ax.set_xlabel("Average Price ($)", fontsize=11, fontweight='600')
    ax.set_ylabel("Sustainability Rating", fontsize=11, fontweight='600')
    ax.legend(title="Brand Category", title_fontsize=10, fontsize=9)

def plot_certification_impact(ax, df):
    colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
    barplot = sns.barplot(data=df, x="certification", y="avg_rating", 
                          palette=colors, ax=ax, alpha=0.9)
    
    for p in barplot.patches:
        barplot.annotate(f"{p.get_height():.3f}", (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='bottom', fontsize=9, fontweight='bold', 
                        color='#1B5E20', xytext=(0, 5), textcoords='offset points')
    
    ax.set_xlabel("Certification Type", fontsize=11, fontweight='600')
    ax.set_ylabel("Average Sustainability Rating", fontsize=11, fontweight='600')
    ax.tick_params(axis='x', rotation=45, labelsize=9)

def plot_market_trend(df_trend_avg):
    if df_trend_avg.empty or len(df_trend_avg) < 2:
        return None
        
    fig, ax = plt.subplots(figsize=(5, 4))
    colors = GREEN_PALETTE[:len(df_trend_avg)]
    
    wedges, texts, autotexts = ax.pie(
        df_trend_avg["sustainability_rating"],
        labels=df_trend_avg["market_trend"],
        autopct=lambda p: f'{p:.1f}%', 
        startangle=140,
        colors=colors
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title("Market Trend Analysis", fontsize=13, color="#1B5E20", fontweight="bold")
    plt.tight_layout()
    return fig

# ====================================================================
# SIMPLIFIED CHART DISPLAY FUNCTION
# ====================================================================
def display_chart(fig, title, col=None):
    """Display chart with perfect container alignment"""
    if fig is None:
        return
        
    container = f"""
    <div class="chart-container">
        <div class="chart-title">{title}</div>
    </div>
    """
    
    if col:
        with col:
            st.markdown(container, unsafe_allow_html=True)
            st.pyplot(fig, use_container_width=True)
    else:
        st.markdown(container, unsafe_allow_html=True)
        st.pyplot(fig, use_container_width=True)

# ====================================================================
# 2. SIMPLIFIED STREAMLIT APP
# ====================================================================

def main():
    # 1. Load Raw Data
    df = load_raw_data()

    if df.empty:
        return

    # --- Enhanced Header ---
    st.markdown("""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; gap: 25px; text-align: center;">
            <div>
                <h1 style="margin: 0; font-size: 2.8rem; color: white;">🌱 Sustainability Analytics Dashboard</h1>
                <p style="margin: 10px 0 0 0; font-size: 1.3rem; opacity: 0.95;">Comprehensive Environmental Impact & Sustainable Performance Tracking</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ----------------------------------------------------
    # 2. Simplified Filtering Section
    # ----------------------------------------------------
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #1B5E20 0%, #388E3C 100%); 
                padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; text-align: center;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">📊 Dashboard Filters</h2>
        <p style="color: #E8F5E8; margin: 5px 0 0 0; font-size: 0.9rem;">Customize your sustainability analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter container
    st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
    
    # Initialize df_filtered with a copy of the original df
    df_filtered = df.copy() 
    
    # Helper to get unique options and set default
    def get_filter_options(column_name):
        if column_name in df.columns:
            options = sorted(df[column_name].unique().tolist())
            return options, options[:min(5, len(options))]  # Limit default selections
        return [], []

    # Filters
    country_options, default_countries = get_filter_options('country_name')
    selected_countries = st.sidebar.multiselect(
        "🌍 Select Countries:", 
        options=country_options, 
        default=default_countries
    )
    if selected_countries:
        df_filtered = df_filtered[df_filtered['country_name'].isin(selected_countries)]
    
    year_options, default_years = get_filter_options('year')
    selected_years = st.sidebar.multiselect(
        "📅 Select Years:", 
        options=year_options, 
        default=default_years
    )
    if selected_years:
        df_filtered = df_filtered[df_filtered['year'].isin(selected_years)]

    certification_options, default_certifications = get_filter_options('certification')
    selected_certifications = st.sidebar.multiselect(
        "🏆 Select Certifications:", 
        options=certification_options, 
        default=default_certifications
    )
    if selected_certifications:
        df_filtered = df_filtered[df_filtered['certification'].isin(selected_certifications)]
    
    product_line_options, default_product_lines = get_filter_options('product_line')
    selected_product_lines = st.sidebar.multiselect(
        "📦 Select Product Lines:", 
        options=product_line_options, 
        default=default_product_lines
    )
    if selected_product_lines:
        df_filtered = df_filtered[df_filtered['product_line'].isin(selected_product_lines)]

    brand_options, default_brands = get_filter_options('brand_name')
    selected_brands = st.sidebar.multiselect(
        "🏢 Select Brands:", 
        options=brand_options, 
        default=default_brands
    )
    if selected_brands:
        df_filtered = df_filtered[df_filtered['brand_name'].isin(selected_brands)]

    # Close filter container
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # Reset filters button
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()

    # Data summary
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
        <h4 style="color: white; margin: 0 0 10px 0;">📈 Data Summary</h4>
        <p style="color: #E8F5E8; margin: 5px 0;">Total Records: <strong>{len(df_filtered):,}</strong></p>
        <p style="color: #E8F5E8; margin: 5px 0;">Filtered from: <strong>{len(df):,}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Fallback if no data matches filters
    if df_filtered.empty:
        st.warning("⚠️ No data matches the current filters. Displaying global data.")
        df_to_use_for_insights = df.copy()
    else:
        df_to_use_for_insights = df_filtered.copy()

    # ----------------------------------------------------
    # 3. Calculate all Insights
    # ----------------------------------------------------
    available_cols_for_insights = df_to_use_for_insights.columns.tolist()

    # Calculate insights (same as before)
    df_top_brands = pd.DataFrame()
    if 'brand_name' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_top_brands = (
            df_to_use_for_insights.groupby("brand_name")["sustainability_rating"].mean().round(2).reset_index()
            .sort_values(by="sustainability_rating", ascending=False).head(10))

    df_top_categories = pd.DataFrame()
    if 'product_line' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_top_categories = (
            df_to_use_for_insights.groupby("product_line")["sustainability_rating"].mean().round(2).reset_index()
            .sort_values(by="sustainability_rating", ascending=False).head(5))

    df_top_countries = pd.DataFrame()
    if 'country_name' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_top_countries = (
            df_to_use_for_insights.groupby("country_name")["sustainability_rating"].mean().round(2).reset_index()
            .sort_values(by="sustainability_rating", ascending=False).head(5))
    
    df_category_cert = pd.DataFrame()
    if 'product_line' in available_cols_for_insights and 'certification' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_category_cert = (
            df_to_use_for_insights.groupby("product_line")["certification"].count().reset_index()
            .rename(columns={"certification": "num_certification"})
            .sort_values(by="num_certification", ascending=False))
    
    df_melted = pd.DataFrame()
    env_cols = ['waste_production', 'water_usage', 'carbon_footprint']
    if all(col in available_cols_for_insights for col in env_cols) and 'product_line' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_avg = df_to_use_for_insights.groupby('product_line')[env_cols].mean().reset_index()
        df_melted = df_avg.melt(id_vars='product_line', value_vars=env_cols, var_name='Metric', value_name='Average Value')
    
    df_avg_time = pd.DataFrame()
    if 'year' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_avg_time = df_to_use_for_insights.groupby('year')['sustainability_rating'].mean().reset_index(name='avg_rating')
    
    audience_sustainability = pd.DataFrame()
    if 'target_audience' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        audience_sustainability = df_to_use_for_insights.groupby('target_audience')['sustainability_rating'].mean().round(3).reset_index().sort_values(by='sustainability_rating', ascending=False)
    
    material_sustainability = pd.DataFrame()
    if 'material_status' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        material_sustainability = df_to_use_for_insights.groupby('material_status')['sustainability_rating'].mean().round(3).reset_index().sort_values(by='sustainability_rating', ascending=False)
    
    eco_counts = pd.Series()
    if 'eco_friendly_manufacturing' in available_cols_for_insights and not df_to_use_for_insights.empty:
        eco_counts = df_to_use_for_insights['eco_friendly_manufacturing'].value_counts()
    
    df_price_vs_sus = pd.DataFrame()
    if all(col in available_cols_for_insights for col in ['average_price', 'sustainability_rating', 'brand_category']) and not df_to_use_for_insights.empty:
        df_price_vs_sus = df_to_use_for_insights.copy() 
    
    certification_avg = pd.DataFrame()
    if 'certification' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        certification_avg = df_to_use_for_insights.groupby("certification", as_index=False).agg(avg_rating=("sustainability_rating", "mean")).round(3).sort_values("avg_rating", ascending=False)
    
    trend_avg = pd.DataFrame()
    if 'market_trend' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        trend_avg = (
            df_to_use_for_insights.groupby("market_trend", as_index=False)["sustainability_rating"]
            .mean()
            .sort_values("sustainability_rating", ascending=False)
        )

    # ----------------------------------------------------
    # 4. KPI Section
    # ----------------------------------------------------
    # Calculate KPIs
    avg_price = safe_kpi_calc(df_to_use_for_insights.get('average_price', pd.Series()), np.mean)
    avg_carbon = safe_kpi_calc(df_to_use_for_insights.get('carbon_footprint', pd.Series()), np.mean)
    avg_water = safe_kpi_calc(df_to_use_for_insights.get('water_usage', pd.Series()), np.mean, rounding=0)
    avg_waste = safe_kpi_calc(df_to_use_for_insights.get('waste_production', pd.Series()), np.mean)
    min_sus_rating = safe_kpi_calc(df_to_use_for_insights.get('sustainability_rating', pd.Series()), np.min)
    max_sus_rating = safe_kpi_calc(df_to_use_for_insights.get('sustainability_rating', pd.Series()), np.max)
    avg_sus_rating = safe_kpi_calc(df_to_use_for_insights.get('sustainability_rating', pd.Series()), np.mean)

    # Display KPIs
    st.markdown('<div class="section-header"><h3>📊 Key Performance Indicators</h3></div>', unsafe_allow_html=True)
    
    kpi_cols = st.columns(7)

    with kpi_cols[0]:
        st.metric(
            label="💰 Average Price",
            value=f"{avg_price:,.2f}" if isinstance(avg_price, (int, float)) else avg_price
        )
    with kpi_cols[1]:
        st.metric(
            label="🏭 Carbon Footprint",
            value=f"{avg_carbon:.2f}" if isinstance(avg_carbon, (int, float)) else avg_carbon
        ) 
    with kpi_cols[2]:
        st.metric(
            label="💧 Water Usage",
            value=f"{avg_water:,.0f}" if isinstance(avg_water, (int, float)) else avg_water
        ) 
    with kpi_cols[3]:
        st.metric(
            label="🗑️ Waste Production",
            value=f"{avg_waste:.2f}" if isinstance(avg_waste, (int, float)) else avg_waste
        ) 
    with kpi_cols[4]:
        st.metric(
            label="⭐️ Min Rating",
            value=f"{min_sus_rating:.2f}" if isinstance(min_sus_rating, (int, float)) else min_sus_rating
        )
    with kpi_cols[5]:
        st.metric(
            label="🌟 Max Rating",
            value=f"{max_sus_rating:.2f}" if isinstance(max_sus_rating, (int, float)) else max_sus_rating
        )
    with kpi_cols[6]:
        st.metric(
            label="📈 Avg Rating",
            value=f"{avg_sus_rating:.2f}" if isinstance(avg_sus_rating, (int, float)) else avg_sus_rating
        )
    
    st.markdown("---")

    # --- SIMPLIFIED TABS WITH PERFECT CONTAINMENT ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏆 Top Performance", 
        "🌍 Geographic & Material", 
        "📈 Trends Over Time", 
        "🌱 Environmental Metrics", 
        "💰 Market Analysis", 
        "🏅 Certifications"
    ])
    
    # ====================================================
    # Tab 1: Top Performance
    # ====================================================
    with tab1:
        st.markdown('<div class="section-header"><h3>🏆 Top Sustainable Performers Analysis</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Create and display charts
        if not df_top_brands.empty:
            fig_brands = create_chart_figure("Top 10 Sustainable Brands", plot_top_brands, df_top_brands, figsize=(7, 4))
            display_chart(fig_brands, "Top 10 Sustainable Brands", col1)
        
        if not df_top_categories.empty:
            fig_categories = create_chart_figure("Top 5 Sustainable Product Lines", plot_top_product_lines, df_top_categories, figsize=(6, 4))
            display_chart(fig_categories, "Top 5 Sustainable Product Lines", col2)

    # ====================================================
    # Tab 2: Geographic & Material
    # ====================================================
    with tab2:
        st.markdown('<div class="section-header"><h3>🌍 Geographic & Material Impact Analysis</h3></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        # Countries chart
        if not df_top_countries.empty:
            fig_countries = create_chart_figure("Top 5 Countries by Sustainability", plot_top_countries, df_top_countries, figsize=(6, 4))
            display_chart(fig_countries, "Top 5 Countries by Sustainability", col1)
        
        # Material status chart
        if not material_sustainability.empty:
            fig_material = plot_material_status(material_sustainability)
            display_chart(fig_material, "Sustainability by Material Status", col2)
        
        # Eco-friendly chart
        if not eco_counts.empty:
            fig_eco = plot_eco_friendly_counts(eco_counts)
            display_chart(fig_eco, "Eco-friendly Manufacturing", col3)

    # ====================================================
    # Tab 3: Trends Over Time
    # ====================================================
    with tab3:
        st.markdown('<div class="section-header"><h3>📈 Sustainability Trends & Market Analysis</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        # Time trend chart
        if not df_avg_time.empty:
            fig_time = create_chart_figure("Sustainability Trend Over Years", plot_time_improvement, df_avg_time, figsize=(7, 4))
            display_chart(fig_time, "Sustainability Trend Over Years", col1)
        
        # Market trend chart
        if not trend_avg.empty:
            fig_trend = plot_market_trend(trend_avg)
            display_chart(fig_trend, "Market Trend Analysis", col2)

    # ====================================================
    # Tab 4: Environmental Metrics
    # ====================================================
    with tab4:
        st.markdown('<div class="section-header"><h3>🌱 Core Environmental Metrics Analysis</h3></div>', unsafe_allow_html=True)
        
        # Environmental metrics chart
        if not df_melted.empty:
            fig_env = create_chart_figure("Environmental Metrics by Product Line", plot_environmental_metrics, df_melted, figsize=(8, 4))
            display_chart(fig_env, "Environmental Metrics by Product Line")
        
    # ====================================================
    # Tab 5: Price & Audience
    # ====================================================
    with tab5:
        st.markdown('<div class="section-header"><h3>💰 Market & Customer Analysis</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Price vs sustainability chart
        if not df_price_vs_sus.empty:
            fig_price = create_chart_figure("Price vs Sustainability Rating", plot_price_vs_sustainability, df_price_vs_sus, figsize=(7, 4))
            display_chart(fig_price, "Price vs Sustainability Rating", col1)
        
        # Audience sustainability chart
        if not audience_sustainability.empty:
            fig_audience = create_chart_figure("Sustainability by Target Audience", plot_audience_sustainability, audience_sustainability, figsize=(6, 4))
            display_chart(fig_audience, "Sustainability by Target Audience", col2)
    
    # ====================================================
    # Tab 6: Certifications
    # ====================================================
    with tab6:
        st.markdown('<div class="section-header"><h3>🏅 Certification Impact Analysis</h3></div>', unsafe_allow_html=True)
        
        # Certification impact chart
        if not certification_avg.empty:
            fig_cert_impact = create_chart_figure("Certification Impact on Rating", plot_certification_impact, certification_avg, figsize=(7, 4))
            display_chart(fig_cert_impact, "Certification Impact on Rating")
        
        # Certifications per product chart
        if not df_category_cert.empty:
            st.markdown("---")
            fig_cert_count = create_chart_figure("Certifications per Product Line", plot_certifications_per_product, df_category_cert, figsize=(6, 4))
            display_chart(fig_cert_count, "Certifications per Product Line")

    # Enhanced Footer
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div style="text-align: left;">
                <h4 style="margin: 0; color: white;">🌍 Sustainability Analytics Dashboard</h4>
                <p style="margin: 5px 0 0 0; color: #E8F5E8; font-size: 0.9rem;">Driving Sustainable Business Decisions</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0; color: #E8F5E8; font-size: 0.9rem;">📅 Last Updated: 2024</p>
                <p style="margin: 5px 0 0 0; color: #E8F5E8; font-size: 0.9rem;">📊 Powered by Streamlit</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Run the main function
if __name__ == "__main__":
    main()
