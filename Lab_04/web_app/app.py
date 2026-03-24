from flask import Flask, request, jsonify, render_template
import hashlib
import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA3_256
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

# --- SERVER STATE for AES-RSA Chat Simulation ---
server_state = {
    'is_running': False,
    'server_key': None,
    'clients': {},
    'server_logs': [],
    'global_messages': []
}

def aes_encrypt(key, text):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
    return base64.b64encode(cipher.iv + ciphertext).decode('utf-8')

def aes_decrypt(key, b64_text):
    data = base64.b64decode(b64_text)
    iv = data[:AES.block_size]
    ciphertext = data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

# ==================== AES + RSA Socket Chat Simulation ====================

@app.route('/api/chat/start_server', methods=['POST'])
def chat_start_server():
    server_state['is_running'] = True
    server_state['server_key'] = RSA.generate(2048)
    server_state['clients'] = {}
    server_state['server_logs'] = [
        "[SYSTEM] Server socket initialized.",
        "[SYSTEM] Server bound to localhost:12345 (listening)",
        "[SYSTEM] Generated Server RSA 2048-bit Key Pair."
    ]
    server_state['global_messages'] = []
    return jsonify({'success': True})

@app.route('/api/chat/add_client', methods=['POST'])
def chat_add_client():
    if not server_state['is_running']:
        return jsonify({'success': False, 'error': 'Server is not running'})
        
    client_id = f"Client {len(server_state['clients']) + 1}"
    
    # Simulate client generating RSA keys
    client_key = RSA.generate(2048)
    
    # Server generates AES session key for this client
    aes_key = get_random_bytes(16)
    
    # Save client state (simulate the client having the decrypted AES key)
    server_state['clients'][client_id] = {
        'aes_key': aes_key, 
        'rsa_pub': client_key.publickey().export_key().decode('utf-8')
    }
    
    server_state['server_logs'].append(f"[CONNECTION] Accepted from {client_id}")
    server_state['server_logs'].append(f"[KEY EXCHANGE] Sent AES session key (encrypted via RSA) to {client_id}")
    
    return jsonify({'success': True, 'client_id': client_id})

@app.route('/api/chat/send', methods=['POST'])
def chat_send():
    data = request.json
    sender_id = data.get('client_id')
    raw_msg = data.get('message')
    
    if sender_id not in server_state['clients']:
        return jsonify({'success': False, 'error': 'Unknown client'})
        
    sender_aes = server_state['clients'][sender_id]['aes_key']
    
    # 1. Client encrypts message
    encrypted_payload_by_sender = aes_encrypt(sender_aes, raw_msg)
    
    # 2. Server receives and decrypts
    try:
        decrypted_at_server = aes_decrypt(sender_aes, encrypted_payload_by_sender)
        server_state['server_logs'].append(f"[MESSAGE] Received from {sender_id}: {decrypted_at_server}")
        
        # 3. Server Broadcasts to all
        broadcast_record = {
            'from': sender_id,
            'raw': decrypted_at_server,
            'deliveries': {}
        }
        
        for cid, cinfo in server_state['clients'].items():
            # Encrypt the message with THIS specific client's AES key
            enc_for_c = aes_encrypt(cinfo['aes_key'], decrypted_at_server)
            broadcast_record['deliveries'][cid] = enc_for_c
            
        server_state['global_messages'].append(broadcast_record)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/chat/state', methods=['GET'])
def chat_state():
    return jsonify({
        'is_running': server_state['is_running'],
        'server_logs': server_state['server_logs'],
        'clients': list(server_state['clients'].keys()),
        'global_messages': server_state['global_messages']
    })

# ==================== Diffie-Hellman ====================
@app.route('/api/dh/simulate', methods=['GET'])
def dh_simulate():
    try:
        parameters = dh.generate_parameters(generator=2, key_size=512)
        alice_private_key = parameters.generate_private_key()
        alice_public_key = alice_private_key.public_key()
        bob_private_key = parameters.generate_private_key()
        bob_public_key = bob_private_key.public_key()
        alice_shared_secret = alice_private_key.exchange(bob_public_key)
        bob_shared_secret = bob_private_key.exchange(alice_public_key)
        
        def to_pem(pub_key):
            return pub_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
            
        return jsonify({
            'success': True,
            'alice_public_key': to_pem(alice_public_key),
            'bob_public_key': to_pem(bob_public_key),
            'alice_shared_secret': alice_shared_secret.hex(),
            'bob_shared_secret': bob_shared_secret.hex(),
            'is_match': alice_shared_secret == bob_shared_secret
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== SHA-256 & SHA-3 ====================
@app.route('/api/sha256/hash', methods=['POST'])
def sha256_hash():
    data = request.json
    text = data.get('data', '')
    sha256 = hashlib.sha256()
    sha256.update(text.encode('utf-8'))
    return jsonify({'success': True, 'hash': sha256.hexdigest()})

@app.route('/api/sha3/hash', methods=['POST'])
def sha3_hash():
    data = request.json
    text = data.get('data', '')
    sha3 = SHA3_256.new()
    sha3.update(text.encode('utf-8'))
    return jsonify({'success': True, 'hash': sha3.hexdigest()})

if __name__ == '__main__':
    app.run(debug=True, port=8000)
