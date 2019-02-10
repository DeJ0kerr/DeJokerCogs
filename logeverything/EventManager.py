import discord
from logeverything.AuditManager import AuditManager
from redbot.core import Config
from redbot.core.bot import Red


class EventManager:

    def __init__(self, bot: Red, config: Config, main):
        self.bot: Red = bot
        self.config: Config = config
        self.main = main

    """
    Called whenever a guild channel is deleted.
    """
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        if not await self.config.guild(channel.guild).log_channel_creation():
            return

        entry: discord.AuditLogEntry = await AuditManager.get_audit_log(channel.guild, discord.AuditLogAction.guild_update)
        user: discord.Member = entry.user
        if isinstance(channel, discord.TextChannel):
            msg = "{user} has deleted a text channel \"{name}\".".format(name=channel.name, user=user.mention)
            await self.main.print_log(msg, channel.guild)
        elif isinstance(channel, discord.VoiceChannel):
            msg = "{user} has deleted a voice channel \"{name}\".".format(name=channel.name, user=user.mention)
            await self.main.print_log(msg, channel.guild)

    """Called whenever a guild channel is created."""
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        if not await self.config.guild(channel.guild).log_channel_creation():
            return

        entry: discord.AuditLogEntry = await AuditManager.get_audit_log(channel.guild, discord.AuditLogAction.guild_update)
        user: discord.Member = entry.user
        if isinstance(channel, discord.TextChannel):
            msg = "{user} has created a text channel \"{name}\".".format(name=channel.name, user=user.mention)
            await self.main.print_log(msg, channel.guild)
        elif isinstance(channel, discord.VoiceChannel):
            msg = "{user} has created a voice channel \"{name}\".".format(name=channel.name, user=user.mention)
            await self.main.print_log(msg, channel.guild)

    """Called whenever a guild channel is updated."""
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        guild: discord.Guild = after.guild
        if not await self.config.guild(guild).log_channel_edit():
            return

        entry: discord.AuditLogEntry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.guild_update)
        user: discord.Member = entry.user
        if isinstance(after, discord.TextChannel) and isinstance(before, discord.TextChannel):
            msg = ""

            if after.name != before.name:
                msg += "\n**Name**: {before} -> {after}".format(before=before.name, after=after.name)
            if after.topic != before.topic:
                after_topic = after.topic if after.topic != "" else "None"
                before_topic = before.topic if before.topic != "" else "None"
                msg += "\n**Topic**:\n{before}\n->\n{after}".format(before=before_topic, after=after_topic)

            if after.nsfw != before.nsfw:
                msg += "\n**NSFW**: {before} -> {after}".format(before=before.nsfw, after=after.nsfw)

            if after.slowmode_delay != before.slowmode_delay:
                before_slow = before.slowmode_delay if before.slowmode_delay != 0 else "Disabled"
                after_slow = after.slowmode_delay if after.slowmode_delay != 0 else "Disabled"
                msg += "\n**Slow Mode**: {before} -> {after}".format(before=before_slow, after=after_slow)

            if msg == "":
                return
            msg = "{user} has edited the text channel \"{name}\":".format(name=before.name, user=user.mention) + msg
            await self.main.print_log(msg, after.guild)
        elif isinstance(after, discord.VoiceChannel) and isinstance(before, discord.VoiceChannel):
            msg = ""
            if after.name != before.name:
                msg += "\n**Name**: {before} -> {after}".format(before=before.name, after=after.name)

            if after.bitrate != before.bitrate:
                msg += "\n**Bitrate**: {before}kbps -> {after}kbps".format(before=int(before.bitrate/1000), after=int(after.bitrate/1000))

            if after.user_limit != before.user_limit:
                after_limit = "Unlimited" if after.user_limit == 0 else after.user_limit
                before_limit = "Unlimited" if before.user_limit == 0 else before.user_limit
                msg += "\n**User Limit**: {before} slots -> {after} slots.".format(before=before_limit, after=after_limit)

            if msg == "":
                return
            msg = "{user} has edited the voice channel \"{name}\":".format(name=before.name, user=user.mention) + msg
            await self.main.print_log(msg, after.guild)

    async def on_guild_emojis_update(self, guild: discord.Guild, before: list, after: list):
        if not self.config.guild(guild).log_emojis():
            return
        msg = ""
        for old in before:
            old: discord.Emoji
            if old not in after:
                msg += "Emoji {emoji} has been deleted.\n".format(emoji=old.name)
        for new in after:
            new: discord.Emoji
            if new not in before:
                msg += "Emoji {emoji} {display} has been added.".format(emoji=new.name, display=new)
        await self.main.print_log(msg, guild=guild)

    """Called when a Guild updates, for example:
        Changing the guild vanity URL
        Changing the guild default notification V  
        Changing the guild invite splash V
        Changing the guild new member message channel V
        Changing the guild AFK channel V
        Changing the guild AFK timeout V
        Changing the guild voice server region V
        Changing the guild icon V
        Changing the guild moderation settings V 
        Changing the guild's owner V
        Changing things related to the guild widget V
        Changed name V
    """
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        if not await self.config.guild(after).log_guild_settings():
            return

        entry: discord.AuditLogEntry = await AuditManager.get_audit_log(after, discord.AuditLogAction.guild_update)

        before_diff = entry.before
        after_diff = entry.after

        user: discord.Member = entry.user

        if before.name != after.name:
            msg = "{user} has changed guild's name from {old} to {new}.".format(
                old=before.name, new=after.name, user=user.mention)
            await self.main.print_log(msg, after)
        elif before.afk_channel is not after.afk_channel:
            if after.afk_channel is None:
                msg = "{user} has remove the AFK channel.".format(
                    user=user.mention)
                await self.main.print_log(msg, after)
            else:
                msg = "{user} has set voice channel {channel} to be the AFK channel.".format(
                    channel=after.afk_channel.name, user=user.mention)
                await self.main.print_log(msg, after)
        elif before.system_channel is not after.system_channel:
            if after.system_channel is None:
                msg = "{user} has remove the new member message channel.".format(
                    user=user.mention)
                await self.main.print_log(msg, after)
            else:
                msg = "{user} has set {channel} to be the new member message channel.".format(
                    channel=after.system_channel.mention, user=user.mention)
                await self.main.print_log(msg, after)
        elif before.afk_timeout != after.afk_timeout:
            msg = "{user} has set the AFK timeout to be {time} minutes.".format(
                time=int(after.afk_timeout / 60), user=user.mention)
            await self.main.print_log(msg, after)
        elif before.region is not after.region:
            msg = "{user} has changed the voice region from {old} to {new}.".format(
                old=before.region, new=after.region, user=user.mention)
            await self.main.print_log(msg, after)
        elif before.icon_url != after.icon_url:
            msg = "{user} has changed the guild's icon from {old} to {new}.".format(
                old=before.icon_url, new=after.icon_url, user=user.mention)
            await self.main.print_log(msg, after)
        elif before.splash_url != after.splash_url:
            msg = "{user} has changed the guild's invite splash from {old} to {new}.".format(
                old=before.splash_url, new=after.splash_url, user=user.mention)
            await self.main.print_log(msg, after)
        elif before.mfa_level != after.mfa_level or before.verification_level != after.verification_level or before.explicit_content_filter != after.explicit_content_filter:
            after_mfa_msg = "2FA disabled" if after.mfa_level == 0 else "2FA enabled"
            before_mfa_msg = "2FA disabled" if before.mfa_level == 0 else "2FA enabled"

            before_verf = str.capitalize(before.verification_level.name)
            after_verf = str.capitalize(after.verification_level.name)
            before_explicit = str.capitalize(
                before.explicit_content_filter.name)
            after_explicit = str.capitalize(after.explicit_content_filter.name)

            before_set = "{verf} with {mfa} and explicit content filter on {explicit}".format(
                verf=before_verf, mfa=before_mfa_msg, explicit=before_explicit)
            after_set = "{verf} with {mfa} and explicit content filter on {explicit}".format(
                verf=after_verf, mfa=after_mfa_msg, explicit=after_explicit)
            msg = "{user} has changed the guild's moderation settings:\nFrom: {old}\nTo: {new}.".format(
                old=before_set, new=after_set, user=user.mention)
            await self.main.print_log(msg, after)
        elif before.default_notifications != after.default_notifications:
            before_set = "Only @mentions" if before.default_notifications == 1 else "All messages"
            after_set = "Only @mentions" if after.default_notifications == 1 else "All messages"
            msg = "{user} has changed the guild's default notification from {old} to {new}.".format(
                old=before_set, new=after_set, user=user.mention)
            await self.main.print_log(msg, after)
        elif before.owner_id != after.owner_id:
            msg = "{user} has transferred the guild's ownership to {new}.".format(
                new=after.owner.mention, user=before.owner.mention)
            await self.main.print_log(msg, after)
        else:
            """
                Using try-catch because of AuditLogDiff functionality 
            """
            try:
                if before_diff.widget_enabled is not after_diff.widget_enabled:
                    enable = "enabled" if after_diff.widget_enabled else "disabled"
                    msg = "{user} has {enable} the server widget.".format(
                        enable=enable, user=user.mention)
                    await self.main.print_log(msg, after)
            except AttributeError:
                pass
            try:
                if after_diff.widget_channel is None:
                    msg = "{user} has remove the server widget.".format(
                        user=user.mention)
                    await self.main.print_log(msg, after)
                elif before_diff.widget_channel is not after_diff.widget_channel:
                    voice_channel = "the voice channel {channel}".format(channel=after_diff.widget_channel.name) if isinstance(
                        after_diff.widget_channel, discord.VoiceChannel) else "{channel}".format(channel=after_diff.widget_channel.mention)
                    msg = "{user} has set the server widget channel to {channel}.".format(
                        channel=voice_channel, user=user.mention)
                    await self.main.print_log(msg, after)
            except AttributeError:
                pass

    """Called when user gets banned from a Guild."""
    async def on_member_ban(self, guild: discord.Guild, member):
        if await self.config.guild(guild).log_member_ban():
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.ban, member)
            print(entry.created_at)
            print(entry.reason)
            msg = "{member} has been banned from the guild.\nReason for ban: {reason}".format(
                member=member.mention, reason=entry.reason)
            await self.main.print_log(msg, guild)

    """Called when a User gets unbanned from a Guild."""
    async def on_member_unban(self, guild: discord.Guild, member: discord.User):
        if await self.config.guild(guild).log_member_unban():
            msg = "{member} has been unbanned from the guild.".format(
                member=member.mention)
            await self.main.print_log(msg, guild)

    """Called when a Member joins a Guild."""
    async def on_member_join(self, member: discord.Member):
        if await self.config.guild(member.guild).log_member_join():
            msg = "{member} has joined the guild.".format(
                member=member.mention)
            await self.main.print_log(msg, member.guild)

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
            await self.main.print_log(msg, member.guild)

    """Called when a Member gets kicked from a Guild."""
    async def on_member_kick(self, member: discord.Member):
        if await self.config.guild(member.guild).log_member_leave():
            entry = await AuditManager.get_audit_log(member.guild, discord.AuditLogAction.kick, member)
            user = entry.user
            msg = "{member} has been kicked by {user}.\nReason for kick: {reason}".format(
                member=member.mention, user=user.mention, reason=entry.reason)
            await self.main.print_log(msg, member.guild)

    """Called when a Message receives an update event."""
    # TODO: add link to message
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.guild is None:
            return
        if await self.config.guild(before.guild).log_edit_message():
            msg = ""
            if before.content != after.content:
                msg = "A message of {member} has been edited in channel {channel}.\n**__Edited message__**:\n{message}\n\n**__Original message__**:\n{old_message}".format(
                    message=after.content, old_message=before.content, member=after.author.mention, channel=after.channel.mention)
            elif before.pinned != after.pinned:
                un = "un" if not after.pinned else ""
                msg = "A message of {member} has been {un}pinned in channel {channel}.".format(un=un, member=after.author.mention, channel=after.channel.mention)
            if msg == "":
                return
            await self.main.print_log(msg, after.guild)

    """Called when a message is deleted."""
    # TODO: Add deleted by, time of deleted message
    async def on_message_delete(self, message: discord.Message):
        if message.guild is None:
            return
        if await self.config.guild(message.guild).log_delete_message():
            msg = "A message of {member} has been deleted in channel {channel}.\nOriginal message:\n{message}".format(
                message=message.content, member=message.author.mention, channel=message.channel.mention)
            await self.main.print_log(msg, message.guild)

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

            message = "{member} nickname has been changed from **{old}** to **{new}** by {user}.".format(
                member=after.mention, old=before.nick, new=after.nick, user=user.mention)
        elif nickname_created:
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, after)
            user: discord.Member = entry.user

            message = "{member} nickname has been set to **{new}** by {user}.".format(
                member=after.mention, new=after.nick, user=user.mention)
        elif nickname_removed:
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, after)
            user: discord.Member = entry.user

            message = "{member} nickname has been removed by {user}.".format(
                member=after.mention, old=before.nick, user=user.mention)
        elif status_changed:
            message = "{member} went {status}.".format(
                member=after.mention, status=after_status.name)
        elif activity_started:
            after_activity_type: discord.ActivityType = after_activity.type
            message = "{member} started {action} {activity}.".format(
                member=after.mention, action=after_activity_type.name, activity=after_activity.name)
        elif activity_finished:
            before_activity_type: discord.ActivityType = before_activity.type
            message = "{member} stopped {action} {activity}.".format(
                member=after.mention, action=before_activity_type.name, activity=before_activity.name)
        elif activity_changed:
            before_activity_type: discord.ActivityType = before_activity.type
            after_activity_type: discord.ActivityType = after_activity.type
            message = "{member} stopped  {action} {activity} and started {action2} {activity2}.".format(
                member=after.mention, action=before_activity_type.name, activity=before_activity.name, action2=after_activity_type.name, activity2=after_activity.name)
        elif avatar_changed:
            message = "{member} has changed his avatar icon.".format(
                member=after.mention)
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
        await self.main.print_log(message, guild)

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
            message = message.format(
                member=member.mention, action=action, user=user.mention)

        elif self_muted or self_deafen or self_unmuted or self_undeafen or self_deafen_and_mute or self_undeafen_and_unmuted:
            message = "{member} has **self {action}** themselves."
            action = "muted and deafen" if self_deafen_and_mute else "unmuted and undeafen" if self_undeafen_and_unmuted else "muted" if self_muted else "unmuted" if self_unmuted else "deafen" if self_deafen else "undeafen"
            user: discord.Member = await AuditManager.get_last_log_user(guild)
            message = message.format(
                member=member.mention, action=action, user=user.mention)

        elif join_voice or left_voice or moved_voice:
            message = "{member} has {action} the voice channel: {channel}."
            action = "connected" if join_voice else "disconnected" if left_voice else "moved to"
            channel_name = before.channel.name if left_voice else after.channel.name
            message = message.format(
                member=member.mention, action=action, channel=channel_name)

        await self.main.print_log(message, guild)
