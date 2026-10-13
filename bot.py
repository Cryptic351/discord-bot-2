import os
import discord
from discord.ext import commands
from flask import Flask
import threading

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

YOUR_ID = 1407065909654323303

# CHANGE THESE TO WHATEVER SCRIPTS YOU WANT FOR THE *OTHER* CHANNEL
SCRIPTS = {
    "duels": {"name": "Duels Fork - Other Channel", "desc": "This version only shows in other channel", "loadstring": 'loadstring(game:HttpGet("https://pixel-perfect-render-80435.lovable.app/raw/t/10618fce6b9b35ed92d2f2ca1a4e6"))()'},
    "bladeball": {"name": "Blade Ball Other", "desc": "Alt version", "loadstring": 'loadstring(game:HttpGet("https://pastebin.com/raw/xxxx"))()'},
}

@bot.event
async def on_ready():
    print(f"Online as {bot.user}")

@bot.command(name="find")
async def find(ctx, *, q=None):
    if not q:
        await ctx.send("Usage: `!find duels`")
        return
    q = q.lower()
    for k, v in SCRIPTS.items():
        if q in k.lower() or q in v["name"].lower():
            embed = discord.Embed(title=f"💛 {v['name']}", description=v["desc"], color=0xFFD400)
            await ctx.send(embed=embed)
            load = v["loadstring"]
            await ctx.send(f"**📱 Mobile 1-tap:**\n`{load}`")
            await ctx.send(f"**💻 PC:**\n```lua\n{load}\n```")
            return
    await ctx.send("Not found. Try `!list`")

@bot.command(name="list")
async def list_s(ctx):
    await ctx.send("**SCRIPTS**\n" + "\n".join([f"`{k}` - {v['name']}" for k,v in SCRIPTS.items()]))

@bot.command()
async def say(ctx, *, message=None):
    if ctx.author.id != YOUR_ID:
        await ctx.send("❌ Only creator", delete_after=5)
        return
    if not message: return
    try: await ctx.message.delete()
    except: pass
    await ctx.send(message)

# Keeps Render alive
app = Flask(__name__)
@app.route("/")
def home(): return "BOT 2 ONLINE"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()

# NEVER put token here - Render will add it
bot.run(os.getenv("DISCORD_TOKEN"))
