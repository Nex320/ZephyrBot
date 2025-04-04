import discord
import os
import random
import requests
import websockets
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument

# Bot configuration
TOKEN = "TONEK"
PREFIX = commands.when_mentioned_or("!Z ", "!z ")
STATUS_MESSAGE = "Type \"!Z help\" for assistance!"
ERROR_DIR = "errordict"
OG_ERROR_DIR = "ogerrordict"
HELP_FILE = "help.txt"

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None, case_insensitive=True)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=STATUS_MESSAGE))
    print(f"Bot is ready! Logged in as {bot.user}")
    
#@bot.event    
#async def fetch_xbl_status():
   # url = 'wss://kvchecker.com/ws/LIVEAuthentication'
#    
 #   async with websockets.connect(url) as websocket:
#        while True:
 #           try:
 #               # Receiving message from WebSocket
 #               message = await websocket.recv()
 #               data = json.loads(message)
 #               
 #               # Check if it's an xbl_status message
 #               if data.get("message_type") == "xbl_status":
  #                  services = data.get("services", [])
 #                   status_message = ""
 #                   
                    # Iterate over each service and build the status message
 #                   for service in services:
  #                      service_status = f"{service['name']}: {service['description']}"
 #                       status_message += f"{service_status}\n"
                    
 #                   # Add the last update time
 #                   last_update = datetime.now().strftime("%I:%M:%S %p")
#                    status_message += f"Last Update: {last_update}"
#
  #                  return status_message

  #         except Exception as e:
   #             print(f"Error: {e}")
  #              return "Error fetching Xbox Live status."







@bot.command(name="error")
async def error(ctx, code: str):
    """Fetches the error message from a corresponding text file."""
    code = code.upper()
    file_path = os.path.join(ERROR_DIR, f"{code}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            message = file.read()
        await ctx.reply(f"{message}\n*``We take edit sugestions, Just contact us!``*")
    else:
        await ctx.reply(f"Error {code} not found.")
     
@bot.command(name="ogerror")
async def ogerror(ctx, code: str):
    """Fetches the error message from a corresponding text file."""
    code = code.upper()
    file_path = os.path.join(OG_ERROR_DIR, f"{code}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            message = file.read()
        await ctx.reply(f"{message}\n*``We take edit sugestions, Just contact us!``*")
        
    else:
        await ctx.reply(f"Error {code} not found.")

@bot.command(name="help")
async def help_command(ctx):
    """Sends the help message from help.txt."""
    if os.path.exists(HELP_FILE):
        with open(HELP_FILE, "r", encoding="utf-8") as file:
            message = file.read()
        await ctx.reply(message)
    else:
        await ctx.reply("Help file not found.")
        
@bot.command(name="falseoh")
async def falseoh(ctx):
    if os.path.exists("foh.txt"):
        with open("foh.txt", "r", encoding="utf-8") as file:
            message = file.read()
        await ctx.reply(message)
    else:
        await ctx.reply("Help file not found.")
        
@bot.command(name="ena")
async def ena(ctx):
    await ctx.reply("https://tenor.com/view/temptation-stairway-ena-gif-20394886")
    
@bot.command(name="blazer")
async def blazer(ctx):
    await ctx.reply("https://cdn.discordapp.com/attachments/539628526043660300/1357211571327209543/IMG20240619051540.jpg?ex=67ef6146&is=67ee0fc6&hm=4c8d7b91fdc047c4fd5745ac9e5de14521a16b14b906e69c68fa4f7f67d43d27&")
 
@bot.command(name="howto")
async def howto(ctx):
    for i in range(1, 5):
        file_name = f"howto{i}.txt"
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                message = file.read()
                await ctx.reply(message)

@bot.command(name="index")
async def index_command(ctx):
    """Lists all known errors from errordict and ogerrordict."""
    error_files = set()
    for directory in [ERROR_DIR, OG_ERROR_DIR]:
        if os.path.exists(directory):
            error_files.update(f[:-4] for f in os.listdir(directory) if f.endswith(".txt"))
    
    if error_files:
        await ctx.reply("```Known xbox error codes: ```" + ", ".join(sorted(error_files)))
    else:
        await ctx.reply("No error codes found.")

@bot.command(name="randomerror")
async def random_error(ctx):
    """Selects a random error from either errordict or ogerrordict."""
    error_files = []
    for directory in [ERROR_DIR, OG_ERROR_DIR]:
        if os.path.exists(directory):
            error_files.extend(os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".txt"))
    
    if error_files:
        selected_file = random.choice(error_files)
        with open(selected_file, "r", encoding="utf-8") as file:
            message = file.read()
        await ctx.reply(message)
    else:
        await ctx.reply("No errors found.")
        
@bot.command(name="say")
async def say(ctx, *, message: str):
    """Parrots what the user says unless it contains a blacklisted word."""
    try:
        # Read blacklist words from filter.txt
        with open("filter.txt", "r") as f:
            blacklist = [line.strip().lower() for line in f if line.strip()]
        
        # Normalize message for comparison
        message_words = message.lower().split()

        # Check for blacklisted words
        if any(word in blacklist for word in message_words):
            await ctx.send(f"{ctx.author.display_name} has just used a blacklisted word!")
        else:
            await ctx.send(message)
    except Exception as e:
        await ctx.send("An error occurred while processing your request.")
        print(f"Error in say command: {e}")



#@bot.command(name="xbl")
#async def xbl(ctx):
 #   status_message = await fetch_xbl_status()
  #  await message.channel.send(status_message)  


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.reply(f"Command not found: {error}")
    elif isinstance(error, MissingRequiredArgument):
        await ctx.reply(f"Erm.. Not quite sure i understood that, You may have forgot an argument.")
    else:
        raise error


# Run the bot
bot.run(TOKEN)
