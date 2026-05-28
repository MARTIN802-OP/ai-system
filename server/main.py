from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import subprocess
import os
import uuid
from typing import List

from communication.task_queue import queue
from agents.language_agent import language_agent


# =========================================================
# APP (DOIT ÊTRE EN PREMIER)
# =========================================================

app = FastAPI(
    title="AI SYSTEM",
    description="Autonomous Multi-Agent AI System",
    version="3.0"
)

# =========================================================
# CORS (IMPORTANT POUR TON FRONTEND HTML)
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# MESSAGE BUS
# =========================================================

class MessageBus:

    def __init__(self):
        self.messages = []

    def send_message(self, sender, receiver, task, content):

        message = {
            "id": str(uuid.uuid4()),
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

        return [
            msg for msg in self.messages
            if msg["receiver"] == receiver
        ]


bus = MessageBus()


# =========================================================
# MODELS
# =========================================================

class CommandRequest(BaseModel):
    command: str
    cwd: str


class FileRequest(BaseModel):
    path: str
    content: str


class ReadFileRequest(BaseModel):
    path: str


class ImageRequest(BaseModel):
    prompt: str


class AgentMessage(BaseModel):
    sender: str
    receiver: str
    task: str
    content: str


class TaskRequest(BaseModel):
    title: str
    agent: str
    payload: str
    priority: str = "normal"


class TaskUpdate(BaseModel):
    task_id: str
    status: str


class LanguageRequest(BaseModel):
    text: str


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def home():
    return {
        "status": "AI SYSTEM RUNNING",
        "version": "3.0"
    }


# =========================================================
# SYSTEM STATUS
# =========================================================

@app.get("/system-status")
def system_status():
    return {
        "status": "online",
        "version": "3.0",
        "agents": [
            "Orchestrator AI",
            "Research Agent",
            "Planning Agent",
            "Memory Agent",
            "Code Agent",
            "Debug Agent",
            "DevOps Agent",
            "Image Agent",
            "Universal Language Agent"
        ],
        "message_count": len(bus.messages),
        "task_count": len(queue.tasks)
    }


# =========================================================
# SEND MESSAGE (IMPORTANT POUR TON FRONTEND)
# =========================================================

@app.post("/send-message")
def send_message(data: AgentMessage):

    return bus.send_message(
        sender=data.sender,
        receiver=data.receiver,
        task=data.task,
        content=data.content
    )


# =========================================================
# GET MESSAGES
# =========================================================

@app.get("/messages/{agent}")
def get_messages(agent: str):

    return {
        "agent": agent,
        "messages": bus.get_messages(agent)
    }


# =========================================================
# LANGUAGE DETECTION (AGENT MULTI-LANGUE)
# =========================================================

@app.post("/detect-language")
def detect_language(data: LanguageRequest):

    return language_agent.detect_language(data.text)


# =========================================================
# TASK SYSTEM
# =========================================================

@app.post("/create-task")
def create_task(data: TaskRequest):

    task = queue.create_task(
        title=data.title,
        agent=data.agent,
        payload=data.payload,
        priority=data.priority
    )

    return {"success": True, "task": task}


@app.get("/tasks/{agent}")
def get_tasks(agent: str):

    return {
        "agent": agent,
        "tasks": queue.get_tasks(agent)
    }


@app.post("/update-task")
def update_task(data: TaskUpdate):

    return {
        "success": True,
        "task": queue.update_task(
            task_id=data.task_id,
            status=data.status
        )
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():
    return {"healthy": True}


# =========================================================
# STARTUP
# =========================================================

@app.on_event("startup")
def startup_event():

    print("\n======================================")
    print("AI SYSTEM STARTED")
    print("Version 3.0")
    print("MULTI-LANGUAGE SUPPORT ENABLED")
    print("======================================\n")