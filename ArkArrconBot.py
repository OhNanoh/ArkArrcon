from mcrcon import MCRcon
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import os


load_dotenv("Config/UserConfig.ini")
host = os.getenv('RCON_IP')
rcon_port = os.getenv('RCON_PORT')
rcon_password = str(os.getenv('RCON_PASS'))
TOKEN = str(os.getenv('DISCORD_TOKEN'))
intents = discord.Intents.default()
intents.messages = True
intents.guild_messages = True
intents.message_content = True
intents.webhooks = True
intents.guilds = True
intents.typing = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)


def execute_rcon(command):
    try:
        with MCRcon(host, rcon_password, port=rcon_port) as mcr:
            response = mcr.command(command)
            return f"Server Response to '{command}': \n\n{response}"

    except Exception as e:
        return f"Failed to connect or run command: {e}"


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='rconcommand', help='Executes an rcon command')
async def bot_rcon(ctx, *rcon_command):
    try:
        await ctx.send(f"Executing rcon command...")
        result = execute_rcon(' '.join(rcon_command))
        await ctx.send(result)

    except Exception as e:
        await ctx.send(f'Failed to execute rcon command: {e}')

bot.run(TOKEN)
