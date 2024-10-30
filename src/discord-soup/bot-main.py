import discord
import config
import requests
import emoji
from discord import app_commands

cfg = config.read_config()

target_guild = discord.Object(id=cfg['discord']['server_id'])

class SoupClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=target_guild)
        await self.tree.sync(guild=target_guild)

intents = discord.Intents.default()
client = SoupClient(intents=intents)

# Event hooks
@client.event
async def on_ready():
    print('We have successfully logged in as {0.user}'.format(client))

# arrive
@client.tree.command(name='enter', description='Make Soup arrive')
async def cmd_enter(interaction: discord.Interaction):
    handle_interraction(interaction)

@client.tree.command(name='hello', description='Make Soup arrive')
async def cmd_hello(interaction: discord.Interaction):
    handle_interraction(interaction)

# depart
@client.tree.command(name='exit', description='Make Soup leave')
async def cmd_exit(interaction: discord.Interaction):
    handle_interraction(interaction)

@client.tree.command(name='bye', description='Make Soup leave')
async def cmd_bye(interaction: discord.Interaction):
    handle_interraction(interaction)

# laughing
@client.tree.command(name='shortlaugh', description='Soup will laugh')
async def cmd_short_laugh(interaction: discord.Interaction):
    handle_interraction(interaction)

@client.tree.command(name='lol', description='Soup will laugh')
async def cmd_lol(interaction: discord.Interaction):
    handle_interraction(interaction)

@client.tree.command(name='longlaugh', description='Soup will lose her shit')
async def cmd_long_laugh(interaction: discord.Interaction):
    handle_interraction(interaction)

@client.tree.command(name='rofl', description='Soup will lose her shit')
async def cmd_rofl(interaction: discord.Interaction):
    handle_interraction(interaction)

# interactive commands
@client.tree.command(name='say', description='Soup will say what you tell her')
@app_commands.describe(message='What you want Soup to say')
async def cmd_say(interaction: discord.Interaction, message: str):
    handle_interraction(interaction, message)

@client.tree.command(name='talk', description='Soup will say what you tell her')
@app_commands.describe(message='What you want Soup to say')
async def cmd_talk(interaction: discord.Interaction, message: str):
    handle_interraction(interaction, message)

# Private functions
async def handle_interraction(interaction: discord.Interaction, message: str = ''):
    if is_the_right_channel(interaction):
        log_interaction(interaction, message)
        relay_message(interaction.command.name, message)
        await interaction.response.send_message(
            content=f"sent {interaction.command.name} command {emoji.checkmark}",
            silent=True,
            ephemeral=True,
            delete_after=30,
        )

def is_the_right_channel(interaction: discord.Interaction):
    return str(interaction.channel_id) == cfg['discord']['read_channel_id']

def log_interaction(interaction: discord.Interaction, message: str = ''):
    if message == '':
        print(f"{interaction.user.name} - {interaction.command.name}")
    else:
        print(f"{interaction.user.name} - {interaction.command.name} - {message}")

def relay_message(type: str, message: str = ''):
    relay_message = {
        'gtitle': type,
        'gbody': message,
    }

    resp = requests.post(cfg['mixitup']['webhook_url'], json = relay_message)

    if(resp.text != ''):
        print(resp.text)

client.run(config.read_auth_key())