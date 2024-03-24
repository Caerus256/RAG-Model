function sendMessage() {
    var userInput = document.getElementById('user-input').value;
    if (userInput.trim() !== '') {
        appendMessage('You', userInput);
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: userInput })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('Bot', data.answer);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function appendMessage(sender, message) {
    var chatBox = document.getElementById('chat-box');
    var messageElement = document.createElement('p');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}
