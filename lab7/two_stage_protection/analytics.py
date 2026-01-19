import time
import os
from datetime import datetime

class Analytics:
    def __init__(self):
        self.metrics = {
            'encryption': {},
            'steganography': {},
            'decryption': {},
            'extraction': {},
            'total': {}
        }
        
    def start_timer(self):
        return time.time()
    
    def end_timer(self, start_time):
        return time.time() - start_time
    
    def record_encryption(self, original_size, encrypted_size, time_taken):
        self.metrics['encryption'] = {
            'original_size': original_size,
            'encrypted_size': encrypted_size,
            'time': time_taken,
            'overhead': encrypted_size - original_size
        }
    
    def record_steganography(self, encrypted_size, image_size, stego_size, time_taken):
        self.metrics['steganography'] = {
            'encrypted_size': encrypted_size,
            'cover_image_size': image_size,
            'stego_image_size': stego_size,
            'time': time_taken
        }
    
    def record_extraction(self, extracted_size, time_taken):
        self.metrics['extraction'] = {
            'extracted_size': extracted_size,
            'time': time_taken
        }
    
    def record_decryption(self, decrypted_size, time_taken):
        self.metrics['decryption'] = {
            'decrypted_size': decrypted_size,
            'time': time_taken
        }
    
    def record_total(self, protection_time, recovery_time):
        self.metrics['total'] = {
            'total_protection_time': protection_time,
            'total_recovery_time': recovery_time,
            'total_time': protection_time + recovery_time
        }
    
    def generate_report(self):
        report = []
        report.append("=" * 60)
        report.append("ЗВІТ ПРО ЕФЕКТИВНІСТЬ ДВОЕТАПНОЇ СИСТЕМИ ЗАХИСТУ")
        report.append("=" * 60)
        report.append(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("ЕТАП 1: ШИФРУВАННЯ AES")
        report.append("-" * 60)
        enc = self.metrics['encryption']
        report.append(f"Розмір оригінального файлу: {enc['original_size']} байт")
        report.append(f"Розмір зашифрованих даних: {enc['encrypted_size']} байт")
        report.append(f"Накладні витрати: {enc['overhead']} байт ({enc['overhead']/enc['original_size']*100:.2f}%)")
        report.append(f"Час виконання: {enc['time']:.4f} сек")
        report.append("")
        
        report.append("ЕТАП 2: LSB-СТЕГАНОГРАФІЯ")
        report.append("-" * 60)
        steg = self.metrics['steganography']
        report.append(f"Розмір зашифрованих даних: {steg['encrypted_size']} байт")
        report.append(f"Розмір зображення-контейнера: {steg['cover_image_size']} байт")
        report.append(f"Розмір стего-зображення: {steg['stego_image_size']} байт")
        report.append(f"Час виконання: {steg['time']:.4f} сек")
        report.append("")
        
        report.append("ВІДНОВЛЕННЯ: ЕКСТРАКЦІЯ")
        report.append("-" * 60)
        extr = self.metrics['extraction']
        report.append(f"Розмір витягнутих даних: {extr['extracted_size']} байт")
        report.append(f"Час виконання: {extr['time']:.4f} сек")
        report.append("")
        
        report.append("ВІДНОВЛЕННЯ: ДЕШИФРУВАННЯ")
        report.append("-" * 60)
        dec = self.metrics['decryption']
        report.append(f"Розмір розшифрованих даних: {dec['decrypted_size']} байт")
        report.append(f"Час виконання: {dec['time']:.4f} сек")
        report.append("")
        
        report.append("ЗАГАЛЬНА СТАТИСТИКА")
        report.append("-" * 60)
        total = self.metrics['total']
        report.append(f"Загальний час захисту: {total['total_protection_time']:.4f} сек")
        report.append(f"Загальний час відновлення: {total['total_recovery_time']:.4f} сек")
        report.append(f"Загальний час операцій: {total['total_time']:.4f} сек")
        report.append("")
        
        report.append("АНАЛІЗ ТА РЕКОМЕНДАЦІЇ")
        report.append("-" * 60)
        
        if enc['time'] > 1.0:
            report.append("⚠ Час шифрування перевищує 1 секунду - для великих файлів розгляньте оптимізацію")
        else:
            report.append("✓ Час шифрування прийнятний")
            
        capacity = steg['cover_image_size'] * 3 / 8
        usage = (steg['encrypted_size'] / capacity) * 100
        report.append(f"Використання ємності зображення: {usage:.2f}%")
        
        if usage > 50:
            report.append("⚠ Високе використання ємності - може впливати на непомітність")
        else:
            report.append("✓ Низьке використання ємності - висока непомітність")
        
        report.append("")
        report.append("ВИСНОВОК")
        report.append("-" * 60)
        report.append("Система успішно реалізує двоетапний захист:")
        report.append("1. AES-256 шифрування забезпечує конфіденційність даних")
        report.append("2. LSB-стеганографія приховує факт наявності зашифрованих даних")
        report.append("Обидва етапи необхідні для повного відновлення даних")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_report(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.generate_report())
