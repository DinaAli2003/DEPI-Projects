
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import warnings
import os
# Ignore Matplotlib and Seaborn warnings related to styles
warnings.filterwarnings("ignore")

# ====================================================================
# ⚠️ STREAMLIT PAGE CONFIGURATION (MUST BE FIRST STREAMLIT COMMAND)
# ====================================================================
st.set_page_config(page_title="Sustainability Dashboard", layout="wide") 

# ====================================================================
# 0. Helper Functions and Data Loading (Initial Data Prep)
# ====================================================================


@st.cache_data
def load_raw_data():
    try:
        # Get the directory where dashboard_app.py is located
        # script_dir = os.path.dirname(os.path.abspath(file))

        # Create correct absolute path to the CSV file
        # file_path = os.path.join(script_dir, "Sustainability_Raw_Data.csv")

        # Load CSV
        # df = pd.read_csv(file_path)
        df = pd.read_csv("Sustainability-Python/Sustainability_Raw_Data.csv")  

        
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
# 1. Visualization Functions (Returning fig instead of plt.show())
# ====================================================================

# Helper function to create a small figure (for better dashboard fit)

def create_figure(df, title, func, figsize=(6, 3.5)): 
    if df.empty: 
        return None
    try:
        fig, ax = plt.subplots(figsize=figsize)
        
        
        fig.patch.set_alpha(0.0) 
        
         
        ax.patch.set_alpha(0.0) 
        
        func(fig, ax, df) 
        ax.set_title(title, fontsize=12, color='darkgreen', fontweight='bold', pad=10) 
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.25)
        return fig
    except Exception as e:
        # st.error(f"Error in creating figure: {e}") 
        return None
# 1. Top 10 Sustainable Brands
def plot_top_brands(df_brands): 
    
    return create_figure(df_brands, "Top 10 Sustainable Brands", figsize=(7, 4), 
        func=lambda fig, ax, df: (
            sns.set_theme(style="whitegrid"),
            norm := plt.Normalize(df["sustainability_rating"].min(), df["sustainability_rating"].max()),
            colors := plt.cm.Greens_r(norm(df["sustainability_rating"])),
            bars := ax.bar(df["brand_name"], df["sustainability_rating"], color=colors, edgecolor="#2E8B57", linewidth=1.0),
            [ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=8, fontweight='bold', color='darkgreen') for bar in bars], # تصغير حجم نص القيم
            ax.set_xlabel("Brand Name", fontsize=10),
            ax.set_ylabel("Avg. Rating", fontsize=10),
            rotation_angle := 45 if max([len(str(label)) for label in df["brand_name"]]) > 8 else 30,
            ax.set_xticklabels(df["brand_name"], rotation=rotation_angle, ha='right', fontsize=8),
            sns.despine(ax=ax)
        )
    )

