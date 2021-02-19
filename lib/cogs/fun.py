from random import choice, randint
from typing import Optional

from aiohttp import request
from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import BadArgument
from discord.ext.commands import command


class Fun(Cog):
	def __init__(self, bot):
		self.bot = bot

	@command(name="dice", aliases=["roll"])
	async def roll_dice(self, ctx, die_string: str):
		dice, value = (int(term) for term in die_string.split("d"))

		if dice <= 25:
			rolls = [randint(1, value) for i in range(dice)]

			await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

		else:
			await ctx.send("I can't roll that many dice please try a lower number.")
			
	@command(name="slap", aliases=["hit"])
	async def slap_member(self, ctx, member: Member, *, reason:Optional[str] = "For No Reason!"):
		await ctx.send(f"{ctx.author.display_name} slapped {member.display_name} for {reason}!")

	@slap_member.error
	async def slap_member_error(self, ctx, exc):
		if isinstance(exc, BadArgument):
			await ctx.send("I can't find that member.")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("fun")

def setup(bot):
	bot.add_cog(Fun(bot))