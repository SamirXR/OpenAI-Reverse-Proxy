from replit import db
import discord
from discord.ext import commands
import os
from datetime import datetime, timedelta

import random
import string

intents = discord.Intents.all()
bot = discord.Bot(command_prefix="!", intents=intents)

def get_key_by_discord_id(discord_id):
  if discord_id in db:
    return db[discord_id]["nyxkey"]
  else:
    return None

@bot.slash_command(name="generate_key", description="Generates a new API key")
async def generate_key(ctx):
    await ctx.defer(ephemeral=True)
    key = 'nx-' + ''.join(random.choices(string.ascii_letters + string.digits, k=35))
    if get_key_by_discord_id(str(ctx.author.id)):
        await ctx.respond('You already have an API key.')
    else:
        try:
            newkeydata = {
                "nyxkey": key,
                "requests": 0,
                "reset_time": str(datetime.now().isoformat())
            }
            db[str(ctx.author.id)] = newkeydata
            await ctx.respond(f'{ctx.author.mention}, your API key is: {key}')
        except Exception as e:
            await ctx.respond(f'Error generating key: {str(e)}')

@bot.slash_command(name="regenerate_key", description="Regenerates your API key")
async def regenerate_key(ctx):
    await ctx.defer(ephemeral=True)
    try:
        key = 'nx-' + ''.join(random.choices(string.ascii_letters + string.digits, k=35))
        newkeydata = {
            "nyxkey": key,
            "requests": 0,
            "reset_time": str(datetime.now().isoformat())
        }
        db[str(ctx.author.id)] = newkeydata
        await ctx.respond(f'{ctx.author.mention}, your new API key is: {key}')
    except Exception as e:
        await ctx.respond(f'Error regenerating key: {str(e)}')

@bot.slash_command(name="key", description="Retrieves your API key")
async def key(ctx):
    await ctx.defer(ephemeral=True)
    try:
        key_data = get_key_by_discord_id(str(ctx.author.id))
        if key_data:
            await ctx.respond(f'{ctx.author.mention}, your API key is: {key_data}')
        else:
            await ctx.respond('You do not have an API key. Please generate one using the generate_key command.')
    except Exception as e:
        await ctx.respond(f'Error fetching key: {str(e)}')

@bot.slash_command(name="usage", description="Shows the usage of your API key")
async def usage(ctx):
    await ctx.defer(ephemeral=True)
    try:
        key_data = db[str(ctx.author.id)]
        if key_data:
            requests = key_data["requests"]
            reset_time = datetime.fromisoformat(key_data["reset_time"])
            if datetime.now() - reset_time > timedelta(days=1):
                requests = 0
                reset_time = datetime.now().isoformat()
                key_data["requests"] = requests
                key_data["reset_time"] = reset_time
                db[str(ctx.author.id)] = key_data
            await ctx.respond(f'{ctx.author.mention}, your API key usage is: {requests}/600')
        else:
            await ctx.respond('You do not have an API key. Please generate one using the generate_key command.')
    except Exception as e:
        await ctx.respond(f'Error fetching usage: {str(e)}')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Made by NyX AI"))

@bot.event
async def on_member_remove(member):
    if str(member.id) in db:
        del db[str(member.id)]

@bot.slash_command(name="example-python", description="Shows an example of Python code for OpenAI")
async def example_python(ctx):
    try:
        code = """
# Non Streaming 
```py
from openai import OpenAI

client = OpenAI(api_key="/generate-key", base_url="https://nyx-api.samirawm7.repl.co/openai")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
)

print(completion.choices[0].message.content)```
"""
        await ctx.respond(code)
    except Exception as e:
        await ctx.respond(f'Error fetching code: {str(e)}')


@bot.slash_command(name="example-curl", description="Shows an example of cURL code for OpenAI")
async def example_pythonnnnn(ctx):
    try:
        code = """
# cURL 
```c
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_API_KEY" \
-d '{
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "user", "content": "Hey! How Are you?"}
  ]
}' https://nyx-api.samirawm7.repl.co/openai/chat/completions
```
"""
        await ctx.respond(code)
    except Exception as e:
        await ctx.respond(f'Error fetching code: {str(e)}')

