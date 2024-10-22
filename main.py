import discord
import aiohttp
import json

token = 'TOKEN'
channel_id = CHANNEL ID
aiurl = "http://localhost:11434/api/generate"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

async def ask_ai(message):
    global actual_response
    prompt = str(message.content)
    data = {
        "model": "mistral",
        "stream": False,
        "prompt": prompt
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(aiurl, headers={"Content-Type": "application/json"}, json=data) as response:
            if response.status == 200:
                response_text = await response.text()
                data = json.loads(response_text)
                actual_response = data["response"]
            else:
                actual_response = "Error: Request failed with status code {response.status}"
            return actual_response

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_message_author = None

    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        if message.channel.id == channel_id and message.author != self.user:
            print(f'Message from {message.author}: {message.content}')
            print("Requesting response...")
            headers = {
                "Authorization": f"Bot {token}",
                "Content-Type": "application/json"
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(f"https://discord.com/api/v10/channels/{channel_id}/typing", headers=headers) as response:
                    if response.status != 204:
                        print(f"Error: Request failed with status code {response.status}")

            actual_response = await ask_ai(message)

            await message.channel.send(actual_response)

            print("Response sent: " + actual_response)
            self.last_message_author = message.author

client = MyClient(intents=intents)
client.run(token)
