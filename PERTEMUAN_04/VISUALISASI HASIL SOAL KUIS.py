
import matplotlib.pyplot as plt

# DDA
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


# Bresenham
def bresenham_line(x1, y1, x2, y2):
    pixels = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    x, y = x1, y1

    # menentukan arah pergerakan utama
    if dx >= dy:
        p = 2 * dy - dx

        while x != x2:
            pixels.append((x, y))

            if p >= 0:
                y += sy
                p -= 2 * dx

            x += sx
            p += 2 * dy

    else:
        p = 2 * dx - dy

        while y != y2:
            pixels.append((x, y))

            if p >= 0:
                x += sx
                p -= 2 * dy

            y += sy
            p += 2 * dx

    pixels.append((x2, y2))

    return pixels


# titik awal dan akhir
x1, y1 = 3, 5
x2, y2 = 9, 10

# hasil program
dda_pixels = dda_line(x1, y1, x2, y2)
bresenham_pixels = bresenham_line(x1, y1, x2, y2)

print("Output DDA (Program):", dda_pixels)
print("Output Bresenham (Program):", bresenham_pixels)


# visualisasi DDA
x_vals, y_vals = zip(*dda_pixels)

plt.figure(figsize=(7, 5))
plt.plot([x1, x2], [y1, y2], 'b--', label='Garis Ideal')
plt.scatter(x_vals, y_vals, c='red', marker='s',
            s=70, label='Piksel DDA')

for x, y in dda_pixels:
    plt.annotate(f'({x}, {y})', (x, y),
                 xytext=(0, -13),
                 textcoords='offset points',
                 ha='center', fontsize=9)

plt.title('Visualisasi Algoritma DDA: Garis (3, 5) ke (9, 10)')
plt.xlabel('X')
plt.ylabel('Y')
plt.xticks(range(2, 11))
plt.yticks(range(4, 12))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.axis('equal')
plt.tight_layout()
plt.show()


# visualisasi Bresenham
x_vals, y_vals = zip(*bresenham_pixels)

plt.figure(figsize=(7, 5))
plt.plot([x1, x2], [y1, y2], 'b--', label='Garis Ideal')
plt.scatter(x_vals, y_vals, c='red', marker='s',
            s=70, label='Piksel Bresenham')

for x, y in bresenham_pixels:
    plt.annotate(f'({x}, {y})', (x, y),
                 xytext=(0, -13),
                 textcoords='offset points',
                 ha='center', fontsize=9)

plt.title('Visualisasi Algoritma Bresenham: Garis (3, 5) ke (9, 10)')
plt.xlabel('X')
plt.ylabel('Y')
plt.xticks(range(2, 11))
plt.yticks(range(4, 12))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.axis('equal')
plt.tight_layout()
plt.show()

