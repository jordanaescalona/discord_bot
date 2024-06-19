import os

import discord
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Configuración del cliente de Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


def get_joke():
    response = requests.get("https://v2.jokeapi.dev/joke/Any")
    if response.status_code == 200:
        joke_data = response.json()
        if joke_data['type'] == 'single':
            return joke_data['joke']
        else:
            return f"{joke_data['setup']} ... {joke_data['delivery']}"
    else:
        return "No pude encontrar un chiste en este momento, intenta más tarde."

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    
    if message.content.lower().startswith('hello'):
        await message.channel.send(f'¡Hello, {message.author.name}!Do you want me to tell you a joke?please type *!joke*')
    
    if message.content.lower().startswith('!joke'):
        joke = get_joke()
        await message.channel.send(joke)

# Iniciar el bot
client.run(TOKEN)