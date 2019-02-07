import discord
import asyncio
from logeverything.AuditManager import AuditManager
from redbot.core import Config
from redbot.core.bot import Red


class CommandManager:

    def __init__(self, bot):
        self.bot: Red
        self.config: Config

    # TODO: Remove asyncio.sleep() When there is a new way to get audit logs.
    @staticmethod
    async def get_audit_log(guild, action: discord.AuditLogAction, target) -> discord.AuditLogEntry:
        await asyncio.sleep(0.5)
        async for entry in guild.audit_logs(action=action):
            if entry.target.id == target.id:
                return entry

    # TODO: Remove asyncio.sleep() When there is a new way to get audit logs.
    @staticmethod
    async def get_last_audit_entry(guild) -> discord.AuditLogEntry:
        await asyncio.sleep(0.5)
        async for entry in guild.audit_logs(limit=1):
            return entry

    @staticmethod
    async def get_last_log_user(guild) -> discord.Member:
        entry = await AuditManager.get_last_audit_entry(guild)
        return entry.user

    @staticmethod
    async def get_last_audit_action(guild) -> discord.AuditLogAction:
        entry = await AuditManager.get_last_audit_entry(guild)
        return entry.action

    """Called when user gets banned from a Guild."""
    async def on_member_ban(self, guild: discord.Guild, member):
        if await self.config.guild(guild).log_member_ban():
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.ban, member)
            print(entry.created_at)
            print(entry.reason)
            msg = "{member} has been banned from the guild.\nReason for ban: {reason}".format(member=member.mention, reason=entry.reason)
            await self.print_log(msg, guild)

    """Called when a User gets unbanned from a Guild."""
    async def on_member_unban(self, guild: discord.Guild, member: discord.User):
        if await self.config.guild(guild).log_member_unban():
            msg = "{member} has been unbanned from the guild.".format(member=member.mention)
            await self.print_log(msg, guild)

    """Called when a Member joins a Guild."""
    async def on_member_join(self, member: discord.Member):
        if await self.config.guild(member.guild).log_member_join():
            msg = "{member} has joined the guild.".format(member=member.mention)
            await self.print_log(msg, member.guild)

    """Called when a Member leaves a Guild."""
    async def on_member_remove(self, member: discord.Member):
        if await self.config.guild(member.guild).log_member_leave():
            action = await AuditManager.get_last_audit_action(member.guild)
            if action is discord.AuditLogAction.kick:
                await self.on_member_kick(member)
                return
            if action is discord.AuditLogAction.ban:
                return
            msg = "{member} has left the guild.".format(member=member.mention)
            await self.print_log(msg, member.guild)

    """Called when a Member gets kicked from a Guild."""
    async def on_member_kick(self, member: discord.Member):
        if await self.config.guild(member.guild).log_member_leave():
            entry = await AuditManager.get_audit_log(member.guild, discord.AuditLogAction.kick, member)
            user = entry.user
            msg = "{member} has been kicked by {user}.\nReason for kick: {reason}".format(member=member.mention, user=user.mention, reason=entry.reason)
            await self.print_log(msg, member.guild)

    """
    Called when a message is deleted.
    """
    # TODO: Add deleted by, time of deleted message
    async def on_message_delete(self, message: discord.Message):
        if await self.config.guild(message.guild).log_delete_message():
            msg = "A message of {member} has been deleted in channel {channel}.\nOriginal message:\n{message}".format(message=message.content, member=message.author.mention, channel=message.channel.mention)
            await self.print_log(msg, message.guild)

    """
    Called when a Member updates their profile.
    This is called when one or more of the following things change:
        status V
        game playing V
        avatar V
        nickname V
        roles V
    """
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        guild: discord.Guild = before.guild if before.guild is not None else after.guild

        status_changed = False
        activity_changed = False
        activity_started = False
        activity_finished = False
        avatar_changed = False
        nickname_created = False
        nickname_changed = False
        nickname_removed = False
        roles_changed = False

        before_activity: discord.Activity
        after_activity: discord.Activity
        after_status: discord.Status

        if await self.config.guild(guild).log_status_change():
            before_status: discord.Status = before.status
            after_status: discord.Status = after.status
            status_changed = before_status.name is not after_status.name

        if await self.config.guild(guild).log_activity_change():
            before_activity: discord.Activity = before.activity
            after_activity: discord.Activity = after.activity

            activity_started = before_activity is None and after_activity is not None
            activity_finished = before_activity is not None and after_activity is None

            activity_changed = False
            if before_activity is not None and after_activity is not None:
                activity_changed = before_activity.name != after_activity.name

        if await self.config.guild(guild).log_avatar_change():
            avatar_changed = before.avatar_url != after.avatar_url

        if await self.config.guild(guild).log_nickname_change():
            nickname_changed = before.nick != after.nick
            nickname_removed = nickname_changed and after.nick is None
            nickname_created = nickname_changed and before.nick is None

        if await self.config.guild(guild).log_role_change():
            roles_changed = before.roles != after.roles

        message = ""

        if nickname_changed and not nickname_removed and not nickname_created:
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, after)
            user: discord.Member = entry.user

            message = "{member} nickname has been changed from **{old}** to **{new}** by {user}.".format(member=after.mention, old=before.nick, new=after.nick, user=user.mention)
        elif nickname_created:
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, after)
            user: discord.Member = entry.user

            message = "{member} nickname has been set to **{new}** by {user}.".format(member=after.mention, new=after.nick, user=user.mention)
        elif nickname_removed:
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, after)
            user: discord.Member = entry.user

            message = "{member} nickname has been removed by {user}.".format(member=after.mention, old=before.nick, user=user.mention)
        elif status_changed:
            message = "{member} went {status}.".format(member=after.mention, status=after_status.name)
        elif activity_started:
            after_activity_type: discord.ActivityType = after_activity.type
            message = "{member} started {action} {activity}.".format(member=after.mention, action=after_activity_type.name, activity=after_activity.name)
        elif activity_finished:
            before_activity_type: discord.ActivityType = before_activity.type
            message = "{member} stopped {action} {activity}.".format(member=after.mention, action=before_activity_type.name, activity=before_activity.name)
        elif activity_changed:
            before_activity_type: discord.ActivityType = before_activity.type
            after_activity_type: discord.ActivityType = after_activity.type
            message = "{member} stopped  {action} {activity} and started {action2} {activity2}.".format(member=after.mention, action=before_activity_type.name, activity=before_activity.name, action2=after_activity_type.name, activity2=after_activity.name)
        elif avatar_changed:
            message = "{member} has changed his avatar icon.".format(member=after.mention)
        elif roles_changed:
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, after)
            user: discord.Member = entry.user

            message = "{member} roles has been changed by {user}:\n"
            for br in before.roles:
                if br not in after.roles:
                    br: discord.Role
                    message += "Demoted from {role}\n".format(role=br.name)
            for ar in after.roles:
                if ar not in before.roles:
                    ar: discord.Role
                    message += "Promoted to {role}\n".format(role=ar.name)
            message = message.format(member=after.mention, user=user.mention)
        await self.print_log(message, guild)

    """
    Called when a Member changes their VoiceState.
    The following, but not limited to, examples illustrate when this event is called:
        A member joins a voice room. V
        A member leaves a voice room. V
        A member is muted or deafened by their own accord. V
        A member is muted or deafened by a guild administrator. V
    """
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild: discord.Guild = member.guild

        message = ""

        join_voice = False
        left_voice = False
        moved_voice = False
        self_muted = False
        self_unmuted = False
        self_deafen = False
        self_undeafen = False
        self_deafen_and_mute = False
        self_undeafen_and_unmuted = False
        muted = False
        unmuted = False
        deafen = False
        undeafen = False

        if await self.config.guild(guild).log_join_leave_voice():
            join_voice = before.channel is None and after.channel is not None
            left_voice = before.channel is not None and after.channel is None
            moved_voice = before.channel is not None and after.channel is not None and after.channel is not before.channel

        if await self.config.guild(guild).log_self_mute():
            self_muted = not before.self_mute and after.self_mute
            self_unmuted = before.self_mute and not after.self_mute

        if await self.config.guild(guild).log_self_deafen():
            self_deafen = not before.self_deaf and after.self_deaf
            self_undeafen = before.self_deaf and not after.self_deaf

        if await self.config.guild(guild).log_self_mute() and await self.config.guild(guild).log_self_deafen():
            self_deafen_and_mute = self_muted and self_deafen
            self_undeafen_and_unmuted = self_unmuted and self_undeafen

        if await self.config.guild(guild).log_mute():
            muted = not before.mute and after.mute
            unmuted = before.mute and not after.mute

        if await self.config.guild(guild).log_deafen():
            deafen = not before.deaf and after.deaf
            undeafen = before.deaf and not after.deaf

        if muted or unmuted or deafen or undeafen:
            message = "{member} has been **{action}** by {user}."
            action = "muted" if muted else "unmuted" if unmuted else "deafen" if deafen else "undeafen"
            user: discord.Member = await AuditManager.get_last_log_user(guild)
            message = message.format(member=member.mention, action=action, user=user.mention)

        elif self_muted or self_deafen or self_unmuted or self_undeafen or self_deafen_and_mute or self_undeafen_and_unmuted:
            message = "{member} has **self {action}** themselves."
            action = "muted and deafen" if self_deafen_and_mute else "unmuted and undeafen" if self_undeafen_and_unmuted else "muted" if self_muted else "unmuted" if self_unmuted else "deafen" if self_deafen else "undeafen"
            user: discord.Member = await AuditManager.get_last_log_user(guild)
            message = message.format(member=member.mention, action=action, user=user.mention)

        elif join_voice or left_voice or moved_voice:
            message = "{member} has {action} the voice channel: {channel}."
            action = "connected" if join_voice else "disconnected" if left_voice else "moved to"
            channel_name = before.channel.name if left_voice else after.channel.name
            message = message.format(member=member.mention, action=action, channel=channel_name)

        await self.print_log(message, guild)
