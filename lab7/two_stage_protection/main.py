import os
import sys
from encryption import encrypt_file, decrypt_data
from steganography import hide_in_image, extract_from_image
from analytics import Analytics

class TwoStageProtection:
    def __init__(self, password):
        self.password = password
        self.analytics = Analytics()
    
    def protect(self, input_file, cover_image, output_image):
        print("Початок двоетапного захисту...")
        protection_start = self.analytics.start_timer()
        
        print("\nЕТАП 1: Шифрування файлу...")
        original_size = os.path.getsize(input_file)
        
        enc_start = self.analytics.start_timer()
        encrypted_data = encrypt_file(input_file, self.password)
        enc_time = self.analytics.end_timer(enc_start)
        
        encrypted_size = len(encrypted_data)
        self.analytics.record_encryption(original_size, encrypted_size, enc_time)
        print(f"  ✓ Файл зашифровано: {original_size} → {encrypted_size} байт за {enc_time:.4f} сек")
        
        print("\nЕТАП 2: Приховування в зображення...")
        image_size = os.path.getsize(cover_image)
        
        steg_start = self.analytics.start_timer()
        hide_in_image(cover_image, encrypted_data, output_image)
        steg_time = self.analytics.end_timer(steg_start)
        
        stego_size = os.path.getsize(output_image)
        self.analytics.record_steganography(encrypted_size, image_size, stego_size, steg_time)
        print(f"  ✓ Дані приховано в зображенні за {steg_time:.4f} сек")
        
        protection_time = self.analytics.end_timer(protection_start)
        print(f"\n✓ Захист завершено за {protection_time:.4f} сек")
        
        return protection_time
    
    def recover(self, stego_image, output_file):
        print("\nПочаток відновлення даних...")
        recovery_start = self.analytics.start_timer()
        
        print("\nЕТАП 1: Екстракція з зображення...")
        extr_start = self.analytics.start_timer()
        encrypted_data = extract_from_image(stego_image)
        extr_time = self.analytics.end_timer(extr_start)
        
        extracted_size = len(encrypted_data)
        self.analytics.record_extraction(extracted_size, extr_time)
        print(f"  ✓ Витягнуто {extracted_size} байт за {extr_time:.4f} сек")
        
        print("\nЕТАП 2: Дешифрування...")
        dec_start = self.analytics.start_timer()
        decrypted_data = decrypt_data(encrypted_data, self.password)
        dec_time = self.analytics.end_timer(dec_start)
        
        decrypted_size = len(decrypted_data)
        self.analytics.record_decryption(decrypted_size, dec_time)
        print(f"  ✓ Дані розшифровано: {decrypted_size} байт за {dec_time:.4f} сек")
        
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        
        recovery_time = self.analytics.end_timer(recovery_start)
        print(f"\n✓ Відновлення завершено за {recovery_time:.4f} сек")
        
        return recovery_time
    
    def test_integrity(self, original_file, recovered_file):
        print("\nПеревірка цілісності...")
        with open(original_file, 'rb') as f:
            original_data = f.read()
        with open(recovered_file, 'rb') as f:
            recovered_data = f.read()
        
        if original_data == recovered_data:
            print("✓ УСПІХ: Файли ідентичні!")
            return True
        else:
            print("✗ ПОМИЛКА: Файли відрізняються!")
            return False
    
    def generate_report(self, report_file):
        self.analytics.save_report(report_file)
        print(f"\n✓ Звіт збережено: {report_file}")

def main():
    if len(sys.argv) < 2:
        print("Використання:")
        print("  python main.py protect <файл> <зображення> <вихідне_зображення> <пароль>")
        print("  python main.py recover <стего_зображення> <вихідний_файл> <пароль>")
        print("  python main.py test <оригінальний_файл> <зображення> <пароль>")
        return
    
    mode = sys.argv[1]
    
    if mode == 'protect':
        if len(sys.argv) != 6:
            print("Використання: python main.py protect <файл> <зображення> <вихідне_зображення> <пароль>")
            return
        
        input_file = sys.argv[2]
        cover_image = sys.argv[3]
        output_image = sys.argv[4]
        password = sys.argv[5]
        
        system = TwoStageProtection(password)
        system.protect(input_file, cover_image, output_image)
        
    elif mode == 'recover':
        if len(sys.argv) != 5:
            print("Використання: python main.py recover <стего_зображення> <вихідний_файл> <пароль>")
            return
        
        stego_image = sys.argv[2]
        output_file = sys.argv[3]
        password = sys.argv[4]
        
        system = TwoStageProtection(password)
        system.recover(stego_image, output_file)
        
    elif mode == 'test':
        if len(sys.argv) != 5:
            print("Використання: python main.py test <оригінальний_файл> <зображення> <пароль>")
            return
        
        original_file = sys.argv[2]
        cover_image = sys.argv[3]
        password = sys.argv[4]
        
        stego_image = 'test_stego.png'
        recovered_file = 'test_recovered.txt'
        
        system = TwoStageProtection(password)
        
        prot_time = system.protect(original_file, cover_image, stego_image)
        rec_time = system.recover(stego_image, recovered_file)
        
        system.analytics.record_total(prot_time, rec_time)
        
        is_valid = system.test_integrity(original_file, recovered_file)
        
        system.generate_report('report.txt')
        print("\n" + "="*60)
        print(system.analytics.generate_report())
        
        os.remove(stego_image)
        os.remove(recovered_file)
        
    else:
        print(f"Невідомий режим: {mode}")
        print("Доступні режими: protect, recover, test")

if __name__ == '__main__':
    main()
