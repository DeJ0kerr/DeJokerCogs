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

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        channel: discord.DMChannel = self.bot.get_channel(id=520225411070689280)
        # await channel.send("before {} after {}".format(before.display_name, after.display_name))

    async def on_voice_state_update(self, before: discord.Member, after: discord.Member):
        channel: discord.DMChannel = self.bot.get_channel(id=520225411070689280)
        before_state: discord.VoiceState = before.voice
        after_state: discord.VoiceState = after.voice

        muted = not before_state.mute and after_state.mute
        unmuted = before_state.mute and not after_state.mute

        deafen = not before_state.deaf and after_state.deaf
        undeafen = before_state.deaf and not after_state.deaf

        message = "{member} has been ".format(member=after.mention)

        if muted:
            message += "muted"
        elif unmuted:
            message += "unmuted"
        elif deafen:
            message += "deafen"
        elif undeafen:
            message += "undeafen"

        message += "by TODO."
        channel.send(message)
