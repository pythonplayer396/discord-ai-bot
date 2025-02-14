import discord
from discord.ext import commands
import google.generativeai as genai
import os
from utils.rate_limiter import RateLimiter
import logging

logger = logging.getLogger('discord')

class AIResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
        self.rate_limiter = RateLimiter()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions:
            if self.rate_limiter.is_rate_limited(str(message.author.id)):
                await message.reply("You're sending messages too quickly! Please wait a moment.")
                return

            try:
                content = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
                response = await self.get_ai_response(content)
                await message.reply(response)

            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await message.reply("Sorry, I encountered an error processing your message. Please try again.")

    async def get_ai_response(self, message: str) -> str:
        try:
            response = await self.model.generate_content_async(message)
            return response.text or "I'm not sure how to respond to that."
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

async def setup(bot):
    await bot.add_cog(AIResponse(bot))
