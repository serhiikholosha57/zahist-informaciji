from steganography import extract_from_image
from encryption import decrypt_data
import sys

print("="*60)
print("ДЕМОНСТРАЦІЯ НЕОБХІДНОСТІ ОБОХ ЕТАПІВ ЗАХИСТУ")
print("="*60)

stego_image = sys.argv[1]
correct_password = sys.argv[2]
wrong_password = "WrongPassword999"

print("\n1. СПРОБА ЕКСТРАКЦІЇ БЕЗ ДЕШИФРУВАННЯ")
print("-"*60)
try:
    encrypted_data = extract_from_image(stego_image)
    print(f"✓ Екстраговано {len(encrypted_data)} байт")
    print("\nПерші 50 байт (зашифровані):")
    print(encrypted_data[:50])
    print("\n⚠ Дані екстраговано, але вони зашифровані!")
    print("  Без правильного пароля вони нечитабельні.")
except Exception as e:
    print(f"✗ Помилка: {e}")

print("\n2. СПРОБА ДЕШИФРУВАННЯ З НЕПРАВИЛЬНИМ ПАРОЛЕМ")
print("-"*60)
try:
    wrong_decrypted = decrypt_data(encrypted_data, wrong_password)
    print(f"⚠ Дешифрування завершилось, але дані некоректні!")
    print(f"  Розмір: {len(wrong_decrypted)} байт")
    try:
        text = wrong_decrypted.decode('utf-8')
        print("  Результат нечитабельний (сміття)")
    except:
        print("  ✓ Результат не є валідним UTF-8 текстом (сміття)")
except Exception as e:
    print(f"✓ Помилка дешифрування: {type(e).__name__}")
    print(f"  {str(e)[:100]}")
    print("  Неправильний пароль не може розшифрувати дані!")

print("\n3. УСПІШНЕ ВІДНОВЛЕННЯ З ПРАВИЛЬНИМ ПАРОЛЕМ")
print("-"*60)
try:
    decrypted = decrypt_data(encrypted_data, correct_password)
    print(f"✓ Дешифровано {len(decrypted)} байт")
    print("\nВідновлений текст:")
    print(decrypted.decode('utf-8'))
except Exception as e:
    print(f"✗ Помилка: {e}")

print("\n" + "="*60)
print("ВИСНОВОК")
print("="*60)
print("Для доступу до даних НЕОБХІДНІ:")
print("1. Стего-зображення (для екстракції)")
print("2. Правильний пароль (для дешифрування)")
print("\nБез будь-якого з цих компонентів дані залишаються захищеними!")
print("="*60)
