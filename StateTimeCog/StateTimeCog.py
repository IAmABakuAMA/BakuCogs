import asyncio
from datetime import datetime
from pytz import timezone
from discord.ext import commands
from discord import Permissions
from redbot.core import commands, Config, checks


class StateTimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_tasks = {}

    @commands.group(name="timemsg", invoke_without_command=True)
    async def timemsg(self, ctx):
        """Set the timezone for the current channel"""
        await ctx.send("Please provide a timezone in the format of `continent/city`.")
    
    @timemsg.command(name="set")
    @commands.has_permissions(administrator=True)
    async def timemsg_set(self, ctx, timezone_str):
        """Set the timezone for the current channel"""
        try:
            timezone(timezone_str)
        except Exception:
            await ctx.send("Invalid timezone. Please provide a timezone in the format of `continent/city`.")
            return
        await ctx.send(f"Timezone set to {timezone_str}.")
        
        if ctx.channel.id not in self.message_tasks:
            self.message_tasks[ctx.channel.id] = self.bot.loop.create_task(self.update_message(ctx.channel.id, timezone_str))

        
    @timemsg.command(name="remove")
    @commands.has_permissions(administrator=True)
    async def timemsg_remove(self, ctx):
        """Remove the timezone message from the channel"""
        channel_id = ctx.channel.id
        if channel_id in self.message_tasks:
            self.message_tasks[channel_id].cancel()
            del self.message_tasks[channel_id]
            await ctx.send("Timezone message removed.")
        else:
            await ctx.send("There is no timezone message in this channel.")
    
    async def update_message(self, channel_id, timezone_str):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(channel_id)
        if channel is None:
            return
        while True:
            now = datetime.now(timezone(timezone_str))
            message = f"In {timezone_str}, it is currently {now.strftime('%Y-%m-%d %H:%M')}"
            try:
                last_message = await channel.fetch_message(channel.last_message_id)
                await last_message.edit(content=message)
            except Exception:
                await channel.send(message)
            await asyncio.sleep(10) # 60 seconds


def setup(bot):
    bot.add_cog(StateTimeCog(bot))
