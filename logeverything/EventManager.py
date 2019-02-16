import discord
from .AuditManager import AuditManager
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

        embed_message = discord.Embed(title="Channel Deletion Log")
        msg = ""

        entry: discord.AuditLogEntry = await AuditManager.get_audit_log(channel.guild, discord.AuditLogAction.guild_update)
        user: discord.Member = entry.user
        if isinstance(channel, discord.TextChannel):
            msg = "{user} has deleted a text channel \"{name}\".".format(name=channel.name, user=user.mention)

            embed_message.add_field(name="Deleted Text Channel", value=channel.name)
            embed_message.add_field(name="Moderator", value=user.mention)

        elif isinstance(channel, discord.VoiceChannel):
            msg = "{user} has deleted a voice channel \"{name}\".".format(name=channel.name, user=user.mention)

            embed_message.add_field(name="Deleted Voice Channel", value=channel.name)
            embed_message.add_field(name="Moderator", value=user.mention)

        elif isinstance(channel, discord.CategoryChannel):
            msg = "{user} has deleted a category channel \"{name}\".".format(name=channel.name, user=user.mention)

            embed_message.add_field(name="Deleted Category Channel", value=channel.name)
            embed_message.add_field(name="Moderator", value=user.mention)

        if await self.config.guild(channel.guild).use_embed():
            await self.main.print_log_embed(embed_message, channel.guild)
        else:
            await self.main.print_log(msg, channel.guild)

    """Called whenever a guild channel is created."""

    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        if not await self.config.guild(channel.guild).log_channel_creation():
            return

        embed_message = discord.Embed(title="Channel Creation Log")
        msg = ""

        entry: discord.AuditLogEntry = await AuditManager.get_audit_log(channel.guild, discord.AuditLogAction.guild_update)
        user: discord.Member = entry.user
        if isinstance(channel, discord.TextChannel):
            msg = "{user} has created a text channel \"{name}\".".format(name=channel.name, user=user.mention)

            embed_message.add_field(name="Created Text Channel", value=channel.mention)
            embed_message.add_field(name="Moderator", value=user.mention)

        elif isinstance(channel, discord.VoiceChannel):
            msg = "{user} has created a voice channel \"{name}\".".format(name=channel.name, user=user.mention)

            embed_message.add_field(name="Created Voice Channel", value=channel.name)
            embed_message.add_field(name="Moderator", value=user.mention)

        elif isinstance(channel, discord.CategoryChannel):
            msg = "{user} has created a category channel \"{name}\".".format(name=channel.name, user=user.mention)

            embed_message.add_field(name="Created Category Channel", value=channel.name)
            embed_message.add_field(name="Moderator", value=user.mention)

        if await self.config.guild(channel.guild).use_embed():
            await self.main.print_log_embed(embed_message, channel.guild)
        else:
            await self.main.print_log(msg, channel.guild)

    """Called whenever a guild channel is updated."""

    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        guild: discord.Guild = after.guild
        if not await self.config.guild(guild).log_channel_edit():
            return

        msg = ""
        embed_message = discord.Embed(title="Channel Update Log")

        entry: discord.AuditLogEntry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.guild_update)
        user: discord.Member = entry.user
        if isinstance(after, discord.TextChannel) and isinstance(before, discord.TextChannel):
            embed_message.add_field(name="Text Channel", value=before.mention)
            embed_message.add_field(name="Moderator", value=user.mention)

            if after.name != before.name:
                msg += "\n**Name**: {before} 🠆 {after}".format(before=before.name, after=after.name)

                embed_message.add_field(name="Channel Name", value="{before} 🠆 {after}".format(before=before.name, after=after.name))
            if after.topic != before.topic:
                after_topic = after.topic if after.topic != "" else "None"
                before_topic = before.topic if before.topic != "" else "None"
                msg += "\n**Topic**:\n{before}\n->\n{after}".format(before=before_topic, after=after_topic)

                embed_message.add_field(name="Previous Topic", value=before_topic)
                embed_message.add_field(name="Current Topic", value=after_topic)

            if after.nsfw != before.nsfw:
                on = "on" if after.nsfw else "off"
                msg += "\n**NSFW**: NSFW has been turned {on}".format(on=on)

                embed_message.add_field(name="NSFW", value="NSFW has been turned {on}".format(on=on), inline=False)
            if after.slowmode_delay != before.slowmode_delay:
                before_slow = before.slowmode_delay if before.slowmode_delay != 0 else "Disabled"
                after_slow = after.slowmode_delay if after.slowmode_delay != 0 else "Disabled"
                msg += "\n**Slow Mode**: {before} 🠆 {after}".format(before=before_slow, after=after_slow)

                embed_message.add_field(name="Slow Mode", value="{before} 🠆 {after}".format(before=before_slow, after=after_slow))
            if msg == "":
                return
            msg = "{user} has edited the text channel \"{name}\":".format(name=before.name, user=user.mention) + msg
        elif isinstance(after, discord.VoiceChannel) and isinstance(before, discord.VoiceChannel):
            embed_message.add_field(name="Voice Channel", value=before.name)
            embed_message.add_field(name="Moderator", value=user.mention)

            if after.name != before.name:
                msg += "\n**Name**: {before} 🠆 {after}".format(before=before.name, after=after.name)

                embed_message.add_field(name="Channel Name", value="{before} 🠆 {after}".format(before=before.name, after=after.name))
            if after.bitrate != before.bitrate:
                msg += "\n**Bitrate**: {before}kbps 🠆 {after}kbps".format(before=int(before.bitrate / 1000), after=int(after.bitrate / 1000))

                embed_message.add_field(name="Bitrate", value="{before}kbps 🠆 {after}kbps".format(before=int(before.bitrate / 1000), after=int(after.bitrate / 1000)))
            if after.user_limit != before.user_limit:
                after_limit = "Unlimited" if after.user_limit == 0 else after.user_limit
                before_limit = "Unlimited" if before.user_limit == 0 else before.user_limit
                msg += "\n**User Limit**: {before} slots 🠆 {after} slots.".format(before=before_limit, after=after_limit)

                embed_message.add_field(name="User Limit", value="{before} slots 🠆 {after} slots".format(before=before_limit, after=after_limit))
            if msg == "":
                return
            msg = "{user} has edited the voice channel \"{name}\":".format(name=before.name, user=user.mention) + msg
            embed_message.add_field(name="Moderator", value=user.mention)

        if await self.config.guild(after.guild).use_embed():
            await self.main.print_log_embed(embed_message, after.guild)
        else:
            await self.main.print_log(msg, after.guild)

    # TODO: User created/deleted/updated
    async def on_guild_emojis_update(self, guild: discord.Guild, before: list, after: list):
        if not self.config.guild(guild).log_emojis():
            return

        msg = ""
        embed_message = discord.Embed(title="Emoji Update Log")
        for old in before:
            old: discord.Emoji
            deleted_emojis = ""
            if old not in after:
                msg += "Emoji {emoji} has been deleted.\n".format(emoji=old.name)
                deleted_emojis += "{emoji}\n".format(emoji=old.name)
            if deleted_emojis != "":
                embed_message.add_field(name="Deleted Emojis", value=deleted_emojis)
        for new in after:
            new: discord.Emoji
            added_emojis = ""
            updated_emojis = ""
            if new not in before:
                msg += "Emoji {emoji} {display} has been added.".format(emoji=new.name, display=new)
                added_emojis += "{display} = :{emoji}:\n".format(emoji=new.name, display=new)
            else:
                for old in before:
                    if old.id == new.id:
                        if new.name != old.name:
                            msg += "Emoji name updated {old} 🠆 {new} {display}\n".format(new=new.name, old=old.name, display=new)
                            updated_emojis += ":{emoji}: 🠆 :{new}: {display}\n".format(emoji=old.name, new=new.name, display=new)
            if added_emojis != "":
                embed_message.add_field(name="New Emojis", value=added_emojis)
            if updated_emojis != "":
                embed_message.add_field(name="Updated Emojis", value=updated_emojis)

        if await self.config.guild(guild).use_embed():
            await self.main.print_log_embed(embed_message, guild)
        else:
            await self.main.print_log(msg, guild)

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
        msg = ""
        embed_message = discord.Embed(title="Guild Update Log")
        embed_message.add_field(name="Moderator", value=user.mention)

        if before.name != after.name:
            msg += "Guild's Name: {old} 🠆 {new}.\n".format(old=before.name, new=after.name)
            embed_message.add_field(name="Guild's Name", value="{old} 🠆 {new}".format(old=before.name, new=after.name))
        if before.afk_channel is not after.afk_channel:
            if after.afk_channel is None:
                msg += "AFK channel has been removed.\n"
                embed_message.add_field(name="AFK channel", value="AFK channel has been removed")
            else:
                msg += "AFK channel: {channel}.\n".format(channel=after.afk_channel.name)
                embed_message.add_field(name="AFK channel", value=after.afk_channel.name)
        if before.afk_timeout != after.afk_timeout:
            msg += "AFK Timeout: {time} minutes.\n".format(time=int(after.afk_timeout / 60))
            embed_message.add_field(name="AFK Timeout", value="{time} minutes".format(time=int(after.afk_timeout / 60)))
        if before.system_channel is not after.system_channel:
            if after.system_channel is None:
                msg += "New Member Message channel has been removed.\n"
                embed_message.add_field(name="New Member Message channel", value="New Member Message channel has been removed")
            else:
                msg += "New Member Message channel: {channel}.\n".format(channel=after.system_channel.mention)
                embed_message.add_field(name="New Member Message channel", value=after.system_channel.mention)
        if before.region is not after.region:
            msg += "Voice Region: {old} 🠆 {new}.\n".format(old=before.region, new=after.region)
            embed_message.add_field(name="Voice Region", value="{old} 🠆 {new}".format(old=before.region, new=after.region))
        if before.icon_url != after.icon_url:
            msg += "Guild's Icon: {old} 🠆 {new}.\n".format(old=before.icon_url, new=after.icon_url)
            embed_message.add_field(name="Guild's Icon", value="{old} 🠆 {new}".format(old=before.icon_url, new=after.icon_url))
        if before.splash_url != after.splash_url:
            msg += "Guild's Invite Splash: {old} 🠆 {new}.\n".format(old=before.splash_url, new=after.splash_url)
            embed_message.add_field(name="Guild's Invite Splash URL", value="{old} 🠆 {new}".format(old=before.splash_url, new=after.splash_url))
        if before.mfa_level != after.mfa_level or before.verification_level != after.verification_level or before.explicit_content_filter != after.explicit_content_filter:
            after_mfa_msg = "2FA disabled" if after.mfa_level == 0 else "2FA enabled"
            before_mfa_msg = "2FA disabled" if before.mfa_level == 0 else "2FA enabled"

            before_verf = str.capitalize(before.verification_level.name)
            after_verf = str.capitalize(after.verification_level.name)
            before_explicit = str.capitalize(before.explicit_content_filter.name)
            after_explicit = str.capitalize(after.explicit_content_filter.name)

            before_set = "{verf} verification with {mfa} and explicit content filter on {explicit}".format(verf=before_verf, mfa=before_mfa_msg, explicit=before_explicit)
            after_set = "{verf} verification with {mfa} and explicit content filter on {explicit}".format(verf=after_verf, mfa=after_mfa_msg, explicit=after_explicit)
            msg += "Guild's Moderation Settings: {old}\n🠇\n{new}.\n".format(old=before_set, new=after_set)
            embed_message.add_field(name="Guild's Moderation Settings", value="{old}\n🠇\n{new}".format(old=before_set, new=after_set))
        if before.default_notifications != after.default_notifications:
            before_set = "Only @mentions" if before.default_notifications == 1 else "All messages"
            after_set = "Only @mentions" if after.default_notifications == 1 else "All messages"
            msg += "Guild's Default Notification: {old} 🠆 {new}.\n".format(old=before_set, new=after_set)
            embed_message.add_field(name="Guild's Default Notification", value="{old} 🠆 {new}".format(old=before_set, new=after_set))
        if before.owner_id != after.owner_id:
            msg += "Guild's Ownership: {user} 🠆 {new}.\n".format(new=after.owner.mention, user=before.owner.mention)
            embed_message.add_field(name="Guild's Ownership", value="{user} 🠆 {new}".format(new=after.owner.mention, user=before.owner.mention))
        """
            Using try-catch because of AuditLogDiff functionality 
        """
        try:
            if before_diff.widget_enabled is not after_diff.widget_enabled:
                enable = "enabled" if after_diff.widget_enabled else "disabled"
                old = "enabled" if before_diff.widget_enabled else "disabled"
                msg += "Server Widget: {old} 🠆 {new}.\n".format(new=enable, old=old)
                embed_message.add_field(name="Server Widget", value="{old} 🠆 {new}".format(new=enable, old=old))
        except AttributeError:
            pass
        try:
            if after_diff.widget_channel is None:
                msg += "Server Widget has been removed.\n"
                embed_message.add_field(name="Server Widget Channel", value="Server Widget has been removed")
            elif before_diff.widget_channel is not after_diff.widget_channel:
                voice_channel = "the voice channel {channel}".format(channel=after_diff.widget_channel.name) if isinstance(
                    after_diff.widget_channel, discord.VoiceChannel) else "{channel}".format(channel=after_diff.widget_channel.mention)
                msg += "Server Widget Channel: {channel}.\n".format(channel=voice_channel)
                embed_message.add_field(name="Server Widget Channel", value="{channel}".format(channel=voice_channel))
        except AttributeError:
            pass

        if msg != "":
            msg = "{user} has updated the guild's settings:\n".format(user=user.mention) + msg
            if await self.config.guild(after).use_embed():
                await self.main.print_log_embed(embed_message, after)
            else:
                await self.main.print_log(msg, after)

    """Called when user gets banned from a Guild."""

    async def on_member_ban(self, guild: discord.Guild, member):
        if await self.config.guild(guild).log_member_ban():
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.ban, member)
            print(entry.created_at)
            print(entry.reason)
            msg = "{member} has been banned from the guild by {user},\nReason for ban: {reason}".format(member=member.mention, reason=entry.reason, user=entry.user.mention)
            embed_message = discord.Embed(title="Ban Member Log")
            embed_message.add_field(name="Banned Member", value=member.mention)
            embed_message.add_field(name="Reason", value=entry.reason)
            embed_message.add_field(name="Moderator", value=entry.user.mention)
            if await self.config.guild(guild).use_embed():
                await self.main.print_log_embed(embed_message, guild)
            else:
                await self.main.print_log(msg, guild)

    """Called when a User gets unbanned from a Guild."""

    async def on_member_unban(self, guild: discord.Guild, member: discord.User):
        if await self.config.guild(guild).log_member_unban():
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.unban, member)
            msg = "{member} has been unbanned from the guild by {user}.".format(member=member.mention, user=entry.user.mention)
            embed_message = discord.Embed(title="Unban Member Log")
            embed_message.add_field(name="Unbanned Member", value=member.mention)
            embed_message.add_field(name="Moderator", value=entry.user.mention)
            if await self.config.guild(guild).use_embed():
                await self.main.print_log_embed(embed_message, guild)
            else:
                await self.main.print_log(msg, guild)

    """Called when a Member joins a Guild."""

    async def on_member_join(self, member: discord.Member):
        if await self.config.guild(member.guild).log_member_join():
            msg = "{member} has joined the guild.".format(member=member.mention)
            embed_message = discord.Embed(title="Member Join Log")
            embed_message.add_field(name="Member", value=member.mention)
            if await self.config.guild(member.guild).use_embed():
                await self.main.print_log_embed(embed_message, member.guild)
            else:
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
            embed_message = discord.Embed(title="Member Leave Log")
            embed_message.add_field(name="Member", value=member.mention)
            if await self.config.guild(member.guild).use_embed():
                await self.main.print_log_embed(embed_message, member.guild)
            else:
                await self.main.print_log(msg, member.guild)

    """Called when a Member gets kicked from a Guild."""

    async def on_member_kick(self, member: discord.Member):
        if await self.config.guild(member.guild).log_member_leave():
            entry = await AuditManager.get_audit_log(member.guild, discord.AuditLogAction.kick, member)
            user = entry.user
            msg = "{member} has been kicked by {user}.\nReason for kick: {reason}".format(member=member.mention, user=user.mention, reason=entry.reason)
            embed_message = discord.Embed(title="Member Kick Log")
            embed_message.add_field(name="Member", value=member.mention)
            embed_message.add_field(name="Reason", value=entry.reason)
            embed_message.add_field(name="Moderator", value=entry.user.mention)
            if await self.config.guild(member.guild).use_embed():
                await self.main.print_log_embed(embed_message, member.guild)
            else:
                await self.main.print_log(msg, member.guild)

    """Called when a Message receives an update event."""

    # TODO: add link to message
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if after.guild is None:
            return
        if await self.config.guild(before.guild).log_edit_message():
            msg = ""

            embed_message = discord.Embed(title="Message Edit Log")
            embed_message.add_field(name="Author of message", value=after.author.mention)
            embed_message.add_field(name="Channel", value=after.channel.mention)

            if before.content != after.content:
                msg = "A message of {member} has been edited in channel {channel}.\n**__Edited message__**:\n{message}\n\n**__Original message__**:\n{old_message}".format(
                    message=after.content, old_message=before.content, member=after.author.mention, channel=after.channel.mention)

                embed_message.add_field(name="Edited message", value=after.content, inline=False)
                embed_message.add_field(name="Original message", value=before.content, inline=False)

            elif before.pinned != after.pinned:
                un = "un" if not after.pinned else ""
                msg = "A message of {member} has been {un}pinned in channel {channel}.".format(un=un, member=after.author.mention, channel=after.channel.mention)

                embed_message.add_field(name="Message", value=after.content, inline=False)
                embed_message.add_field(name="Pinned", value=after.pinned)

            if msg == "":
                return
            if await self.config.guild(before.guild).use_embed():
                embed_message.url = after.jump_url
                await self.main.print_log_embed(embed_message, after.guild)
            else:
                await self.main.print_log(msg, after.guild)

    """Called when a message is deleted."""

    # TODO: Add deleted by, time of deleted message
    async def on_message_delete(self, message: discord.Message):
        if message.guild is None:
            return
        if await self.config.guild(message.guild).log_delete_message():
            msg = "A message of {member} has been deleted in channel {channel}.\nOriginal message:\n{message}".format(message=message.system_content, member=message.author.mention, channel=message.channel.mention)
            embed_message = discord.Embed(title="Message Delete Log")
            embed_message.add_field(name="Author", value=message.author.mention)
            embed_message.add_field(name="Channel", value=message.channel.mention)

            # Embed message probably
            if message.system_content == "":
                embed_message.add_field(name="Embed", value="The message contained {num} embed".format(num=len(message.embeds)))
                msg = "A message of {member} has been deleted in channel {channel}.\nThe message contained {num} embed:\n".format(member=message.author.mention, channel=message.channel.mention,num=len(message.embeds))
            else:
                if len(message.embeds) > 0:
                    embed_message.add_field(name="Embed", value="The message contained {num} embed".format(num=len(message.embeds)))
                    msg += "\nThe message contained {num} embed:\n"
                embed_message.add_field(name="Message", value=message.system_content)

            channel: discord.TextChannel = await self.main.get_channel(message.guild)
            if await self.config.guild(message.guild).use_embed():
                await self.main.print_log_embed(embed_message, message.guild)
            else:
                await self.main.print_log(msg, message.guild)

            for embed in message.embeds:
                await channel.send(embed=embed)

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

        if before.roles != after.roles:
            await self.on_member_role_change(before, after)

        if before.nick != after.nick:
            await self.on_nickname_change(before, after)

        if before.status != after.status:
            await self.on_status_change(before, after)

        if before.activity != after.activity:
            await self.on_activity_change(before, after)

        if before.avatar_url != after.avatar_url:
            await self.on_avatar_change(before, after)

    async def on_member_role_change(self, before: discord.Member, after: discord.Member):
        guild: discord.Guild = after.guild

        if not await self.config.guild(guild).log_role_change():
            return

        entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, after)
        user: discord.Member = entry.user

        msg = "{member} roles has been changed by {user}:\n"
        embed_message = discord.Embed(title="Member Role Update Log")
        embed_message.add_field(name="Member", value=after.mention)
        embed_message.add_field(name="Moderator", value=user.mention)

        demoted_roles = ""
        promoted_roles = ""

        for br in before.roles:
            if br not in after.roles:
                br: discord.Role
                msg += "Demoted from {role}\n".format(role=br.name)
                demoted_roles += "{role}\n".format(role=br.name)
        for ar in after.roles:
            if ar not in before.roles:
                ar: discord.Role
                msg += "Promoted to {role}\n".format(role=ar.name)
                promoted_roles += "{role}\n".format(role=ar.name)

        msg = msg.format(member=after.mention, user=user.mention)

        if demoted_roles != "":
            embed_message.add_field(name="Roles Removed", value=demoted_roles)
        if promoted_roles != "":
            embed_message.add_field(name="Roles Added", value=promoted_roles)

        if await self.config.guild(guild).use_embed():
            await self.main.print_log_embed(embed_message, guild)
        else:
            await self.main.print_log(msg, guild)

    """Called when a Member updates their avatar."""

    async def on_avatar_change(self, before: discord.Member, after: discord.Member):
        guild: discord.Guild = after.guild
        if not await self.config.guild(guild).log_avatar_change():
            return

        msg = "{member} has changed his avatar icon.".format(member=after.mention)
        embed_message = discord.Embed(title="Avatar Change Log")
        embed_message.add_field(name="Member", value=after.mention)
        embed_message.add_field(name="Avatar Update", value="[Old Avatar]({old_url}) 🠆 [New Avatar]({new_url})".format(old_url=before.avatar_url, new_url=after.avatar_url))

        if await self.config.guild(guild).use_embed():
            await self.main.print_log_embed(embed_message, guild)
        else:
            await self.main.print_log(msg, guild)

    """Called when a Member updates their activity."""
    async def on_activity_change(self, before: discord.Member, after: discord.Member):
        guild: discord.Guild = after.guild

        if not await self.config.guild(guild).log_activity_change():
            return

        msg = ""
        embed_message = discord.Embed(title="Activity Change Log")

        before_activity = before.activity
        after_activity = after.activity

        activity_started = before_activity is None and after_activity is not None
        activity_finished = before_activity is not None and after_activity is None

        activity_changed = False
        if before_activity is not None and after_activity is not None:
            activity_changed = before_activity.name != after_activity.name

        embed_message.add_field(name="Member", value=after.mention)
        if activity_started:
            after_activity_type: discord.ActivityType = after_activity.type
            msg = "{member} started {action} {activity}.".format(member=after.mention, action=after_activity_type.name, activity=after_activity.name)
            embed_message.add_field(name="Activity", value="Started {action} {activity}".format(action=after_activity_type.name, activity=after_activity.name))
        elif activity_finished:
            before_activity_type: discord.ActivityType = before_activity.type
            msg = "{member} stopped {action} {activity}.".format(member=after.mention, action=before_activity_type.name, activity=before_activity.name)
            embed_message.add_field(name="Activity", value="Stopped {action} {activity}".format(action=before_activity_type.name, activity=after_activity.name))
        elif activity_changed:
            before_activity_type: discord.ActivityType = before_activity.type
            after_activity_type: discord.ActivityType = after_activity.type
            msg = "{member} stopped  {action} {activity} and started {action2} {activity2}.".format(member=after.mention, action=before_activity_type.name, activity=before_activity.name, action2=after_activity_type.name, activity2=after_activity.name)
            embed_message.add_field(name="Activity", value="{action} {activity} 🠆 {action2} {activity2}".format(action=before_activity_type.name, activity=before_activity.name, action2=after_activity_type, activity2=after_activity.name))

        if await self.config.guild(guild).use_embed():
            await self.main.print_log_embed(embed_message, guild)
        else:
            await self.main.print_log(msg, guild)

    """Called when a Member updates their status."""
    async def on_status_change(self, before: discord.Member, after: discord.Member):
        guild: discord.Guild = after.guild

        if not await self.config.guild(guild).log_status_change():
            return

        after_status: discord.Status = after.status

        msg = "{member} went {status}.".format(member=after.mention, status=after_status.name)
        embed_message = discord.Embed(title="Status Change Log")
        embed_message.add_field(name="Member", value=after.mention)
        embed_message.add_field(name="Status", value=after_status.name)

        if await self.config.guild(guild).use_embed():
            await self.main.print_log_embed(embed_message, guild)
        else:
            await self.main.print_log(msg, guild)

    """Called when a Member updates their nickname."""
    async def on_nickname_change(self, before: discord.Member, after: discord.Member):
        guild: discord.Guild = after.guild

        if not await self.config.guild(guild).log_nickname_change():
            return

        msg = ""
        embed_message = discord.Embed(title="Nickname Update Log")

        nickname_changed = before.nick != after.nick
        nickname_removed = nickname_changed and after.nick is None
        nickname_created = nickname_changed and before.nick is None

        embed_message.add_field(name="Member", value=after.mention)
        if nickname_changed and not nickname_removed and not nickname_created:
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, after)
            user: discord.Member = entry.user
            msg = "{member} nickname has been changed from **{old}** 🠆 **{new}** by {user}.".format(member=after.mention, old=before.nick, new=after.nick, user=user.mention)

            embed_message.add_field(name="Nickname Changed", value="{old} 🠆 {new}".format(old=before.nick, new=after.nick))
            embed_message.add_field(name="Changed by", value=user.mention)
        elif nickname_created:
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, after)
            user: discord.Member = entry.user
            msg = "{member} nickname has been set to **{new}** by {user}.".format(member=after.mention, new=after.nick, user=user.mention)

            embed_message.add_field(name="Nickname Created", value="{old} 🠆 {new}".format(old=before.display_name, new=after.nick))
            embed_message.add_field(name="Created by", value=user.mention)
        elif nickname_removed:
            entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, after)
            user: discord.Member = entry.user
            msg = "{member} nickname has been removed by {user}.".format(member=after.mention, old=before.nick, user=user.mention)

            embed_message.add_field(name="Nickname Removed", value="{old} 🠆 {new}".format(old=before.nick, new=after.display_name))
            embed_message.add_field(name="Removed by", value=user.mention)

        if await self.config.guild(guild).use_embed():
            await self.main.print_log_embed(embed_message, guild)
        else:
            await self.main.print_log(msg, guild)

    """
    Called when a Member changes their VoiceState.
    The following, but not limited to, examples illustrate when this event is called:
        A member joins a voice room. V
        A member leaves a voice room. V
        A member is muted or deafened by their own accord. V
        A member is muted or deafened by a guild administrator. V
    """

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel != after.channel:
            await self.on_member_voice_join(member, before, after)
        elif before.mute != after.mute or before.deaf != after.deaf:
            await self.on_member_voice_update(member, before, after)
        elif before.self_mute != after.self_mute or before.self_deaf != after.self_deaf:
            await self.on_member_self_voice_update(member, before, after)

    async def on_member_voice_join(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild: discord.Guild = member.guild
        if not await self.config.guild(guild).log_join_leave_voice():
            return

        msg = "{member} has {action} the voice channel: {channel}."
        action = ""

        embed_message = discord.Embed()
        embed_message.add_field(name="Member", value=member.mention)

        join_voice = before.channel is None and after.channel is not None
        left_voice = before.channel is not None and after.channel is None
        moved_voice = before.channel is not None and after.channel is not None and after.channel is not before.channel

        if join_voice:
            embed_message.title = "Member Join Voice Log"
            embed_message.add_field(name="Voice Channel", value=after.channel.name)
            action = "connected"
        elif left_voice:
            embed_message.title = "Member Left Voice Log"
            embed_message.add_field(name="Voice Channel", value=before.channel.name)
            action = "disconnected"
        elif moved_voice:
            embed_message.title = "Member Move Voice Log"
            embed_message.add_field(name="Voice Channel", value="{old} 🠆 {new}".format(old=before.channel.name, new=after.channel.name))
            action = "moved to"

        channel_name = before.channel.name if left_voice else after.channel.name
        msg = msg.format(member=member.mention, action=action, channel=channel_name)

        if await self.config.guild(guild).use_embed():
            await self.main.print_log_embed(embed_message, guild)
        else:
            await self.main.print_log(msg, guild)

    async def on_member_voice_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild: discord.Guild = member.guild

        muted = not before.mute and after.mute
        unmuted = before.mute and not after.mute
        deafen = not before.deaf and after.deaf
        undeafen = before.deaf and not after.deaf

        entry = await AuditManager.get_audit_log(guild, discord.AuditLogAction.member_update, member)
        user: discord.Member = entry.user

        msg = ""

        embed_message = discord.Embed()
        embed_message.add_field(name="Member", value=member.mention)
        embed_message.add_field(name="Moderator", value=user.mention)

        if await self.config.guild(guild).log_mute():
            if muted:
                msg = "{member} has been muted by {user}."
                embed_message.title = "Member Mute Log"
            elif unmuted:
                msg = "{member} has been unmuted by {user}."
                embed_message.title = "Member Unmute Log"
        if await self.config.guild(guild).log_deafen():
            if deafen:
                msg = "{member} has been deafen by {user}."
                embed_message.title = "Member Deafen Log"
            elif undeafen:
                msg = "{member} has been undeafen by {user}."
                embed_message.title = "Member Undeafen Log"

        if msg == "":
            return

        msg = msg.format(member=member.mention, user=user.mention)
        if await self.config.guild(guild).use_embed():
            await self.main.print_log_embed(embed_message, guild)
        else:
            await self.main.print_log(msg, guild)

    async def on_member_self_voice_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild: discord.Guild = member.guild

        self_muted = not before.self_mute and after.self_mute
        self_unmuted = before.self_mute and not after.self_mute
        self_deafen = not before.self_deaf and after.self_deaf
        self_undeafen = before.self_deaf and not after.self_deaf

        msg = ""
        embed_message = discord.Embed()
        embed_message.add_field(name="Member", value=member.mention)

        if await self.config.guild(guild).log_self_mute():
            if self_muted:
                msg = "{member} has self muted themselves."
                embed_message.title = "Member Self-Mute Log"
            elif self_unmuted:
                msg = "{member} has self unmuted themselves."
                embed_message.title = "Member Self-Unmute Log"
        if await self.config.guild(guild).log_self_deafen():
            if self_deafen:
                msg = "{member} has self deafen themselves."
                embed_message.title = "Member Self-Deafen Log"
            elif self_undeafen:
                msg = "{member} has self undeafen themselves."
                embed_message.title = "Member Self-Undeafen Log"
        if await self.config.guild(guild).log_self_mute() and await self.config.guild(guild).log_self_deafen():
            if self_muted and self_deafen:
                msg = "{member} has self muted and deafen themselves."
                embed_message.title = "Member Self-MutedDeafen Log"
            elif self_unmuted and self_undeafen:
                msg = "{member} has self unmuted and undeafen themselves."
                embed_message.title = "Member Self-UnmutedUndeafen Log"

        if msg == "":
            return

        msg = msg.format(member=member.mention)
        if await self.config.guild(guild).use_embed():
            await self.main.print_log_embed(embed_message, guild)
        else:
            await self.main.print_log(msg, guild)
