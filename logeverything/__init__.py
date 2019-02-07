from logeverything.logeverything import LogEverything


async def setup(bot):
    cog = LogEverything(bot)
    bot.add_cog(cog)
    await cog.startup()
