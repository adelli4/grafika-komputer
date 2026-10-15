import matplotlib.pyplot as plt

# daftar poligon yang berisi nama, koordinat titik, dan warna
poligon = [
    ('Telinga kiri', [(2, 6), (2.3, 7), (3.2, 6.5), (3, 5.8)], 'saddlebrown'),
    ('Telinga kanan', [(5, 6.5), (5.9, 7), (6.2, 6), (5.2, 5.8)], 'saddlebrown'),

    ('Kepala', [(2.5, 5.8), (2.2, 5), (2.5, 4.3),
                (3.5, 4), (4.5, 4.3), (4.8, 5),
                (4.5, 5.8), (3.5, 6.2)], 'peru'),

    ('Badan', [(2.8, 3.8), (2.3, 2.5), (2.8, 1.5),
               (4.2, 1.5), (4.7, 2.5), (4.2, 3.8)], 'peru'),

    ('Tangan kiri', [(2.7, 3.5), (1.8, 3.2),
                     (1.3, 2.5), (1.8, 2.2),
                     (2.5, 2.8)], 'saddlebrown'),

    ('Tangan kanan', [(4.3, 3.5), (5.2, 3.2),
                      (5.7, 2.5), (5.2, 2.2),
                      (4.5, 2.8)], 'saddlebrown'),

    ('Kaki kiri', [(2.8, 1.8), (2.2, 1.2),
                   (2.3, 0.7), (3.5, 0.7),
                   (3.6, 1.5)], 'saddlebrown'),

    ('Kaki kanan', [(3.5, 1.5), (3.7, 0.7),
                    (4.8, 0.7), (4.9, 1.2),
                    (4.2, 1.8)], 'saddlebrown'),

    ('Moncong', [(3, 4.8), (3.2, 4.4),
                 (3.8, 4.4), (4, 4.8),
                 (3.5, 5)], 'bisque'),

    ('Hidung', [(3.35, 4.85), (3.65, 4.85),
                (3.5, 4.65)], 'black'),

    ('Pita kiri', [(3.1, 4), (2.6, 4.3),
                   (2.7, 3.8)], 'turquoise'),

    ('Pita kanan', [(3.9, 4), (4.4, 4.3),
                    (4.3, 3.8)], 'turquoise'),

    ('Perut', [(3, 3.2), (2.9, 2.5),
               (3.5, 2.2), (4.1, 2.5),
               (4, 3.2)], 'bisque'),

    ('Bintang', [(3.5, 3.1), (3.65, 2.8),
                 (4, 2.75), (3.75, 2.5),
                 (3.8, 2.2), (3.5, 2.35),
                 (3.2, 2.2), (3.25, 2.5),
                 (3, 2.75), (3.35, 2.8)], 'gold')
]

# membuat bidang gambar dengan ukuran 8 x 8
plt.figure(figsize=(8, 8))

# menggambar setiap poligon berdasarkan koordinat dan warna
for nama, titik, warna in poligon:
    # memisahkan koordinat x dan y dari setiap titik
    x = [p[0] for p in titik]
    y = [p[1] for p in titik]

    # menghubungkan titik terakhir ke titik pertama
    x.append(x[0])
    y.append(y[0])

    # menggambar garis luar setiap bagian boneka
    plt.plot(x, y, color='black', linewidth=2)

    # memberikan warna pada bagian dalam poligon
    plt.fill(x, y, color=warna, alpha=0.9)

# menggambar mata kiri dan kanan
plt.scatter(
    [3.1, 3.9], [5.3, 5.3],
    color='black', s=50, zorder=5
)

# menggambar mulut boneka
plt.plot(
    [3.5, 3.5, 3.3],
    [4.65, 4.5, 4.45],
    color='black', linewidth=2
)

plt.plot(
    [3.5, 3.7],
    [4.5, 4.45],
    color='black', linewidth=2
)

# mengatur batas tampilan sumbu x dan sumbu y
plt.xlim(0, 7)
plt.ylim(0, 8)

# mengatur angka pada sumbu dengan jarak satu satuan
plt.xticks(range(0, 8, 1))
plt.yticks(range(0, 9, 1))

# memberikan nama pada sumbu x dan sumbu y
plt.xlabel('X')
plt.ylabel('Y')

# memberikan judul pada grafik
plt.title('Menggambar Boneka dari Koordinat')

# menampilkan garis bantu dengan pola putus-putus
plt.grid(True, linestyle='--', alpha=0.5)

# mengatur skala sumbu x dan y agar seimbang
plt.axis('equal')

# menampilkan hasil gambar
plt.show()
