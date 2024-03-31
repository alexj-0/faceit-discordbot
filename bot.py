import discord
import requests
import asyncio
import json
import datetime

# Discord bot token
TOKEN = 'BOT TOKEN'

# List of usernames
usernames = ["USERNAME LIST"]

# Function to fetch data from the API
async def fetch_data():
    results = {}
    for username in usernames:
        url = f'https://api.satont.ru/faceit?nick={username}&view=%7Blvl%7D%2C%20%7Belo%7D&game=cs2'
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.text.split(', ')  # Split the response by ', ' to extract level and elo
                lvl = int(data[0])
                elo = int(data[1])
                results[username] = lvl, elo
            except (IndexError, ValueError) as e:
                print(f"Error parsing response for user {username}: {e}. Response content: {response.content}")
    return results

# Discord client
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Function to update leaderboard every 5 minutes
def format_leaderboard_embed(results):
    embed = discord.Embed(title="CS2 FACEIT Leaderboard", color=discord.Color.orange())
    emoji_ids = {
        10: 1223739013207166996,
        9: 1223739012137750699,
        8: 1223739010665414769,
        7: 1223739009667170364,
        6: 1223739008220270813
    }
    sorted_results = sorted(results.items(), key=lambda x: x[1][1], reverse=True)  # Sort by elo rating (index 1)
    for username, (lvl, elo) in sorted_results:
        padding = " " * (30 - len(username))  # Calculate padding to make the length of username 30 characters
        emoji_id = emoji_ids.get(lvl, None)
        if emoji_id:
            emoji = f"<:{lvl}:{emoji_id}>"
        else:
            emoji = ""
        # Create a clickable username using Discord's markdown syntax for hyperlinks
        embed.add_field(name=f"<:{lvl}:{emoji_id}> ```{username}{padding}{elo}```", value="", inline=False)

    # Add footer with timestamp in BST (UTC+1)
    timestamp_utc = datetime.datetime.utcnow()
    timestamp_bst = timestamp_utc + datetime.timedelta(hours=1)  # Convert UTC to BST
    timestamp = timestamp_bst.strftime("%Y-%m-%d %H:%M:%S")
    embed.set_footer(text=f"Last updated: {timestamp} UTC+1")

    return embed

# Function to update leaderboard every minute
async def update_leaderboard():
    await client.wait_until_ready()
    channel = client.get_channel("CHANNEL ID")  # Replace your_channel_id_here with actual channel ID
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

        await asyncio.sleep(300)  # 60 seconds = 1 minute


# Event: Bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    client.loop.create_task(update_leaderboard())

# Run the bot
async def main():
    await client.start(TOKEN)

asyncio.run(main())
