from PIL import Image
import numpy as np

# Baca citra
image_path = 'D:/joji/Allaple.png'  # Ganti dengan path citra Anda
image = Image.open(image_path)

# Dapatkan ukuran citra
width, height = image.size

# Inisialisasi matriks untuk citra RGB
rgb_matrix = np.zeros((height, width, 3), dtype=np.uint8)

# Iterasi melalui setiap pixel
for y in range(height):
    for x in range(width):
        # Dapatkan nilai RGB untuk pixel saat ini
        r, g, b = image.getpixel((x, y))
        # Simpan nilai dalam matriks
        rgb_matrix[y, x] = [r, g, b]

# Cetak matriks RGB
print("Matriks RGB:")
print(rgb_matrix)