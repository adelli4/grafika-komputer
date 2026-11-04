import matplotlib.pyplot as plt

# menentukan daftar titik (vertex) yang membentuk poligon segi lima
# setiap titik terdiri dari koordinat x dan y
vertex = [(1, 1), (4, 1), (5, 3), (3, 5), (1, 3)]

# memisahkan koordinat x dan y dari setiap titik poligon
# vertex[0] ditambahkan kembali agar titik terakhir terhubung
# dengan titik pertama sehingga membentuk bangun tertutup
x = [p[0] for p in vertex + [vertex[0]]]
y = [p[1] for p in vertex + [vertex[0]]]

# membuat area gambar dengan ukuran 6 x 5 inci
plt.figure(figsize=(6, 5))

# menggambar garis yang menghubungkan setiap titik poligon
# warna biru digunakan untuk garis, marker o untuk menampilkan titik
# lw=2 digunakan untuk mengatur ketebalan garis
plt.plot(x, y, 'b-', marker='o', lw=2)

# memberikan warna pada bagian dalam atau area poligon
# alpha=0.4 digunakan untuk mengatur tingkat transparansi warna
plt.fill(x, y, 'lightskyblue', alpha=0.4)

# mengatur batas tampilan sumbu x dari 0 sampai 6
plt.xlim(0, 6)

# mengatur batas tampilan sumbu y dari 0 sampai 6
plt.ylim(0, 6)

# menampilkan garis bantu pada grafik agar koordinat mudah dilihat
plt.grid(True)

# menyamakan skala sumbu x dan y agar bentuk poligon tidak berubah
plt.gca().set_aspect('equal')

# memberikan judul pada gambar
plt.title('Poligon (Segi-Lima)')

# memberikan nama pada sumbu horizontal dan vertikal
plt.xlabel('X')
plt.ylabel('Y')

# menampilkan hasil gambar poligon ke layar
plt.show()
