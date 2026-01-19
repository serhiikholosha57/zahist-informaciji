from PIL import Image
import numpy as np

img_array = np.random.randint(0, 256, (400, 400, 3), dtype=np.uint8)
img = Image.fromarray(img_array)
img.save('test_cover.png')
print("Створено test_cover.png (400x400)")

with open('test_secret.txt', 'w', encoding='utf-8') as f:
    f.write("Це секретне повідомлення для тестування системи двоетапного захисту!\n")
    f.write("Воно буде зашифроване та приховане в зображенні.\n")
    f.write("Для відновлення потрібні обидва етапи: екстракція та дешифрування.\n")
print("Створено test_secret.txt")
