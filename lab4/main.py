import hashlib
import os

def generate_keys(surname, birthdate, secret):
    private_key = int(hashlib.sha256(f"{surname}{birthdate}{secret}".encode()).hexdigest(), 16) % 1000000
    public_key = (private_key * 7) % 1000007
    return private_key, public_key

def hash_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    return int(hashlib.sha256(content.encode()).hexdigest(), 16)

def sign_document(document_hash, private_key):
    return document_hash ^ private_key

def verify_signature(signature, document_hash, private_key):
    decrypted_hash = signature ^ private_key
    return decrypted_hash == document_hash

def main():
    print("=== СИСТЕМА ЦИФРОВИХ ПІДПИСІВ ===\n")
    
    surname = input("Прізвище: ")
    birthdate = input("Дата народження (DDMMYYYY): ")
    secret = input("Секретне слово: ")
    
    private_key, public_key = generate_keys(surname, birthdate, secret)
    print(f"\nПриватний ключ: {private_key}")
    print(f"Публічний ключ: {public_key}")
    
    doc_filename = input("\nІм'я файлу документа (без розширення): ") + ".txt"
    document_text = input("Введіть текст документа: ")
    
    with open(doc_filename, 'w', encoding='utf-8') as f:
        f.write(document_text)
    print(f"Документ збережено: {doc_filename}")
    
    doc_hash = hash_file(doc_filename)
    print(f"Хеш документа: {doc_hash}")
    
    signature = sign_document(doc_hash, private_key)
    print(f"Цифровий підпис: {signature}")
    
    sig_filename = doc_filename.replace('.txt', '_signature.txt')
    with open(sig_filename, 'w', encoding='utf-8') as f:
        f.write(str(signature))
    print(f"Підпис збережено: {sig_filename}")
    
    print("\n--- ПЕРЕВІРКА ПІДПИСУ ---")
    verify_file = input("Введіть ім'я файлу для перевірки: ")
    
    if not os.path.exists(verify_file):
        print("Файл не знайдено!")
        return
    
    verify_hash = hash_file(verify_file)
    
    is_valid = verify_signature(signature, verify_hash, private_key)
    
    if is_valid:
        print("✓ Підпис ДІЙСНИЙ")
    else:
        print("✗ Підпис ПІДРОБЛЕНИЙ")
    
    print("\n--- ДЕМОНСТРАЦІЯ ПІДРОБКИ ---")
    fake_filename = "fake_" + doc_filename
    with open(fake_filename, 'w', encoding='utf-8') as f:
        f.write(document_text + " [змінено]")
    
    fake_hash = hash_file(fake_filename)
    is_fake = verify_signature(signature, fake_hash, private_key)
    
    print(f"Створено підроблений документ: {fake_filename}")
    if is_fake:
        print("✓ Підпис ДІЙСНИЙ")
    else:
        print("✗ Підпис ПІДРОБЛЕНИЙ (зміни виявлено)")

if __name__ == "__main__":
    main()
