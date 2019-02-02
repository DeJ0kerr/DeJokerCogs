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

    # async def on_member_update(self, before: discord.Member, after: discord.Member):
        # channel: discord.DMChannel = self.bot.get_channel(id=520225411070689280)
        # await channel.send("before {} after {}".format(before.display_name, after.display_name))

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        channel: discord.DMChannel = self.bot.get_channel(id=520225411070689280)

        join_voice = before.channel is None and after.channel is not None
        left_voice = before.channel is not None and after.channel is None

        muted = not before.mute and after.mute
        unmuted = before.mute and not after.mute

        deafen = not before.deaf and after.deaf
        undeafen = before.deaf and not after.deaf

        message = "{member} has been ".format(member=member.mention)

        if muted:
            message += "muted"
        elif unmuted:
            message += "unmuted"
        elif deafen:
            message += "deafen"
        elif undeafen:
            message += "undeafen"
        elif join_voice or left_voice:
            action = "joined" if join_voice else "left"
            message = "{member} has {action} the voice channel: {channel}.".format(member=member.mention, action=action, channel=after.channel.name)

        await channel.send(message)
