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
        await LogEverything.print_last_log(guild)

    @staticmethod
    async def print_last_log(guild):
        async for entry in guild.audit_logs(limit=1):
            entry: discord.AuditLogEntry
            action: discord.AuditLogAction = entry.action
            user: discord.Member = entry.user
            target: discord.Member = entry.target
            reason: str = entry.reason

            if entry is discord.AuditLogAction.member_update:
                print("asgasdasd")

            print('{user} did {action} to {target}'.format(user=user.mention, action=action, target=target.mention))

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        channel: discord.DMChannel = self.bot.get_channel(id=520225411070689280)
        guild: discord.Guild = member.guild

        await LogEverything.print_last_log(guild)

        """join_voice = before.channel is None and after.channel is not None
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
            channel_name = after.channel.name if join_voice else before.channel.name
            message = "{member} has {action} the voice channel: {channel}.".format(member=member.mention, action=action, channel=channel_name)

        await channel.send(message)"""
