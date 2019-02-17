import discord
import time

from .CommandManager import CommandManager
from .EventManager import EventManager
from redbot.core import modlog
from redbot.core import commands
from redbot.core import Config
from redbot.core.bot import Red


class LogEverything(CommandManager, EventManager, commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config: Config = Config.get_conf(self, 217681978223)
        self.config.register_guild(
            log_status_change=False,
            log_activity_change=False,
            log_avatar_change=False,
            log_nickname_change=False,
            log_role_change=True,
            log_join_leave_voice=False,
            log_mute=True,
            log_deafen=True,
            log_self_mute=False,
            log_self_deafen=False,
            log_delete_message=False,
            log_member_join=True,
            log_member_leave=True,
            log_member_ban=True,
            log_member_unban=True,
            log_edit_message=True,
            log_guild_settings=True,
            log_channel_creation=True,
            log_channel_edit=True,
            log_emojis=True,
            disable_modlog=True,
            use_embed=True,
            channel_log=None
        )
        super().__init__(self.bot, self.config, self)

    async def startup(self):
        for g in self.bot.guilds:
            if await self.config.guild(g).disable_modlog():
                try:
                    await modlog.get_modlog_channel(g)
                except RuntimeError:
                    pass
                else:
                    prefix = await self.bot.db.prefix()
                    await self.print_log("Disabling modlog cog. ``{prefix}logset modlogcog to change``".format(prefix=prefix[0]), g)
                    await modlog.set_modlog_channel(g, None)

    @staticmethod
    async def disable_modlog_cog(guild):
        await modlog.set_modlog_channel(guild, None)

    async def get_channel(self, guild: discord.Guild):
        if not await self.is_channel_set(guild):
            return None

        channel_id = await self.config.guild(guild).channel_log()
        channel = guild.get_channel(channel_id)
        return channel

    async def is_channel_set(self, guild: discord.Guild):
        channel_id = await self.config.guild(guild).channel_log()
        channel: discord.TextChannel = guild.get_channel(channel_id)
        return channel is not None

    async def print_log(self, message: str, guild: discord.Guild):
        if not await self.is_channel_set(guild):
            prefix = await self.bot.db.prefix()
            print("Use \"{prefix}logset logchannel #yourchannel\" In order to start using LogEverything Cog.".format(
                prefix=prefix[0]))
            return

        channel_id = await self.config.guild(guild).channel_log()
        channel = guild.get_channel(channel_id)

        if message == "":
            return
        message = message.replace("\n", "\n\t\t\t\t\t")
        message = "[{time}] ".format(time=time.strftime("%H:%M:%S")) + message
        await channel.send(message)

    async def print_log_embed(self, embed_message: discord.Embed, guild: discord.Guild):
        if not await self.is_channel_set(guild):
            prefix = await self.bot.db.prefix()
            print("Use \"{prefix}logset logchannel #yourchannel\" In order to start using LogEverything Cog.".format(
                prefix=prefix[0]))
            return

        channel_id = await self.config.guild(guild).channel_log()
        channel = guild.get_channel(channel_id)
        embed_message.set_footer(text=time.strftime("%d/%m/%Y - %H:%M:%S"))
        embed_message.set_author(name="Log Everything", icon_url="https://www.shareicon.net/data/512x512/2016/09/21/830532_log_512x512.png")
        await channel.send(embed=embed_message)