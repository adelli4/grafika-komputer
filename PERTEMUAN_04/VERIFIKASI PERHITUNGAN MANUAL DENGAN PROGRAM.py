
import matplotlib.pyplot as plt
import numpy as np

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
    dx = x2 - x1
    dy = y2 - y1
    p = 2 * dy - dx
    x, y = x1, y1
    pixels.append((x, y))

    for _ in range(dx):
        if p < 0:
            p = p + 2 * dy
        else:
            y = y + 1
            p = p + 2 * dy - 2 * dx

        x = x + 1
        pixels.append((x, y))

    return pixels


# Kasus uji
x1, y1 = 2, 2
x2, y2 = 8, 5

# Hasil program
dda_pixels = dda_line(x1, y1, x2, y2)
bresenham_pixels = bresenham_line(x1, y1, x2, y2)

print("Output DDA (Program):", dda_pixels)
print("Output Bresenham (Program):", bresenham_pixels)


# Visualisasi hasil program
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Visualisasi DDA
x_vals, y_vals = zip(*dda_pixels)

axes[0].plot(
    [x1, x2], [y1, y2],
    'b--', label='Garis ideal'
)

axes[0].scatter(
    x_vals, y_vals,
    c='red', marker='s', s=50,
    label='Piksel DDA'
)

for x, y in dda_pixels:
    axes[0].annotate(
        f'({x}, {y})', (x, y),
        xytext=(0, -12),
        textcoords='offset points',
        ha='center', fontsize=8
    )

axes[0].set_title('Hasil DDA (Program)')


# Visualisasi Bresenham
x_vals, y_vals = zip(*bresenham_pixels)

axes[1].plot(
    [x1, x2], [y1, y2],
    'b--', label='Garis ideal'
)

axes[1].scatter(
    x_vals, y_vals,
    c='red', marker='s', s=50,
    label='Piksel Bresenham'
)

for x, y in bresenham_pixels:
    axes[1].annotate(
        f'({x}, {y})', (x, y),
        xytext=(0, -12),
        textcoords='offset points',
        ha='center', fontsize=8
    )

axes[1].set_title('Hasil Bresenham (Program)')


# Pengaturan grafik
for ax in axes:
    ax.set_xticks(range(0, 10))
    ax.set_yticks(range(0, 8))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 7)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

plt.tight_layout()
plt.show()
