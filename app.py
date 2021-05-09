import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
from pprint import pprint
import slack_token
from flask import Flask, render_template, request, jsonify


# WebClient insantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=slack_token.token)

# Store conversation history
conversation_history = []
# ID of the channel you want to send the message to
channel_id = "CLN89A4S0"  # photo 채널

try:
    # Call the conversations.history method using the WebClient
    # conversations.history returns the first 100 messages by default
    # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
    result = client.conversations_history(channel=channel_id, limit=1)

    conversation_history = result["messages"]

    # Print results
    logging.info("{} messages found in {}".format(
        len(conversation_history), id))


except SlackApiError as e:
    logging.error("Error creating conversation: {}".format(e))


app = Flask(__name__)

logging.basicConfig(filename="logs/project.log", level=logging.DEBUG)
application = Flask(__name__)

text = conversation_history[0]['text']
img_url = conversation_history[0]['files'][0]['url_private']


@app.route('/')
def landing_page():
    text = conversation_history[0]['text']
    img_url = conversation_history[0]['files'][0]['url_private']
    return render_template('index.html', text=text, img_url=img_url, token=slack_token.token)


@app.route('/test')
def test_page():
    # img_url = conversation_history[0]['files'][0]['url_private']
    return img_url


@app.route('/jy')
def jy_page():
    return '진영입니다'


if __name__ == "__main__":
    application.run(host="0.0.0.0", debug=True)
