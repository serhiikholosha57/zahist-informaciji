from PIL import Image
import os

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)

def hide_message(image_path, message, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = list(img.getdata())
    
    delimiter = '1111111111111110'
    binary_message = text_to_binary(message) + delimiter
    
    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Повідомлення завелике для цього зображення")
    
    new_pixels = []
    bit_index = 0
    
    for pixel in pixels:
        r, g, b = pixel
        
        if bit_index < len(binary_message):
            r = (r & 0xFE) | int(binary_message[bit_index])
            bit_index += 1
        
        if bit_index < len(binary_message):
            g = (g & 0xFE) | int(binary_message[bit_index])
            bit_index += 1
        
        if bit_index < len(binary_message):
            b = (b & 0xFE) | int(binary_message[bit_index])
            bit_index += 1
        
        new_pixels.append((r, g, b))
    
    stego_img = Image.new(img.mode, img.size)
    stego_img.putdata(new_pixels)
    stego_img.save(output_path, 'PNG')
    
    return output_path

def extract_message(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    binary_message = ''
    delimiter = '1111111111111110'
    
    for pixel in pixels:
        for value in pixel:
            binary_message += str(value & 1)
            
            if binary_message.endswith(delimiter):
                binary_message = binary_message[:-len(delimiter)]
                return binary_to_text(binary_message)
    
    return binary_to_text(binary_message)

if __name__ == '__main__':
    original_image = 'original.png'
    stego_image = 'stego.png'
    
    personal_message = "My name is Serhii Holosha and I love programming!"
    
    print(f"Оригінальне повідомлення: {personal_message}")
    print(f"Довжина: {len(personal_message)} символів")
    print(f"Бінарне представлення (перші 40 біт): {text_to_binary(personal_message)[:40]}...")
    
    hide_message(original_image, personal_message, stego_image)
    print(f"\n✓ Повідомлення приховано в {stego_image}")
    
    extracted = extract_message(stego_image)
    print(f"\n✓ Витягнуте повідомлення: {extracted}")
    print(f"✓ Співпадіння: {personal_message == extracted}")
    
    original_size = os.path.getsize(original_image)
    stego_size = os.path.getsize(stego_image)
    
    print(f"\n--- Аналіз зображення ---")
    print(f"Розмір оригіналу: {original_size} байт")
    print(f"Розмір стего: {stego_size} байт")
    print(f"Різниця: {stego_size - original_size} байт")
    
    orig_img = Image.open(original_image)
    steg_img = Image.open(stego_image)
    
    orig_pixels = list(orig_img.getdata())
    steg_pixels = list(steg_img.getdata())
    
    changed_pixels = sum(1 for op, sp in zip(orig_pixels, steg_pixels) if op != sp)
    total_pixels = len(orig_pixels)
    
    print(f"Змінено пікселів: {changed_pixels}/{total_pixels} ({changed_pixels/total_pixels*100:.2f}%)")
    print(f"Візуальна різниця: непомітна для ока (зміна LSB на ±1)")
