const API_URL = 'http://localhost:8000';

// Elements
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const uploadStatus = document.getElementById('uploadStatus');
const totalChunks = document.getElementById('totalChunks');
const clearBtn = document.getElementById('clearBtn');
const chatMessages = document.getElementById('chatMessages');
const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');

// Load stats on page load
loadStats();

// Upload documents
uploadBtn.addEventListener('click', async () => {
    const files = fileInput.files;
    
    if (files.length === 0) {
        showStatus('Please select files to upload', 'warning');
        return;
    }
    
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Processing...';
    
    let successCount = 0;
    let totalChunksAdded = 0;
    
    for (let file of files) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                successCount++;
                totalChunksAdded += data.chunks_added;
            }
        } catch (error) {
            console.error('Upload error:', error);
        }
    }
    
    showStatus(`✅ Uploaded ${successCount}/${files.length} files (${totalChunksAdded} chunks)`, 'success');
    uploadBtn.disabled = false;
    uploadBtn.textContent = 'Upload & Process';
    fileInput.value = '';
    
    loadStats();
});

// Ask question
askBtn.addEventListener('click', askQuestion);
questionInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') askQuestion();
});

async function askQuestion() {
    const question = questionInput.value.trim();
    
    if (!question) return;
    
    // Add user message
    addMessage(question, 'user');
    questionInput.value = '';
    
    // Show loading
    const loadingId = addMessage('Thinking...', 'assistant', true);
    
    try {
        const response = await fetch(`${API_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                n_results: 3
            })
        });
        
        const data = await response.json();
        
        // Remove loading message
        document.getElementById(loadingId).remove();
        
        // Add answer
        let answerHTML = `<strong>Answer:</strong><br>${data.answer}`;
        
        if (data.sources && data.sources.length > 0) {
            answerHTML += '<br><br><strong>📚 Sources:</strong><br>';
            data.sources.forEach((source, i) => {
                answerHTML += `<small><em>${i+1}. ${source.source}</em></small><br>`;
            });
        }
        
        addMessage(answerHTML, 'assistant');
        
    } catch (error) {
        document.getElementById(loadingId).remove();
        addMessage('❌ Error: Could not get answer. Make sure backend is running.', 'assistant');
        console.error('Query error:', error);
    }
}

// Load database stats
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        const data = await response.json();
        totalChunks.textContent = data.total_chunks;
    } catch (error) {
        console.error('Stats error:', error);
    }
}

// Clear database
clearBtn.addEventListener('click', async () => {
    if (!confirm('Are you sure you want to clear all documents?')) return;
    
    try {
        await fetch(`${API_URL}/clear`, { method: 'DELETE' });
        showStatus('Database cleared!', 'success');
        chatMessages.innerHTML = '<div class="alert alert-info">Upload documents and ask questions to get started!</div>';
        loadStats();
    } catch (error) {
        showStatus('Error clearing database', 'danger');
    }
});

// Helper functions
function addMessage(content, role, isLoading = false) {
    const messageDiv = document.createElement('div');
    const id = 'msg_' + Date.now();
    messageDiv.id = id;
    messageDiv.className = `mb-3 ${role === 'user' ? 'text-end' : ''}`;
    
    const bubble = document.createElement('div');
    bubble.className = `d-inline-block p-3 rounded ${role === 'user' ? 'bg-primary text-white' : 'bg-light'}`;
    bubble.style.maxWidth = '80%';
    
    if (isLoading) {
        bubble.innerHTML = '<div class="spinner-border spinner-border-sm" role="status"></div> ' + content;
    } else {
        bubble.innerHTML = content;
    }
    
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    return id;
}

function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `alert alert-${type}`;
    uploadStatus.style.display = 'block';
    
    setTimeout(() => {
        uploadStatus.style.display = 'none';
    }, 5000);
}