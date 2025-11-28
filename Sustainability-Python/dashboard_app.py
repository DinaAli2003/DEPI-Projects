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
# 2. Main Streamlit App - Expertly Styled
# ====================================================================
def main():
    # 1. Load Raw Data
    df = load_raw_data()
    if df.empty:
        return

    # --- Streamlit Styling (Expert Layout & Colors) ---
    st.markdown(
        """
        <style>
        /* Overall background */
        .stApp { background-color: #E6F2E6; font-family: 'Arial', sans-serif; }

        /* Sidebar background and filters */
        div[data-testid="stSidebar"] { background-color: #DFF0D8; padding: 10px; }
        div[data-baseweb="select"] > div { background-color: #E6F2E6 !important; color: black; border-radius: 6px; padding: 5px; }

        /* Sidebar title */
        .css-1d391kg { color: black; font-weight: bold; }

        /* Tabs styling */
        .css-1lcbmhc.e1fqkh3o4 { color: black; font-weight: bold; font-size: 16px; }
        .stTabs [role="tab"] { padding: 6px 10px; }

        /* KPI metric values */
        .stMetricValue { color: #1B5E20 !important; font-weight: bold; }

        /* Compact layout adjustments */
        .css-1d391kg, .stTextInput>div>input { font-size: 14px; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Header with Logos ---
    header_cols = st.columns([1, 5, 1])
    with header_cols[0]:
        st.image("Sustainability-Python/logo_ministry.png", width=90)
    with header_cols[1]:
        st.markdown("<h1 style='text-align:center; color:#1B5E20; font-weight:bold'>Sustainability Dashboard</h1>", unsafe_allow_html=True)
    with header_cols[2]:
        st.image("Sustainability-Python/logo_project.png", width=90)
    st.markdown("---")

    # ----------------------------------------------------
    # Sidebar Filters
    # ----------------------------------------------------
    st.sidebar.title("Filters")  
    df_filtered = df.copy()

    def get_filter_options(column_name):
        if column_name in df.columns:
            options = sorted(df[column_name].dropna().unique().tolist())
            return options, options
        return [], []

    selected_countries = st.sidebar.multiselect("Country:", *get_filter_options('country_name'))
    selected_years = st.sidebar.multiselect("Year:", *get_filter_options('year'))
    selected_certifications = st.sidebar.multiselect("Certification:", *get_filter_options('certification'))
    selected_product_lines = st.sidebar.multiselect("Product Line:", *get_filter_options('product_line'))
    selected_brands = st.sidebar.multiselect("Brand:", *get_filter_options('brand_name'))

    # Apply filters safely
    if selected_countries and 'country_name' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['country_name'].isin(selected_countries)]
    if selected_years and 'year' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['year'].isin(selected_years)]
    if selected_certifications and 'certification' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['certification'].isin(selected_certifications)]
    if selected_product_lines and 'product_line' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['product_line'].isin(selected_product_lines)]
    if selected_brands and 'brand_name' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['brand_name'].isin(selected_brands)]

    if df_filtered.empty:
        st.warning("⚠️ No data matches the current filters. Displaying full data as fallback.")
        df_to_use_for_insights = df.copy()
    else:
        df_to_use_for_insights = df_filtered.copy()

    # ----------------------------------------------------
    # KPIs (Compact & Friendly)
    # ----------------------------------------------------
    avg_price = safe_kpi_calc(df_to_use_for_insights.get('average_price', pd.Series()), np.mean)
    avg_carbon = safe_kpi_calc(df_to_use_for_insights.get('carbon_footprint', pd.Series()), np.mean)
    avg_water = safe_kpi_calc(df_to_use_for_insights.get('water_usage', pd.Series()), np.mean, rounding=0)
    avg_waste = safe_kpi_calc(df_to_use_for_insights.get('waste_production', pd.Series()), np.mean)
    min_sus_rating = safe_kpi_calc(df_to_use_for_insights.get('sustainability_rating', pd.Series()), np.min)
    max_sus_rating = safe_kpi_calc(df_to_use_for_insights.get('sustainability_rating', pd.Series()), np.max)

    kpi_cols = st.columns(6, gap="small")
    kpi_cols[0].metric("💰 AVG PRICE", f"{avg_price:,.2f}" if isinstance(avg_price, (int, float)) else avg_price)
    kpi_cols[1].metric("🏭 AVG CARBON", f"{avg_carbon:.2f}" if isinstance(avg_carbon, (int, float)) else avg_carbon)
    kpi_cols[2].metric("💧 AVG WATER", f"{avg_water:,.0f}" if isinstance(avg_water, (int, float)) else avg_water)
    kpi_cols[3].metric("🗑️ AVG WASTE", f"{avg_waste:.2f}" if isinstance(avg_waste, (int, float)) else avg_waste)
    kpi_cols[4].metric("⭐ MIN SUS RATING", f"{min_sus_rating}")
    kpi_cols[5].metric("🌟 MAX SUS RATING", f"{max_sus_rating}")

    st.markdown("---")

    # ----------------------------------------------------
    # Tabs (Black font, bold, clean layout)
    # ----------------------------------------------------
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Top Performance", 
        "Geographic & Material", 
        "Trends Over Time", 
        "Environmental Metrics", 
        "Price & Audience", 
        "Certifications"
    ])

    # --- Tab 1: Top Performance ---
    with tab1:
        if 'brand_name' in df_to_use_for_insights.columns and 'sustainability_rating' in df_to_use_for_insights.columns:
            df_top_brands = df_to_use_for_insights.groupby("brand_name")["sustainability_rating"].mean().reset_index().sort_values("sustainability_rating", ascending=False).head(10)
            st.pyplot(plot_top_brands(df_top_brands))
        if 'product_line' in df_to_use_for_insights.columns and 'sustainability_rating' in df_to_use_for_insights.columns:
            df_top_categories = df_to_use_for_insights.groupby("product_line")["sustainability_rating"].mean().reset_index().sort_values("sustainability_rating", ascending=False).head(5)
            st.pyplot(plot_top_product_lines(df_top_categories))

    # --- Tab 2: Geographic & Material Impact ---
    with tab2:
        if 'country_name' in df_to_use_for_insights.columns and 'sustainability_rating' in df_to_use_for_insights.columns:
            df_top_countries = df_to_use_for_insights.groupby("country_name")["sustainability_rating"].mean().reset_index().sort_values("sustainability_rating", ascending=False).head(5)
            st.pyplot(plot_top_countries(df_top_countries))
        if 'material_status' in df_to_use_for_insights.columns and 'sustainability_rating' in df_to_use_for_insights.columns:
            material_sus = df_to_use_for_insights.groupby('material_status')['sustainability_rating'].mean().reset_index()
            st.pyplot(plot_material_status(material_sus))

    # --- Tab 3: Trends Over Time ---
    with tab3:
        if 'year' in df_to_use_for_insights.columns and 'sustainability_rating' in df_to_use_for_insights.columns:
            df_time_avg = df_to_use_for_insights.groupby('year')['sustainability_rating'].mean().reset_index(name='avg_rating')
            st.pyplot(plot_time_improvement(df_time_avg))
        if 'market_trend' in df_to_use_for_insights.columns and 'sustainability_rating' in df_to_use_for_insights.columns:
            trend_avg = df_to_use_for_insights.groupby('market_trend')['sustainability_rating'].mean().reset_index()
            st.pyplot(plot_market_trend(trend_avg))

    # --- Tab 4: Environmental Metrics ---
    with tab4:
        env_cols = ['waste_production', 'water_usage', 'carbon_footprint']
        if all(col in df_to_use_for_insights.columns for col in env_cols + ['product_line']):
            df_melted = df_to_use_for_insights.groupby('product_line')[env_cols].mean().reset_index().melt(id_vars='product_line', var_name='Metric', value_name='Average Value')
            st.pyplot(plot_environmental_metrics(df_melted))

    # --- Tab 5: Price & Audience ---
    with tab5:
        if all(col in df_to_use_for_insights.columns for col in ['average_price', 'sustainability_rating', 'brand_category']):
            st.pyplot(plot_price_vs_sustainability(df_to_use_for_insights))
        if 'target_audience' in df_to_use_for_insights.columns and 'sustainability_rating' in df_to_use_for_insights.columns:
            audience_sus = df_to_use_for_insights.groupby('target_audience')['sustainability_rating'].mean().reset_index()
            st.pyplot(plot_audience_sustainability(audience_sus))

    # --- Tab 6: Certifications ---
    with tab6:
        if 'product_line' in df_to_use_for_insights.columns and 'certification' in df_to_use_for_insights.columns:
            cert_count = df_to_use_for_insights.groupby('product_line')['certification'].count().reset_index().rename(columns={'certification':'num_certification'})
            st.pyplot(plot_certifications_per_product(cert_count))
        if 'certification' in df_to_use_for_insights.columns and 'sustainability_rating' in df_to_use_for_insights.columns:
            cert_avg = df_to_use_for_insights.groupby('certification')['sustainability_rating'].mean().reset_index().rename(columns={'sustainability_rating':'avg_rating'})
            st.pyplot(plot_certification_impact(cert_avg))
        if 'eco_friendly_manufacturing' in df_to_use_for_insights.columns:
            eco_counts = df_to_use_for_insights['eco_friendly_manufacturing'].value_counts()
            st.pyplot(plot_eco_friendly_counts(eco_counts))

# Run the main function
if __name__ == "__main__":
    main()
