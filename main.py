# Import because of french stuff lol
from ftfy import fix_text
import matplotlib.pyplot as plt
import os
import wordcloud
import json

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
def getMessages(data):
    messages = data["messages"]
    for i in range(len(messages)):
        if "content" in messages[i].keys():
            sender = fix_text(messages[i].get("sender_name"))
            content = fix_text(messages[i].get("content"))
            if "http" in content:
                # Skip if there is an HTTP link, TODO: change to just remove the link
                continue
            text[sender] += content + " "
                
            

# Iterate through all the .json in the dir that it's run
for filename in os.listdir("."):
    if filename.endswith(".json"): 
        data = parseJson(filename)
        if not bool(text):
            getParticipants(data)
        getMessages(data)
        print(text["Felix Rouleau"])
        