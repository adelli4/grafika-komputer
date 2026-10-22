
import matplotlib.pyplot as plt
import numpy as np

# DDA
def dda_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))

    if steps == 0:
        return [(x1, y1)]

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
    err = dx - dy
    x, y = x1, y1

    while True:
        pixels.append((x, y))

        if x == x2 and y == y2:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x += sx

        if e2 < dx:
            err += dx
            y += sy

    return pixels


# Kasus uji sesuai soal nomor 2 sampai 6
garis = [
    ((1, 1), (7, 6)),
    ((3, 7), (9, 3)),
    ((0, 5), (6, 5)),
    ((4, 1), (4, 8)),
    ((8, 5), (2, 2))
]

# Hasil program dan visualisasi
for i, (awal, akhir) in enumerate(garis, start=2):
    x1, y1 = awal
    x2, y2 = akhir

    dda_pixels = dda_line(x1, y1, x2, y2)
    bresenham_pixels = bresenham_line(x1, y1, x2, y2)

    print(f"\nNomor {i}: Garis ({x1}, {y1}) ke ({x2}, {y2})")
    print("Output DDA (Program):", dda_pixels)
    print("Output Bresenham (Program):", bresenham_pixels)

    # Membuat grafik DDA dan Bresenham
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Visualisasi DDA
    x_vals, y_vals = zip(*dda_pixels)

    axes[0].plot(
        [x1, x2], [y1, y2],
        'b--', label='Garis Ideal'
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

    axes[0].set_title(
        f'Nomor {i}: Garis DDA ({x1}, {y1}) ke ({x2}, {y2})'
    )

    # Visualisasi Bresenham
    x_vals, y_vals = zip(*bresenham_pixels)

    axes[1].plot(
        [x1, x2], [y1, y2],
        'b--', label='Garis Ideal'
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

    axes[1].set_title(
        f'Nomor {i}: Garis Bresenham ({x1}, {y1}) ke ({x2}, {y2})'
    )

    # Pengaturan grafik
    for ax in axes:
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()
        ax.set_aspect('equal', adjustable='box')

    plt.tight_layout()
    plt.show()
