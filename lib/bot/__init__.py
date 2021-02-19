from asyncio import sleep
from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Intents
from discord import Embed, File
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)

from ..db import db

PREFIX = "`"
OWNER_IDS = [158639613991321600]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
INGORE_EXCEPTRIONS = (CommandNotFound, BadArgument)

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f" {cog} cog ready")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.cogs_ready = Ready()
		
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		db.autosave(self.scheduler)
		super().__init__(
			command_prefix=PREFIX, 
			owner_ids=OWNER_IDS,
			intents=Intents.all(),
			)

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f" {cog} cog loaded")

		print("setup complete")

	def run(self, version):
		self.VERSION = version

		print("Connecting to server!")
		self.setup()

		with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		super().run(self.TOKEN, reconnect=True)

	async def process_commands(self, message):
		ctx = await self.get_context(message, cls=Context)
		
		if ctx.command is not None and ctx.guild is not None:
			if self.ready:
				await self.invoke(ctx)

			else:
				await ctx.send("I'm not ready to receieve commands. Please wait a few seconds.")

	async def bump_us(self):
		await self.stdout.send("Don't forget to bump our server! <#810154296808701952>")

	async def on_connect(self):
		print("bot connected")

	async def on_disconnect(self):
		print("bot disconnected")

	async def on_error(self, err, *args, **kwargs):
		if err == "on_command_error":
			await args[0].send("something went wrong.")

		await self.stdout.send("An Error has Occured!!!")
		raise

	async def on_command_error(self, ctx, exc):
		if any([isinstance(exc, error) for error in INGORE_EXCEPTRIONS]):
			pass

		elif isinstance(exc, MissingRequiredArgument):
			await ctx.send("One or more required arguments are missing!")

		elif isinstance(exc.original, HTTPException):
			await ctx.send("Unable to send message.")

		elif isinstance(exc.original, Forbidden):
			await ctx.send("I do not have permission to do that.")
			
		elif hasattr(exc, "original"):
			raise exc.original

		else:
			raise exc.original

	async def on_ready(self):
		if not self.ready:
			self.guild = self.get_guild(694207514853638184)
			self.stdout = self.get_channel(811273873139433552)
			self.scheduler.add_job(self.bump_us, CronTrigger(hour=23, minute=59, second=59))
			self.scheduler.start()

			# embed = Embed(title="Now Online!", decription="Elsyium bot is now online!", colour=0xFF0000)
			# fields = [("Name", "Value", True), 
			# 		 ("another field", "this field will be next to the other one", True),
			# 		 ("a non-inline field", "this field will appear on its own row.", False)]
			# for name, value, inline in fields:		 
			# 	embed.add_field(name=name, value=value, inline=inline)
			# embed.set_author(name="Elsyium Bot", icon_url=self.guild.icon_url)
			# embed.set_footer(text="Don't Forget to check out our server!")
			# embed.set_thumbnail(url=self.guild.icon_url)
			# embed.set_image(url=self.guild.icon_url)
			# await channel.send(embed=embed)

			# await channel.send(file=File("./data/images/main_logo.png"))

			while not self.cogs_ready.all_ready():
				 await sleep(0.5)

			await self.stdout.send("Elsyium bot is now online!")
			self.ready = True
			print("bot ready")

		else:
			print("bot reconnected")

	async def on_message(self, message):
		if not message.author.bot:
			await self.process_commands(message)


bot = Bot()