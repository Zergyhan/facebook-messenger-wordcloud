# Import because of french stuff lol
from ftfy import fix_text
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, STOPWORDS
from tqdm import tqdm
import json
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description="Create a wordcloud out of the .json that you receive from Facebook Messenger.")
parser.add_argument("-s", "--stopwords", default="", help="Words, seperated by space, which will be ignored when making the wordcloud. " 
                    "Can take a .txt as an input.")
args = parser.parse_args()
# Dict contains the text of each sender in a string, key being their name
text = {}

# Open the file with .json as extension and return the data
def parseJson(filename):
    with open(filename, 'r') as f: 
        data = json.load(f)
        return data
    
# Get the participants from the JSON file and make dicts out of it
def getParticipants(data):
    participants = data["participants"]
    for i in range(len(participants)):
        text[fix_text(participants[i]['name'])] = ""
        
# Get the messages data from the JSON, if there is a URL, then we drop it
# TODO: Only remove URL instead of dropping
def getMessages(data, filename):
    messages = data["messages"]
    for i in tqdm(range(len(messages)), desc=filename):
        if "content" in messages[i].keys():
            sender = fix_text(messages[i].get("sender_name"))
            content = fix_text(messages[i].get("content"))
            if ("http" or "attachment") in content:
                # Skip if there is an HTTP link, TODO: change to just remove the link
                continue
            text[sender] += content + " "

# Iterate through all the .json in the dir that it's run
for filename in os.listdir("."):
    if filename.endswith(".json"): 
        data = parseJson(filename)
        if not bool(text):
            getParticipants(data)
        getMessages(data, filename)

stopwordsNew = list(STOPWORDS)

for key in tqdm(text, desc = "WordCloud"):  
    wordcloud = WordCloud(width=3000, height=2000).generate(text[key])
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(key+'.png', bbox_inches = "tight", dpi=300)
    
print("Creating cumulative wordcloud")
fullWordCloud = WordCloud(width=3000, height=2000).generate("".join(text.values()))
plt.imshow(fullWordCloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("everyone.png", bbox_inches = "tight", dpi=300)