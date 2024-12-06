from discord import ui, Interaction, ButtonStyle, Embed
from discord.ui import Modal, TextInput
from discord.ext import commands
from datetime import datetime
from logger_config import logger
from FirebaseData import FirebaseData
import discord
from utils import create_league_data


class SetupView(ui.View):
    def __init__(self, firebase_data: FirebaseData):
        super().__init__(timeout=None)
        self.is_private = False  # Toggle state for league type
        self.firebase_data = firebase_data  # Store the FirebaseData instance


    @ui.button(label="Public League", style=ButtonStyle.primary, custom_id="public_league")
    async def public_league(self, interaction: Interaction, button: ui.Button):
        self.is_private = False
        await self.open_setup_modal(interaction)

    @ui.button(label="Private League", style=ButtonStyle.secondary, custom_id="private_league")
    async def private_league(self, interaction: Interaction, button: ui.Button):
        self.is_private = True
        await self.open_setup_modal(interaction)

    async def open_setup_modal(self, interaction: Interaction):
        """Open the modal with fields based on the league type."""
        modal = SetupModal(is_private=self.is_private, firebase_data=self.firebase_data)
        await interaction.response.send_modal(modal)


class SetupModal(Modal, title="Setup Your Fantasy League"):
    def __init__(self, is_private: bool, firebase_data: FirebaseData):
        super().__init__()
        self.is_private = is_private
        self.firebase_data = firebase_data

        # Always required field
        self.league_id = TextInput(
            label="League ID",
            placeholder="Enter your Fantasy League ID",
            required=True,
            style=discord.TextStyle.short,
        )
        self.add_item(self.league_id)

        if is_private:
            # Add optional fields for private leagues
            self.espn_s2 = TextInput(
                label="ESPN_s2",
                placeholder="Only required for private leagues",
                required=False,
                style=discord.TextStyle.short,
            )
            self.add_item(self.espn_s2)

            self.swid = TextInput(
                label="SWID",
                placeholder="Only required for private leagues",
                required=False,
                style=discord.TextStyle.short,
            )
            self.add_item(self.swid)

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        league_id = self.league_id.value
        espn_s2 = self.espn_s2.value if self.is_private else None
        swid = self.swid.value if self.is_private else None

        # Log the submitted data
        logger.info(f"Setup Modal Submitted: League ID={league_id}, ESPN_s2={espn_s2}, SWID={swid}")

        # Validate and process the data
        try:
            # Validate the league data
            league_data = await create_league_data(
                interaction=interaction, league_id=league_id, espn_s2=espn_s2, swid=swid
            )

            # Save to Firebase
            guild_info = {
                "discord_guild_name": interaction.guild.name,
                "guild_entry_created_at": datetime.utcnow().isoformat(),
                "guild_entry_last_updated": datetime.utcnow().isoformat(),
                "is_registered": True,
            }

            fantasy_league_info = {"league_id": str(league_id)}
            if self.is_private:
                fantasy_league_info["espn"] = {"espn_s2": espn_s2, "swid": swid}

            new_guild_data = {"guild_info": guild_info, "fantasy_league_info": fantasy_league_info}
            logger.debug(f"New guild data: {new_guild_data}")
            logger.debug(f"Guild ID: {interaction.guild.id}")
            self.firebase_data.add_new_guild(data=new_guild_data, guild_id=str(interaction.guild.id))

            # Success message
            await interaction.response.send_message(
                "Setup successful! Call `/standings` to see how your season is going!", ephemeral=True
            )
        except Exception as e:
            logger.error(f"Error during setup: {e}")
            await interaction.response.send_message(
                "Invalid credentials or league ID. Please check your inputs and try again.", ephemeral=True
            )