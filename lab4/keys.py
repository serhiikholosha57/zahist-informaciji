import hashlib
import json

def generate_keys():
    name = input("Введіть ім'я: ")
    birthdate = input("Введіть дату народження (ДД.ММ.РРРР): ")
    secret = input("Введіть секретне слово: ")
    
    combined = f"{name}{birthdate}{secret}"
    private_key = hashlib.sha256(combined.encode()).hexdigest()
    
    private_int = int(private_key[:16], 16)
    public_key = pow(private_int, 2, 2**64 - 1)
    
    with open("private_key.json", "w", encoding="utf-8") as f:
        json.dump({"private_key": private_key}, f, ensure_ascii=False, indent=2)
    
    with open("public_key.json", "w", encoding="utf-8") as f:
        json.dump({"public_key": str(public_key)}, f, ensure_ascii=False, indent=2)
    
    print(f"\nПриватний ключ: {private_key}")
    print(f"Публічний ключ: {public_key}")
    print("\nКлючі збережено у файли private_key.json та public_key.json")

if __name__ == "__main__":
    generate_keys()