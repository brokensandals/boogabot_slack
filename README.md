If you're self-hosting an LLM using the [oobabooga text-generation-webui](https://github.com/oobabooga/text-generation-webui), this app lets you chat with it via Slack.

Currently, this is a very lazy, hacky, barebones implementation. Maybe I'll improve it, maybe not.

# Assumptions

- You have text-generation-webui running.
- You have its new OpenAI-compatible API enabled.

# Setup

- Create a Slack app and add it to your workspace. See Slack's [Getting started with Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started) guide for help (the parts of it that _don't_ involve writing code). Make sure to turn on Socket Mode, turn on the ability for users to DM the app, and have it listen for `message.im` events.

- Ensure that you have python installed (preferably the version listed in the `.python-version` file).

- Clone this repository.

- Install dependencies: `pip install -r requirements.txt`

- Set the `BOOGA_API_URL`, `SLACK_APP_TOKEN`, and `SLACK_BOT_TOKEN` environment variables (see `.env.example`).

- Run: `./app.py`

# Usage

- If you message the bot, it will send your text - and all previous text in the conversation - to oobabooga, and reply with whatever text is generated.
- If you send a message containing just the text `reset`, earlier messages will be excluded from the prompt.
- Currently—due to my aforementioned extreme laziness—history is just stored in memory. This means the bot will forget everything all previous context if you restart it, even though the old messages are still there in Slack. And its memory usage can grow unboundedly if you never send `reset` messages.
