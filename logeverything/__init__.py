from logeverything.logeverything import LogEverything


def setup(bot):
    bot.add_cog(LogEverything(bot))
