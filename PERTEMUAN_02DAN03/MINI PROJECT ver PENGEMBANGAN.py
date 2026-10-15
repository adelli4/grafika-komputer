import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon

# daftar bagian boneka yang berisi nama, bentuk, koordinat, ukuran, dan warna
bagian_boneka = [
    # telinga kiri dan kanan
    ('telinga kiri', 'lingkaran', (2.8, 6.8), 0.65, 0.65, 'saddlebrown'),
    ('telinga kanan', 'lingkaran', (5.2, 6.8), 0.65, 0.65, 'saddlebrown'),

    # bagian dalam telinga
    ('dalam telinga kiri', 'lingkaran', (2.8, 6.8), 0.32, 0.32, 'pink'),
    ('dalam telinga kanan', 'lingkaran', (5.2, 6.8), 0.32, 0.32, 'pink'),

    # kedua kaki
    ('kaki kiri', 'oval', (3.1, 1.5), 1.3, 0.9, 'saddlebrown'),
    ('kaki kanan', 'oval', (4.9, 1.5), 1.3, 0.9, 'saddlebrown'),

    # telapak kaki
    ('telapak kaki kiri', 'oval', (3.1, 1.45), 0.55, 0.35, 'pink'),
    ('telapak kaki kanan', 'oval', (4.9, 1.45), 0.55, 0.35, 'pink'),

    # kedua tangan
    ('tangan kiri', 'oval', (2.45, 3.4), 0.85, 1.7, 'saddlebrown'),
    ('tangan kanan', 'oval', (5.55, 3.4), 0.85, 1.7, 'saddlebrown'),

    # badan boneka
    ('badan', 'oval', (4, 3.0), 2.5, 3.0, 'peru'),

    # perut boneka
    ('perut', 'oval', (4, 2.9), 1.55, 1.8, 'bisque'),

    # kepala boneka
    ('kepala', 'lingkaran', (4, 5.6), 1.65, 1.65, 'peru'),

    # moncong boneka
    ('moncong', 'oval', (4, 5.1), 0.95, 0.7, 'bisque'),

    # mata kiri dan kanan
    ('mata kiri', 'lingkaran', (3.45, 5.75), 0.12, 0.12, 'black'),
    ('mata kanan', 'lingkaran', (4.55, 5.75), 0.12, 0.12, 'black'),

    # hidung boneka
    ('hidung', 'lingkaran', (4, 5.2), 0.13, 0.1, 'black'),

    # bagian tengah pita
    ('tengah pita', 'lingkaran', (4, 4.25), 0.18, 0.18, 'gold')
]

# membuat bidang gambar dengan ukuran 8 x 8
plt.figure(figsize=(8, 8))

# membuat bidang koordinat
ax = plt.gca()

# menggambar setiap bagian boneka
for nama, bentuk, posisi, ukuran_x, ukuran_y, warna in bagian_boneka:
    # mengambil koordinat tengah setiap bagian
    x, y = posisi

    # menggambar bagian berbentuk lingkaran
    if bentuk == 'lingkaran':
        ax.add_patch(Circle(
            (x, y),
            ukuran_x,
            facecolor=warna,
            edgecolor='black',
            linewidth=2,
            zorder=2
        ))

    # menggambar bagian berbentuk oval
    elif bentuk == 'oval':
        ax.add_patch(Ellipse(
            (x, y),
            ukuran_x,
            ukuran_y,
            facecolor=warna,
            edgecolor='black',
            linewidth=2,
            zorder=2
        ))

# menggambar pita bagian kiri
ax.add_patch(Polygon(
    [(3.8, 4.3), (3.0, 4.65), (3.2, 4.0)],
    closed=True,
    facecolor='turquoise',
    edgecolor='black',
    linewidth=2,
    zorder=4
))

# menggambar pita bagian kanan
ax.add_patch(Polygon(
    [(4.2, 4.3), (5.0, 4.65), (4.8, 4.0)],
    closed=True,
    facecolor='turquoise',
    edgecolor='black',
    linewidth=2,
    zorder=4
))

# menggambar hiasan bintang pada perut
ax.add_patch(Polygon(
    [
        (4, 3.5), (4.2, 3.15), (4.6, 3.1),
        (4.3, 2.85), (4.4, 2.45), (4, 2.65),
        (3.6, 2.45), (3.7, 2.85), (3.4, 3.1),
        (3.8, 3.15)
    ],
    closed=True,
    facecolor='gold',
    edgecolor='black',
    linewidth=2,
    zorder=4
))

# menggambar mulut boneka
plt.plot(
    [4, 4], [5.2, 4.95],
    color='black',
    linewidth=2,
    zorder=5
)

plt.plot(
    [4, 3.8], [4.95, 4.85],
    color='black',
    linewidth=2,
    zorder=5
)

plt.plot(
    [4, 4.2], [4.95, 4.85],
    color='black',
    linewidth=2,
    zorder=5
)

# mengatur batas tampilan sumbu x dan sumbu y
plt.xlim(1, 7)
plt.ylim(0, 8)

# mengatur angka pada sumbu
plt.xticks(range(1, 8, 1))
plt.yticks(range(0, 9, 1))

# memberikan nama pada sumbu
plt.xlabel('X')
plt.ylabel('Y')

# memberikan judul gambar
plt.title('Menggambar Boneka Beruang dari Koordinat')

# menampilkan garis bantu putus-putus
plt.grid(True, linestyle='--', alpha=0.5)

# mengatur skala sumbu agar seimbang
plt.axis('equal')

# menampilkan gambar boneka
plt.show()