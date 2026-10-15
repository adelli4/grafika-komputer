import matplotlib.pyplot as plt

# daftar poligon yang berisi nama, koordinat titik, dan warna
poligon = [
    ('Segitiga', [(1, 1), (4, 1), (2.5, 4)], 'magenta'),
    ('Persegi', [(8, 1), (11, 1), (11, 4), (8, 4)], 'orange'),
    ('Segi Lima', [(1, 7), (2, 9), (4, 9), (5, 7), (3, 6)], 'cyan'),
    ('Trapesium', [(8, 7), (12, 7), (11, 9), (9, 9)], 'purple')
]

# membuat bidang gambar
fig, ax = plt.subplots(figsize=(12, 8))

# menggambar setiap poligon
for nama, titik, warna in poligon:

    # memisahkan koordinat x dan y
    x = [p[0] for p in titik]
    y = [p[1] for p in titik]

    # menghubungkan titik terakhir ke titik pertama
    x_garis = x + [x[0]]
    y_garis = y + [y[0]]

    # menentukan ketebalan garis, jenis garis, dan marker
    if nama == 'Segitiga':
        ketebalan = 2
        gaya_garis = '--'
        marker = 'o'
    elif nama == 'Persegi':
        ketebalan = 3
        gaya_garis = '-.'
        marker = 's'
    elif nama == 'Segi Lima':
        ketebalan = 2.5
        gaya_garis = ':'
        marker = '^'
    else:
        ketebalan = 3
        gaya_garis = '-'
        marker = 'D'

    # menggambar poligon tanpa isian
    ax.plot(
        x_garis, y_garis,
        color=warna,
        linewidth=ketebalan,
        linestyle=gaya_garis,
        marker=marker,
        markersize=6,
        label=nama
    )

    # menghitung posisi nama poligon
    tengah_x = sum(x) / len(x)
    tengah_y = sum(y) / len(y)

    # menampilkan nama poligon
    ax.text(
        tengah_x, tengah_y, nama,
        fontsize=9,
        ha='center',
        va='center',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
    )

    # menampilkan label koordinat setiap titik
    for px, py in titik:
        ax.annotate(
            f'({px:g}, {py:g})',
            (px, py),
            xytext=(0, 8),
            textcoords='offset points',
            ha='center',
            fontsize=8
        )

# mengatur batas sumbu
ax.set_xlim(0, 14)
ax.set_ylim(0, 11)

# mengatur angka pada sumbu
ax.set_xticks(range(0, 15, 1))
ax.set_yticks(range(0, 12, 1))

# memberikan nama sumbu dan judul
ax.set_xlabel('Sumbu X')
ax.set_ylabel('Sumbu Y')
ax.set_title('Visualisasi Pengembangan Poligon dengan Python')

# menampilkan garis bantu
ax.grid(True, linestyle='--', alpha=0.4)

# mengatur skala sumbu agar seimbang
ax.set_aspect('equal', adjustable='box')

# menampilkan legenda di luar grafik
ax.legend(
    loc='upper left',
    bbox_to_anchor=(1.02, 1),
    frameon=True
)

# merapikan tata letak grafik
plt.tight_layout()

# menyimpan grafik dalam format png
plt.savefig(
    'hasil_poligon.png',
    dpi=300,
    bbox_inches='tight'
)

# menampilkan grafik
plt.show()