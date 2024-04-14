import discord
import requests
import asyncio
import json
import datetime

# Discord bot token
TOKEN = 'TOKEN' # REPLACE WITH YOUR BOT TOKEN
CHANNEL_ID = 0 # REPLACE WITH YOUR CHANNEL ID

# List of usernames
usernames = []

# Function to fetch data from the API
async def fetch_data():
    results = {}
    for username in usernames:
        url = f'http://api.faceit.myhosting.info:81/?n={username}'
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = json.loads(response.text)
                level = data["level"]
                elo = data["elo"]
                trend = data["trend"]
                elogain = data["today"]["elo"]
                results[username] = level, elo, trend, elogain
            except (KeyError, ValueError) as e:
                print(f"Error parsing response for user {username}: {e}. Response content: {response.content}")
    return results

# Discord client
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Function to update leaderboard every 3 minutes
def format_leaderboard_embed(results):
    embed = discord.Embed(title="CS2 FACEIT Leaderboard", color=discord.Color.orange(), description="A leaderboard to show FACEIT recent match trend, elo and today's difference.")
    emoji_ids = {
        # REPLACE EACH 0 WITH EMOJI ID
        10: 0,
        9: 0,
        8: 0,
        7: 0,
        6: 0,
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0 
    }
    sorted_results = sorted(results.items(), key=lambda x: x[1][1], reverse=True)  # Sort by elo rating (index 1)

    # Get len of longest elo gain to generate padding after
    try:
        highest_elogain = max(len(str(item[-1])) for _, item in sorted_results)
        print(highest_elogain)
    except:
        highest_elogain = 1

    for username, (level, elo, trend, elogain) in sorted_results:
        padding = " " * (30 - len(username))  # Calculate padding to make the length of username 30 characters
        padding2 = " " * (highest_elogain - len(str(elogain)))
        emoji_id = emoji_ids.get(int(level), None)
        trend = trend.replace('W', '🟢').replace('L', '🔴')
        embed.add_field(name=f"<:{level}:{emoji_id}> ```{username}{padding}{trend} • {elo} ({elogain}){padding2}``` ", value="", inline=False)

    # Add footer with timestamp in BST (UTC+1)
    timestamp_utc = datetime.datetime.utcnow()
    timestamp_bst = timestamp_utc + datetime.timedelta(hours=1)  # Convert UTC to BST
    timestamp = timestamp_bst.strftime("%b %d, %Y - %H:%M:%S")
    embed.set_footer(text=f"Last updated: {timestamp} (UTC+1)", icon_url="https://play-lh.googleusercontent.com/4iFS-rI0ImIFZyTwjidPChDOTUGxZqX2sCBLRsf9g_noMIUnH9ywsCmCzSu9vSM9Jg")

    return embed

# Function to update leaderboard every 3 minutes
async def update_leaderboard():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)  
    leaderboard_message = None  # Variable to store the leaderboard message
    while not client.is_closed():
        results = await fetch_data()
        leaderboard_embed = format_leaderboard_embed(results)

        # If the leaderboard message hasn't been sent yet, send it
        if leaderboard_message is None:
            leaderboard_message = await channel.send(embed=leaderboard_embed)
        else:
            # Edit the existing message with the updated leaderboard and timestamp
            await leaderboard_message.edit(embed=leaderboard_embed)

        await asyncio.sleep(180)

# Event: Bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID) 

    # Check for existing messages in the channel
    async for message in channel.history(limit=None):
        if message.author == client.user:
            # If the message is sent by the bot, delete it
            await message.delete()

    client.loop.create_task(update_leaderboard())

# Run the bot
async def main():
    await client.start(TOKEN)

asyncio.run(main())

