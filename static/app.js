const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");

let sessionId = localStorage.getItem("weekend_buddy_session");

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  bubble.textContent = text;
  div.appendChild(bubble);
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
  const div = document.createElement("div");
  div.className = "message assistant";
  div.id = "typingIndicator";
  div.innerHTML = `
    <div class="typing-indicator">
      <span></span><span></span><span></span>
    </div>
  `;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTyping() {
  const el = document.getElementById("typingIndicator");
  if (el) el.remove();
}

function setLoading(loading) {
  sendButton.disabled = loading;
  messageInput.disabled = loading;
  if (!loading) messageInput.focus();
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  addMessage("user", message);
  messageInput.value = "";
  setLoading(true);
  showTyping();

  try {
    const resp = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        message: message,
      }),
    });

    if (!resp.ok) {
      throw new Error(`서버 오류: ${resp.status}`);
    }

    const data = await resp.json();
    sessionId = data.session_id;
    localStorage.setItem("weekend_buddy_session", sessionId);

    hideTyping();
    addMessage("assistant", data.reply);
  } catch (err) {
    hideTyping();
    addMessage("assistant", `죄송합니다. 오류가 발생했습니다: ${err.message}`);
  } finally {
    setLoading(false);
  }
});

messageInput.focus();
