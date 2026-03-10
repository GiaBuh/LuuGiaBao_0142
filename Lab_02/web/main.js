const BASE_URL = '/api';

async function processCipher(cipherName, action) {
    const plainTextElem = document.getElementById('input-text');
    const cipherTextElem = document.getElementById('output-text');
    const keyElem = document.getElementById('key');

    if (!plainTextElem.value.trim() || !keyElem.value.trim()) {
        alert("Please enter both text and a key.");
        return;
    }

    // Trigger Hacker Error Effect
    simulateHackerError();


    let keyStr = keyElem.value;
    let key;

    // Parse key type based on cipher
    if (cipherName === 'caesar' || cipherName === 'railfence' || cipherName === 'transposition') {
        key = parseInt(keyStr);
        if (isNaN(key)) {
            alert("Key must be an integer for this cipher.");
            return;
        }
    } else {
        key = keyStr;
    }

    let payload = { key: key };
    if (action === 'encrypt') {
        payload.plain_text = plainTextElem.value;
    } else {
        payload.cipher_text = plainTextElem.value;
    }

    try {
        const response = await fetch(`${BASE_URL}/${cipherName}/${action}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (action === 'encrypt') {
            cipherTextElem.value = data.encrypted_text || '';
        } else {
            cipherTextElem.value = data.decrypted_text || '';
        }

        if (cipherName === 'playfair') {
            loadPlayfairMatrix(key);
        }

    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Make sure your Python API is running!');
    }
}

async function loadPlayfairMatrix(key) {
    try {
        const response = await fetch(`${BASE_URL}/playfair/creatematrix`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ key: key })
        });
        const data = await response.json();
        const matrixContainer = document.getElementById('playfair-matrix');
        if (matrixContainer && data.playfair_matrix) {
            matrixContainer.innerHTML = '';
            data.playfair_matrix.forEach(row => {
                row.forEach(char => {
                    const cell = document.createElement('div');
                    cell.className = 'matrix-cell';
                    cell.textContent = char;
                    matrixContainer.appendChild(cell);
                });
            });
        }
    } catch (e) {
        console.error("Matrix load failed:", e);
    }
}

// Matrix Rain Effect
const canvas = document.getElementById('matrix-bg');
if (canvas) {
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const katakana = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレゲゼデベペオォコソトノホモヨョロゴゾドボポヴッン';
    const latin = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const nums = '0123456789';

    const alphabet = katakana + latin + nums;

    const fontSize = 16;
    const columns = canvas.width / fontSize;

    const rainDrops = [];

    for (let x = 0; x < columns; x++) {
        rainDrops[x] = 1;
    }

    const draw = () => {
        ctx.fillStyle = 'rgba(11, 15, 25, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#00ff88';
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < rainDrops.length; i++) {
            const text = alphabet.charAt(Math.floor(Math.random() * alphabet.length));
            ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);

            if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                rainDrops[i] = 0;
            }
            rainDrops[i]++;
        }
    };

    setInterval(draw, 30);

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// Hacker Error Popup Effect
function simulateHackerError() {
    const duration = 2000;
    const intervalTime = 50;
    let ellapsed = 0;

    const popupInterval = setInterval(() => {
        createErrorPopup();
        ellapsed += intervalTime;
        if (ellapsed >= duration) {
            clearInterval(popupInterval);
            removeAllPopups();
        }
    }, intervalTime);
}

function createErrorPopup() {
    const popup = document.createElement('div');
    popup.className = 'hacker-popup';

    popup.innerHTML = `
        <div class="hacker-popup-header">
            <span>Error</span>
            <button class="hacker-popup-close">X</button>
        </div>
        <div class="hacker-popup-body">
            <div class="hacker-popup-icon">⚠️</div>
            <div class="hacker-popup-message">Critical error</div>
        </div>
        <div class="hacker-popup-footer">
            <button class="hacker-popup-btn">OK</button>
        </div>
    `;

    // Random position
    const maxWidth = window.innerWidth - 300;
    const maxHeight = window.innerHeight - 150;
    const left = Math.floor(Math.random() * maxWidth);
    const top = Math.floor(Math.random() * maxHeight);

    popup.style.left = `${left}px`;
    popup.style.top = `${top}px`;

    document.body.appendChild(popup);
}

function removeAllPopups() {
    const popups = document.querySelectorAll('.hacker-popup');
    popups.forEach(p => p.remove());
}
