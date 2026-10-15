
import matplotlib.pyplot as plt

# mengimpor fungsi Rectangle untuk membuat bentuk persegi panjang
from matplotlib.patches import Rectangle

# membuat bidang gambar dengan ukuran 8 x 6
plt.figure(figsize=(8, 6))

# membuat bidang koordinat dengan sumbu x dan y
ax = plt.gca()

# menentukan koordinat empat sudut badan rumah
badan_rumah = [(2, 0), (8, 0), (8, 4), (2, 4)]

# memisahkan koordinat x dan y dari badan rumah
x = [t[0] for t in badan_rumah]
y = [t[1] for t in badan_rumah]

# menghubungkan titik terakhir ke titik pertama
x.append(x[0])
y.append(y[0])

# menggambar badan rumah dengan garis berwarna hitam
plt.plot(x, y, color='black', linewidth=3)

# memberikan warna putih pada bagian dalam badan rumah
plt.fill(x, y, color='white')

# menentukan koordinat titik-titik atap rumah
atap = [(1.6, 3.7), (5, 7), (8.4, 3.7)]

# memisahkan koordinat x dan y dari atap rumah
x = [t[0] for t in atap]
y = [t[1] for t in atap]

# menggambar garis luar atap dengan warna hitam
plt.plot(x, y, color='black', linewidth=18)

# menggambar atap rumah dengan warna merah
plt.plot(x, y, color='red', linewidth=12)

# menentukan koordinat cerobong asap
cerobong = (6.8, 5.1, 0.8, 1.4)

# menggambar cerobong asap dengan warna merah dan garis hitam
ax.add_patch(Rectangle(
    (cerobong[0], cerobong[1]),
    cerobong[2],
    cerobong[3],
    facecolor='red',
    edgecolor='black',
    linewidth=3
))

# menggambar bagian atas cerobong asap
plt.plot(
    [6.8, 7.6], [6.5, 6.5],
    color='black',
    linewidth=3
)

# menentukan koordinat pintu rumah
pintu = (4.3, 0, 1.4, 2.4)

# menggambar pintu rumah dengan warna merah
ax.add_patch(Rectangle(
    (pintu[0], pintu[1]),
    pintu[2],
    pintu[3],
    facecolor='red',
    edgecolor='black',
    linewidth=3
))

# menentukan koordinat tiga jendela rumah
jendela = [
    (2.5, 1.4, 1.2, 1.3),
    (4.4, 4.0, 1.2, 1.2),
    (6.3, 1.4, 1.2, 1.3)
]

# menggambar setiap jendela dengan warna kuning
for x, y, lebar, tinggi in jendela:
    # membuat bingkai jendela
    ax.add_patch(Rectangle(
        (x, y),
        lebar,
        tinggi,
        facecolor='yellow',
        edgecolor='black',
        linewidth=3
    ))

    # membuat garis vertikal pada jendela
    plt.plot(
        [x + lebar / 2, x + lebar / 2],
        [y, y + tinggi],
        color='black',
        linewidth=2
    )

    # membuat garis horizontal pada jendela
    plt.plot(
        [x, x + lebar],
        [y + tinggi / 2, y + tinggi / 2],
        color='black',
        linewidth=2
    )

# menentukan koordinat gagang pintu
gagang_pintu = (4.5, 1.0)

# menggambar gagang pintu berbentuk lingkaran
plt.scatter(
    gagang_pintu[0],
    gagang_pintu[1],
    color='yellow',
    edgecolors='black',
    s=80,
    zorder=5
)

# mengatur batas tampilan sumbu x dan sumbu y
plt.xlim(0, 10)
plt.ylim(0, 8)

# mengatur angka pada sumbu dengan jarak satu satuan
plt.xticks(range(0, 11, 1))
plt.yticks(range(0, 9, 1))

# memberikan nama pada sumbu x dan sumbu y
plt.xlabel('X')
plt.ylabel('Y')

# memberikan judul pada grafik
plt.title('Menggambar Rumah dari Koordinat')

# menampilkan garis bantu dengan pola putus-putus
plt.grid(True, linestyle='--', alpha=0.5)

# mengatur skala sumbu x dan y agar seimbang
plt.axis('equal')

# menampilkan hasil gambar rumah
plt.show()