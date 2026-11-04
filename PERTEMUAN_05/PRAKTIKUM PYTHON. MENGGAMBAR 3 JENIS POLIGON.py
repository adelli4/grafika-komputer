import matplotlib.pyplot as plt

# menentukan daftar titik (vertex) yang membentuk poligon segitiga
# setiap titik terdiri dari koordinat x dan y
segitiga = [(1, 1), (3, 4), (5, 1)]

# menentukan daftar titik (vertex) yang membentuk poligon persegi
persegi = [(1, 1), (1, 5), (5, 5), (5, 1)]

# menentukan daftar titik (vertex) yang membentuk poligon segi enam
segi_enam = [(3, 1), (5, 2), (5, 4), (3, 5), (1, 4), (1, 2)]


# menggambar poligon segitiga

# memisahkan koordinat x dan y dari setiap titik segitiga
# titik pertama ditambahkan kembali agar garis poligon tertutup
x = [p[0] for p in segitiga + [segitiga[0]]]
y = [p[1] for p in segitiga + [segitiga[0]]]

# membuat area gambar dengan ukuran 12 x 4 inci
plt.figure(figsize=(12, 4))

# membagi area gambar menjadi 1 baris dan 3 kolom
# gambar segitiga ditempatkan pada posisi pertama
plt.subplot(1, 3, 1)

# menggambar garis yang menghubungkan setiap titik segitiga
# warna biru digunakan untuk garis dan lingkaran kecil sebagai penanda titik
# lw=2 digunakan untuk mengatur ketebalan garis
plt.plot(x, y, 'b-', marker='o', lw=2)

# memberikan warna biru muda pada bagian dalam segitiga
# alpha=0.4 digunakan untuk mengatur tingkat transparansi warna
plt.fill(x, y, 'lightskyblue', alpha=0.4)

# memberikan judul pada gambar segitiga
plt.title('Segitiga')

# mengatur batas tampilan sumbu x dan y
plt.xlim(0, 6)
plt.ylim(0, 6)

# menampilkan garis bantu pada grafik
plt.grid(True)

# menyamakan skala sumbu x dan y agar bentuk tidak berubah
plt.gca().set_aspect('equal')


# menggambar poligon persegi

# memisahkan koordinat x dan y dari setiap titik persegi
# titik pertama ditambahkan kembali agar garis poligon tertutup
x = [p[0] for p in persegi + [persegi[0]]]
y = [p[1] for p in persegi + [persegi[0]]]

# menempatkan gambar persegi pada posisi kedua
plt.subplot(1, 3, 2)

# menggambar garis yang menghubungkan setiap titik persegi
plt.plot(x, y, 'b-', marker='o', lw=2)

# memberikan warna hijau muda pada bagian dalam persegi
plt.fill(x, y, 'lightgreen', alpha=0.4)

# memberikan judul pada gambar persegi
plt.title('Persegi')

# mengatur batas tampilan sumbu x dan y
plt.xlim(0, 6)
plt.ylim(0, 6)

# menampilkan garis bantu pada grafik
plt.grid(True)

# menyamakan skala sumbu x dan y agar bentuk tidak berubah
plt.gca().set_aspect('equal')


# menggambar poligon segi enam

# memisahkan koordinat x dan y dari setiap titik segi enam
# titik pertama ditambahkan kembali agar garis poligon tertutup
x = [p[0] for p in segi_enam + [segi_enam[0]]]
y = [p[1] for p in segi_enam + [segi_enam[0]]]

# menempatkan gambar segi enam pada posisi ketiga
plt.subplot(1, 3, 3)

# menggambar garis yang menghubungkan setiap titik segi enam
plt.plot(x, y, 'b-', marker='o', lw=2)

# memberikan warna merah muda pada bagian dalam segi enam
plt.fill(x, y, 'lightpink', alpha=0.4)

# memberikan judul pada gambar segi enam
plt.title('Segi-Enam')

# mengatur batas tampilan sumbu x dan y
plt.xlim(0, 6)
plt.ylim(0, 6)

# menampilkan garis bantu pada grafik
plt.grid(True)

# menyamakan skala sumbu x dan y agar bentuk tidak berubah
plt.gca().set_aspect('equal')


# mengatur jarak antar gambar agar tampil lebih rapi
plt.tight_layout()

# menyimpan hasil gambar ketiga poligon ke dalam file png
plt.savefig('hasil_poligon.png')

# menampilkan seluruh hasil gambar poligon ke layar
plt.show()

# KESIMPULAN
# kerapatan titik pada poligon dipengaruhi oleh jumlah titik vertex
# dan jarak antar titik koordinat yang digunakan.
# semakin banyak titik vertex, semakin banyak titik sudut
# yang membentuk poligon.
# bentuk poligon juga dipengaruhi oleh posisi setiap titik koordinat.
# semakin dekat jarak antar titik, semakin pendek garis penghubungnya.
# ukuran titik dan skala grafik memengaruhi tampilan poligon.