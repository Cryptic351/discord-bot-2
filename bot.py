import os
import threading
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# PASTE YOUR LOADSTRINGS HERE
SCRIPTS = {
    "duels": {
        "name": "LUA STUDIO DUELS",
        "desc": "lua studio",
        "loadstring": 'loadstring(game:HttpGet("https://your-link-here.lua"))()',
    },
    "bladeball": {
        "name": "LUA STUDIO BLADE BALL",
        "desc": "alt version",
        "loadstring": 'loadstring(game:HttpGet("https://your-link-2.lua"))()',
    },
}

@bot.event
async def on_ready():
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} slash command(s).")
  except Exception as e:
    print(f"Failed to sync commands: {e}")
  print(f"Online as {bot.user}")

@bot.tree.command(name="find", description="Search for a script by name or key")
@app_commands.describe(query="The script name or key you are looking for")
async def find(interaction: discord.Interaction, query: str):
  q = query.lower()
  for k, v in SCRIPTS.items():
    if q in k.lower() or q in v["name"].lower():
      load = v["loadstring"]
      embed = discord.Embed(
          title=f"\U0001f49b {v['name']}",
          description=f"**{v['desc']}**",
          color=0xFFD400
      )
      embed.set_footer(text="LUA STUDIO ON TOP | IM TOO GOOD")
      await interaction.response.send_message(embed=embed)
      await interaction.followup.send(
          f"\U0001f4f1 **Mobile 1-tap:**\n`{load}`\n\n\U0001f4bb **PC / Normal:**\n```lua\n{load}\n```"
      )
      return
  await interaction.response.send_message("\u274c Not found. Try `/list`", ephemeral=True)

@bot.tree.command(name="list", description="List all available scripts")
async def list_s(interaction: discord.Interaction):
  embed = discord.Embed(title="LUA STUDIO - ALL SCRIPTS", color=0xFFD400)
  content_lines = ["Use `/find <name>` - No more scrolling 20 channels\n"]
  for k, v in SCRIPTS.items():
      content_lines.append(f"**{v['name'].upper()}**\n`/find {k}` - {v['desc']}")
  embed.description = "\n\n".join(content_lines)
  embed.set_footer(text="Yellow & Black | Pixel Logo | Fade-In")
  await interaction.response.send_message(embed=embed)

@bot.tree.command(name="add", description="Add a new script (Admin only)")
@app_commands.describe(key="Unique short key", name="Display name", desc="Short description", loadstring="The full lua loadstring")
async def add_script(interaction: discord.Interaction, key: str, name: str, desc: str, loadstring: str):
  if not interaction.user.guild_permissions.administrator:
    await interaction.response.send_message("\u274c Administrator only.", ephemeral=True)
    return
  SCRIPTS[key.lower()] = {"name": name, "desc": desc, "loadstring": loadstring}
  await interaction.response.send_message(embed=discord.Embed(title="\u2705 SCRIPT ADDED", description=f"**{name}** as `{key.lower()}`\n```lua\n{loadstring}\n```", color=0x57F287))

@bot.tree.command(name="delete", description="Delete a script (Admin only)")
@app_commands.describe(key="The key to delete")
async def delete_script(interaction: discord.Interaction, key: str):
  if not interaction.user.guild_permissions.administrator:
    await interaction.response.send_message("\u274c Administrator only.", ephemeral=True)
    return
  if key.lower() in SCRIPTS:
    del SCRIPTS[key.lower()]
    await interaction.response.send_message(f"\U0001f5d1️ Deleted `{key.lower()}`")
  else:
    await interaction.response.send_message(f"\u274c `{key.lower()}` not found.", ephemeral=True)

@bot.tree.command(name="say", description="Make the bot say a message (Admin only)")
@app_commands.describe(message="The message")
async def say(interaction: discord.Interaction, message: str):
  if not interaction.user.guild_permissions.administrator:
    await interaction.response.send_message("\u274c Administrator only.", ephemeral=True)
    return
  await interaction.response.send_message("\u2705 Sent!", ephemeral=True)
  await interaction.channel.send(message)

app = Flask(__name__)
@app.route("/")
def home():
  return "BOT 2 ONLINE"
def run_flask():
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_flask, daemon=True).start()
bot.run(os.getenv("DISCORD_TOKEN"))
