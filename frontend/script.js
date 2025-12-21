const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatContainer = document.getElementById('chat-container');

// Backend API URL (assuming default FastAPI port)
const API_URL = 'http://127.0.0.1:8000/ask';

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message
    addMessage(message, 'user');
    userInput.value = '';

    // Show loading indicator
    const loadingId = showLoading();

    try {
        const response = await fetch(`${API_URL}?q=${encodeURIComponent(message)}`);
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();

        // Remove loading and add AI response
        removeLoading(loadingId);

        let answerText = data.answer;
        if (typeof answerText === 'object') {
            console.warn('Received object as answer:', answerText);
            answerText = JSON.stringify(answerText, null, 2);
        }

        addMessage(answerText, 'ai');
    } catch (error) {
        console.error('Error:', error);
        removeLoading(loadingId);
        addMessage('죄송합니다. 오류가 발생했습니다. 잠시 후 다시 시도해주세요.', 'ai');
    }
});

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    contentDiv.textContent = text;

    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showLoading() {
    const id = 'loading-' + Date.now();
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('typing-indicator');
    loadingDiv.id = id;

    loadingDiv.innerHTML = `
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    `;

    chatContainer.appendChild(loadingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return id;
}

function removeLoading(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}
