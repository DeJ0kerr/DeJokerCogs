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
        guild: discord.Guild = before.guild if before.guild is not None else after.guild

    @staticmethod
    async def get_last_log_user(guild):
        async for entry in guild.audit_logs(limit=1):
            return entry.user

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        channel: discord.DMChannel = self.bot.get_channel(id=520225411070689280)
        guild: discord.Guild = member.guild

        join_voice = before.channel is None and after.channel is not None
        left_voice = before.channel is not None and after.channel is None

        moved_voice = before.channel is not None and after.channel is not None and after.channel is not before.channel

        muted = not before.mute and after.mute
        unmuted = before.mute and not after.mute

        deafen = not before.deaf and after.deaf
        undeafen = before.deaf and not after.deaf

        action = ""
        user: discord.Member = await LogEverything.get_last_log_user(guild)
        message = "{member} has been {action} by {user}."

        if muted:
            action = "muted"
        elif unmuted:
            action = "unmuted"
        elif deafen:
            action = "deafen"
        elif undeafen:
            action = "undeafen"
        elif join_voice or left_voice or moved_voice:
            action = "connected" if join_voice else "disconnected" if left_voice else "moved"
            channel_name = after.channel.name if join_voice else before.channel.name
            message = "{member} has been {action} to the voice channel: {channel}.".format(member=member.mention, action=action, channel=channel_name)

        message = message.format(member=member.mention, action=action, user=user.mention)
        await channel.send(message)
