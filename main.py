import discord
from discord.ext import commands
import requests
import os

from keep_alive import keep_alive

TOKEN = os.getenv("DISCORD_TOKEN")
URL = "https://cdn2.arkdedicated.com/asa/dynamicconfig.ini"

# initiate
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"✅ Bot {bot.user} sudah online! Slash commands synced: {len(synced)}")

# Rich Presence (Custom Status)
    activity = discord.Game(
        name="Shit with scammed ppl" 
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)

# command /raw
@bot.tree.command(name="raw", description="Fetching data from arkdedicated")
async def rate(interaction: discord.Interaction):
    """Fetching data from arkdedicated and show to guild"""
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.text[:2000]  # Batasi 2000 karakter (batas Discord)
            await interaction.response.send_message(f"```ini\n{data}\n```")
        else:
            await interaction.response.send_message("⚠️ Failed for fetching the data.")
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}")

# run_bot
keep_alive()
bot.run(TOKEN)
