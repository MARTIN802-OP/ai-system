const API_URL = "http://127.0.0.1:8000";


// =========================================================
// SYSTEM STATUS
// =========================================================

async function loadSystemStatus() {

    try {

        const res = await fetch(`${API_URL}/system-status`);
        const data = await res.json();

        document.getElementById("agents-count").innerText = data.agents.length;
        document.getElementById("tasks-count").innerText = data.task_count || 0;
        document.getElementById("system-status").innerText = data.status;

        let html = "";

        data.agents.forEach(a => {
            html += `<div class="alert alert-info">${a}</div>`;
        });

        document.getElementById("agents-list").innerHTML = html;

    } catch (e) {
        console.error(e);
    }
}

loadSystemStatus();


// =========================================================
// SEND MESSAGE (FIXED)
// =========================================================

async function sendMessage() {

    const sender = document.getElementById("sender").value.trim();
    const receiver = document.getElementById("receiver").value.trim();
    const task = document.getElementById("task").value.trim();
    const content = document.getElementById("message").value.trim();

    // ❌ VALIDATION
    if (!sender || !receiver || !content) {
        alert("Remplis sender / receiver / message");
        return;
    }

    const response = await fetch(`${API_URL}/send-message`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            sender,
            receiver,
            task,
            content
        })
    });

    const data = await response.json();

    console.log("Message sent:", data);

    loadMessages(receiver);
}


// =========================================================
// LOAD MESSAGES (OPTIONAL REST)
// =========================================================

async function loadMessages(agent) {

    const res = await fetch(`${API_URL}/messages/${agent}`);
    const data = await res.json();

    let html = "";

    data.messages.forEach(m => {

        html += `
        <div class="chat-message">
            <b>${m.sender}</b> → <b>${m.receiver}</b>
            <br>
            <small>${m.task}</small>
            <p>${m.content}</p>
        </div>`;
    });

    document.getElementById("chat-box").innerHTML = html;
}


// =========================================================
// WEBSOCKET (REAL FIX)
// =========================================================

const socket = new WebSocket("ws://127.0.0.1:8000/ws");

socket.onopen = () => {
    console.log("WebSocket OK");
};

socket.onmessage = (event) => {

    const box = document.getElementById("chat-box");

    const div = document.createElement("div");
    div.className = "chat-message";

    div.innerText = event.data;

    box.appendChild(div);
};

socket.onerror = (e) => console.error("WS ERROR", e);
socket.onclose = () => console.log("WS CLOSED");