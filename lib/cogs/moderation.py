from random import choice, randint
from typing import Optional

from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import BadArgument
from discord.ext.commands import command


class Moderation(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="bt", aliases=["botspam", "bspam"])
	async def command_spam(self, ctx):
		await ctx.send(f"Please Keep Bot Commands to <#694212081381146684>")

	@command_spam.error
	async def command_spam_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.send("Command Issue, please try again")


	@command(name="bump", aliases=["vote", "voting"])
	async def bump_our_server(self, ctx):
		await ctx.send(f"If your interested in bumping our server go to <#810154296808701952> \nIf you are not willing to go to websites and login then please just go to <#694212081381146684> and do !d bump")

	@command(name="")

	@bump_our_server.error
	async def bump_our_server_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.send("Sorry something went wrong trying to send bump info please try again later!")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("moderation")

def setup(bot):
	bot.add_cog(Moderation(bot))
