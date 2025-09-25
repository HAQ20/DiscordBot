# Discord Poll Bot

A Discord bot that runs daily polls and tracks results over time. The bot asks a daily question and keeps track of voting results in a leaderboard.

### Prerequisites

- Python 3.7 or higher
- A Discord bot token from the [Discord Developer Portal](https://discord.com/developers/applications)

### Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd DiscordBot
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory:
   ```env
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   ```

4. Configure the bot:
   - Replace `POLL_CHANNEL_ID` in `gooddaybot.py` with your Discord channel ID
   - Customize `POLL_QUESTION` and `POLL_OPTIONS` as needed

5. Run the bot:
   ```bash
   python gooddaybot.py
   ```

## Configuration

Edit the following variables in `gooddaybot.py`:

- `POLL_CHANNEL_ID`: The Discord channel ID where polls will be posted
- `POLL_QUESTION`: The question asked in daily polls
- `POLL_OPTIONS`: The emoji options for voting (currently ✅ and ❌)

## Commands

- `!larry` - Simple larry response
- `!larry_gif` - Posts a larry cat GIF
- `!larry_check` - Shows current poll results and leaderboard

## Environment Variables

The bot requires the following environment variable:

- `DISCORD_BOT_TOKEN`: Your Discord bot token

**Important**: Never commit your `.env` file or expose your bot token. The `.env` file is excluded from version control via `.gitignore`.

## Getting a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application or select an existing one
3. Go to the "Bot" section
4. Click "Reset Token" to generate a new token
5. Copy the token and add it to your `.env` file

## Security

- The bot token is stored in a `.env` file that is excluded from version control
- Never share your bot token publicly
- If your token is compromised, regenerate it immediately in the Discord Developer Portal

## License

This project is open source and available under the [MIT License](LICENSE).