import os
import json
import random
from datetime import datetime, timezone
from dotenv import load_dotenv
import discord
import asyncio

# Load environment variables
load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')  # Bot token from the Discord Developer Portal
channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))  # Channel ID where the bot will post the message

def load_json_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}.")
        exit(1)

def save_json_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Load environment variables
load_dotenv()

# Load questions and used questions
questions = load_json_file('questionsList.json').get('questions', [])
used_questions = load_json_file('usedQuestions.json')

# If all questions have been used, reset the used questions
if len(used_questions) >= len(questions):
    used_questions = []

# Choose a question not in used questions
random_question = random.choice([q for q in questions if q not in used_questions])
used_questions.append(random_question)
save_json_file('usedQuestions.json', used_questions)

# Create an embed for the message
embed = discord.Embed(
    title="Question of the Day",
    description=random_question,
    color=0x00ff00,
    timestamp=datetime.now(timezone.utc)
)
embed.set_footer(text="Alex's QOTD Bot")

# Define the required intents
intents = discord.Intents.default()

# Discord client with intents
client = discord.Client(intents=intents)

async def post_question():
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    await channel.send(embed=embed)
    await client.close()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await post_question()

client.run(bot_token)

