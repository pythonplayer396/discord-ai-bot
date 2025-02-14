import os
import discord
from discord.ext import commands
import asyncio
from config import load_config

# Set up logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord')

class AIBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        try:
            await self.load_extension('cogs.ai_response')
            logger.info('AI Response cog loaded')
        except Exception as e:
            logger.error(f'Error loading AI Response cog: {e}')
            raise

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('Bot is ready to respond to mentions!')

    async def on_error(self, event_method: str, *args, **kwargs):
        logger.error(f'Error in {event_method}:', exc_info=True)

async def main():
    if not load_config():
        logger.error("Failed to load configuration")
        return

    bot = AIBot()
    try:
        async with bot:
            await bot.start(os.getenv('DISCORD_TOKEN'))
    except discord.LoginFailure:
        logger.error("Failed to login. Please check your Discord token.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    asyncio.run(main())
