import asyncio
import json
from quart import Quart, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Quart(__name__)
app.clients = []
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50))
    message = db.Column(db.Text)

    def __repr__(self):
        return f'{self.sender}: {self.message}'

class ServerSentEvent():
    def __init__(self, data, *, event=None, id=None, retry=None):
        self.data = data
        self.event = event
        self.id = id
        self.retry = retry

    def encode(self):
        message = f"data: {self.data}"
        if self.event is not None:
            message = f"{message}\nevent: {self.event}"
        if self.id is not None:
            message = f"{message}\nid: {self.id}"
        if self.retry is not None:
            message = f"{message}\nretry: {self.retry}"
        message = f"{message}\r\n\r\n"
        return message.encode('utf-8')

@app.route('/', methods=['GET'])
async def index():
    chats = Chat.query.all()
    return await render_template('chat.html', chats=chats)

@app.route('/submit', methods=['POST'])
async def submit_message():
    form = await request.form
    print(form.__dict__)
    sender = form['sender']
    message = form['message']
    new_chat = Chat(sender=sender, message=message)
    db.session.add(new_chat)
    db.session.commit()
    for queue in app.clients:
        await queue.put(json.dumps(
            {'sender':sender,'message':message}
        ))
    return 'true'

@app.route('/stream')
async def stream():
    queue = asyncio.Queue()
    app.clients.append(queue)
    async def send_events():
        while True:
            data = await queue.get()
            event = ServerSentEvent(data)
            yield event.encode()

    return send_events(), {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Transfer-Encoding': 'chunked',
    }


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

