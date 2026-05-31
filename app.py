import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import (
    load_default_data, load_custom_data, validate_dataframe,
    get_countries, get_players_by_country, get_country_stats, get_top_players_by_country
)
from src.predictions import calculate_country_strength, get_detailed_analysis
from src.constants import COUNTRY_FLAGS, SPORT_COLORS, POSITION_GROUPS, CONTINENT_MAP

# Utility function to convert cm to feet and inches
def cm_to_feet_inches(cm):
    """Convert centimeters to feet and inches format"""
    if not cm or cm == "":
        return "N/A"
    try:
        cm = int(cm)
        feet = cm // 30.48
        inches = (cm % 30.48) / 2.54
        return f"{int(feet)}-{int(inches)}"
    except (ValueError, TypeError):
        return "N/A"

# Page config
st.set_page_config(
    page_title="🏆 World Cup 2026 Companion",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern sporty look
st.markdown("""
    <style>
    :root {
        --primary: #1f77e3;
        --secondary: #ff6b35;
        --accent: #ffd60a;
        --success: #06a77d;
        --dark: #1a1a1a;
        --light: #f8f9fa;
    }

    * {
        margin: 0;
        padding: 0;
    }

    body {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%);
        color: #fff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .main {
        padding: 0;
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%);
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        border-bottom: 3px solid #1f77e3;
        background: transparent;
        padding: 0 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 1.2rem 2.5rem !important;
        border-radius: 8px 8px 0 0;
        background: transparent !important;
        border: none !important;
        color: #fff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1f77e3, #ff6b35) !important;
        color: #fff !important;
        border: none !important;
    }

    .stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
        background: rgba(31, 119, 227, 0.15) !important;
        color: #fff !important;
    }

    /* Tab content */
    [data-testid="stTabContent"] {
        padding: 2.5rem 2rem !important;
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(31, 119, 227, 0.1), rgba(255, 107, 53, 0.1));
        border: 2px solid #1f77e3;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #ff6b35;
        box-shadow: 0 8px 20px rgba(255, 107, 53, 0.2);
    }

    .stat-box {
        background: linear-gradient(135deg, #1f77e3, #00d4ff);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        color: white;
        font-weight: bold;
    }

    .team-card {
        background: linear-gradient(135deg, rgba(31, 119, 227, 0.15), rgba(255, 107, 53, 0.15));
        border: 2px solid rgba(31, 119, 227, 0.3);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .team-card:hover {
        border-color: #ff6b35;
        transform: scale(1.05);
        box-shadow: 0 8px 24px rgba(255, 107, 53, 0.3);
    }

    .player-card {
        background: linear-gradient(135deg, rgba(31, 119, 227, 0.2), rgba(255, 107, 53, 0.1));
        border-left: 4px solid #ff6b35;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .player-card:hover {
        border-left-color: #ffd60a;
        box-shadow: 0 8px 20px rgba(31, 119, 227, 0.2);
        transform: translateX(5px);
    }

    .prediction-box {
        background: linear-gradient(135deg, #1f77e3, #0099ff);
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin: 1.5rem 0;
    }

    .mvp-badge {
        display: inline-block;
        background: linear-gradient(135deg, #ffd60a, #ff6b35);
        color: #000;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
    }

    h1, h2, h3 {
        background: linear-gradient(135deg, #1f77e3, #ff6b35);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 1rem;
    }

    .header-logo {
        text-align: center;
        font-size: 4rem;
        margin: 2rem 0;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .progress-bar {
        background: linear-gradient(90deg, #1f77e3, #ff6b35, #ffd60a);
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
    }

    .stButton>button {
        background: linear-gradient(135deg, #1f77e3, #ff6b35);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(255, 107, 53, 0.3);
    }

    .stSelectbox, .stMultiSelect {
        border-radius: 8px !important;
    }

    .flag-emoji {
        font-size: 2.5rem;
        margin: 0.5rem;
    }

    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "df" not in st.session_state:
    st.session_state.df = None
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

def render_header():
    """Render app header with WC 2026 logo and title"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='header-logo'>🏆⚽🌍</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin: 0;'>World Cup 2026 Companion</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #ff6b35; font-size: 1.1rem; margin-top: 0.5rem;'>📍 USA</p>", unsafe_allow_html=True)

def render_team_showcase(df):
    """Render teams in an artistic grid layout"""
    countries = sorted(get_countries(df))

    st.markdown("### 🌐 Participating Teams")

    # Group countries by continent
    continent_cols = {}
    for continent, country_list in CONTINENT_MAP.items():
        continent_cols[continent] = [c for c in country_list if c in countries]

    for continent, countries_in_continent in continent_cols.items():
        if countries_in_continent:
            st.markdown(f"#### {continent}")
            cols = st.columns(min(8, len(countries_in_continent)))
            for idx, country in enumerate(countries_in_continent):
                with cols[idx % len(cols)]:
                    flag = COUNTRY_FLAGS.get(country, "🏳️")
                    stats = get_country_stats(df, country)
                    st.markdown(f"""
                        <div class='team-card' title='{country}'>
                            <div style='font-size: 2.5rem;'>{flag}</div>
                            <div style='font-weight: bold; margin: 0.5rem 0;'>{country}</div>
                            <div style='font-size: 0.8rem; color: #00d4ff;'>👥 {stats['total_players']} players</div>
                            <div style='font-size: 0.8rem; color: #ffd60a;'>⭐ {stats['mvp_count']} MVPs</div>
                        </div>
                        """, unsafe_allow_html=True)
            st.markdown("---")

# Tab 1: File Loader & Team Showcase
def tab1_showcase():
    render_header()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📤 Load Player Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", label_visibility="collapsed")

        if uploaded_file is not None:
            df, is_valid, missing = load_custom_data(uploaded_file)
            if is_valid:
                st.session_state.df = df
                st.session_state.data_loaded = True
                st.success("✅ Data loaded successfully!")
            else:
                st.error(f"❌ Missing required columns: {', '.join(missing)}")
        elif not st.session_state.data_loaded:
            if st.button("📂 Load Default Data", use_container_width=True):
                df = load_default_data()
                if df is not None:
                    is_valid, missing = validate_dataframe(df)
                    if is_valid:
                        st.session_state.df = df
                        st.session_state.data_loaded = True
                        st.success("✅ Default data loaded!")
                    else:
                        st.error(f"❌ Invalid default data: {missing}")

    with col2:
        if st.session_state.data_loaded and st.session_state.df is not None:
            df = st.session_state.df
            st.markdown("### 📊 Data Summary")
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                        <div class='stat-box'>
                            <div style='font-size: 2rem;'>🌍</div>
                            <div>{len(get_countries(df))} Teams</div>
                        </div>
                        <div class='stat-box'>
                            <div style='font-size: 2rem;'>👥</div>
                            <div>{len(df)} Players</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    if st.session_state.data_loaded and st.session_state.df is not None:
        render_team_showcase(st.session_state.df)
    else:
        st.info("👉 Load a CSV file to see participating teams!")

# Tab 2: Player Finder
def tab2_player_finder():
    if not st.session_state.data_loaded or st.session_state.df is None:
        st.warning("⚠️ Please load data from Tab 1 first!")
        return

    df = st.session_state.df

    st.markdown("<h1 style='text-align: center;'>🔍 Player Finder</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_country = st.selectbox(
            "Select Country",
            options=get_countries(df),
            key="player_country"
        )

    players = get_players_by_country(df, selected_country)
    player_names = [p["Player_Name"] for p in players]

    with col2:
        selected_player_name = st.selectbox(
            "Select Player",
            options=player_names,
            key="player_name"
        )

    with col3:
        flag = COUNTRY_FLAGS.get(selected_country, "🏳️")
        st.markdown(f"""
            <div style='text-align: center; padding: 1rem; background: rgba(31, 119, 227, 0.1); border-radius: 8px; height: 100%;'>
                <div style='font-size: 2.5rem;'>{flag}</div>
                <div style='font-weight: bold; margin-top: 0.5rem;'>{selected_country}</div>
            </div>
            """, unsafe_allow_html=True)

    # Get selected player
    player = next((p for p in players if p["Player_Name"] == selected_player_name), None)

    if player:
        st.markdown("---")

        mvp_badge = "⭐ MVP" if player["IsMVP"] == "Yes" else ""

        st.markdown(f"""
            <div class='metric-card'>
                <h2>{player['Player_Name']} {COUNTRY_FLAGS.get(selected_country, '🏳️')} #{player['Jersey_Number']}</h2>
                {f"<div class='mvp-badge'>{mvp_badge}</div>" if mvp_badge else ""}
            </div>
            """, unsafe_allow_html=True)

        # Basic Info
        st.markdown("### 👤 Basic Information")
        col_a, col_b, col_c, col_d = st.columns(4)

        with col_a:
            st.markdown(f"""
                <div class='stat-box' style='background: linear-gradient(135deg, #1f77e3, #00d4ff);'>
                    <div style='font-size: 0.9rem; opacity: 0.9;'>Position</div>
                    <div style='font-size: 1.5rem; margin-top: 0.5rem;'>{POSITION_GROUPS.get(player['Position'].split('/')[0], '⚽')}</div>
                    <div style='font-size: 1rem;'>{player['Position']}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
                <div class='stat-box' style='background: linear-gradient(135deg, #ff6b35, #ff9a56);'>
                    <div style='font-size: 0.9rem; opacity: 0.9;'>Age</div>
                    <div style='font-size: 1.5rem; margin-top: 0.5rem;'>{player['Age']}</div>
                    <div style='font-size: 0.8rem;'>years old</div>
                </div>
                """, unsafe_allow_html=True)

        with col_c:
            st.markdown(f"""
                <div class='stat-box' style='background: linear-gradient(135deg, #ffd60a, #ffd60a);'>
                    <div style='font-size: 0.9rem; opacity: 0.9; color: #000;'>Club</div>
                    <div style='font-size: 0.85rem; margin-top: 0.5rem; color: #000;'>{player['Club']}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_d:
            height_ft = cm_to_feet_inches(player['Height_cm'])
            st.markdown(f"""
                <div class='stat-box' style='background: linear-gradient(135deg, #06a77d, #00d4aa);'>
                    <div style='font-size: 0.9rem; opacity: 0.9;'>Height</div>
                    <div style='font-size: 1.2rem; margin-top: 0.5rem;'>{height_ft}</div>
                    <div style='font-size: 0.8rem;'>{player['Height_cm']} cm</div>
                </div>
                """, unsafe_allow_html=True)

        # World Cup Stats
        st.markdown("### 🏆 World Cup Statistics")
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown(f"""
                <div class='stat-box' style='background: linear-gradient(135deg, #1f77e3, #00d4ff);'>
                    <div style='font-size: 0.9rem; opacity: 0.9;'>Appearances</div>
                    <div style='font-size: 2rem; margin-top: 0.5rem;'>{player['WC_Appearances']}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
                <div class='stat-box' style='background: linear-gradient(135deg, #ff6b35, #ff9a56);'>
                    <div style='font-size: 0.9rem; opacity: 0.9;'>Goals</div>
                    <div style='font-size: 2rem; margin-top: 0.5rem;'>⚽ {player['WC_Goals']}</div>
                </div>
                """, unsafe_allow_html=True)

        with col_c:
            st.markdown(f"""
                <div class='stat-box' style='background: linear-gradient(135deg, #06a77d, #00d4aa);'>
                    <div style='font-size: 0.9rem; opacity: 0.9;'>Assists</div>
                    <div style='font-size: 2rem; margin-top: 0.5rem;'>🎯 {player['WC_Assists']}</div>
                </div>
                """, unsafe_allow_html=True)

        # Physical Stats
        st.markdown("### 💪 Additional Details")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span>⚖️ Weight</span>
                        <strong>{player['Weight_lbs']} lbs ({player['Weight_kg']} kg)</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span>🏟️ Jersey</span>
                        <strong>#{player['Jersey_Number']}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Tab 3: Country Analysis & Predictions
def tab3_analysis():
    if not st.session_state.data_loaded or st.session_state.df is None:
        st.warning("⚠️ Please load data from Tab 1 first!")
        return

    df = st.session_state.df

    st.markdown("<h1 style='text-align: center;'>📊 Country Analysis & Predictions</h1>", unsafe_allow_html=True)

    selected_country = st.selectbox(
        "Select Country for Analysis",
        options=get_countries(df),
        key="analysis_country"
    )

    flag = COUNTRY_FLAGS.get(selected_country, "🏳️")

    # Country Header
    st.markdown(f"""
        <div style='text-align: center; margin: 2rem 0;'>
            <div style='font-size: 3.5rem;'>{flag}</div>
            <h1>{selected_country}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Country Overview Section
    st.markdown("### 🌐 Country Overview")

    stats = get_country_stats(df, selected_country)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"""
            <div class='stat-box' style='background: linear-gradient(135deg, #1f77e3, #00d4ff);'>
                <div>👥 Players</div>
                <div style='font-size: 2rem; margin-top: 0.5rem;'>{stats['total_players']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='stat-box' style='background: linear-gradient(135deg, #ffd60a, #ff6b35);'>
                <div>⭐ MVPs</div>
                <div style='font-size: 2rem; margin-top: 0.5rem;'>{stats['mvp_count']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='stat-box' style='background: linear-gradient(135deg, #ff6b35, #ff9a56);'>
                <div>⚽ Goals</div>
                <div style='font-size: 2rem; margin-top: 0.5rem;'>{stats['total_wc_goals']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class='stat-box' style='background: linear-gradient(135deg, #06a77d, #00d4aa);'>
                <div>🎯 Assists</div>
                <div style='font-size: 2rem; margin-top: 0.5rem;'>{stats['total_wc_assists']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
            <div class='stat-box' style='background: linear-gradient(135deg, #9d4edd, #c77dff);'>
                <div>📈 Avg Age</div>
                <div style='font-size: 2rem; margin-top: 0.5rem;'>{stats['avg_age']:.1f}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Top 5 Players
    st.markdown("### 🏅 Top 5 Players")

    top_players = get_top_players_by_country(df, selected_country, limit=5)

    if top_players:
        for idx, player in enumerate(top_players, 1):
            mvp_indicator = "⭐" if player["IsMVP"] == "Yes" else ""
            combined_score = int(player["WC_Goals"]) + int(player["WC_Assists"])

            st.markdown(f"""
                <div class='player-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h3 style='margin: 0;'>#{idx} {player['Player_Name']} {mvp_indicator}</h3>
                            <div style='color: #999; margin-top: 0.3rem;'>{player['Club']} • {player['Position']}</div>
                        </div>
                        <div style='text-align: right;'>
                            <div style='font-size: 2.5rem; color: #ffd60a;'>{combined_score}</div>
                            <div style='color: #999; font-size: 0.85rem;'>Goals + Assists</div>
                        </div>
                    </div>
                    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem; font-size: 0.9rem;'>
                        <div>⚽ Goals: <strong>{player['WC_Goals']}</strong></div>
                        <div>🎯 Assists: <strong>{player['WC_Assists']}</strong></div>
                        <div>🏆 Appearances: <strong>{player['WC_Appearances']}</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No players found for this country.")

    st.markdown("---")

    # Performance Analysis & Prediction
    st.markdown("### 🎯 Performance Analysis & Prediction")

    strength_score, stage, detail, confidence = calculate_country_strength(df, selected_country)

    # Prediction card
    st.markdown(f"""
        <div class='prediction-box'>
            <h2 style='-webkit-text-fill-color: white; color: white;'>Tournament Prediction</h2>
            <div style='font-size: 2.5rem; margin: 1rem 0;'>{stage}</div>
            <div style='font-size: 1.2rem; margin: 1rem 0; color: rgba(255, 255, 255, 0.9);'>{detail}</div>
            <div style='margin-top: 1.5rem;'>
                <div style='font-size: 0.9rem; color: rgba(255, 255, 255, 0.8); margin-bottom: 0.5rem;'>Confidence Level: {confidence}</div>
                <div style='background: rgba(0, 0, 0, 0.3); border-radius: 10px; height: 12px; overflow: hidden;'>
                    <div style='background: linear-gradient(90deg, #ffd60a, #ff6b35); height: 100%; width: {strength_score}%;'></div>
                </div>
                <div style='margin-top: 0.5rem; font-size: 0.9rem;'>Strength Score: {strength_score:.1f}/100</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Detailed Analysis
    st.markdown("### 📈 Detailed Analysis")

    analysis = get_detailed_analysis(df, selected_country)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem; color: #999; margin-bottom: 0.5rem;'>Experienced Players</div>
                <div style='font-size: 2.5rem; color: #00d4ff;'>{analysis['experienced_players']}</div>
                <div style='font-size: 0.8rem; color: #999; margin-top: 0.5rem;'>2+ WC appearances</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem; color: #999; margin-bottom: 0.5rem;'>Goalscorers</div>
                <div style='font-size: 2.5rem; color: #ff6b35;'>{analysis['goalscorers']}</div>
                <div style='font-size: 0.8rem; color: #999; margin-top: 0.5rem;'>1+ WC goals</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 0.9rem; color: #999; margin-bottom: 0.5rem;'>Playmakers</div>
                <div style='font-size: 2.5rem; color: #06a77d;'>{analysis['assisters']}</div>
                <div style='font-size: 0.8rem; color: #999; margin-top: 0.5rem;'>1+ WC assists</div>
            </div>
            """, unsafe_allow_html=True)

    # Position Distribution
    st.markdown("### 🎯 Squad Composition")

    positions = analysis['position_distribution']
    position_data = []

    for position, count in sorted(positions.items(), key=lambda x: x[1], reverse=True):
        icon = POSITION_GROUPS.get(position, "⚽")
        position_data.append({"Position": position, "Count": count, "Icon": icon})

    col_positions = st.columns(min(4, len(position_data)))
    for idx, pos_info in enumerate(position_data):
        with col_positions[idx % len(col_positions)]:
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 2rem;'>{pos_info['Icon']}</div>
                    <div style='margin-top: 0.5rem;'><strong>{pos_info['Position']}</strong></div>
                    <div style='font-size: 1.5rem; color: #00d4ff; margin-top: 0.3rem;'>{pos_info['Count']}</div>
                </div>
                """, unsafe_allow_html=True)

# Main app logic
def main():
    tab1, tab2, tab3 = st.tabs(["🏆 Teams & Data", "🔍 Player Details", "📊 Analysis"])

    with tab1:
        tab1_showcase()

    with tab2:
        tab2_player_finder()

    with tab3:
        tab3_analysis()

if __name__ == "__main__":
    main()
