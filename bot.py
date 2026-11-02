import os
import threading
import discord
from discord.ext import commands
from flask import Flask

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

YOUR_ID = 1407065909654323303

# SCRIPT DICTIONARY
SCRIPTS = {
    "duels": {
        "name": "Duels Fork - Other Channel",
        "desc": "This version only shows in other channel",
        "loadstring": (
            'loadstring(game:HttpGet("https://pixel-perfect-render-80435.lovable.app/raw/t/10618fce6b9b35ed92d2f2ca1a4e6"))()'
        ),
    },
    "bladeball": {
        "name": "Blade Ball Other",
        "desc": "Alt version",
        "loadstring": (
            'loadstring(game:HttpGet("https://pastebin.com/raw/xxxx"))()'
        ),
    },
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
      embed = discord.Embed(
          title=f"💛 {v['name']}", description=v["desc"], color=0xFFD400
      )
      await ctx.send(embed=embed)
      load = v["loadstring"]
      await ctx.send(f"**📱 Mobile 1-tap:**\n`{load}`")
      await ctx.send(f"**💻 PC:**\n```lua\n{load}\n```")
      return
  await ctx.send("Not found. Try `!list`")


@bot.command(name="list")
async def list_s(ctx):
  await ctx.send(
      "**SCRIPTS**\n"
      + "\n".join([f"`{k}` - {v['name']}" for k, v in SCRIPTS.items()])
  )


@bot.command(name="add")
async def add_script(
    ctx, key: str = None, name: str = None, desc: str = None, loadstring: str = None
):
  if ctx.author.id != YOUR_ID:
    await ctx.send("❌ Only creator can add scripts.", delete_after=5)
    return

  # If any part is missing, show the correct format guide
  if not key or not name or not desc or not loadstring:
    await ctx.send(
        "❌ **Invalid usage!**\n"
        "**Format:** `!add key \"Display Name\" \"Description\""
        ' "loadstring(game:HttpGet(...))()"`\n'
        "*(Make sure to use quotes for names, descriptions, and loadstrings that have spaces!)*"
    )
    return

  key = key.lower()
  SCRIPTS[key] = {"name": name, "desc": desc, "loadstring": loadstring}
  await ctx.send(f"✅ Successfully added script: `{key}`")


@bot.command(name="delete")
async def delete_script(ctx, key: str = None):
  if ctx.author.id != YOUR_ID:
    await ctx.send("❌ Only creator can delete scripts.", delete_after=5)
    return

  # If key is missing, show format guide
  if not key:
    await ctx.send(
        "❌ **Invalid usage!**\n"
        "**Format:** `!delete scriptkey`\n"
        "*(Example: `!delete duels`)*"
    )
    return

  key = key.lower()
  if key in SCRIPTS:
    del SCRIPTS[key]
    await ctx.send(f"🗑️ Successfully deleted script: `{key}`")
  else:
    await ctx.send(f"❌ Script `{key}` not found.")


@bot.command()
async def say(ctx, *, message=None):
  if ctx.author.id != YOUR_ID:
    await ctx.send("❌ Only creator", delete_after=5)
    return
  if not message:
    return
  try:
    await ctx.message.delete()
  except:
    pass
  await ctx.send(message)


# Keeps Render alive via Flask web server
app = Flask(__name__)


@app.route("/")
def home():
  return "BOT 2 ONLINE"


def run_flask():
  app.run(host="0.0.0.0", port=10000)


threading.Thread(target=run_flask).start()

# Run the Discord bot using the token from Render Environment variables
bot.run(os.getenv("DISCORD_TOKEN"))
