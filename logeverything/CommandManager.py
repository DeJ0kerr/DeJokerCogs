import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core import Config
from redbot.core.bot import Red


class CommandManager:

    def __init__(self, bot: Red, config: Config, main):
        self.bot: Red = bot
        self.config: Config = config
        self.main = main

    @commands.group(name="logset")
    @commands.guild_only()
    @checks.guildowner_or_permissions()
    async def logset(self, ctx: commands.Context):
        """
        LogEverything Configuration Options

        Use ``[p]logset <option> <True/False>``
        """
        pass

    @logset.command(name="logchannel")
    async def set_log_channel(self, ctx: commands.Context, value: discord.TextChannel = None):
        """Configure where the logs will be sent to."""
        if value is not None:
            channel_id = value.id
            await self.config.guild(ctx.guild).channel_log.set(channel_id)

        channel_id = await self.config.guild(ctx.guild).channel_log()
        channel: discord.TextChannel = ctx.guild.get_channel(channel_id)
        if channel is None:
            await ctx.send("No channel was set. To set type {prefix}logset logchannel #channel".format(prefix=ctx.clean_prefix))
            await ctx.send_help()
        else:
            await ctx.send("Bot will send logs to {channel}.".format(channel=channel.mention))

    @logset.command(name="status")
    async def set_status_change(self, ctx: commands.Context, value: str = None):
        """Configure log status changes."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_status_change.set(v)

        v = await self.config.guild(ctx.guild).log_status_change()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log member's status change.".format(will=will_log))

    @logset.command(name="activity")
    async def set_activity_change(self, ctx: commands.Context, value: str = None):
        """Configure log activity changes."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_activity_change.set(v)

        v = await self.config.guild(ctx.guild).log_activity_change()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log member's activity change.".format(will=will_log))

    @logset.command(name="avatar")
    async def set_avatar_change(self, ctx: commands.Context, value: str = None):
        """Configure log avatar changes."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_avatar_change.set(v)

        v = await self.config.guild(ctx.guild).log_avatar_change()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log member's avatar change.".format(will=will_log))

    @logset.command(name="nickname")
    async def set_nickname_change(self, ctx: commands.Context, value: str = None):
        """Configure log nickname changes"""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_nickname_change.set(v)

        v = await self.config.guild(ctx.guild).log_nickname_change()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log member's nickname change.".format(will=will_log))

    @logset.command(name="rolemember")
    async def set_role_change(self, ctx: commands.Context, value: str = None):
        """Configure log member's role changes."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_role_change.set(v)

        v = await self.config.guild(ctx.guild).log_role_change()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log member's role change.".format(will=will_log))

    @logset.command(name="voice")
    async def set_voice(self, ctx: commands.Context, value: str = None):
        """Configure log voice connections."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_join_leave_voice.set(v)

        v = await self.config.guild(ctx.guild).log_join_leave_voice()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log member's voice connection.".format(will=will_log))

    @logset.command(name="mute")
    async def set_mute(self, ctx: commands.Context, value: str = None):
        """Configure log muting members."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_mute.set(v)

        v = await self.config.guild(ctx.guild).log_mute()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log muting members.".format(will=will_log))

    @logset.command(name="deafen")
    async def set_deafen(self, ctx: commands.Context, value: str = None):
        """Configure log deafening members."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_deafen.set(v)

        v = await self.config.guild(ctx.guild).log_deafen()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log deafening members.".format(will=will_log))

    @logset.command(name="selfmute")
    async def set_self_mute(self, ctx: commands.Context, value: str = None):
        """Configure log self-mute members."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_self_mute.set(v)

        v = await self.config.guild(ctx.guild).log_self_mute()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log self-mute members.".format(will=will_log))

    @logset.command(name="selfdeafen")
    async def set_self_deafen(self, ctx: commands.Context, value: str = None):
        """Configure log self-deafen members."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_self_deafen.set(v)

        v = await self.config.guild(ctx.guild).log_self_deafen()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log self-deafen members.".format(will=will_log))

    @logset.command(name="deletemsg")
    async def set_delete_messge(self, ctx: commands.Context, value: str = None):
        """Configure log deleted messages."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_delete_message.set(v)

        v = await self.config.guild(ctx.guild).log_delete_message()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log deleted messages.".format(will=will_log))

    @logset.command(name="memberjoin")
    async def set_member_join(self, ctx: commands.Context, value: str = None):
        """Configure log joining members."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_member_join.set(v)

        v = await self.config.guild(ctx.guild).log_member_join()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log members joining the guild.".format(will=will_log))

    @logset.command(name="memberleave")
    async def set_member_leave(self, ctx: commands.Context, value: str = None):
        """Configure log leaving members."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_member_leave.set(v)

        v = await self.config.guild(ctx.guild).log_member_leave()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log members leaving the guild.".format(will=will_log))

    @logset.command(name="ban")
    async def set_ban(self, ctx: commands.Context, value: str = None):
        """Configure log banning members."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_member_ban.set(v)

        v = await self.config.guild(ctx.guild).log_member_ban()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log banning members.".format(will=will_log))

    @logset.command(name="unban")
    async def set_unban(self, ctx: commands.Context, value: str = None):
        """Configure log unbanning users."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_member_unban.set(v)

        v = await self.config.guild(ctx.guild).log_member_unban()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log unbanning members.".format(will=will_log))

    @logset.command(name="modlogcog")
    async def set_modlog(self, ctx: commands.Context, value: str = None):
        """Configure disabling modlog cog."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).disable_modlog.set(v)

        v = await self.config.guild(ctx.guild).disable_modlog()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}disable modlog cog.".format(will=will_log))
        if v:
            await self.main.disable_modlog_cog(ctx.guild)

    @logset.command(name="channel")
    async def set_guild_settings(self, ctx: commands.Context, value: str = None):
        """Configure log creation and deletion of channels."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_channel_creation.set(v)

        v = await self.config.guild(ctx.guild).log_channel_creation()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log creation and deletion of channels.".format(will=will_log))

    @logset.command(name="editchannel")
    async def set_guild_settings(self, ctx: commands.Context, value: str = None):
        """Configure log channel editing."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_channel_edit.set(v)

        v = await self.config.guild(ctx.guild).log_channel_edit()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log channel editing.".format(will=will_log))

    @logset.command(name="guildsettings")
    async def set_guild_settings(self, ctx: commands.Context, value: str = None):
        """Configure log changes in the guild settings."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_guild_settings.set(v)

        v = await self.config.guild(ctx.guild).log_guild_settings()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log changes in the guild settings.".format(will=will_log))

    @logset.command(name="editmessage")
    async def set_edit_message(self, ctx: commands.Context, value: str = None):
        """Configure log message editing."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_edit_message.set(v)

        v = await self.config.guild(ctx.guild).log_edit_message()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log message editing.".format(will=will_log))

    @logset.command(name="emoji")
    async def set_edit_message(self, ctx: commands.Context, value: str = None):
        """Configure log emoji updates."""
        if value is not None:
            v = value.lower() == "true"
            await self.config.guild(ctx.guild).log_emojis.set(v)

        v = await self.config.guild(ctx.guild).log_emojis()
        will_log = "" if v else "not "
        await ctx.send("Bot will {will}log emoji updates.".format(will=will_log))
