import matplotlib.pyplot as plt

# daftar titik yang berisi koordinat x, y, label, dan warna
titik = [
    (1, 2, 'A', 'red'),
    (3, 4, 'B', 'blue'),
    (5, 1, 'C', 'green'),
    (4, 3, 'D', 'orange'),
    (2, 5, 'E', 'purple')
]

# memisahkan koordinat dan label dari setiap titik
x = [t[0] for t in titik]
y = [t[1] for t in titik]
label = [t[2] for t in titik]
warna = [t[3] for t in titik]

# membuat bidang gambar dengan ukuran 6 x 5
plt.figure(figsize=(6, 5))

# menggambar titik berdasarkan koordinat dan warna
plt.scatter(x, y, c=warna, s=100)

# menambahkan label dan koordinat pada setiap titik
for (xi, yi, lab, wrn) in titik:
    plt.annotate(
        f'{lab}({xi}, {yi})',
        (xi, yi),
        textcoords='offset points',
        xytext=(5, 5),
        fontsize=12
    )

# mengatur batas tampilan sumbu x dan sumbu y
plt.xlim(0, 6)
plt.ylim(0, 6)

# mengatur angka pada sumbu dengan jarak satu satuan
plt.xticks(range(0, 7, 1))
plt.yticks(range(0, 7, 1))

# memberikan nama pada sumbu x dan sumbu y
plt.xlabel('X')
plt.ylabel('Y')

# memberikan judul pada grafik
plt.title('Visualisasi Beberapa Titik pada Bidang Koordinat')

# menampilkan garis bantu dengan pola putus-putus
plt.grid(True, linestyle='--', alpha=0.7)

# menampilkan hasil grafik
plt.show()


# ================= PENGEMBANGAN =================

# mengubah jumlah dan posisi titik sesuai keinginan
titik_baru = [
    (1, 2, 'A', (1, 0, 0)),
    (3, 4, 'B', (0, 0, 1)),
    (5, 1, 'C', (0, 0.7, 0)),
    (4, 3, 'D', (1, 0.5, 0)),
    (2, 5, 'E', (0.5, 0, 0.5)),
    (5, 5, 'F', (0, 0.7, 0.7))
]

# memisahkan koordinat, label, dan warna RGB
x_baru = [t[0] for t in titik_baru]
y_baru = [t[1] for t in titik_baru]
label_baru = [t[2] for t in titik_baru]
warna_rgb = [t[3] for t in titik_baru]

# membuat bidang gambar dengan ukuran 6 x 5
plt.figure(figsize=(6, 5))

# menggambar garis penghubung antar titik
plt.plot(x_baru, y_baru, color='gray', linestyle='--')

# menggambar titik dengan ukuran dan bentuk marker berbeda
plt.scatter(
    x_baru[0], y_baru[0],
    c=[warna_rgb[0]], s=100, marker='o'
)
plt.scatter(
    x_baru[1], y_baru[1],
    c=[warna_rgb[1]], s=150, marker='s'
)
plt.scatter(
    x_baru[2], y_baru[2],
    c=[warna_rgb[2]], s=200, marker='^'
)
plt.scatter(
    x_baru[3], y_baru[3],
    c=[warna_rgb[3]], s=250, marker='D'
)
plt.scatter(
    x_baru[4], y_baru[4],
    c=[warna_rgb[4]], s=300, marker='*'
)
plt.scatter(
    x_baru[5], y_baru[5],
    c=[warna_rgb[5]], s=350, marker='P'
)

# menambahkan label dan koordinat pada setiap titik
for (xi, yi, lab, wrn) in titik_baru:
    plt.annotate(
        f'{lab}({xi}, {yi})',
        (xi, yi),
        textcoords='offset points',
        xytext=(5, 5),
        fontsize=10
    )

# mengatur batas tampilan sumbu x dan sumbu y
plt.xlim(0, 6)
plt.ylim(0, 6)

# mengatur angka pada sumbu dengan jarak satu satuan
plt.xticks(range(0, 7, 1))
plt.yticks(range(0, 7, 1))

# memberikan nama pada sumbu x dan sumbu y
plt.xlabel('X')
plt.ylabel('Y')

# memberikan judul pada grafik pengembangan
plt.title('Pengembangan Visualisasi Titik Koordinat')

# menampilkan garis bantu dengan pola putus-putus
plt.grid(True, linestyle='--', alpha=0.7)

# menyimpan hasil gambar ke file PNG
plt.savefig('grafik_pengembangan.png')

# menampilkan hasil grafik
plt.show()
