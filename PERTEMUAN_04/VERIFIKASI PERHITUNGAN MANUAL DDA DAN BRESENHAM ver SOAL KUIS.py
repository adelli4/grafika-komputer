
import matplotlib.pyplot as plt

# algoritma dda
def dda_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1
    pixels = []

    for i in range(steps + 1):
        pixels.append((round(x), round(y)))
        x += x_inc
        y += y_inc

    return pixels


# algoritma bresenham
def bresenham_line(x1, y1, x2, y2):
    pixels = []
    dx = x2 - x1
    dy = y2 - y1
    p = 2 * dy - dx
    x, y = x1, y1

    for i in range(dx + 1):
        pixels.append((x, y))

        if p < 0:
            x += 1
            p = p + 2 * dy
        else:
            x += 1
            y += 1
            p = p + 2 * dy - 2 * dx

    return pixels


# kasus uji
x1, y1 = 3, 5
x2, y2 = 9, 10

# perhitungan manual
manual_dda = [
    (3, 5), (4, 6), (5, 7), (6, 8),
    (7, 8), (8, 9), (9, 10)
]

manual_bresenham = [
    (3, 5), (4, 6), (5, 7), (6, 8),
    (7, 8), (8, 9), (9, 10)
]

# hasil program
hasil_dda = dda_line(x1, y1, x2, y2)
hasil_bresenham = bresenham_line(x1, y1, x2, y2)

# menampilkan hasil perhitungan
print("=== verifikasi dda ===")
print("hasil manual :", manual_dda)
print("hasil program:", hasil_dda)
print("sesuai:", manual_dda == hasil_dda)

print("\n=== verifikasi bresenham ===")
print("hasil manual :", manual_bresenham)
print("hasil program:", hasil_bresenham)
print("sesuai:", manual_bresenham == hasil_bresenham)

# menampilkan tabel hasil program
print("\n=== tabel koordinat piksel ===")
print("k | dda        | bresenham")
for k, (dda, br) in enumerate(zip(hasil_dda, hasil_bresenham)):
    print(f"{k} | {str(dda):10} | {br}")

# visualisasi hasil
plt.figure(figsize=(10, 5))

# grafik dda
plt.subplot(1, 2, 1)
plt.plot([x1, x2], [y1, y2], 'b--', label='garis ideal')
x_dda, y_dda = zip(*hasil_dda)
plt.scatter(x_dda, y_dda, color='red', marker='s',
            s=70, label='piksel dda')

for x, y in hasil_dda:
    plt.text(x, y + 0.15, f'({x},{y})', ha='center', fontsize=8)

plt.title('hasil DDA')
plt.xlabel('X')
plt.ylabel('Y')
plt.xticks(range(2, 11))
plt.yticks(range(4, 12))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

# grafik bresenham
plt.subplot(1, 2, 2)
plt.plot([x1, x2], [y1, y2], 'b--', label='garis ideal')
x_br, y_br = zip(*hasil_bresenham)
plt.scatter(x_br, y_br, color='red', marker='s',
            s=70, label='piksel bresenham')

for x, y in hasil_bresenham:
    plt.text(x, y + 0.15, f'({x},{y})', ha='center', fontsize=8)

plt.title('hasil bresenham')
plt.xlabel('X')
plt.ylabel('Y')
plt.xticks(range(2, 11))
plt.yticks(range(4, 12))
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.show()
