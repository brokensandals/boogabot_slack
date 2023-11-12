#!/usr/bin/env python3

import os
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
BOOGA_API_URL = os.environ.get("BOOGA_API_URL")

app = App(token=BOT_TOKEN)

# TODO retrieve history from slack
class BoogaContext:
    def __init__(self):
        self.histories = {}
    
    def get_history(self, channel_id):
        if channel_id in self.histories:
            return self.histories[channel_id]
        return []

    def add_slack_message(self, message):
        channel_id = message["channel"]
        if channel_id not in self.histories:
            self.histories[channel_id] = []
        if message["text"].lower() == "reset":
            self.histories[channel_id] = []
        else:
            self.histories[channel_id].append({"role": "user", "content": message["text"]})
    
    def add_generated(self, channel_id, content):
        if channel_id not in self.histories:
            self.histories[channel_id] = []
        self.histories[channel_id].append({"role": "assistant", "content": content})

CONTEXT = BoogaContext()

class BoogaClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def generate(self, history):
        headers = {"Content-Type": "application/json"}
        url = f"{self.base_url}/v1/chat/completions"
        req = {"mode": "chat", "messages": history}
        resp = requests.post(url, headers=headers, json=req)
        return resp.json()["choices"][0]["message"]["content"]


BOOGA_CLIENT = BoogaClient(BOOGA_API_URL)


@app.message()
def handle_message(message, say):
    CONTEXT.add_slack_message(message)
    booga_hist = CONTEXT.get_history(message["channel"])
    if booga_hist:
        generated = BOOGA_CLIENT.generate(booga_hist)
        say(generated)
        CONTEXT.add_generated(message["channel"], generated)

if __name__ == "__main__":
    SocketModeHandler(app, APP_TOKEN).start()
