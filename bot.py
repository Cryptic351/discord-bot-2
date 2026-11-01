import os
print("=== BOT.PY FILE LOADED ===", flush=True)

import discord
from discord.ext import commands
from flask import Flask
import threading

print("=== IMPORTS DONE ===", flush=True)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

YOUR_ID = 1407065909654323303

SCRIPTS = {
    "duels": {"name": "Duels Fork - Other Channel", "desc": "This version only shows in other channel", "loadstring": 'loadstring(game:HttpGet("https://pixel-perfect-render-80435.lovable.app/raw/t/10618fce6b9b35ed92d2f2ca1a4e6"))()'},
    "bladeball": {"name": "Blade Ball Other", "desc": "Alt version", "loadstring": 'loadstring(game:HttpGet("https://pastebin.com/raw/xxxx"))()'},
}

@bot.event
async def on_ready():
    print(f"Online as {bot.user}", flush=True)

@bot.command(name="find")
async def find(ctx, *, q=None):
    if not q:
        await ctx.send("Usage: `!find duels`")
        return
    q = q.lower()
    for k, v in SCRIPTS.items():
        if q in k.lower() or q in v["name"].lower():
            embed = discord.Embed(title=v["name"], description=v["desc"], color=0xFFD400)
            await ctx.send(embed=embed)
            load = v["loadstring"]
            await ctx.send(f"**Mobile 1-tap:**\n`{load}`")
            await ctx.send(f"**PC:**\n```lua\n{load}\n```")
            return
    await ctx.send("Not found. Try `!list`")

@bot.command(name="list")
async def list_s(ctx):
    await ctx.send("**SCRIPTS**\n" + "\n".join([f"`{k}` - {v['name']}" for k,v in SCRIPTS.items()]))

@bot.command()
async def say(ctx, *, message=None):
    if ctx.author.id != YOUR_ID:
        await ctx.send("Only creator", delete_after=5)
        return
    if not message:
        return
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(message)

app = Flask(__name__)

@app.route("/")
def home():
    status = "BOT ONLINE" if bot.is_ready() else "BOT OFFLINE - Flask up but bot not connected"
    return status

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting Flask on port {port}", flush=True)
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    print("=== MAIN STARTING ===", flush=True)
    threading.Thread(target=run_flask, daemon=True).start()
    token = os.getenv("DISCORD_TOKEN")
    print(f"Token is None? {token is None}", flush=True)
    if not token:
        print("CRITICAL: DISCORD_TOKEN is None! Add it in Render > Environment", flush=True)
        import time
        while True:
            time.sleep(3600)
    print("Token found, starting bot...", flush=True)
    bot.run(token)
