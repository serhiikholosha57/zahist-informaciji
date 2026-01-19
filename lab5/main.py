from cryptography.fernet import Fernet
import hashlib
import base64

class EmailEncryptor:
    def __init__(self, user_data):
        self.key = self._generate_key(user_data)
        self.cipher = Fernet(self.key)
    
    def _generate_key(self, user_data):
        hash_object = hashlib.sha256(user_data.encode())
        key_bytes = hash_object.digest()
        return base64.urlsafe_b64encode(key_bytes)
    
    def encrypt(self, message):
        encrypted = self.cipher.encrypt(message.encode())
        return encrypted.decode()
    
    def decrypt(self, encrypted_message):
        decrypted = self.cipher.decrypt(encrypted_message.encode())
        return decrypted.decode()


def main():
    print("=== Демонстрація захищеної комунікації ===\n")
    
    email = "ivan.petrenko@gmail.com"
    user_data = "IvanPetrenko1995"
    message = "Секретні дані про місцеположення ворога"
    
    print(f"Відправник: {email}")
    print(f"Персональні дані для ключа: {user_data}")
    print(f"Вихідне повідомлення: {message}\n")
    
    sender = EmailEncryptor(user_data)
    
    encrypted = sender.encrypt(message)
    print(f"Зашифроване повідомлення:\n{encrypted}\n")
    
    print("--- Передача зашифрованого повідомлення ---\n")
    
    receiver = EmailEncryptor(user_data)
    
    decrypted = receiver.decrypt(encrypted)
    print(f"Розшифроване повідомлення: {decrypted}")


if __name__ == "__main__":
    main()