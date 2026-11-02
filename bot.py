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
  try:
    # Sync slash commands with Discord so they appear instantly
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
      load = v["loadstring"]

      # Bundle mobile/PC code blocks and the embed into a single response call
      content = f"**📱 Mobile 1-tap:**\n`{load}`\n\n**💻 PC:**\n```lua\n{load}\n```"
      await interaction.response.send_message(content=content, embed=embed)
      return

  await interaction.response.send_message(
      "❌ Not found. Try `/list`", ephemeral=True
  )


@bot.tree.command(name="list", description="List all available scripts")
async def list_s(interaction: discord.Interaction):
  text = "**SCRIPTS**\n" + "\n".join(
      [f"`{k}` - {v['name']}" for k, v in SCRIPTS.items()]
  )
  await interaction.response.send_message(text)


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
  await interaction.response.send_message(
      f"✅ Successfully added script: `{key_clean}`"
  )


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
