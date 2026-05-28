from fastapi import WebSocket, WebSocketDisconnect
from typing import List


# =========================================================
# MESSAGE BUS (AGENTS COMMUNICATION)
# =========================================================

class MessageBus:

    def __init__(self):
        self.messages = []

    def send_message(self, sender, receiver, task, content):

        message = {
            "sender": sender,
            "receiver": receiver,
            "task": task,
            "content": content,
            "status": "pending"
        }

        self.messages.append(message)

        return {
            "status": "message_sent",
            "message": message
        }

    def get_messages(self, receiver):

        receiver_messages = []

        for msg in self.messages:

            if msg["receiver"] == receiver:
                receiver_messages.append(msg)

        return receiver_messages


bus = MessageBus()


# =========================================================
# WEBSOCKET CONNECTION MANAGER
# =========================================================

class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):

        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):

        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):

        await websocket.send_text(message)

    async def broadcast(self, message: str):

        for connection in self.active_connections:
            await connection.send_text(message)


ws_manager = ConnectionManager()


# =========================================================
# WEBSOCKET ENDPOINT
# =========================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await ws_manager.connect(websocket)

    try:

        while True:

            data = await websocket.receive_text()

            await ws_manager.broadcast(data)

    except WebSocketDisconnect:

        ws_manager.disconnect(websocket)