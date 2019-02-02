from typing import Any

import discord
from redbot.core import commands
from redbot.core.bot import Red

Cog: Any = getattr(commands, "Cog", object)


class LogEverything(Cog):

    def __init__(self, bot: Red):
        self.bot = bot

    @commands.command(name="channelid")
    async def channel_id_cmd(self, ctx: commands.Context):
        channel: discord.DMChannel = ctx.channel
        await channel.send(channel.id)

    def on_member_update(self, before: discord.Member, after: discord.Member):
        channel: discord.DMChannel = self.bot.get_channel(id=520225411070689280)
        await channel.send("before {} after {}".format(before.display_name, after.display_name))
