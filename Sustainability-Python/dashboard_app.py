import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import warnings
import os

warnings.filterwarnings("ignore")

# ====================================================================
# ⚠️ STREAMLIT PAGE CONFIGURATION
# ====================================================================
st.set_page_config(page_title="Sustainability Dashboard", layout="wide")

# ====================================================================
# 0. Helper Functions
# ====================================================================
@st.cache_data
def load_raw_data():
    try:
        df = pd.read_csv("Sustainability-Python/Sustainability_Raw_Data.csv")  
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
    if series.empty or not pd.api.types.is_numeric_dtype(series):
        return "N/A"
    try:
        result = func(series.dropna())
        if isinstance(result, (int, float)):
            return round(result, rounding)
        return "N/A"
    except Exception:
        return "N/A"

def create_figure(df, title, func, figsize=(6,3.5)):
    if df.empty: return None
    try:
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        func(fig, ax, df)
        ax.set_title(title, fontsize=12, color='#1B5E20', fontweight='bold', pad=10)
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.25)
        return fig
    except Exception:
        return None

# --- Visualization Functions (examples: top brands, top products, countries, etc.) ---
# You can keep your previous plot_* functions here
# Make sure the figsize is slightly smaller (e.g., width=6-7, height=3-4)
# Ensure colors use lighter greens (#DFF0D8, #E6F2E6, #1B5E20, etc.)

