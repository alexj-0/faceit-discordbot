
# FACEIT Discord Leaderboard
This bot will produce a FACEIT elo leaderboard in a Discord channel. It is created in Python, has no commands. It will remove its own messages upon restarting and edit the leaderboard message every 3 minutes upon refresh.

## Setting Up
There are four things which are required:
- List of usernames (FACEIT usernames)
- A Discord bot token
- A Discord channel ID (by right clicking on a channel )
- Emojis in your Discord for FACEIT levels (these images are included in the assets folder)

First, create a list of FACEIT usernames. Add these to the `usernames` list in `bot.py`.

You will then need to create a bot on the Discord Developer portal. Navigate to https://discord.com/developers/applications and create a "New Application". Once the bot is set up, ensure it has permissions to manage messages and copy the bot token. Assign this in `bot.py` under the `TOKEN` variable.

Add the bot to your Discord server through an invite link.

Next, find a channel to contain the leaderboard. Ensure nobody can message in this channel except for the bot. Right click the channel and choose "Copy Channel ID". Assign this to the `CHANNEL_ID` variable in `bot.py`.

Finally, add the emojis to your Discord server. Get the emoji IDs and assign them to each respective variable in `bot.py`. The assets for the FACEIT levels can be found in the assets folder in this repo. You can get the emoji ID by simply selecting an emoji and prefixing it with a backslash. It will return the emoji ID in the channel. If you wish to remove the emojis in the leaderboard, change the `showEmoji` variable to `False`.

The bot also refreshes every ten minutes. This can be adjusted by changing the `refreshTimer` variable. However, I recommend keeping this at 10 minutes to avoid being rate limited. The embed message uses the hex code `#ff6d27` for the colour strip along the left side of the leaderboard message. This can also be changed by changing the `customColor` variable.

## API 
This bot collects data from the following API:
http://api.faceit.myhosting.info:81/

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required** |

It will cycle through the `usernames` list to check for every `username`.

Takes takes a username and we pull the following fields:
- `level`
- `elo`
- `trend`
- `today/elo`

## Example Output
![Leaderboard Screenshot](https://i.imgur.com/GCQ31Yo.png)
