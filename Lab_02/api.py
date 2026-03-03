from flask import Flask, request, jsonify
from cipher import CaesarCipher, VigenereCipher

app = Flask(__name__)

#=================================================================
# Caesar Cipher ALGORITHM
ceasar_cipher = CaesarCipher()

# encrypt
@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    encrypted_text = ceasar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

# decrypt
@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = ceasar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})
#=================================================================

#=================================================================
# Vigenere Cipher ALGORITHM
vigenere_cipher = VigenereCipher()

# encrypt
@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    encrypted_text = vigenere_cipher.viginere_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

# decrypt
@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    decrypted_text = vigenere_cipher.viginere_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})
#=================================================================

# main function
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)