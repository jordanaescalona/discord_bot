import os
from flask import Flask
from discord.ext import commands
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

app = Flask(__name__)
bot = commands.Bot(command_prefix="!")

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

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.lower().startswith('hello'):
        await message.channel.send(f'¡Hello, {message.author.name}!Do you want me to tell you a joke?please type *!joke*')
    
    if message.content.lower().startswith('!joke'):
        joke = get_joke()
        await message.channel.send(joke)

@app.route('/')
def index():
    return "¡El bot de Discord está funcionando!"

if __name__ == "__main__":
    bot.loop.create_task(bot.start(TOKEN))
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))