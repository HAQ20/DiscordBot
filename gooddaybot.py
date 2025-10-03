import discord
from discord.ext import commands, tasks
import json
import asyncio
import os
from datetime import time
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

POLL_CHANNEL_ID = 1415757692424687778  # replace with your channel ID
POLL_OPTIONS = ["✅", "❌"]      # Choices only emojis
POLL_QUESTION = "Czy dzisiejszy dzień był chujowy?" # Poll question

DATA_FILE = "poll_results.json"

#Bot timezone
TIMEZONE = pytz.timezone('Europe/Warsaw')

# --- Load/save data ---
def load_results():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"✅": 0, "❌": 0, "tie": 0}

def save_results(results):
    with open(DATA_FILE, "w") as f:
        json.dump(results, f)

# Add to load/save functions
def load_poll_state():
    try:
        with open("current_poll.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_poll_state(message_id, end_time):
    with open("current_poll.json", "w") as f:
        json.dump({"message_id": message_id, "end_time": end_time.isoformat()}, f)

def clear_poll_state():
    try:
        os.remove("current_poll.json")
    except FileNotFoundError:
        pass

# --- Daily poll task ---
@tasks.loop(hours=24)
async def daily_poll():
    # Calculate next 18:00 in Warsaw timezone
    now = datetime.now(TIMEZONE)
    target = now.replace(hour=18, minute=0, second=0, microsecond=0)
    
    # If it's already past 18:00 today, schedule for tomorrow
    if now >= target:
        target += timedelta(days=1)
    
    # Wait until the target time
    wait_seconds = (target - now).total_seconds()
    if wait_seconds > 0:
        await asyncio.sleep(wait_seconds)

    channel = bot.get_channel(POLL_CHANNEL_ID)
    if not channel:
        return

    # Send poll message
    msg = await channel.send(f"📊 {POLL_QUESTION}")
    # Send role ping immediately after (separate message as you wanted)
    role_ping = await channel.send(f"<@&{1415758700685033584}>")
    
    for emoji in POLL_OPTIONS:
        await msg.add_reaction(emoji)

    # Give users time to vote (e.g. 4 hours)
    await asyncio.sleep(14400)

    # Fetch updated message with reactions
    msg = await channel.fetch_message(msg.id)

    # Count votes
    votes = {emoji: 0 for emoji in POLL_OPTIONS}
    for reaction in msg.reactions:
        if reaction.emoji in POLL_OPTIONS:
            votes[reaction.emoji] = reaction.count - 1  # exclude bot's own reaction

    # Find winner
    if votes["✅"] == votes["❌"]:
        winner = "tie"
    else:
        winner = max(votes, key=votes.get)

    # Save cumulative results
    results = load_results()
    results[winner] += 1
    save_results(results)

    # Announce
    labels = {"✅": "chujowe dni", "❌": "dobre dni", "tie": "remis"}
    leaderboard = "\n".join(f"{labels.get(emoji, emoji)}: {count}" for emoji, count in results.items())
    winner_messages = {
        "✅": "Dziś był chujowy dzień!",
        "❌": "Dziś był dobry dzień!",
        "tie": "Dziś był średni dzień"
    }
    winner_message = winner_messages.get(winner, f"Wynik: {winner}")
    await channel.send(f"{winner_message}\n\n🏆 Leaderboard:\n{leaderboard}")

@bot.command()
async def larry(ctx):
    await ctx.send("larry")

@bot.command()
async def larry_gif(ctx):
    await ctx.send("https://tenor.com/view/larry-larry-cat-chat-larry-meme-chat-meme-cat-gif-10061556685042597078")

@bot.command()
async def larry_check(ctx):
    results = load_results()
    labels = {"✅": "chujowe dni", "❌": "dobre dni", "tie": "remis"}
    leaderboard = "\n".join(f"{labels.get(emoji, emoji)}: {count}" for emoji, count in results.items())
    # Determine winner based on current results
    if results:
        winner = max(results, key=results.get)
        winner_messages = {
            "✅": "Dziś był chujowy dzień!",
            "❌": "Dziś był dobry dzień!",
            "tie": "Dziś był średni dzień"
        }
        winner_message = winner_messages.get(winner, f"Wynik: {winner}")
    else:
        winner_message = "Brak wyników."
    await ctx.send(f"{winner_message}\n\n🏆 Leaderboard:\n{leaderboard}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not daily_poll.is_running():
        daily_poll.start()


# Get the bot token from environment variable
bot_token = os.getenv("DISCORD_BOT_TOKEN")
if not bot_token:
    raise ValueError("DISCORD_BOT_TOKEN environment variable is not set!")

bot.run(bot_token)
