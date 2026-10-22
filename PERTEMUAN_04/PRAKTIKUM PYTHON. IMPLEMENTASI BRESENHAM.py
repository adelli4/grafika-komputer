
import matplotlib.pyplot as plt
import numpy as np

def bresenham_line(x1, y1, x2, y2):
    pixels = []
    dx = x2 - x1
    dy = y2 - y1
    p = 2*dy - dx
    x, y = x1, y1
    pixels.append((x, y))
    for _ in range(dx):
        if p < 0:
            p = p + 2*dy
        else:
            p = p + 2*dy - 2*dx
            y = y + 1
        x = x + 1
        pixels.append((x, y))
    return pixels

# contoh penggunaan
x1, y1 = 2, 2
x2, y2 = 8, 5
pixels = bresenham_line(x1, y1, x2, y2)
print("koordinat piksel:", pixels)

# visualisasi hasil
x_vals, y_vals = zip(*pixels)
plt.figure(figsize=(6, 5))
plt.plot([x1, x2], [y1, y2], 'b--', label='garis ideal')
plt.scatter(x_vals, y_vals, c='red', marker='s',
            s=100, label='piksel hasil bresenham')

# menampilkan koordinat setiap titik
for x, y in pixels:
    plt.text(x, y - 0.4, f'({x}, {y})',
             ha='center', fontsize=9)

plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(range(0, 10))
plt.yticks(range(0, 8))
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Implementasi Bresenham: Garis (2,2) ke (8,5)')
plt.show()
