import discord
from redbot.core import commands
from redbot.core import checks
from redbot.core import bank
from redbot.core.bot import Red
from random import randint
from typing import Any

Cog: Any = getattr(commands, "Cog", object)


class RaffleMain(Cog):

    def __init__(self, bot: Red):
        self.bot = bot
        self.economy = self.bot.get_cog("Economy")
        self.raffles = {}

    @commands.group(name="raffle")
    async def raffle(self, ctx: commands.Context):
        pass

    @checks.mod()
    @raffle.command(name="create")
    async def create_raffle(self, ctx: commands.Context, keyword, amount: int):
        channel: discord.DMChannel = ctx.channel

        if not isinstance(amount, int):
            raise TypeError("Ticket price must be of type int, not {}.".format(type(amount)))

        if keyword in self.raffles.keys():
            await channel.send("The keyword {keyword} is already in use!".format(keyword=keyword))
            return

        raffle: Raffle = Raffle(keyword, amount, ctx.author)
        self.raffles[keyword] = raffle

        currency = await bank.get_currency_name(ctx.guild)
        message = "A **{amount} {currency}** worth raffle has started!" \
                  "\n\nType \"**{prefix}raffle join {keyword}**\" to enter!".format(amount=amount, currency=currency, prefix=ctx.clean_prefix, keyword=keyword)
        footer = "Entering the raffle cost {amount} {currency}".format(amount=amount, currency=currency)

        embed_message: discord.Embed = discord.Embed(title="A Raffle Has Started!", color=discord.Color.gold(), description=message)
        embed_message.set_footer(text=footer)
        await channel.send(embed=embed_message)

    @staticmethod
    def get_embed_message_not_found(ctx, keyword):
        embed_message = discord.Embed(title="Raffle Was Not Found.", description="{}\nThere is no raffle named **{}** ".format(ctx.author.mention, keyword))
        embed_message.set_footer(text="{}raffle list | this might help".format(ctx.clean_prefix))
        return embed_message

    @raffle.command(name="join")
    async def join_raffle(self, ctx: commands.Context, keyword):
        channel: discord.DMChannel = ctx.channel
        member: discord.Member = ctx.author

        raffle: Raffle = self.raffles.get(keyword)
        if raffle is None:
            await channel.send(embed=self.get_embed_message_not_found(ctx, keyword))
            return

        if raffle.is_finished():
            await channel.send("{member} The raffle {keyword} has already finished!".format(member=member.mention, keyword=keyword))
            return

        account: bank.Account = await bank.get_account(member)

        if raffle.has_member(member):
            await channel.send("{member} You are already in the raffle {keyword}!".format(member=member.mention, keyword=keyword))
            return

        if account.balance >= raffle.get_ticket_price():
            ticket_price = raffle.get_ticket_price()

            raffle.add_coins(ticket_price)
            await bank.withdraw_credits(member, ticket_price)

            raffle.add_member(member)
            message = "{member} has payed {ticket_price} entered **{keyword}** raffle!\n They got a chance to win **{amount} {currency}**".format(keyword=keyword, member=member.mention, ticket_price=raffle.get_ticket_price(), amount=raffle.get_amount(),
                                                                                                                                                  currency=await bank.get_currency_name(ctx.guild))
            embed_message = discord.Embed(description=message, title="{keyword} Raffle Update!".format(keyword=keyword))

            await channel.send(embed=embed_message)
        else:
            await channel.send("{member}\nYou do not have enough {currency} to enter the raffle!".format(member=member.mention, currency=await bank.get_currency_name(ctx.guild)))

    @checks.mod()
    @raffle.command(name="winner")
    async def winner_raffle(self, ctx: commands.Context, keyword):
        channel: discord.DMChannel = ctx.channel
        member: discord.Member = ctx.author

        raffle: Raffle = self.raffles.get(keyword)
        if raffle is None:
            await channel.send(embed=self.get_embed_message_not_found(ctx, keyword))
            return

        if len(raffle.get_members()) <= 0:
            message = "Could not choose a winner for raffle {keyword}\nThere are no members participating in this raffle!".format(keyword=keyword)
            embed_message = discord.Embed(description=message, title="Awkward...")
            await channel.send(embed=embed_message)
            return

        winner_id = raffle.get_winner()
        winner: discord.Member = ctx.guild.get_member(winner_id)
        raffle.set_finished()
        self.raffles.pop(raffle.get_keyword())

        message = "The winner of the {keyword} raffle is...\n\n Winner: **{winner}**! \n{winner} Congratulation! You have won {amount} {currency}!".format(keyword=keyword, winner=winner.mention, amount=raffle.get_amount(), currency=await bank.get_currency_name(ctx.guild))
        embed_message = discord.Embed(description=message, title="Raffle Winner Is...")
        await channel.send(embed=embed_message)

        await bank.deposit_credits(winner, raffle.get_amount())

    @raffle.command(name="list")
    async def member_list_raffle(self, ctx: commands.Context, keyword=None):
        channel: discord.DMChannel = ctx.channel
        member: discord.Member = ctx.author

        if keyword is None:
            raffle_list = ""
            counter = 1
            for r in self.raffles:
                if not self.raffles[r].is_finished():
                    raffle = self.raffles[r]
                    raffle_list += "**{number}.** {raffle}, Owner: **{owner}**, Win amount: **{amount} {currency}**, Ticket price: **{ticket} {currency}**\n".format(number=counter, raffle=r, owner=raffle.get_owner().mention, amount=raffle.get_amount(),
                                                                                                                                                                     currency=await bank.get_currency_name(ctx.guild), ticket=raffle.get_ticket_price())
                    counter += 1
            if raffle_list is "":
                raffle_list = "There are no raffles opened currently!"
            embed_message = discord.Embed(description=raffle_list, title="Raffles List")
            await channel.send(embed=embed_message)
        else:
            raffle: Raffle = self.raffles.get(keyword)
            if raffle is None:
                await channel.send(embed=self.get_embed_message_not_found(ctx, keyword))
                return

            message = "There are currently {} members participating in {} raffle!".format(len(raffle.get_members()), raffle.get_keyword())
            embed_message = discord.Embed(description=message, title="{} Raffle List".format(raffle.get_keyword()))
            await channel.send(embed=embed_message)


class Raffle:

    def __init__(self, keyword, ticket_price, owner):
        self.amount = 0
        self.ticket_price = ticket_price
        self.keyword = keyword
        self.finished = False
        self.owner = owner
        self.members = []

    def add_coins(self, coins):
        self.amount += coins

    def get_owner(self):
        return self.owner

    def set_owner(self, owner):
        self.owner = owner

    def get_ticket_price(self):
        return int(self.ticket_price)

    def add_member(self, member: discord.Member):
        self.members.append(member.id)

    def has_member(self, member: discord.Member):
        return member.id in self.members

    def get_winner(self):
        return self.members.pop(randint(0, len(self.members) - 1))

    def is_finished(self):
        return self.finished

    def set_finished(self):
        self.finished = True

    def get_members(self):
        return self.members

    def get_keyword(self):
        return self.keyword

    def get_amount(self):
        return self.amount


def setup(bot):
    bot.add_cog(RaffleMain(bot))
