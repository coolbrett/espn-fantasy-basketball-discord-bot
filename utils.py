import discord
from logger_config import logger
import espn_api.requests
from datetime import datetime
from LeagueData import LeagueData


async def create_league_data(interaction: discord.Interaction, league_id, espn_s2, swid):
    """Helper function to handle creation of LeagueData"""
    try:
        # Specifying 2025 as year because it is the most recent year
        data = LeagueData(league_id=int(league_id), year=2025, espn_s2=espn_s2, swid=swid)
        return data
    except espn_api.requests.espn_requests.ESPNInvalidLeague as e:
        # Raise an exception to let the caller handle it
        logger.error(f"Error creating LeagueData object: {e}")
        raise ValueError("League credentials are invalid") from e