import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import warnings
from PIL import Image
import os
import base64
from io import BytesIO

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
# CLEAN CSS STYLING - WITH PROFESSIONAL SMALL LOGO PLACEMENT
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
    
    /* Header area - consistent with dashboard background */
    header[data-testid="stHeader"] {
        background: linear-gradient(135deg, #F0F9F0 0%, #E8F5E8 50%, #F0F9F0 100%) !important;
        border-bottom: 1px solid #C8E6C9;
    }
    
    /* Fix header toolbar area */
    [data-testid="stToolbar"] {
        background: transparent !important;
    }
    
    /* Remove header decoration */
    .decoration {
        background: transparent !important;
    }
    
    /* Style the header buttons area */
    [data-testid="baseButton-header"] {
        background: transparent !important;
    }
    
    /* Sidebar - complete green theme */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%) !important;
    }
    
    /* Sidebar text - all white including filter labels */
    .stSidebar label, .stSidebar p, .stSidebar div, .stSidebar span {
        color: #FFFFFF !important;
    }
    
    /* Specific styling for filter labels */
    .stMultiSelect label, .stSelectbox label, .stSlider label {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 8px !important;
    }
    
    /* Sidebar select boxes - green theme */
    .stMultiSelect > div > div > div {
        background-color: #E8F5E8 !important;
        border-color: #4CAF50 !important;
        border-radius: 8px !important;
        color: #1B5E20 !important;
    }
    
    /* Multi-select dropdown options */
    div[data-baseweb="select"] > div {
        background-color: #E8F5E8 !important;
        color: #1B5E20 !important;
    }
    
    /* Fix multi-select selected items */
    [data-baseweb="tag"] {
        background-color: #4CAF50 !important;
        color: white !important;
        border: none !important;
    }
    
    /* Enhanced Main Header with Integrated Small Logos */
    .main-header {
        background: linear-gradient(135deg, #1B5E20 0%, #388E3C 100%);
        padding: 1.5rem 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(27, 94, 32, 0.3);
    }
    
    /* Header title styling */
    .header-title {
        text-align: center;
        margin: 0;
    }
    
    /* Ultra small logo styling */
    .logo-image {
        max-height: 25px !important;
        max-width: 40px !important;
        height: 25px !important;
        width: auto !important;
        object-fit: contain !important;
        filter: brightness(0) invert(1) !important;
        opacity: 0.9;
        transition: opacity 0.3s ease;
    }
    
    .logo-image:hover {
        opacity: 1;
    }
    
    /* Ultra small logo placeholder */
    .logo-placeholder {
        width: 40px;
        height: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 3px;
        color: white;
        font-weight: bold;
        font-size: 0.5rem;
        text-align: center;
        line-height: 1;
        padding: 2px;
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
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
    
    /* Ensure KPI text is fully visible */
    [data-testid="stMetric"] div {
        overflow: visible !important;
        white-space: normal !important;
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
    
    /* Tab content area */
    .stTabs [data-baseweb="tab-panel"] {
        background: transparent;
        padding: 0;
    }
    
    /* Custom green button style */
    .stButton button {
        background: linear-gradient(135deg, #4CAF50 0%, #388E3C 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 6px rgba(76, 175, 80, 0.3);
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #388E3C 0%, #2E7D32 100%) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(76, 175, 80, 0.4);
    }
    
    /* Remove all default white backgrounds */
    .css-1y4p8pa {
        background: transparent;
    }
    
    /* Fix any remaining white elements */
    div[data-testid="stVerticalBlock"] {
        background: transparent !important;
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
    
    /* Filter section in sidebar */
    .filter-section {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Consistent chart sizing */
    .element-container {
        height: 100% !important;
    }
    
    /* Fix for any remaining orange elements */
    [style*="background-color: rgb(250, 250, 250)"],
    [style*="background-color: #fafafa"],
    [style*="background-color: rgb(255, 255, 255)"],
    [style*="background-color: white"] {
        background: transparent !important;
    }
    
    /* Professional grid alignment */
    .chart-grid {
        display: grid;
        gap: 20px;
        width: 100%;
    }
    
    .grid-2-col {
        grid-template-columns: 1fr 1fr;
    }
    
    .grid-3-col {
        grid-template-columns: 1fr 1fr 1fr;
    }
    
    /* FIXED: Streamlit column containment */
    [data-testid="column"] {
        min-height: 450px;
    }
    
    /* Remove any chart container backgrounds */
    .chart-container-wrapper, .chart-wrapper {
        background: transparent !important;
        padding: 0 !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Mobile responsiveness for header */
    @media (max-width: 768px) {
        .main-header {
            padding: 1rem;
        }
        
        .logo-image {
            max-height: 20px !important;
            max-width: 30px !important;
            height: 20px !important;
        }
        
        .logo-placeholder {
            width: 30px;
            height: 20px;
            font-size: 0.4rem;
        }
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
# 1. PROFESSIONAL VISUALIZATION FUNCTIONS (Clean and Simple)
# ====================================================================

# Set global green color palette
GREEN_PALETTE = ['#1B5E20', '#2E7D32', '#388E3C', '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7']
sns.set_palette(GREEN_PALETTE)

def create_professional_figure(df, title, func, figsize=(6, 4)):
    """Enhanced figure creation with perfect container alignment"""
    if df.empty: 
        return None
    try:
        # CONSISTENT FIGURE SIZE with tight layout
        fig, ax = plt.subplots(figsize=figsize)
        
        # Set transparent background to match dashboard
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)
        
        # Apply the plotting function
        func(fig, ax, df) 
        
        # Professional title styling
        ax.set_title(title, fontsize=14, color='#1B5E20', fontweight='bold', pad=12)
        
        # Professional axis labels
        ax.set_xlabel(ax.get_xlabel(), fontsize=11, color='#2E7D32', fontweight='600')
        ax.set_ylabel(ax.get_ylabel(), fontsize=11, color='#2E7D32', fontweight='600')
        
        # Professional ticks
        ax.tick_params(colors='#388E3C', labelsize=10)
        
        # Professional spines
        for spine in ax.spines.values():
            spine.set_color('#4CAF50')
            spine.set_linewidth(1.5)
            
        # Professional grid
        ax.grid(True, alpha=0.2, color='#C8E6C9')
        
        # TIGHT LAYOUT for perfect fit
        plt.tight_layout(pad=1.0)
        return fig
    except Exception as e:
        st.error(f"Chart error: {e}")
        return None

# All plotting functions - CLEAN AND SIMPLE
def plot_top_brands(df_brands): 
    def plot_func(fig, ax, df):
        sns.set_theme(style="whitegrid")
        colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
        bars = ax.bar(df["brand_name"], df["sustainability_rating"], color=colors, 
                      edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
        
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{bar.get_height():.2f}', 
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1B5E20',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='#E8F5E8', alpha=0.8))
        
        ax.set_xlabel("Brand Name", fontsize=11, fontweight='600')
        ax.set_ylabel("Sustainability Rating", fontsize=11, fontweight='600')
        rotation_angle = 45 if max([len(str(label)) for label in df["brand_name"]]) > 8 else 30
        ax.set_xticklabels(df["brand_name"], rotation=rotation_angle, ha='right', fontsize=9)
        ax.set_ylim(0, df["sustainability_rating"].max() * 1.15)
    
    return create_professional_figure(df_brands, "Top 10 Sustainable Brands", plot_func, figsize=(7, 4))

def plot_top_product_lines(df_categories): 
    def plot_func(fig, ax, df):
        sns.set_theme(style="whitegrid")
        colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
        bars = ax.bar(df["product_line"], df["sustainability_rating"], 
                      color=colors, edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
        
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f'{bar.get_height():.2f}', 
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1B5E20',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='#E8F5E8', alpha=0.8))
        
        ax.set_xlabel("Product Line", fontsize=11, fontweight='600')
        ax.set_ylabel("Sustainability Rating", fontsize=11, fontweight='600')
        rotation_angle = 45 if max([len(str(label)) for label in df["product_line"]]) > 10 else 30
        ax.set_xticklabels(df["product_line"], rotation=rotation_angle, ha='right', fontsize=10)
        ax.set_ylim(0, df["sustainability_rating"].max() * 1.15)
    
    return create_professional_figure(df_categories, "Top 5 Sustainable Product Lines", plot_func, figsize=(6, 4))

def plot_top_countries(df_countries):
    def plot_func(fig, ax, df):
        sns.set_theme(style="whitegrid")
        colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
        bars = ax.bar(df["country_name"], df["sustainability_rating"], 
                      color=colors, edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
        
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, f"{bar.get_height():.2f}", 
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1B5E20',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='#E8F5E8', alpha=0.8))
        
        ax.set_xlabel("Country", fontsize=11, fontweight='600')
        ax.set_ylabel("Sustainability Rating", fontsize=11, fontweight='600')
        ax.set_xticklabels(df["country_name"], rotation=25, ha='right', fontsize=10)
        ax.set_ylim(0, df["sustainability_rating"].max() * 1.15)
    
    return create_professional_figure(df_countries, "Top 5 Countries by Sustainability", plot_func, figsize=(6, 4))

def plot_certifications_per_product(df_cert_counts): 
    def plot_func(fig, ax, df):
        colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
        bars = ax.bar(df['product_line'], df['num_certification'], color=colors, 
                      edgecolor="#1B5E20", linewidth=1.2, alpha=0.9)
        
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, str(int(bar.get_height())), 
                    ha='center', va='bottom', fontsize=9, color='#1B5E20', fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='#E8F5E8', alpha=0.8))
        
        ax.set_xlabel('Product Line', fontsize=11, fontweight='600')
        ax.set_ylabel('Number of Certifications', fontsize=11, fontweight='600')
        ax.tick_params(axis='x', rotation=30, labelsize=9)
    
    return create_professional_figure(df_cert_counts, "Certifications per Product Line", plot_func, figsize=(6, 4))

def plot_environmental_metrics(df_melted):
    def plot_func(fig, ax, df):
        sns.barplot(data=df, x='product_line', y='Average Value', hue='Metric', 
                   palette=['#1B5E20', '#388E3C', '#4CAF50'], ax=ax, alpha=0.9)
        
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f', label_type='edge', fontsize=8, 
                         color='#1B5E20', fontweight='bold', padding=3)
        
        ax.set_xlabel('Product Line', fontsize=11, fontweight='600')
        ax.set_ylabel('Average Value', fontsize=11, fontweight='600')
        ax.tick_params(axis='x', rotation=30, labelsize=9)
        ax.legend(title='Environmental Metric', title_fontsize=10, fontsize=9, 
                 loc='upper right', bbox_to_anchor=(1.25, 1), 
                 frameon=True, facecolor='#E8F5E8', edgecolor='#C8E6C9')
    
    return create_professional_figure(df_melted, "Environmental Metrics by Product Line", plot_func, figsize=(8, 4))

def plot_time_improvement(df_time_avg): 
    def plot_func(fig, ax, df):
        sns.lineplot(data=df, x='year', y='avg_rating', marker='o', color='#2E7D32', 
                    linewidth=3, markersize=8, ax=ax, markerfacecolor='#1B5E20')
        
        for x, y in zip(df['year'], df['avg_rating']):
            ax.text(x, y + 0.005, f"{y:.2f}", ha='center', fontsize=9, fontweight='bold', 
                    color='#1B5E20', bbox=dict(boxstyle="round,pad=0.3", facecolor='#E8F5E8', alpha=0.9))
        
        ax.set_xlabel("Year", fontsize=11, fontweight='600')
        ax.set_ylabel("Average Sustainability Rating", fontsize=11, fontweight='600')
        ax.set_xticks(df['year'])
        ax.tick_params(axis='x', rotation=0, labelsize=10)
        ax.grid(True, alpha=0.3, color='#C8E6C9')
        ax.set_ylim(df['avg_rating'].min() * 0.95, df['avg_rating'].max() * 1.05)
    
    return create_professional_figure(df_time_avg, "Sustainability Trend Over Years", plot_func, figsize=(7, 4))

def plot_audience_sustainability(df_audience_sus): 
    def plot_func(fig, ax, df):
        colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
        bars = sns.barplot(data=df, x='target_audience', y='sustainability_rating', 
                           palette=colors, ax=ax, alpha=0.9)
        
        for index, row in df.iterrows():
            ax.text(index, row['sustainability_rating'] + 0.008, f"{row['sustainability_rating']:.3f}", 
                    ha='center', fontsize=9, fontweight='bold', color='#1B5E20',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor='#E8F5E8', alpha=0.8))
        
        ax.set_xlabel('Target Audience', fontsize=11, fontweight='600')
        ax.set_ylabel('Sustainability Rating', fontsize=11, fontweight='600')
        ax.tick_params(axis='x', rotation=15, labelsize=9)
    
    return create_professional_figure(df_audience_sus, "Sustainability by Target Audience", plot_func, figsize=(6, 4))

def plot_material_status(df_material_sus): 
    if df_material_sus.empty or len(df_material_sus) < 2 or 'sustainability_rating' not in df_material_sus.columns:
        return None
        
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    colors = GREEN_PALETTE[:len(df_material_sus)]
    
    wedges, texts, autotexts = ax.pie(df_material_sus['sustainability_rating'], 
                           labels=df_material_sus['material_status'], 
                           autopct='%1.1f%%',
                           startangle=90, colors=colors, 
                           textprops={'color': '#1B5E20', 'fontsize': 10, 'fontweight': 'bold'},
                           wedgeprops={'edgecolor': '#1B5E20', 'linewidth': 1.5})

    centre_circle = plt.Circle((0, 0), 0.70, fc='#F0F9F0')
    fig.gca().add_artist(centre_circle)
    
    # Add center text
    ax.text(0, 0, f"Avg:\n{df_material_sus['sustainability_rating'].mean():.2f}", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#1B5E20')
    
    ax.axis('equal')
    ax.set_title('Sustainability by Material Status', fontsize=13, color='#1B5E20', fontweight='bold', pad=20)
    plt.tight_layout(pad=2.0)
    return fig

def plot_eco_friendly_counts(eco_counts_series): 
    if eco_counts_series.empty or len(eco_counts_series) < 2: 
        return None

    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    colors = ['#A5D6A7', '#1B5E20'][:len(eco_counts_series)]
    labels = ['Non Eco-friendly', 'Eco-friendly'][:len(eco_counts_series)]
    
    wedges, texts, autotexts = ax.pie(eco_counts_series.values, 
           labels=labels, 
           autopct='%1.1f%%', 
           colors=colors, 
           startangle=90,
           textprops={'fontsize': 11, 'color': '#1B5E20', 'fontweight': 'bold'},
           wedgeprops={'edgecolor': '#1B5E20', 'linewidth': 1.5})
    
    # Style autopct text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title("Eco-friendly Manufacturing", fontsize=13, color='#1B5E20', fontweight='bold', pad=20)
    plt.tight_layout(pad=2.0)
    return fig

def plot_price_vs_sustainability(df_price_sus): 
    def plot_func(fig, ax, df):
        sns.scatterplot(data=df, x="average_price", y="sustainability_rating", 
                       hue="brand_category", palette=GREEN_PALETTE, alpha=0.8, s=80, 
                       edgecolor="white", linewidth=1, ax=ax)
        ax.set_xlabel("Average Price ($)", fontsize=11, fontweight='600')
        ax.set_ylabel("Sustainability Rating", fontsize=11, fontweight='600')
        ax.legend(title="Brand Category", title_fontsize=10, fontsize=9, 
                 bbox_to_anchor=(1.05, 1), loc="upper left", 
                 frameon=True, facecolor='#E8F5E8', edgecolor='#C8E6C9')
    
    return create_professional_figure(df_price_sus, "Price vs Sustainability Rating", plot_func, figsize=(7, 4))

def plot_certification_impact(df_certification_avg): 
    def plot_func(fig, ax, df):
        colors = [GREEN_PALETTE[i % len(GREEN_PALETTE)] for i in range(len(df))]
        barplot = sns.barplot(data=df, x="certification", y="avg_rating", 
                              palette=colors, ax=ax, alpha=0.9)
        
        for p in barplot.patches:
            barplot.annotate(f"{p.get_height():.3f}", (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha='center', va='bottom', fontsize=9, fontweight='bold', 
                            color='#1B5E20', xytext=(0, 5), textcoords='offset points',
                            bbox=dict(boxstyle="round,pad=0.2", facecolor='#E8F5E8', alpha=0.8))
        
        ax.set_xlabel("Certification Type", fontsize=11, fontweight='600')
        ax.set_ylabel("Average Sustainability Rating", fontsize=11, fontweight='600')
        ax.tick_params(axis='x', rotation=45, labelsize=9)
    
    return create_professional_figure(df_certification_avg, "Certification Impact on Rating", plot_func, figsize=(7, 4))

def plot_market_trend(df_trend_avg): 
    if df_trend_avg.empty or len(df_trend_avg) < 2 or 'sustainability_rating' not in df_trend_avg.columns:
        return None
        
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    
    colors = GREEN_PALETTE[:len(df_trend_avg)]
    
    wedges, texts, autotexts = ax.pie(
        df_trend_avg["sustainability_rating"],
        labels=df_trend_avg["market_trend"],
        autopct=lambda p: f'{p:.1f}%', 
        startangle=140,
        colors=colors,
        pctdistance=0.85,
        textprops={"fontsize": 10, "color": "#1B5E20", "fontweight": "bold"},
        wedgeprops={'edgecolor': '#1B5E20', 'linewidth': 1.5}
    )
    
    # Style percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    centre_circle = plt.Circle((0, 0), 0.70, fc="#F0F9F0")
    fig.gca().add_artist(centre_circle)
    
    # Add center text
    total_avg = df_trend_avg["sustainability_rating"].mean()
    ax.text(0, 0, f"Avg:\n{total_avg:.2f}", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#1B5E20')
    
    ax.axis('equal')
    ax.set_title("Market Trend Analysis", fontsize=13, color="#1B5E20", fontweight="bold", pad=20)
    plt.tight_layout(pad=2.0)
    return fig

# ====================================================================
# 2. LOGO HANDLING FUNCTIONS - ULTRA SMALL SIZING
# ====================================================================

def load_logo(image_path):
    """Load logo with ultra small sizing and error handling"""
    try:
        if os.path.exists(image_path):
            logo = Image.open(image_path)
            return logo
        else:
            st.warning(f"Logo not found: {image_path}")
            return None
    except Exception as e:
        st.warning(f"Error loading logo {image_path}: {e}")
        return None

# ====================================================================
# 3. CLEAN STREAMLIT APP - WITH ULTRA SMALL INTEGRATED LOGOS
# ====================================================================

def main():
    # 1. Load Raw Data
    df = load_raw_data()

    if df.empty:
        return

    # --- ULTRA SMALL LOGOS INTEGRATED INTO HEADER ---
    left_logo = load_logo('Sustainability-Python/logo_ministry.png')
    right_logo = load_logo('Sustainability-Python/logo_project.png')
    
    # Professional header with ultra small logos using Streamlit columns
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        # Left logo - ultra small (25px height)
        if left_logo:
            st.image(left_logo, width=40, use_column_width=False)
        else:
            st.markdown("""
            <div class="logo-placeholder">
                L
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Center title
        st.markdown("""
        <div class="main-header">
            <div class="header-title">
                <h1 style="margin: 0; font-size: 2.5rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); letter-spacing: 0.5px;">🌱 Sustainability Analytics Dashboard</h1>
                <p style="margin: 8px 0 0 0; font-size: 1.1rem; opacity: 0.95; font-weight: 300; line-height: 1.4;">Comprehensive Environmental Impact & Sustainable Performance Tracking</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Right logo - ultra small (25px height)
        if right_logo:
            st.image(right_logo, width=40, use_column_width=False)
        else:
            st.markdown("""
            <div class="logo-placeholder">
                R
            </div>
            """, unsafe_allow_html=True)
    
    # ----------------------------------------------------
    # 2. Enhanced Filtering Section with White Text Labels
    # ----------------------------------------------------
    
    # Style the sidebar header with enhanced design
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

    # 1. Countries Filter
    country_options, default_countries = get_filter_options('country_name')
    selected_countries = st.sidebar.multiselect(
        "🌍 Select Countries:", 
        options=country_options, 
        default=default_countries
    )
    if selected_countries:
        df_filtered = df_filtered[df_filtered['country_name'].isin(selected_countries)]
    
    # 2. Years Filter
    year_options, default_years = get_filter_options('year')
    selected_years = st.sidebar.multiselect(
        "📅 Select Years:", 
        options=year_options, 
        default=default_years
    )
    if selected_years:
        df_filtered = df_filtered[df_filtered['year'].isin(selected_years)]

    # 3. Certifications Filter
    certification_options, default_certifications = get_filter_options('certification')
    selected_certifications = st.sidebar.multiselect(
        "🏆 Select Certifications:", 
        options=certification_options, 
        default=default_certifications
    )
    if selected_certifications:
        df_filtered = df_filtered[df_filtered['certification'].isin(selected_certifications)]
    
    # 4. Product Lines Filter
    product_line_options, default_product_lines = get_filter_options('product_line')
    selected_product_lines = st.sidebar.multiselect(
        "📦 Select Product Lines:", 
        options=product_line_options, 
        default=default_product_lines
    )
    if selected_product_lines:
        df_filtered = df_filtered[df_filtered['product_line'].isin(selected_product_lines)]

    # 5. Brands Filter
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

    # Enhanced reset filters button
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True, type="primary"):
        st.rerun()

    # Data summary in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2);">
        <h4 style="color: white; margin: 0 0 10px 0;">📈 Data Summary</h4>
        <p style="color: #E8F5E8; margin: 5px 0; font-size: 0.9rem;">Total Records: <strong>{len(df_filtered):,}</strong></p>
        <p style="color: #E8F5E8; margin: 5px 0; font-size: 0.9rem;">Filtered from: <strong>{len(df):,}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    # Fallback if no data matches filters
    if df_filtered.empty:
        st.warning("⚠️ No data matches the current filters. Please adjust your selections. Displaying global KPIs and charts with full data as fallback.")
        df_to_use_for_insights = df.copy()
    else:
        df_to_use_for_insights = df_filtered.copy()

    # ----------------------------------------------------
    # 3. Calculate all Insights
    # ----------------------------------------------------
    available_cols_for_insights = df_to_use_for_insights.columns.tolist()

    # Calculate all insights
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
    
    material_sustainability = pd.DataFrame(columns=['material_status', 'sustainability_rating', 'label'])
    if 'material_status' in available_cols_for_insights and 'sustainability_rating' in available_cols_for_insights and not df_to_use_for_insights.empty:
        material_sustainability = df_to_use_for_insights.groupby('material_status')['sustainability_rating'].mean().round(3).reset_index().sort_values(by='sustainability_rating', ascending=False)
        if not material_sustainability.empty:
             material_sustainability['label'] = (material_sustainability['material_status'] + ' (' + material_sustainability['sustainability_rating'].astype(str) + ')')
    
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
    # 4. Enhanced KPI Section with Better Visibility
    # ----------------------------------------------------
    
    # Calculate KPIs
    avg_price = safe_kpi_calc(df_to_use_for_insights.get('average_price', pd.Series()), np.mean)
    avg_carbon = safe_kpi_calc(df_to_use_for_insights.get('carbon_footprint', pd.Series()), np.mean)
    avg_water = safe_kpi_calc(df_to_use_for_insights.get('water_usage', pd.Series()), np.mean, rounding=0)
    avg_waste = safe_kpi_calc(df_to_use_for_insights.get('waste_production', pd.Series()), np.mean)
    min_sus_rating = safe_kpi_calc(df_to_use_for_insights.get('sustainability_rating', pd.Series()), np.min)
    max_sus_rating = safe_kpi_calc(df_to_use_for_insights.get('sustainability_rating', pd.Series()), np.max)
    avg_sus_rating = safe_kpi_calc(df_to_use_for_insights.get('sustainability_rating', pd.Series()), np.mean)

    # Display KPIs in a styled row
    st.markdown('<div class="section-header"><h3>📊 Key Performance Indicators</h3></div>', unsafe_allow_html=True)
    
    kpi_cols = st.columns(7)

    with kpi_cols[0]:
        st.metric(
            label="💰 Average Price",
            value=f"{avg_price:,.2f}" if isinstance(avg_price, (int, float)) else avg_price,
            delta=None
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

    # --- PROFESSIONAL TABS - NO CONTAINERS ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏆 Top Performance", 
        "🌍 Geographic & Material", 
        "📈 Trends Over Time", 
        "🌱 Environmental Metrics", 
        "💰 Market Analysis", 
        "🏅 Certifications"
    ])
    
    # SIMPLIFIED: Direct chart display - NO CONTAINERS
    def display_chart(fig, col=None):
        """Display chart directly without containers"""
        if fig is not None:
            if col:
                with col:
                    st.pyplot(fig, use_container_width=True)
            else:
                st.pyplot(fig, use_container_width=True)

    # ====================================================
    # Tab 1: Top Performance - NO CONTAINERS
    # ====================================================
    with tab1:
        st.markdown('<div class="section-header"><h3>🏆 Top Sustainable Performers Analysis</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        # Only display charts that have data
        top_brands_chart = plot_top_brands(df_top_brands)
        top_categories_chart = plot_top_product_lines(df_top_categories)
        
        if top_brands_chart is not None:
            display_chart(top_brands_chart, col1)
        
        if top_categories_chart is not None:
            display_chart(top_categories_chart, col2)

    # ====================================================
    # Tab 2: Geographic & Material - NO CONTAINERS
    # ====================================================
    with tab2:
        st.markdown('<div class="section-header"><h3>🌍 Geographic & Material Impact Analysis</h3></div>', unsafe_allow_html=True)
        
        # Create charts first
        countries_chart = plot_top_countries(df_top_countries)
        material_chart = plot_material_status(material_sustainability)
        eco_chart = plot_eco_friendly_counts(eco_counts)
        
        # Count available charts
        available_charts = [chart for chart in [countries_chart, material_chart, eco_chart] if chart is not None]
        
        if len(available_charts) == 3:
            # All charts available - use 3-column layout
            col1, col2, col3 = st.columns(3)
            display_chart(countries_chart, col1)
            display_chart(material_chart, col2)
            display_chart(eco_chart, col3)
        elif len(available_charts) == 2:
            # Two charts available - use 2-column layout
            col1, col2 = st.columns(2)
            display_chart(available_charts[0], col1)
            display_chart(available_charts[1], col2)
        elif len(available_charts) == 1:
            # One chart available - use full width
            display_chart(available_charts[0])

    # ====================================================
    # Tab 3: Trends Over Time - NO CONTAINERS
    # ====================================================
    with tab3:
        st.markdown('<div class="section-header"><h3>📈 Sustainability Trends & Market Analysis</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        time_chart = plot_time_improvement(df_avg_time)
        trend_chart = plot_market_trend(trend_avg)
        
        if time_chart is not None:
            display_chart(time_chart, col1)
                
        if trend_chart is not None:
            display_chart(trend_chart, col2)

    # ====================================================
    # Tab 4: Environmental Metrics - NO CONTAINERS
    # ====================================================
    with tab4:
        st.markdown('<div class="section-header"><h3>🌱 Core Environmental Metrics Analysis</h3></div>', unsafe_allow_html=True)
        
        env_chart = plot_environmental_metrics(df_melted)
        if env_chart is not None:
            display_chart(env_chart)
        
    # ====================================================
    # Tab 5: Price & Audience - NO CONTAINERS
    # ====================================================
    with tab5:
        st.markdown('<div class="section-header"><h3>💰 Market & Customer Analysis</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        price_chart = plot_price_vs_sustainability(df_price_vs_sus)
        audience_chart = plot_audience_sustainability(audience_sustainability)
        
        if price_chart is not None:
            display_chart(price_chart, col1)
                
        if audience_chart is not None:
            display_chart(audience_chart, col2)
    
    # ====================================================
    # Tab 6: Certifications - NO CONTAINERS
    # ====================================================
    with tab6:
        st.markdown('<div class="section-header"><h3>🏅 Certification Impact Analysis</h3></div>', unsafe_allow_html=True)
        
        cert_impact_chart = plot_certification_impact(certification_avg)
        cert_count_chart = plot_certifications_per_product(df_category_cert)
        
        if cert_impact_chart is not None:
            display_chart(cert_impact_chart)
            
        if cert_count_chart is not None:
            st.markdown("---")
            display_chart(cert_count_chart)

    # Enhanced Footer
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div style="text-align: left;">
                <h4 style="margin: 0; color: white;">🌍 Sustainability Analytics Dashboard</h4>
                <p style="margin: 5px 0 0 0; color: #E8F5E8; font-size: 0.9rem;">Driving Sustainable Business Decisions</p>
            </div>
            <div style="text-align: right;">
                <p style="margin: 0; color: #E8F5E8; font-size: 0.9rem;">📅 Developed in : 2025</p>
                <p style="margin: 5px 0 0 0; color: #E8F5E8; font-size: 0.9rem;">📊 Designed by Dina Ali</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Run the main function
if __name__ == "__main__":
    main()
