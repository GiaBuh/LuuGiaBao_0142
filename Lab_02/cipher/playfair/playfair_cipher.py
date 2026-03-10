class PlayfairCipher:
    def __init__(self):
        pass
    
    def create_playfair_matrix(self, key):
        key = key.replace("J", "I") 
        key = key.upper()
        key = key.replace(" ", "")
        
        # Remove duplicate letters from key while preserving order
        temp_key = ""
        for char in key:
            if char not in temp_key:
                temp_key += char
        key = temp_key

        key_set = set(key)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        remaining_letters = [
            letter for letter in alphabet if letter not in key_set
        ]
        matrix = list(key)

        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coordinates(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        return None

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = plain_text.replace("J", "I")
        plain_text = plain_text.upper()
        plain_text = plain_text.replace(" ", "")

        encrypt_text = ""

        for i in range(0, len(plain_text), 2):
            pair = plain_text[i:i+2]
            if len(pair) == 1:
                pair += "X"
            row1, col1 = self.find_letter_coordinates(matrix, pair[0])
            row2, col2 = self.find_letter_coordinates(matrix, pair[1])
            if row1 == row2:
                encrypt_text += matrix[row1][(col1+1) % 5] + matrix[row2][(col2+1) % 5]
            elif col1 == col2:
                encrypt_text += matrix[(row1+1) % 5][col1] + matrix[(row2+1) % 5][col2]
            else:
                encrypt_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypt_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        decrypt_text = ""
        
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coordinates(matrix, pair[0])
            row2, col2 = self.find_letter_coordinates(matrix, pair[1])
            if row1 == row2:
                decrypt_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypt_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypt_text += matrix[row1][col2] + matrix[row2][col1]
        banro = ""

        for i in range(0, len(decrypt_text) - 2, 2):
            if decrypt_text[i] == decrypt_text[i+2]:
                banro += decrypt_text[i]
            else:
                banro += decrypt_text[i] + "" + decrypt_text[i+1]

        if decrypt_text[-1] == "X":
            banro += decrypt_text[-2]
        else:
            banro += decrypt_text[-2]
            banro += decrypt_text[-1]
        return banro