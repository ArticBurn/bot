import discord
from discord.ext import commands
import requests
import os

from keep_alive import keep_alive


# Masukkan token bot kamu
TOKEN = os.getenv("KEY")
# TOKEN = "NzMyODAxNzc5MDE1NzQ1NjQ3.G1M9P4.L2cN8XZnzFSpHCmT5A0NzueS-eG3pky2qL_OFg"
URL = "https://cdn2.arkdedicated.com/asa/dynamicconfig.ini"

# Inisialisasi bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"✅ Bot {bot.user} sudah online! Slash commands synced: {len(synced)}")

@bot.command()
async def config(ctx):
    """Fetching data from arkdedicated and show to guild"""
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.text[:2000]  # Batasi 2000 karakter (batas Discord)
            await ctx.send(f"```ini\n{data}\n```")
        else:
            await ctx.send("⚠️ Failed for fetching the data.")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# Slash command /rate
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

# Jalankan bot
keep_alive()
bot.run(TOKEN)
