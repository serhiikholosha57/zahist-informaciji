# cipher_comparison.py

class CaesarCipher:
    def __init__(self, shift):
        self.shift = shift
        self.alphabet = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    
    def encrypt(self, text):
        result = ''
        for char in text.lower():
            if char in self.alphabet:
                old_index = self.alphabet.index(char)
                new_index = (old_index + self.shift) % len(self.alphabet)
                result += self.alphabet[new_index]
            else:
                result += char
        return result
    
    def decrypt(self, text):
        result = ''
        for char in text.lower():
            if char in self.alphabet:
                old_index = self.alphabet.index(char)
                new_index = (old_index - self.shift) % len(self.alphabet)
                result += self.alphabet[new_index]
            else:
                result += char
        return result


class VigenereCipher:
    def __init__(self, key):
        self.key = key.lower()
        self.alphabet = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    
    def encrypt(self, text):
        result = ''
        key_index = 0
        for char in text.lower():
            if char in self.alphabet:
                text_index = self.alphabet.index(char)
                key_char = self.key[key_index % len(self.key)]
                key_shift = self.alphabet.index(key_char)
                new_index = (text_index + key_shift) % len(self.alphabet)
                result += self.alphabet[new_index]
                key_index += 1
            else:
                result += char
        return result
    
    def decrypt(self, text):
        result = ''
        key_index = 0
        for char in text.lower():
            if char in self.alphabet:
                text_index = self.alphabet.index(char)
                key_char = self.key[key_index % len(self.key)]
                key_shift = self.alphabet.index(key_char)
                new_index = (text_index - key_shift) % len(self.alphabet)
                result += self.alphabet[new_index]
                key_index += 1
            else:
                result += char
        return result


def generate_caesar_key(birth_date):
    return sum(int(d) for d in birth_date if d.isdigit())


def compare_ciphers(caesar_encrypted, vigenere_encrypted, caesar_key, vigenere_key):
    print("\n" + "="*70)
    print("ПОРІВНЯЛЬНИЙ АНАЛІЗ ШИФРІВ")
    print("="*70)
    
    print(f"\n{'Параметр':<30} {'Цезар':<20} {'Віженер':<20}")
    print("-"*70)
    print(f"{'Ключ':<30} {caesar_key:<20} {vigenere_key:<20}")
    print(f"{'Довжина ключа':<30} {1:<20} {len(vigenere_key):<20}")
    print(f"{'Довжина шифротексту':<30} {len(caesar_encrypted):<20} {len(vigenere_encrypted):<20}")
    
    caesar_unique = len(set(c for c in caesar_encrypted if c.isalpha()))
    vigenere_unique = len(set(c for c in vigenere_encrypted if c.isalpha()))
    print(f"{'Унікальні символи':<30} {caesar_unique:<20} {vigenere_unique:<20}")
    
    print(f"{'Складність злому':<30} {'Дуже низька':<20} {'Низька':<20}")
    print(f"{'Можливі ключі':<30} {'33':<20} {'∞':<20}")

def main():
    # Персональні дані
    birth_date = "14.08.2004"
    surname = "Холоша"
    
    # Генерація ключів
    caesar_shift = generate_caesar_key(birth_date)
    vigenere_key = surname
    
    # Тестовий текст
    plaintext = "Захист інформації – цікава дисципліна"
    
    # Створення шифрів
    caesar = CaesarCipher(caesar_shift)
    vigenere = VigenereCipher(vigenere_key)
    
    # Шифрування
    caesar_encrypted = caesar.encrypt(plaintext)
    vigenere_encrypted = vigenere.encrypt(plaintext)
    
    # Розшифрування
    caesar_decrypted = caesar.decrypt(caesar_encrypted)
    vigenere_decrypted = vigenere.decrypt(vigenere_encrypted)
    
    # Виведення результатів
    print("ДЕМОНСТРАЦІЯ РОБОТИ ШИФРІВ")
    print("="*70)
    
    print(f"\nВихідний текст: {plaintext}")
    
    print(f"\n--- ШИФР ЦЕЗАРЯ (зсув = {caesar_shift}) ---")
    print(f"Зашифровано: {caesar_encrypted}")
    print(f"Розшифровано: {caesar_decrypted}")
    
    print(f"\n--- ШИФР ВІЖЕНЕРА (ключ = '{vigenere_key}') ---")
    print(f"Зашифровано: {vigenere_encrypted}")
    print(f"Розшифровано: {vigenere_decrypted}")
    
    # Порівняльний аналіз
    compare_ciphers(caesar_encrypted, vigenere_encrypted, caesar_shift, vigenere_key)


if __name__ == "__main__":
    main()