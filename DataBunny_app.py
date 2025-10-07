#this project 



import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import io

# 🎀 Page Configuration
st.set_page_config(
    page_title="DataBunny 🐇 - Cute Data Analysis",
    page_icon="🐰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom CSS for Cute Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@300;400;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
        font-family: 'Comic Neue', cursive;
    }
    
    .stApp {
        background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
    }
    
    .cute-header {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 25px;
        box-shadow: 0 8px 32px rgba(255, 182, 193, 0.2);
        border: 3px solid #ffb6c1;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.98);
        padding: 1.5rem;
        border-radius: 20px;
        border: 2px solid #ffb6c1;
        text-align: center;
        box-shadow: 0 4px 16px rgba(255, 182, 193, 0.15);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #FF9A9E 0%, #FAD0C4 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.5rem 2rem;
        font-family: 'Comic Neue', cursive;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(255, 154, 158, 0.3);
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(255, 154, 158, 0.4);
    }
    
    .upload-box {
        background: rgba(255, 255, 255, 0.95);
        border: 3px dashed #ffb6c1;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 🎯 Color Themes
def get_theme_colors(theme_name):
    themes = {
        "Pink Blossom 🌸": {
            "primary": "#ff6b95",
            "secondary": "#ffb6c1", 
            "background": "linear-gradient(135deg, #ffebee 0%, #fce4ec 100%)",
            "metric_colors": ["#ff6b95", "#ff9a00", "#e75480", "#9b59b6"]
        },
        "Mint Candy 🍬": {
            "primary": "#37ecba",
            "secondary": "#72afd3",
            "background": "linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%)",
            "metric_colors": ["#37ecba", "#72afd3", "#4db6ac", "#26c6da"]
        },
        "Lavender Dream 💜": {
            "primary": "#9b59b6",
            "secondary": "#8e44ad", 
            "background": "linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%)",
            "metric_colors": ["#9b59b6", "#8e44ad", "#673ab7", "#5e35b1"]
        },
        "Sunshine Yellow 🌞": {
            "primary": "#ffd700",
            "secondary": "#ffeb3b",
            "background": "linear-gradient(135deg, #fffde7 0%, #fff9c4 100%)",
            "metric_colors": ["#ffd700", "#ff9800", "#ffeb3b", "#ffc107"]
        }
    }
    return themes.get(theme_name, themes["Pink Blossom 🌸"])

# 🐰 Header Section
st.markdown("""
<div class='cute-header'>
    <h1 style='color: #ff6b95; margin: 0; font-size: 3rem;'>DataBunny 🐰</h1>
    <p style='color: #666; font-size: 1.2rem; margin: 0;'>The cutest way to analyze your data!</p>
</div>
""", unsafe_allow_html=True)

# 📊 Data Upload and Management
with st.sidebar:
    st.markdown("<h2 style='color: #ff6b95;'>🎀 Data Setup</h2>", unsafe_allow_html=True)
    
    # Data source selection
    data_source = st.radio(
        "Choose your data:",
        ["📤 Upload Your Data", "🎪 Use Sample Data"],
        help="Upload your CSV/Excel or try with our cute sample data!"
    )
    
    uploaded_file = None
    df = None
    
    if data_source == "📤 Upload Your Data":
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['csv', 'xlsx'],
            help="Upload your CSV or Excel file"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ Successfully loaded {len(df)} rows!")
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
    
    else:  # Sample data
        @st.cache_data
        def generate_sample_data():
            np.random.seed(42)
            dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
            
            data = pd.DataFrame({
                'date': dates,
                'sales': np.random.normal(1000, 200, len(dates)).clip(0),
                'customers': np.random.poisson(50, len(dates)),
                'revenue': np.random.normal(5000, 1000, len(dates)).clip(0),
                'satisfaction': np.random.normal(85, 10, len(dates)).clip(0, 100)
            })
            
            # Add some trends
            data['sales'] += 100 * np.sin((data.date.dt.dayofyear / 365) * 2 * np.pi)
            data['revenue'] = data['sales'] * 5 + np.random.normal(0, 100, len(data))
            
            return data
        
        df = generate_sample_data()
        st.info("🎪 Using sample business data!")
    
    st.markdown("---")
    st.markdown("<h2 style='color: #ff6b95;'>🎨 Customization</h2>", unsafe_allow_html=True)
    
    theme_choice = st.selectbox(
        "Color Theme",
        ["Pink Blossom 🌸", "Mint Candy 🍬", "Lavender Dream 💜", "Sunshine Yellow 🌞"]
    )
    
    # Get theme colors
    theme = get_theme_colors(theme_choice)

# 🎪 Main Dashboard
if df is not None:
    # Display dataset info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: {theme['primary']}; margin: 0;'>📊</h3>
            <h2 style='color: {theme['primary']}; margin: 0;'>{len(df):,}</h2>
            <p style='color: #666; margin: 0;'>Total Rows</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: {theme['primary']}; margin: 0;'>📈</h3>
            <h2 style='color: {theme['primary']}; margin: 0;'>{len(df.columns)}</h2>
            <p style='color: #666; margin: 0;'>Columns</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        st.markdown(f"""
        <div class='metric-card'>
            <h3 style='color: {theme['primary']}; margin: 0;'>🔢</h3>
            <h2 style='color: {theme['primary']}; margin: 0;'>{len(numeric_cols)}</h2>
            <p style='color: #666; margin: 0;'>Numeric Columns</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Data Exploration Section
    st.markdown("---")
    st.markdown(f"<h2 style='color: {theme['primary']};'>🔍 Data Exploration</h2>", unsafe_allow_html=True)
    
    # Column selection for analysis
    col1, col2 = st.columns(2)
    
    with col1:
        x_axis = st.selectbox(
            "X-Axis Column",
            df.columns.tolist(),
            index=0 if len(df.columns) > 0 else 0
        )
    
    with col2:
        y_axis = st.selectbox(
            "Y-Axis Column", 
            df.columns.tolist(),
            index=1 if len(df.columns) > 1 else 0
        )
    
    # Chart type selection
    chart_type = st.selectbox(
        "Chart Type",
        ["Line Chart 📈", "Bar Chart 📊", "Scatter Plot 🔵", "Area Chart 🌈"]
    )
    
    # Create chart based on selection
    if st.button("🎨 Generate Chart", use_container_width=True):
        try:
            if chart_type == "Line Chart 📈":
                fig = px.line(
                    df, 
                    x=x_axis, 
                    y=y_axis,
                    title=f"{y_axis} vs {x_axis}",
                    color_discrete_sequence=[theme['primary']]
                )
            elif chart_type == "Bar Chart 📊":
                # For bar charts, let's take top 20 to avoid clutter
                bar_data = df.head(20) if len(df) > 20 else df
                fig = px.bar(
                    bar_data,
                    x=x_axis,
                    y=y_axis,
                    title=f"{y_axis} by {x_axis}",
                    color_discrete_sequence=[theme['primary']]
                )
            elif chart_type == "Scatter Plot 🔵":
                fig = px.scatter(
                    df,
                    x=x_axis,
                    y=y_axis,
                    title=f"{y_axis} vs {x_axis}",
                    color_discrete_sequence=[theme['primary']]
                )
            else:  # Area Chart
                fig = px.area(
                    df,
                    x=x_axis,
                    y=y_axis,
                    title=f"{y_axis} vs {x_axis}",
                    color_discrete_sequence=[theme['primary']]
                )
            
            # Apply cute styling
            fig.update_layout(
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                paper_bgcolor='rgba(255, 255, 255, 0.5)',
                font_family="Comic Neue",
                title_font_color=theme['primary'],
                showlegend=False,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Could not create chart: {str(e)}")
    
    # Data Summary Section
    st.markdown("---")
    st.markdown(f"<h2 style='color: {theme['primary']};'>📋 Data Summary</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Data Preview", "📈 Statistics", "🔍 Column Info"])
    
    with tab1:
        st.dataframe(df.head(10), use_container_width=True)
    
    with tab2:
        if not numeric_cols:
            st.info("No numeric columns found for statistical analysis.")
        else:
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
    
    with tab3:
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Data Type': df.dtypes.values,
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values
        })
        st.dataframe(col_info, use_container_width=True)
    
    # Quick Insights
    st.markdown("---")
    st.markdown(f"<h2 style='color: {theme['primary']};'>💡 Quick Insights</h2>", unsafe_allow_html=True)
    
    if numeric_cols:
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            # Highest value insight
            max_col = df[numeric_cols].max().idxmax()
            max_val = df[numeric_cols].max().max()
            st.info(f"**Highest Value:** `{max_col}` = {max_val:,.2f}")
            
            # Correlation insight (if we have at least 2 numeric columns)
            if len(numeric_cols) >= 2:
                corr = df[numeric_cols[0]].corr(df[numeric_cols[1]])
                st.info(f"**Correlation** between `{numeric_cols[0]}` and `{numeric_cols[1]}`: {corr:.2f}")
        
        with insights_col2:
            # Data freshness insight
            date_cols = df.select_dtypes(include=['datetime']).columns
            if len(date_cols) > 0:
                latest_date = df[date_cols[0]].max()
                st.info(f"**Latest Date:** {latest_date.strftime('%Y-%m-%d')}")
            
            # Missing data insight
            missing_total = df.isnull().sum().sum()
            if missing_total > 0:
                st.warning(f"**Missing Values:** {missing_total} total")
            else:
                st.success("**No missing values found!** 🎉")
    
else:
    # Welcome screen when no data is loaded
    st.markdown("""
    <div style='text-align: center; padding: 4rem; background: rgba(255, 255, 255, 0.9); border-radius: 25px; border: 3px dashed #ffb6c1;'>
        <h2 style='color: #ff6b95;'>🎀 Welcome to DataBunny! 🐰</h2>
        <p style='color: #666; font-size: 1.1rem;'>Upload your data file or try our sample dataset to get started!</p>
        <p style='color: #888;'>Supported formats: CSV, Excel</p>
    </div>
    """, unsafe_allow_html=True)

# 🎊 Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 2rem; background: rgba(255, 255, 255, 0.8); border-radius: 20px; border: 2px solid {theme["secondary"]};'>
    <h3 style='color: {theme["primary"]};'>🐇 Happy Analyzing! 🐇</h3>
    <p style='color: #666;'>Made with 💖 and lots of 🥕</p>
</div>
""", unsafe_allow_html=True)

# 🎵 Fun interaction
if st.sidebar.button("🎉 Spread Some Joy!", use_container_width=True):
    st.balloons()
    st.sidebar.success("🌈 Yay! You made the data extra happy!")