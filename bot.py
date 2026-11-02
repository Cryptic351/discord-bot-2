import os
import threading
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# SCRIPT DICTIONARY
SCRIPTS = {
    "duels": {
        "name": "LUA STUDIO-DUELS",
        "desc": "Challenge other members, test your skills, and prove yourself in intense 1v1 battles.",
        "loadstring": (
            'loadstring(game:HttpGet("https://raw.githubusercontent.com/Cryptic351/luastudio8/refs/heads/main/(28).lua"))()'
        ),
    },
    "bladeball": {
        "name": "LUA STUDIO BLADE BALL",
        "desc": "alt version",
        "loadstring": (
            'loadstring(game:HttpGet("https://pastebin.com/raw/xxxx"))()'
        ),
    },
}

# /find output layout:
#   "embed" -> one message, loadstrings sit inside the embed under the description
#   "split" -> embed message first, loadstrings as a second message below it
FIND_LAYOUT = "embed"


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
      embed = discord.Embed(
          title=f"💛 {v['name']}", description=v["desc"], color=0xFFD400
      )
      embed.set_footer(text="LUA STUDIO ON TOP | IM TOO GOOD")
      load = v["loadstring"]

      if FIND_LAYOUT == "split":
        await interaction.response.send_message(embed=embed)
        await interaction.followup.send(
            f"**📱 Mobile 1-tap:**\n`{load}`\n\n**💻 PC / Normal:**\n```lua\n{load}\n```"
        )
      else:
        embed.add_field(
            name="📱 Mobile 1-tap", value=f"`{load}`", inline=False
        )
        embed.add_field(
            name="💻 PC / Normal", value=f"```lua\n{load}\n```", inline=False
        )
        await interaction.response.send_message(embed=embed)
      return

  await interaction.response.send_message(
      "❌ Not found. Try `/list`", ephemeral=True
  )


@bot.tree.command(name="list", description="List all available scripts")
async def list_s(interaction: discord.Interaction):
  embed = discord.Embed(
      title="LUA STUDIO - ALL SCRIPTS",
      color=0xFFD400
  )
  
  content_lines = ["Use `/find <name>` - No more scrolling 20 channels\n"]
  for k, v in SCRIPTS.items():
      content_lines.append(f"**{v['name'].upper()}**\n`/find {k}` - {v['desc']}")
      
  embed.description = "\n\n".join(content_lines)
  embed.set_footer(text="Yellow & Black | Pixel Logo | Fade-In")
  
  await interaction.response.send_message(embed=embed)


@bot.tree.command(name="add", description="Add a new script (Admin only)")
@app_commands.describe(
    key="Unique short key (e.g., duels)",
    name="Display name of the script",
    desc="Short description",
    loadstring="The full lua loadstring",
)
async def add_script(
    interaction: discord.Interaction,
    key: str,
    name: str,
    desc: str,
    loadstring: str,
):
  if not interaction.user.guild_permissions.administrator:
    await interaction.response.send_message(
        "❌ You need **Administrator** permissions to use this command.",
        ephemeral=True,
    )
    return

  key_clean = key.lower()
  SCRIPTS[key_clean] = {"name": name, "desc": desc, "loadstring": loadstring}
  
  embed = discord.Embed(
      title="✅ SCRIPT ADDED",
      description=f"**{name.upper()}** added as `{key_clean}`\n\n**Loadstring**\n```lua\n{loadstring}\n```",
      color=0x57F287
  )
  await interaction.response.send_message(embed=embed)


@bot.tree.command(name="delete", description="Delete an existing script (Admin only)")
@app_commands.describe(key="The key of the script you want to delete")
async def delete_script(interaction: discord.Interaction, key: str):
  if not interaction.user.guild_permissions.administrator:
    await interaction.response.send_message(
        "❌ You need **Administrator** permissions to use this command.",
        ephemeral=True,
    )
    return

  key_clean = key.lower()
  if key_clean in SCRIPTS:
    del SCRIPTS[key_clean]
    await interaction.response.send_message(
        f"🗑️ Successfully deleted script: `{key_clean}`"
    )
  else:
    await interaction.response.send_message(
        f"❌ Script `{key_clean}` not found.", ephemeral=True
    )


@bot.tree.command(
    name="say", description="Make the bot say a message (Admin only)"
)
@app_commands.describe(message="The message you want the bot to post")
async def say(interaction: discord.Interaction, message: str):
  if not interaction.user.guild_permissions.administrator:
    await interaction.response.send_message(
        "❌ You need **Administrator** permissions to use this command.",
        ephemeral=True,
    )
    return

  await interaction.response.send_message("✅ Message sent!", ephemeral=True)
  await interaction.channel.send(message)


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
