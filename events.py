from flask import Flask, request
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI, ConversationChain
from flask import Flask, request, render_template, jsonify
from urllib.request import urlopen
import json
import os
from dotenv import load_dotenv
load_dotenv()

os.getenv("OPENAI_API_KEY")

global convo, messages
app = Flask(__name__, template_folder='templates')


llm = OpenAI(temperature=0)
conversation = ConversationChain(
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory()
)


first_input = "Hi there! You are EventBot. Frontend events are sent to you and you will document them in a friendly human readable way."
convo = conversation.predict(input=first_input)
messages = []


@app.route("/")
def hello_world():
    return render_template('events.html')


@app.route("/summary", methods=["POST"])
def summary():
    data = request.get_json()
    events = data.get("events", [])
    # Do something with the events, such as logging them to the console

    prompt = "Please summarize the events that occurred in a conversational way. The events were: " + \
        str(events) + ". Match hovering and clicking events with the corresponding elements. Make the summary in list fashion."
    summary = conversation.predict(input=prompt)
    print(summary)
    return jsonify({'summary': summary})


if __name__ == '__main__':
    app.run(debug=True, PORT=os.getenv("PORT", default=5000))


