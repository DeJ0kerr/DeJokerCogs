import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core.bot import Red
from typing import Any

Cog: Any = getattr(commands, "Cog", object)


class LogEverything(Cog):

    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command("channelid")
    async def channel_id_cmd(self, ctx: commands.Context):
        channel: discord.DMChannel = ctx.channel
        await channel.send(channel.id)

    # def on_member_update(self, before, after):