@bot.slash_command(name="example-python-stream", description="Shows an example of Python code for OpenAI Streaming")
async def example_pythonnnn(ctx):
    try:
        code = """
# Streaming       
```py
from openai import OpenAI

client = OpenAI(api_key="/generate-key", base_url="https://nyx-api.samirawm7.repl.co/openai")

stream = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": "Hey! How Are you?"}],
  stream=True,
)
for part in stream:
  print(part.choices[0].delta.content or "")```
"""
        await ctx.respond(code)
    except Exception as e:
        await ctx.respond(f'Error fetching code: {str(e)}')

@bot.slash_command(name="example-javascript", description="Shows an example of JavaScript code for OpenAI")
async def example_javascript(ctx):
    try:
        code = """
# JavaScript 
```js
const axios = require('axios');

const apiKey = '/generate-key';
const apiUrl = 'https://nyx-api.samirawm7.repl.co/openai';
const model = 'gpt-3.5-turbo';

const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${apiKey}`
};

const data = {
  model: model,
  messages: [
    { role: 'user', content: 'Hey! How Are you?' }
  ]
};

axios.post(`${apiUrl}/chat/completions`, data, { headers: headers })
  .then(response => {
    const responseDataString = JSON.stringify(response.data, null, 2);
    console.log(responseDataString);
  })
  .catch(error => {
    console.error(`Error: ${error.response.status}, ${error.response.data}`);
  });
```
"""
        await ctx.respond(code)
    except Exception as e:
        await ctx.respond(f'Error fetching code: {str(e)}')

@bot.slash_command(name="api-information", description="Returns the NyX AI's Information")
async def website(ctx):
    nyx_website = "https://nyx-ai.glitch.me"
    base_url = "https://nyx-api.samirawm7.repl.co/openai"
    discord_invite = "https://discord.gg/rdC7xYvrxu"
    completion_url = "https://nyx-api.samirawm7.repl.co/openai/chat/completion"
    roleplay_url = "https://nyx-chat.samirawm7.repl.co"
    donation_url = "https://www.buymeacoffee.com/samir.xr"
    github_url = "https://github.com/SamirXR"
    models_url = "https://nyx-api.samirawm7.repl.co/openai/models"

    embed = discord.Embed(title="NyX AI Information", color=discord.Color.default())

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1162893971983437976/1173603370498523147/okkkk.png")
    embed.add_field(name="NyX Website", value=nyx_website, inline=False)
    embed.add_field(name="Roleplay URL", value=roleplay_url, inline=False)
    embed.add_field(name="Base URL", value=base_url, inline=False)
    embed.add_field(name="Discord Invite", value=discord_invite, inline=False)
    embed.add_field(name="Completion URL", value=completion_url, inline=False)
    embed.add_field(name="Donation Link", value=donation_url, inline=False)
    embed.add_field(name="GitHub", value=github_url, inline=False)
    embed.add_field(name="Models", value=models_url, inline=False)
    embed.set_footer(text=f"Requested By {ctx.author.name}")  # Adjust size as needed
    await ctx.respond(embed=embed)



@bot.slash_command(name="usage-information", description="Shows the Information about Daily usage")
async def example_pythonnnnnnnnnnnnn(ctx):
    try:
        code = """
# Daily Usage

You get 600 Credits/Day

Each Request costs 3 (600/3 = 200)

There is No GPT-4 in Api, but Don't worry, There's @NyX DM This Bot you get 50/Day Requests after that it fall backs to Mistral-7b (200 Requests/Day)

Therefore Total Requests Per day 200 (API ) +200+50 (BOT) = 450 & Unlimited Requests with Roleplay Site.
"""
        await ctx.respond(code)
    except Exception as e:
        await ctx.respond(f'Error fetching code: {str(e)}')

@bot.slash_command(name="model-information", description="Shows the Information about NyX Models")
async def example_pythonnnnnnnnnnnnnnn(ctx):
    try:
        code = """
        
# GPT Models  (5/Request)
gpt-3.5-turbo-1106
gpt-3.5-turbo
gpt-3.5-turbo-0613
gpt-3.5-turbo-0301
"""
        await ctx.respond(code)
    except Exception as e:
        await ctx.respond(f'Error fetching code: {str(e)}')


bot.run(os.getenv('DISCORD_TOKEN'))
