const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const loading = document.getElementById('loading');

function addMessage(message, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showLoading(show) {
    loading.style.display = show ? 'block' : 'none';
    sendBtn.disabled = show;
    userInput.disabled = show;
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    addMessage(message, true);
    userInput.value = '';
    showLoading(true);
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        const data = await response.json();
        
        if (data.response) {
            addMessage(data.response, false);
        } else if (data.error) {
            addMessage('❌ Error: ' + data.error, false);
        }
    } catch (error) {
        addMessage('❌ Error: Failed to connect to the server', false);
    } finally {
        showLoading(false);
    }
}

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
