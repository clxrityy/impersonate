import os
from typing import Optional
from discord import app_commands
import discord
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env.local")
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))  # Ensure GUILD_ID is an integer
ENV = os.getenv("ENV", "development")  # Default to 'development' if not set

intents = discord.Intents.default()
intents.webhooks = True
intents.message_content = True  # Required for message content in interactions
intents.members = True  # Required to get member information

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        if ENV == "development":
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()


client = Client()

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})") # type: ignore
    print("------")
    
    
@client.tree.command(name="impersonate", description="Impersonate a user")
@app_commands.describe(user="The user to impersonate", message="The message to send")
async def impersonate(interaction: discord.Interaction, user: discord.User, message: str, channel: Optional[discord.TextChannel]):
    target_channel = channel or interaction.channel
    member = interaction.guild.get_member(user.id) # type: ignore

    if not member or not target_channel.permissions_for(member).manage_webhooks: # type: ignore
        await interaction.response.send_message("You do not have permission to manage webhooks", ephemeral=True)
    
    try:
        webhook = await target_channel.create_webhook(name=user.name, avatar=user._avatar) # type: ignore
        await webhook.send(message, username=user.name, avatar_url=user.display_avatar.url)
        await webhook.delete()
        await interaction.response.send_message(f"Impersonated {user.mention} successfully!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I do not have permission to create webhooks in this channel.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"An error occurred while trying to impersonate: {e}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)

client.run(token=TOKEN) # type: ignore