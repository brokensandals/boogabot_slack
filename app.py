#!/usr/bin/env python3

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

app = App(token=BOT_TOKEN)

if __name__ == "__main__":
    SocketModeHandler(app, APP_TOKEN).start()
