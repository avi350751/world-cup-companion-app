import pandas as pd
import streamlit as st
from pathlib import Path

def load_default_data():
    """Load the default CSV file"""
    try:
        csv_path = Path(__file__).parent.parent / "data" / "2026_FIFA_World_Cup_Players_2.csv"
        if not csv_path.exists():
            return None

        df = pd.read_csv(csv_path)
        df = df.fillna("")
        return df
    except Exception as e:
        st.error(f"Error loading default data: {e}")
        return None

def validate_dataframe(df):
    """Validate that the dataframe has required columns"""
    required_cols = [
        "Player_Name", "Country", "Club", "Position", "Age",
        "WC_Appearances", "WC_Goals", "WC_Assists", "IsMVP",
        "Height_cm", "Weight_kg", "Jersey_Number"
    ]
    missing = [col for col in required_cols if col not in df.columns]
    return len(missing) == 0, missing

def load_custom_data(uploaded_file):
    """Load data from user uploaded file"""
    try:
        df = pd.read_csv(uploaded_file)
        df = df.fillna("")
        is_valid, missing = validate_dataframe(df)
        return df, is_valid, missing
    except Exception as e:
        return None, False, [str(e)]

def get_countries(df):
    """Get list of unique countries from dataframe"""
    return sorted(df["Country"].unique())

def get_players_by_country(df, country):
    """Get all players from a specific country"""
    return df[df["Country"] == country].sort_values("Player_Name").to_dict("records")

def get_country_stats(df, country):
    """Get statistics for a country"""
    country_df = df[df["Country"] == country]

    return {
        "total_players": len(country_df),
        "mvp_count": len(country_df[country_df["IsMVP"] == "Yes"]),
        "total_wc_goals": int(country_df["WC_Goals"].sum()),
        "total_wc_assists": int(country_df["WC_Assists"].sum()),
        "avg_wc_appearances": float(country_df["WC_Appearances"].mean()),
        "positions": country_df["Position"].value_counts().to_dict(),
        "avg_age": float(country_df["Age"].mean()),
    }

def get_top_players_by_country(df, country, limit=5):
    """Get top players by combined score (goals + assists)"""
    country_df = df[df["Country"] == country].copy()
    country_df["combined_score"] = country_df["WC_Goals"].astype(int) + country_df["WC_Assists"].astype(int)
    return country_df.nlargest(limit, "combined_score").to_dict("records")