# 2. Top 5 Product lines
def plot_top_product_lines(df_categories): 
    return create_figure(df_categories, "Top 5 Product Lines", 
        func=lambda fig, ax, df: (
            sns.set_theme(style="whitegrid"),
            norm := plt.Normalize(df["sustainability_rating"].min(), df["sustainability_rating"].max()),
            colors := plt.cm.Greens_r(norm(df["sustainability_rating"])),
            bars := ax.bar(df["product_line"], df["sustainability_rating"], color=colors, edgecolor="#2E8B57", linewidth=1.0),
            [ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkgreen') for bar in bars],
            ax.set_xlabel("Product Line", fontsize=12),
            ax.set_ylabel("Avg. Rating", fontsize=12),
            rotation_angle := 45 if max([len(str(label)) for label in df["product_line"]]) > 10 else 30,
            ax.set_xticklabels(df["product_line"], rotation=rotation_angle, ha='right', fontsize=10),
            sns.despine(ax=ax)
        )
    )

# 3. Top 5 Countries
def plot_top_countries(df_countries):
    return create_figure(df_countries, "Top 5 Countries by Avg. Rating",figsize=(7, 5), 
        func=lambda fig, ax, df: (
            sns.set_theme(style="whitegrid"),
            norm := plt.Normalize(df["sustainability_rating"].min(), df["sustainability_rating"].max()),
            colors := plt.cm.Greens_r(norm(df["sustainability_rating"])),
            bars := ax.bar(df["country_name"], df["sustainability_rating"], color=colors, edgecolor="#2E8B57", linewidth=1.0),
            [ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f"{bar.get_height():.2f}", ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkgreen') for bar in bars],
            ax.set_xlabel("Country", fontsize=12),
            ax.set_ylabel("Avg. Rating", fontsize=12),
            ax.set_xticklabels(df["country_name"], rotation=25, ha='right', fontsize=10),
            sns.despine(ax=ax)
        )
    )


# 4. Number of Certifications per Product line
def plot_certifications_per_product(df_cert_counts): 
    return create_figure(df_cert_counts, "Certifications per Product Line", figsize=(5, 3.5), # 
        func=lambda fig, ax, df: (
            sns.barplot(data=df, x='product_line', y='num_certification', palette='Greens_r', ax=ax),
            [ax.text(index, value + 0.5, str(value), ha='center', va='bottom', fontsize=8, color='#1B5E20', fontweight='bold') for index, value in enumerate(df['num_certification'])],
            ax.set_xlabel('Product Line', fontsize=10),
            ax.set_ylabel('Number of Certifications', fontsize=10),
            ax.tick_params(axis='x', rotation=30, labelsize=8)
        )
    )

# 5. Average Environmental Metrics per Product Line
def plot_environmental_metrics(df_melted):
    return create_figure(df_melted, "Environmental Metrics by Product Line", figsize=(7, 4), 
        func=lambda fig, ax, df: (
            sns.barplot(data=df, x='product_line', y='Average Value', hue='Metric', palette=['#1B5E20', '#388E3C', '#66BB6A'], ax=ax),
            [ax.bar_label(container, fmt='%.1f', label_type='edge', fontsize=7, color='#1B5E20', padding=2) for container in ax.containers],
            ax.set_xlabel('Product Line', fontsize=10),
            ax.set_ylabel('Average Value', fontsize=10),
            ax.tick_params(axis='x', rotation=30, labelsize=8),
            ax.legend(title='Metric', title_fontsize=9, fontsize=8, loc='upper right', bbox_to_anchor=(1.35, 1))
        )
    )

# 6. Sustainability Improvements Over Time
def plot_time_improvement(df_time_avg): 
    return create_figure(df_time_avg, "Sustainability Rating Over Time", 
        func=lambda fig, ax, df: (
            sns.lineplot(data=df, x='year', y='avg_rating', marker='o', color='#2E7D32', linewidth=2.0, ax=ax),
            [ax.text(x, y + 0.002, f"{y:.2f}", ha='center', fontsize=8, fontweight='bold', color='#1B5E20') for x, y in zip(df['year'], df['avg_rating'])],
            ax.set_xlabel("Year", fontsize=10),
            ax.set_ylabel("Avg. Rating", fontsize=10),
            ax.set_xticks(df['year']),
            ax.tick_params(axis='x', rotation=30, labelsize=8)
        )
    )

# 7. Average Sustainability Rating by Target Audience
def plot_audience_sustainability(df_audience_sus): 
    return create_figure(df_audience_sus, "Avg. Rating by Target Audience", 
        func=lambda fig, ax, df: (
            sns.barplot(data=df, x='target_audience', y='sustainability_rating', palette=['#1B5E20', '#2E7D32', '#66BB6A', '#A5D6A7'], ax=ax),
            [ax.text(index, row['sustainability_rating'] + 0.01, f"{row['sustainability_rating']:.3f}", ha='center', fontsize=10, fontweight='bold', color='#1B5E20') for index, row in df.iterrows()],
            ax.set_xlabel('Target Audience', fontsize=12),
            ax.set_ylabel('Avg. Rating', fontsize=12),
            ax.tick_params(axis='x', rotation=15, labelsize=8)
        )
    )

# 8. Average Sustainability Rating by Material Status (Donut Chart)
def plot_material_status(df_material_sus): 
    if df_material_sus.empty or len(df_material_sus) < 2 or 'sustainability_rating' not in df_material_sus.columns:
        return None
        
    fig, ax = plt.subplots(figsize=(4, 4)) # Pie/Donut Chart

    fig.patch.set_alpha(0.0)
    
    
    ax.patch.set_alpha(0.0) 
    
    colors = ['#1B5E20', '#4CAF50', '#A5D6A7']
    colors_to_use = colors[:len(df_material_sus)]
    

    wedges, texts = ax.pie(df_material_sus['sustainability_rating'], 
                           labels=df_material_sus['label'], 
                           startangle=90, colors=colors_to_use, 
                           textprops={'color': '#1B5E20', 'fontsize': 9, 'fontweight': 'bold'}) 

    centre_circle = plt.Circle((0, 0), 0.70, fc='none') 
    fig.gca().add_artist(centre_circle)
    
    ax.axis('off') 

    ax.set_title('Avg. Rating by Material Status', fontsize=12, color='#1B5E20', fontweight='bold', pad=10)
    plt.tight_layout()
    return fig

# 9. Eco-friendly vs Non Eco-friendly Brands #(Pie Chart)
def plot_eco_friendly_counts(eco_counts_series): 
    if eco_counts_series.empty or len(eco_counts_series) < 2: return None

    fig, ax = plt.subplots(figsize=(4, 4)) # Pie/Donut Chart
    fig.patch.set_alpha(0.0)
    ax.pie(eco_counts_series.values, 
           labels=['Non Eco-friendly', 'Eco-friendly'][:len(eco_counts_series)], 
           autopct='%1.1f%%', 
           colors=['#A5D6A7', '#1B5E20'][:len(eco_counts_series)], 
           startangle=90,
           textprops={'fontsize': 11}) 
    ax.set_title("Eco-friendly vs Non Eco-friendly Mfg", fontsize=12, color='darkgreen', fontweight='bold', pad=10)
    plt.tight_layout()
    return fig

# 10. Relationship Between Price and Sustainability Rating (Scatter Plot)
def plot_price_vs_sustainability(df_price_sus): 
    return create_figure(df_price_sus, "Price vs. Sustainability Rating", figsize=(7, 4),
        func=lambda fig, ax, df: (
            sns.scatterplot(data=df, x="average_price", y="sustainability_rating", hue="brand_category", palette="Greens_r", alpha=0.7, s=50, edgecolor="black", ax=ax),
            ax.set_xlabel("Average Price", fontsize=12),
            ax.set_ylabel("Sustainability Rating", fontsize=12),
            ax.legend(title="Brand Category", title_fontsize=8, fontsize=7, bbox_to_anchor=(1.05, 1), loc="upper left")
        )
    )

# 11. Impact of Certification on Sustainability Rating
def plot_certification_impact(df_certification_avg): 
    return create_figure(df_certification_avg, "Impact of Certification on Rating", figsize=(7, 4), 
        func=lambda fig, ax, df: (
            green_palette := sns.color_palette("Greens", n_colors=len(df)),
            barplot := sns.barplot(data=df, x="certification", y="avg_rating", palette=green_palette, ax=ax),
            [barplot.annotate(f"{p.get_height():.3f}", (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='bottom', fontsize=8, fontweight='medium', color='black', xytext=(0, 3), textcoords='offset points') for p in barplot.patches],
            ax.set_xlabel("Certification", fontsize=10),
            ax.set_ylabel("Avg. Rating", fontsize=10),
            ax.tick_params(axis='x', rotation=45, labelsize=8)
        )
    )

# 12. Market Trend vs Sustainability Rating (Donut Chart)
def plot_market_trend(df_trend_avg): 
    if df_trend_avg.empty or len(df_trend_avg) < 2 or 'sustainability_rating' not in df_trend_avg.columns:
        return None
        
    fig, ax = plt.subplots(figsize=(4, 4)) # Pie/Donut Chart
    
    
    fig.patch.set_alpha(0.0)
    
    
    # ax.patch.set_alpha(0.0) 
    # ax.set_facecolor('none')  

    colors = sns.color_palette("Greens", n_colors=len(df_trend_avg))
    
    wedges, texts, autotexts = ax.pie(
        df_trend_avg["sustainability_rating"],
        labels=df_trend_avg["market_trend"],
        autopct=lambda p: f'{p:.1f} ({p*sum(df_trend_avg["sustainability_rating"])/100:.2f})', 
        startangle=140,
        colors=colors,
        pctdistance=0.85, 
        textprops={"fontsize": 9, "color": "black"}
    )
    
   
    centre_circle = plt.Circle((0, 0), 0.70, fc="#F3F9E8") 
    fig.gca().add_artist(centre_circle)
    
   
    ax.axis('off')

    ax.set_title("Market Trend vs Sustainability Rating", fontsize=12, color="green", fontweight="bold", pad=10)
    plt.tight_layout()
    return fig
# ====================================================================
# 2. Main Streamlit App
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
    st.sidebar.title("Filter")  
    df_filtered = df.copy()

    def get_filter_options(column_name):
        if column_name in df.columns:
            options = sorted(df[column_name].dropna().unique().tolist())
            return options, options
        return [], []

    # Filters
    selected_countries = st.sidebar.multiselect("Select Country:", *get_filter_options('country_name'))
    selected_years = st.sidebar.multiselect("Select Year:", *get_filter_options('year'))
    selected_certifications = st.sidebar.multiselect("Select Certification:", *get_filter_options('certification'))
    selected_product_lines = st.sidebar.multiselect("Select Product Line:", *get_filter_options('product_line'))
    selected_brands = st.sidebar.multiselect("Select Sustainable Brand:", *get_filter_options('brand_name'))

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
    # KPIs
    # ----------------------------------------------------
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

    # ----------------------------------------------------
    # Tabs with Charts
    # ----------------------------------------------------
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Top Performance", 
        "Geographic & Material Impact", 
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



