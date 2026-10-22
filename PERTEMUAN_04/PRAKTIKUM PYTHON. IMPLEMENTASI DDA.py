
import numpy as np
import matplotlib.pyplot as plt

def dda_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    pixels = []
    for _ in range(steps + 1):
        pixels.append((round(x), round(y)))
        x += x_inc
        y += y_inc
    return pixels

# contoh penggunaan
x1, y1 = 2, 2
x2, y2 = 8, 5
pixels = dda_line(x1, y1, x2, y2)
print("koordinat piksel:", pixels)

# visualisasi hasil
x_vals, y_vals = zip(*pixels)
plt.figure(figsize=(6, 5))

# menggambar garis ideal
plt.plot([x1, x2], [y1, y2], 'b--',
         label='garis ideal')

# menggambar piksel hasil dda
plt.scatter(x_vals, y_vals, c='red', marker='s',
            s=50, label='piksel hasil dda')

# menampilkan angka koordinat setiap titik
for x, y in pixels:
    plt.annotate(f'({x}, {y})', (x, y),
                 xytext=(0, -12),
                 textcoords='offset points',
                 ha='center', fontsize=9)

plt.xticks(range(0, 10))
plt.yticks(range(0, 8))
plt.xlim(0, 9)
plt.ylim(0, 7.5)
plt.grid(True, alpha=0.5)
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Implementasi DDA: Garis (2,2) ke (8,5)')
plt.show()
