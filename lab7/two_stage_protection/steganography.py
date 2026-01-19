from PIL import Image
import numpy as np

class LSBSteganography:
    @staticmethod
    def hide_data(image_path, data):
        img = Image.open(image_path)
        img_array = np.array(img)
        
        data_size = len(data)
        size_bytes = data_size.to_bytes(4, byteorder='big')
        full_data = size_bytes + data
        
        bits = []
        for byte in full_data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        
        flat_img = img_array.flatten()
        
        if len(bits) > len(flat_img):
            raise ValueError("Дані занадто великі для цього зображення")
        
        for i in range(len(bits)):
            flat_img[i] = (flat_img[i] & 0xFE) | bits[i]
        
        stego_img = flat_img.reshape(img_array.shape)
        return Image.fromarray(stego_img.astype(np.uint8))
    
    @staticmethod
    def extract_data(image_path):
        img = Image.open(image_path)
        img_array = np.array(img)
        flat_img = img_array.flatten()
        
        size_bits = []
        for i in range(32):
            size_bits.append(int(flat_img[i] & 1))
        
        data_size = 0
        for bit in size_bits:
            data_size = (data_size << 1) | bit
        
        if data_size <= 0 or data_size > len(flat_img) // 8:
            raise ValueError(f"Некоректний розмір даних: {data_size}")
        
        data_bits = []
        for i in range(32, 32 + data_size * 8):
            data_bits.append(int(flat_img[i] & 1))
        
        data_bytes = bytearray()
        for i in range(0, len(data_bits), 8):
            byte = 0
            for bit in data_bits[i:i+8]:
                byte = (byte << 1) | bit
            data_bytes.append(byte)
        
        return bytes(data_bytes)

def hide_in_image(image_path, data, output_path):
    steg = LSBSteganography()
    stego_img = steg.hide_data(image_path, data)
    stego_img.save(output_path)

def extract_from_image(image_path):
    steg = LSBSteganography()
    return steg.extract_data(image_path)