# ====================================================================
# 1. Main Streamlit App
# ====================================================================
def main():
    # Load Data
    df = load_raw_data()
    if df.empty: return

    # Streamlit styling
    st.markdown("""
    <style>
    .stApp { background-color: #E6F2E6; font-family: 'Arial', sans-serif; }
    .block-container { padding-top: 1rem; padding-left:1rem; padding-right:1rem; padding-bottom:1rem; }
    div[data-testid="stSidebar"] { background-color: #DFF0D8; padding:15px; }
    div[data-testid="stSidebar"] .css-1lcbmhc.e1fqkh3o4 { color:black; font-weight:bold; }
    div[data-baseweb="select"] > div { background-color:#E6F2E6 !important; color:black !important; border-radius:6px; padding:5px; }
    .stTabs [role="tab"] { color:black !important; font-weight:bold; font-size:16px; background-color:#E6F2E6 !important; }
    .stTabs [role="tab"]:hover { background-color:#DFF0D8 !important; }
    .stTabs [role="tab"][data-selected="true"] { background-color:#DFF0D8 !important; color:black !important; font-weight:bold; }
    .stMetricValue { color:#1B5E20 !important; font-weight:bold; }
    h1 { color:#1B5E20 !important; font-weight:bold; text-align:center; }
    </style>
    """, unsafe_allow_html=True)

    # Header
    header_cols = st.columns([1,5,1])
    with header_cols[0]: st.image("Sustainability-Python/logo_ministry.png", width=90)
    with header_cols[1]: st.markdown("<h1>Sustainability Dashboard</h1>", unsafe_allow_html=True)
    with header_cols[2]: st.image("Sustainability-Python/logo_project.png", width=90)
    st.markdown("---")

    # Sidebar Filters
    st.sidebar.title("Filters")
    df_filtered = df.copy()
    def get_filter_options(col):
        if col in df.columns: options = sorted(df[col].dropna().unique().tolist()); return options, options
        return [], []
    selected_countries = st.sidebar.multiselect("Country:", *get_filter_options('country_name'))
    selected_years = st.sidebar.multiselect("Year:", *get_filter_options('year'))
    selected_certifications = st.sidebar.multiselect("Certification:", *get_filter_options('certification'))
    selected_product_lines = st.sidebar.multiselect("Product Line:", *get_filter_options('product_line'))
    selected_brands = st.sidebar.multiselect("Brand:", *get_filter_options('brand_name'))

    # Apply filters
    if selected_countries: df_filtered = df_filtered[df_filtered['country_name'].isin(selected_countries)]
    if selected_years: df_filtered = df_filtered[df_filtered['year'].isin(selected_years)]
    if selected_certifications: df_filtered = df_filtered[df_filtered['certification'].isin(selected_certifications)]
    if selected_product_lines: df_filtered = df_filtered[df_filtered['product_line'].isin(selected_product_lines)]
    if selected_brands: df_filtered = df_filtered[df_filtered['brand_name'].isin(selected_brands)]
    df_to_use = df_filtered if not df_filtered.empty else df.copy()
    if df_filtered.empty: st.warning("⚠️ No data matches filters. Showing full data.")

    # KPIs
    avg_price = safe_kpi_calc(df_to_use.get('average_price', pd.Series()), np.mean)
    avg_carbon = safe_kpi_calc(df_to_use.get('carbon_footprint', pd.Series()), np.mean)
    avg_water = safe_kpi_calc(df_to_use.get('water_usage', pd.Series()), np.mean, rounding=0)
    avg_waste = safe_kpi_calc(df_to_use.get('waste_production', pd.Series()), np.mean)
    min_sus_rating = safe_kpi_calc(df_to_use.get('sustainability_rating', pd.Series()), np.min)
    max_sus_rating = safe_kpi_calc(df_to_use.get('sustainability_rating', pd.Series()), np.max)

    kpi_cols = st.columns(6, gap="small")
    kpi_cols[0].metric("💰 AVG PRICE", f"{avg_price:,.2f}" if isinstance(avg_price,(int,float)) else avg_price)
    kpi_cols[1].metric("🏭 AVG CARBON", f"{avg_carbon:.2f}" if isinstance(avg_carbon,(int,float)) else avg_carbon)
    kpi_cols[2].metric("💧 AVG WATER", f"{avg_water:,.0f}" if isinstance(avg_water,(int,float)) else avg_water)
    kpi_cols[3].metric("🗑️ AVG WASTE", f"{avg_waste:.2f}" if isinstance(avg_waste,(int,float)) else avg_waste)
    kpi_cols[4].metric("⭐ MIN SUS RATING", f"{min_sus_rating}")
    kpi_cols[5].metric("🌟 MAX SUS RATING", f"{max_sus_rating}")
    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Top Performance","Geographic & Material","Trends Over Time",
        "Environmental Metrics","Price & Audience","Certifications"
    ])

    # --- Tab 1: Top Performance ---
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig_top_brands = plot_top_brands(df_to_use)
            if fig_top_brands: st.pyplot(fig_top_brands, clear_figure=True)
        with col2:
            fig_top_products = plot_top_product_lines(df_to_use)
            if fig_top_products: st.pyplot(fig_top_products, clear_figure=True)

    # --- Tab 2: Geographic & Material ---
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            fig_top_countries = plot_top_countries(df_to_use)
            if fig_top_countries: st.pyplot(fig_top_countries, clear_figure=True)
        with col2:
            fig_material_status = plot_material_status(df_to_use)
            if fig_material_status: st.pyplot(fig_material_status, clear_figure=True)

    # --- Tab 3: Trends Over Time ---
    with tab3:
        fig_trends_time = plot_time_improvement(df_to_use)
        if fig_trends_time: st.pyplot(fig_trends_time, clear_figure=True)
        fig_market_trend = plot_market_trend(df_to_use)
        if fig_market_trend: st.pyplot(fig_market_trend, clear_figure=True)

    # --- Tab 4: Environmental Metrics ---
    with tab4:
        fig_env_metrics = plot_environmental_metrics(df_to_use)
        if fig_env_metrics: st.pyplot(fig_env_metrics, clear_figure=True)
        fig_cert_per_product = plot_certifications_per_product(df_to_use)
        if fig_cert_per_product: st.pyplot(fig_cert_per_product, clear_figure=True)

    # --- Tab 5: Price & Audience ---
    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            fig_price_vs_sus = plot_price_vs_sustainability(df_to_use)
            if fig_price_vs_sus: st.pyplot(fig_price_vs_sus, clear_figure=True)
        with col2:
            fig_audience_sus = plot_audience_sustainability(df_to_use)
            if fig_audience_sus: st.pyplot(fig_audience_sus, clear_figure=True)

    # --- Tab 6: Certifications ---
    with tab6:
        fig_cert_impact = plot_certification_impact(df_to_use)
        if fig_cert_impact: st.pyplot(fig_cert_impact, clear_figure=True)
        fig_eco_counts = plot_eco_friendly_counts(df_to_use.get('eco_friendly_manufacturing', pd.Series()))
        if fig_eco_counts: st.pyplot(fig_eco_counts, clear_figure=True)

# Run main
if __name__ == "__main__":
    main()
