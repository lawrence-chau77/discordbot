import discord
import os
import requests
import json 
import random 
import giphy_client
from giphy_client.rest import ApiException
from replit import db

client = discord.Client()

# list of songs for $song event 
starter_song_list = [
  "https://www.youtube.com/watch?v=dNCWe_6HAM8",
  "https://youtu.be/D9G1VOjN_84",
  "https://www.youtube.com/watch?v=UTHLKHL_whs",
  "https://www.youtube.com/watch?v=xfeys7Jfnx8",
  "https://www.youtube.com/watch?v=Jg9NbDizoPM",
  "https://www.youtube.com/watch?v=czftJ7E7wa4",
  "https://www.youtube.com/watch?v=dlFA0Zq1k2A"
]

coin_flip = ['heads', 'tails']

# gets a random quote from zenquotes for event $inspire
def get_quote():
  # requests data from zenquotes api into response
  response = requests.get("https://zenquotes.io/api/random")
  # convert to json 
  json_data = json.loads(response.text)
  # format the json data 
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

# adds a user inputted song link to the list of song links for $song
def update_songlist(song):
  # check if its a youtube link
  if song.startswith("https://www.youtube.com/"):
    r = requests.get(song)
    # checks if its a valid youtube link
    if "Video unavailable" in r.text:
      return 0 
    # if valid it adds the song link to song_list
    if "song_list" in db.keys():
      song_list = db['song_list']
      song_list.append(song)
      db['song_list'] = song_list
    else:
      db['song_list'] = [song]
  # if invalid return 0 
  else:
    return 0 
         
  
  
@client.event
async def on_ready():
    # Bot is ready to be used calls this 
    print('We have logged in as {0.user}'.format(client))

@client.event
# event triggers everytime a message is received
async def on_message(message):
  # if message sent by itself just return 
  if message.author == client.user:
        return
  # if user inputs $hello sends 'Hello!' back 
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')
    
  # if user inputs $coinflip returns random choice of heads or tails
  if message.content.startswith('$coinflip'):
    await message.channel.send(random.choice(coin_flip))
    
  # if user has inputted song adds it to list of options for $song 
  options = starter_song_list
  if "song_list" in db.keys():
    options = options + list(db['song_list'])

  # user inputs new song link for $song
  if message.content.startswith('$newsong'):
    # get the song link from command
    song = message.content.split("$newsong ", 1)[1]
    if update_songlist(song) == 0:
      await message.channel.send("Invalid link")
    else:
      await message.channel.send("New song link added")

  if message.content.startswith('$gif'):
    # split the search word from command 
    search = message.content.split('$gif ', 1)[1]
    # api key from giphy 
    api_key = 'oRHr4zJyx1iZYVS1QhHKFI6K4HFm9311'
    api_instance = giphy_client.DefaultApi()

    try:
      api_response = api_instance.gifs_search_get(api_key, search, limit=30, rating='g') 
      # turn 10 gifs into list
      gif_list = list(api_response.data)
      # pick a random gif 
      c_gif = random.choice(gif_list)
      # send embed url 
      await message.channel.send(c_gif.embed_url)

    except ApiException as e:
      print("Exception when calling $gif")
  # sends a random song link from user inputted songs + starter list 
  if message.content.startswith('$song'):
    await message.channel.send(random.choice(options))
    
  if message.content.startswith('$inspire'):
    quote = get_quote()
    # send quote from get_quote function 
    await message.channel.send(quote)

client.run(os.getenv('TOKEN'))
