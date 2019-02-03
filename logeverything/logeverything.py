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

        nickname_changed = before.nick is not after.nick
        nickname_removed = nickname_changed and after.nick is None
        nickname_created = nickname_changed and before.nick is None

        roles_changed = before.roles is not after.roles

        user: discord.Member = await LogEverything.get_last_log_user(guild)
        message = "TODO: add logs to this"

        if nickname_changed and not nickname_removed and not nickname_created:
            message = "{member} nickname has been changed from **{old}** to **{new}** by {user}".format(member=after.mention, old=before.nick, new=after.nick, user=user.mention)
        elif nickname_created:
            message = "{member} nickname has been set to **{new}** by {user}".format(member=after.mention, new=after.nick, user=user.mention)
        elif nickname_removed:
            message = "{member} nickname has been removed by {user}".format(member=after.mention, old=before.nick, user=user.mention)
        elif roles_changed:
            message = "TODO: add role change message"

        await channel.send(message)

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

        self_muted = not before.self_mute and after.self_mute
        self_unmuted = before.self_mute and not after.self_mute

        self_deafen = not before.self_deaf and after.self_deaf
        self_undeafen = before.self_deaf and not after.self_deaf

        muted = not before.mute and after.mute
        unmuted = before.mute and not after.mute

        deafen = not before.deaf and after.deaf
        undeafen = before.deaf and not after.deaf

        if muted or unmuted or deafen or undeafen:
            message = "{member} has been **{action}** by {user}."
            action = "muted" if muted else "unmuted" if unmuted else "deafen" if deafen else "undeafen"
            user: discord.Member = await LogEverything.get_last_log_user(guild)
            message = message.format(member=member.mention, action=action, user=user.mention)

        elif self_muted or self_deafen or self_unmuted or self_undeafen:
            message = "{member} has **self {action}** themselves."
            action = "muted" if self_muted else "unmuted" if self_unmuted else "deafen" if self_deafen else "undeafen"
            user: discord.Member = await LogEverything.get_last_log_user(guild)
            message = message.format(member=member.mention, action=action, user=user.mention)

        elif join_voice or left_voice or moved_voice:
            message = "{member} has {action} the voice channel: {channel}."
            action = "connected" if join_voice else "disconnected" if left_voice else "moved to"
            channel_name = before.channel.name if left_voice else after.channel.name
            message = message.format(member=member.mention, action=action, channel=channel_name)

        await channel.send(message)
