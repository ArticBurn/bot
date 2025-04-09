import discord
from discord import app_commands
from discord.ext import commands
import requests
import os
import yt_dlp
from yt-dlp import YoutubeDL

from keep_alive import keep_alive

TOKEN = os.getenv("DISCORD_TOKEN")
URL = "https://cdn2.arkdedicated.com/asa/dynamicconfig.ini"

# initiate
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"✅ Bot {bot.user} online! Slash commands synced: {len(synced)}")

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

# command /play url
@bot.tree.command(name="play", description="Play mberothhhhh")
@app_commands.describe(url="link")
async def play(interaction: discord.Interaction, url: str):
    if not interaction.user.voice:
        await interaction.response.send_message("join dulu coy", ephemeral=True)
        return

    voice_channel = interaction.user.voice.channel
    if interaction.guild.voice_client is None:
        await voice_channel.connect()
    elif interaction.guild.voice_client.channel != voice_channel:
        await interaction.guild.voice_client.move_to(voice_channel)

    await interaction.response.send_message(f"play : {url}")

    ydl_opts = {
        'format': 'bestaudio',
        'cookiefile': 'cookies.txt'
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']

        source = await discord.FFmpegOpusAudio.from_probe(audio_url, method='fallback')
        interaction.guild.voice_client.play(source)
    except Exception as e:
        await interaction.followup.send(f"error {e}")
        
#command /stop
@bot.tree.command(name="stop", description="stop son2an")
async def stop(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc:
        await vc.disconnect()
        await interaction.response.send_message("kokot")
    else:
        await interaction.response.send_message("ganok tanggapan")

# run_bot
keep_alive()
bot.run(TOKEN)
