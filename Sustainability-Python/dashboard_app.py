import streamlit as st
import pandas as pd
import numpy as np
from utils import load_raw_data, safe_kpi_calc
from plots import (
    plot_top_brands, plot_top_product_lines, plot_top_countries, 
    plot_eco_friendly_counts, plot_time_improvement, plot_market_trend,
    plot_environmental_metrics, plot_price_vs_sustainability, 
    plot_audience_sustainability, plot_certification_impact,
    plot_certifications_per_product
)

# -------------------------------
# CSS Styling
# -------------------------------
st.markdown(
    """
    <style>
    /* تغيير خلفية الموقع بالكامل */
    .stApp {
        background-color: #e6f4ea !important;  /* أخضر فاتح هادئ */
    }
    [data-testid="stSidebar"] {
        background-color: #c8e6c9 !important; 
    }
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label {
        color: #1b5e20 !important; 
        font-weight: 600;
    }
    .stMultiSelect div[data-baseweb="tag"] {
        background-color: #1b5e20 !important; 
        color: white !important;
    }
    .stMultiSelect div[role="listbox"] {
        background-color: #e8f5e9 !important;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: #c8e6c9 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# Main Function
# -------------------------------
def main():
    # 1. Load Raw Data
    df = load_raw_data()
    if df.empty:
        st.warning("⚠️ No data loaded.")
        return

    # --- Header with Logos ---
    col_logo1, col_title, col_logo2 = st.columns([1, 4, 1])
    with col_logo1:
        st.image("Sustainability-Python/logo_ministry.png", width=100)
    with col_title:
        st.title("Sustainability Dashboard")
    with col_logo2:
        st.image("Sustainability-Python/logo_project.png", width=100)
    st.markdown("---")

    # -------------------------------
    # 2. Sidebar Filters
    # -------------------------------
    st.sidebar.title("Filter")
    df_filtered = df.copy()

    def get_filter_options(column_name):
        if column_name in df.columns:
            options = sorted(df[column_name].unique().tolist())
            return options, options
        return [], []

    # Countries Filter
    country_options, default_countries = get_filter_options('country_name')
    selected_countries = st.sidebar.multiselect("Select Country:", options=country_options, default=default_countries)
    if selected_countries:
        df_filtered = df_filtered[df_filtered['country_name'].isin(selected_countries)]

    # Years Filter
    year_options, default_years = get_filter_options('year')
    selected_years = st.sidebar.multiselect("Select Year:", options=year_options, default=default_years)
    if selected_years:
        df_filtered = df_filtered[df_filtered['year'].isin(selected_years)]

    # Certifications Filter
    certification_options, default_certifications = get_filter_options('certification')
    selected_certifications = st.sidebar.multiselect("Select Certification:", options=certification_options, default=default_certifications)
    if selected_certifications:
        df_filtered = df_filtered[df_filtered['certification'].isin(selected_certifications)]

    # Product Lines Filter
    product_line_options, default_product_lines = get_filter_options('product_line')
    selected_product_lines = st.sidebar.multiselect("Select Product Line:", options=product_line_options, default=default_product_lines)
    if selected_product_lines:
        df_filtered = df_filtered[df_filtered['product_line'].isin(selected_product_lines)]

    # Brands Filter
    brand_options, default_brands = get_filter_options('brand_name')
    selected_brands = st.sidebar.multiselect("Select Sustainable Brand:", options=brand_options, default=default_brands)
    if selected_brands:
        df_filtered = df_filtered[df_filtered['brand_name'].isin(selected_brands)]

    # Fallback if no data matches filters
    if df_filtered.empty:
        st.warning("⚠️ No data matches the current filters. Using full dataset as fallback.")
        df_to_use_for_insights = df.copy()
    else:
        df_to_use_for_insights = df_filtered.copy()

    # -------------------------------
    # 3. Insights Calculations
    # -------------------------------
    available_cols_for_insights = df_to_use_for_insights.columns.tolist()

    # Top 10 Sustainable Brands
    df_top_brands = pd.DataFrame()
    if 'brand_name' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_top_brands = (
            df_to_use_for_insights.groupby("brand_name")["sustainability_rating"]
            .mean().round(2).reset_index()
            .sort_values(by="sustainability_rating", ascending=False)
            .head(10)
        )

    # Top 5 Product Lines
    df_top_categories = pd.DataFrame()
    if 'product_line' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_top_categories = (
            df_to_use_for_insights.groupby("product_line")["sustainability_rating"]
            .mean().round(2).reset_index()
            .sort_values(by="sustainability_rating", ascending=False)
            .head(5)
        )

    # Top 5 Countries
    df_top_countries = pd.DataFrame()
    if 'country_name' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_top_countries = (
            df_to_use_for_insights.groupby("country_name")["sustainability_rating"]
            .mean().round(2).reset_index()
            .sort_values(by="sustainability_rating", ascending=False)
            .head(5)
        )

    # Certifications per Product line
    df_category_cert = pd.DataFrame()
    if 'product_line' in available_cols_for_insights and 'certification' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_category_cert = (
            df_to_use_for_insights.groupby("product_line")["certification"]
            .count().reset_index()
            .rename(columns={"certification": "num_certification"})
            .sort_values(by="num_certification", ascending=False)
        )

    # Environmental Metrics
    df_melted = pd.DataFrame()
    env_cols = ['waste_production', 'water_usage', 'carbon_footprint']
    if all(col in available_cols_for_insights for col in env_cols) and 'product_line' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_avg = df_to_use_for_insights.groupby('product_line')[env_cols].mean().reset_index()
        df_melted = df_avg.melt(id_vars='product_line', value_vars=env_cols, var_name='Metric', value_name='Average Value')

    # Time Improvement
    df_avg_time = pd.DataFrame()
    if 'year' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        df_avg_time = df_to_use_for_insights.groupby('year')['sustainability_rating'].mean().reset_index(name='avg_rating')

    # Audience Sustainability
    audience_sustainability = pd.DataFrame()
    if 'target_audience' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        audience_sustainability = df_to_use_for_insights.groupby('target_audience')['sustainability_rating'].mean().round(3).reset_index().sort_values(by='sustainability_rating', ascending=False)

    # Material Status
    material_sustainability = pd.DataFrame(columns=['material_status', 'sustainability_rating', 'label'])
    if 'material_status' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        material_sustainability = df_to_use_for_insights.groupby('material_status')['sustainability_rating'].mean().round(3).reset_index().sort_values(by='sustainability_rating', ascending=False)
        if not material_sustainability.empty:
            material_sustainability['label'] = material_sustainability['material_status'] + ' (' + material_sustainability['sustainability_rating'].astype(str) + ')'

    # Eco-Friendly Counts
    eco_counts = pd.Series()
    if 'eco_friendly_manufacturing' in available_cols_for_insights and not df_to_use_for_insights.empty:
        eco_counts = df_to_use_for_insights['eco_friendly_manufacturing'].value_counts()

    # Price vs Sustainability
    df_price_vs_sus = pd.DataFrame()
    if all(col in available_cols_for_insights for col in ['average_price', 'sustainability_rating', 'brand_category']) and not df_to_use_for_insights.empty:
        df_price_vs_sus = df_to_use_for_insights.copy()

    # Certification Impact
    certification_avg = pd.DataFrame()
    if 'certification' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        certification_avg = df_to_use_for_insights.groupby("certification", as_index=False).agg(avg_rating=("sustainability_rating", "mean")).round(3).sort_values("avg_rating", ascending=False)

    # Market Trend
    trend_avg = pd.DataFrame()
    if 'market_trend' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        trend_avg = df_to_use_for_insights.groupby("market_trend", as_index=False)["sustainability_rating"].mean().sort_values("sustainability_rating", ascending=False)

    # -------------------------------
    # 4. KPIs
    # -------------------------------
    avg_price = safe_kpi_calc(df_to_use_for_insights.get('average_price', pd.Series()), np.mean)
    avg_carbon = safe_kpi_calc(df_to_use_for_insights.get('carbon_footprint', pd.Series()), np.mean)
    avg_water = safe_kpi_calc(df_to_use_for_insights.get('water_usage', pd.Series()), np.mean, rounding=0)
    avg_waste = safe_kpi_calc(df_to_use_for_insights.get('waste_production', pd.Series()), np.mean)
    min_sus_rating = safe_kpi_calc(df_to_use_for_insights.get('sustainability_rating', pd.Series()), np.min)
    max_sus_rating = safe_kpi_calc(df_to_use_for_insights.get('sustainability_rating', pd.Series()), np.max)

    kpi_cols = st.columns(6)
    kpi_cols[0].metric("💰 AVG PRICE", f"{avg_price:,.2f}" if isinstance(avg_price, (int, float)) else avg_price)
    kpi_cols[1].metric("🏭 AVG CARBON", f"{avg_carbon:.2f}" if isinstance(avg_carbon, (int, float)) else avg_carbon)
    kpi_cols[2].metric("💧 AVG WATER", f"{avg_water:,.0f}" if isinstance(avg_water, (int, float)) else avg_water)
    kpi_cols[3].metric("🗑️ AVG WASTE", f"{avg_waste:.2f}" if isinstance(avg_waste, (int, float)) else avg_waste)
    kpi_cols[4].metric("⭐ MIN SUS RATING", f"{min_sus_rating}")
    kpi_cols[5].metric("🌟 MAX SUS RATING", f"{max_sus_rating}")

    st.markdown("---")

    # -------------------------------
    # Tabs
    # -------------------------------
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Top Performance",
        "Geographic & Material Impact",
        "Trends Over Time",
        "Environmental Metrics",
        "Price & Audience",
        "Certifications"
    ])

    # Tab 1: Top Performance
    with tab1:
        st.header("Top Sustainable Performers")
        colA, colB = st.columns([1.5, 1])
        with colA:
            st.subheader("Top 10 Sustainable Brands")
            fig = plot_top_brands(df_top_brands)
            if fig: st.pyplot(fig)
        with colB:
            st.subheader("Top 5 Product Lines")
            fig = plot_top_product_lines(df_top_categories)
            if fig: st.pyplot(fig)

    # Tab 2: Geographic & Material Impact
    with tab2:
        st.header("Geographic & Material Impact Analysis")
        colC, colE = st.columns([2, 1])
        with colC:
            st.subheader("Top 5 Countries by Avg. Rating")
            fig = plot_top_countries(df_top_countries)
            if fig: st.pyplot(fig)
        with colE:
            st.subheader("Eco-friendly vs. Non Eco-friendly")
            fig = plot_eco_friendly_counts(eco_counts)
            if fig: st.pyplot(fig)

    # Tab 3: Trends Over Time
    with tab3:
        st.header("Sustainability Trends")
        colF, colG = st.columns([1.5, 1])
        with colF:
            st.subheader("Avg. Rating Improvement Over Time")
            fig = plot_time_improvement(df_avg_time)
            if fig: st.pyplot(fig)
        with colG:
            st.subheader("Market Trend vs. Avg. Rating")
            fig = plot_market_trend(trend_avg)
            if fig: st.pyplot(fig)

    # Tab 4: Environmental Metrics
    with tab4:
        st.header("Core Environmental Metrics")
        st.subheader("Average Waste, Water, and Carbon Footprint per Product Line")
        fig = plot_environmental_metrics(df_melted)
        if fig: st.pyplot(fig)

    # Tab 5: Price & Audience
    with tab5:
        st.header("Market and Customer Analysis")
        colI, colJ = st.columns(2)
        with colI:
            st.subheader("Price vs. Sustainability Rating")
            fig = plot_price_vs_sustainability(df_price_vs_sus)
            if fig: st.pyplot(fig)
        with colJ:
            st.subheader("Avg. Rating by Target Audience")
            fig = plot_audience_sustainability(audience_sustainability)
            if fig: st.pyplot(fig)

    # Tab 6: Certifications
    with tab6:
        st.header("Certification Analysis")
        st.subheader("Impact of Certification on Rating")
        fig = plot_certification_impact(certification_avg)
        if fig: st.pyplot(fig)
        st.markdown("---")
        st.subheader("Number of Certifications per Product Line")
        fig = plot_certifications_per_product(df_category_cert)
        if fig: st.pyplot(fig)


# Run the app
if __name__ == "__main__":
    main()
