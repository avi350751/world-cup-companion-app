import pandas as pd
from typing import Tuple, Dict

def calculate_country_strength(df, country: str) -> Tuple[float, str, str]:
    """
    Calculate country strength score based on historical WC performance
    Returns: (score, prediction_stage, confidence)
    """
    country_df = df[df["Country"] == country]

    if len(country_df) == 0:
        return 0, "No Data", "Unknown"

    # Calculate metrics
    avg_goals_per_player = country_df["WC_Goals"].astype(int).sum() / len(country_df) if len(country_df) > 0 else 0
    avg_assists_per_player = country_df["WC_Assists"].astype(int).sum() / len(country_df) if len(country_df) > 0 else 0
    mvp_count = len(country_df[country_df["IsMVP"] == "Yes"])
    squad_size = len(country_df)
    avg_wc_appearances = country_df["WC_Appearances"].astype(int).mean()

    # Heuristic scoring
    strength_score = (
        (avg_goals_per_player * 25) +  # Goal scoring potential
        (avg_assists_per_player * 15) +  # Playmaking ability
        (mvp_count * 8) +  # Star power
        (squad_size * 0.2) +  # Squad depth
        (avg_wc_appearances * 3)  # Experience
    )

    # Normalize to 0-100
    strength_score = min(100, strength_score)

    # Determine prediction stage
    if strength_score >= 80:
        stage = "🏆 Strong Contender"
        detail = "Likely to reach Semifinals or Finals"
        confidence = "Very High"
    elif strength_score >= 65:
        stage = "🥈 Competitive Team"
        detail = "Likely to reach Quarterfinals or Semifinals"
        confidence = "High"
    elif strength_score >= 50:
        stage = "⚡ Mid-tier Team"
        detail = "Likely to reach Quarterfinals"
        confidence = "Medium"
    elif strength_score >= 35:
        stage = "🎯 Challenger"
        detail = "Likely to progress from Group Stage"
        confidence = "Medium"
    else:
        stage = "🌟 Underdog"
        detail = "Potential for surprise performances"
        confidence = "Low"

    return strength_score, stage, detail, confidence


def get_detailed_analysis(df, country: str) -> Dict:
    """Get detailed analysis of a country's performance potential"""
    country_df = df[df["Country"] == country]

    if len(country_df) == 0:
        return None

    analysis = {
        "total_players": len(country_df),
        "mvp_count": len(country_df[country_df["IsMVP"] == "Yes"]),
        "goalscorers": len(country_df[country_df["WC_Goals"].astype(int) > 0]),
        "assisters": len(country_df[country_df["WC_Assists"].astype(int) > 0]),
        "avg_wc_appearances": round(country_df["WC_Appearances"].astype(int).mean(), 2),
        "experienced_players": len(country_df[country_df["WC_Appearances"].astype(int) >= 2]),
        "avg_age": round(country_df["Age"].astype(int).mean(), 1),
        "position_distribution": country_df["Position"].value_counts().to_dict(),
    }

    return analysis
