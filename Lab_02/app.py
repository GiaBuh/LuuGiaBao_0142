from flask import Flask, render_template, request, json, jsonify
from cipher import CaesarCipher, VigenereCipher, RailFenceCipher, PlayfairCipher, TranspositionCipher

app = Flask(__name__, template_folder='web', static_folder='web', static_url_path='')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/<path:path>', methods=['OPTIONS'])
def options_routes(path):
    return jsonify({}), 200

#router routes for home page
@app.route("/")
def home():
    return render_template('index.html')

#=================================================================
# Caesar Cipher ALGORITHM
ceasar_cipher = CaesarCipher()

@app.route('/api/caesar/encrypt', methods=['POST'])
def api_caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    encrypted_text = ceasar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/caesar/decrypt', methods=['POST'])
def api_caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = ceasar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})
#=================================================================

#=================================================================
# Vigenere Cipher ALGORITHM
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def api_vigenere_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    encrypted_text = vigenere_cipher.viginere_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def api_vigenere_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    decrypted_text = vigenere_cipher.viginere_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})
#=================================================================

#=================================================================
# Rail Fence Cipher ALGORITHM
rail_fence_cipher = RailFenceCipher()

@app.route('/api/railfence/encrypt', methods=['POST'])
def api_railfence_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = rail_fence_cipher.rail_fence_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/railfence/decrypt', methods=['POST'])
def api_railfence_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = rail_fence_cipher.rail_fence_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})
#=================================================================

#=================================================================
# Playfair Cipher ALGORITHM
playfair_cipher = PlayfairCipher()

@app.route('/api/playfair/creatematrix', methods=['POST'])
def api_playfair_create_matrix():
    data = request.json
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({'playfair_matrix': playfair_matrix})

@app.route('/api/playfair/encrypt', methods=['POST'])
def api_playfair_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/playfair/decrypt', methods=['POST'])
def api_playfair_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)
    return jsonify({'decrypted_text': decrypted_text})
#=================================================================

#=================================================================
# TRANSPOSITION CIPHER ALGORITHM
transposition_cipher = TranspositionCipher()

@app.route('/api/transposition/encrypt', methods=['POST'])
def api_transposition_encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text')
    key = int(data.get('key'))
    encrypted_text = transposition_cipher.encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/transposition/decrypt', methods=['POST'])
def api_transposition_decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text')
    key = int(data.get('key'))
    decrypted_text = transposition_cipher.decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})
#=================================================================

#main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
