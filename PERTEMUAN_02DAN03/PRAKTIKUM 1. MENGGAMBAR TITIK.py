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