# ============================================================
# PRAKTIKUM 1: ANIMASI TRANSLASI DAN ROTASI
# MEMBUAT BOLA BERGERAK DAN RODA BERPUTAR
# GRAFIKA KOMPUTER - PERTEMUAN 6
# ============================================================


# 1. mengimpor library
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.patches import Circle, Ellipse


# ============================================================
# 2. konfigurasi area animasi
# ============================================================

fig, ax = plt.subplots(figsize=(12, 7))

# mengatur warna latar belakang
fig.patch.set_facecolor('#0b1220')
ax.set_facecolor('#111c2e')

# mengatur batas area gambar
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.set_aspect('equal')
ax.axis('off')

# mengatur tata letak gambar
fig.subplots_adjust(
    left=0.04,
    right=0.96,
    top=0.87,
    bottom=0.08
)


# ============================================================
# 3. membuat judul dan keterangan animasi
# ============================================================

fig.text(
    0.5, 0.94,
    'ANIMASI TRANSFORMASI GEOMETRI',
    ha='center',
    fontsize=21,
    fontweight='bold',
    color='white'
)

fig.text(
    0.5, 0.895,
    'PRAKTIKUM 1: TRANSLASI DAN ROTASI 2D',
    ha='center',
    fontsize=11,
    color='#38bdf8'
)

# judul bagian translasi
ax.text(
    3, 6.1,
    '01 | ANIMASI TRANSLASI',
    ha='center',
    color='#f87171',
    fontsize=13,
    fontweight='bold'
)

# judul bagian rotasi
ax.text(
    9, 6.1,
    '02 | ANIMASI ROTASI',
    ha='center',
    color='#38bdf8',
    fontsize=13,
    fontweight='bold'
)


# ============================================================
# 4. membuat objek bola untuk translasi
# ============================================================

# membuat garis lintasan bola
ax.plot(
    [0.8, 5.3],
    [4.4, 4.4],
    color='#475569',
    linestyle='--',
    linewidth=1.5
)

# membuat tanda pada lintasan bola
for posisi in np.linspace(1, 5.2, 12):
    ax.plot(
        [posisi, posisi],
        [4.32, 4.48],
        color='#64748b',
        linewidth=0.8
    )

# membuat bayangan bola
bayangan = Ellipse(
    (1, 4.05),
    width=0.7,
    height=0.13,
    color='black',
    alpha=0.35
)

ax.add_patch(bayangan)

# membuat badan bola
bola = Circle(
    (1, 4.4),
    radius=0.27,
    facecolor='#ef2929',
    edgecolor='#ff7777',
    linewidth=2
)

ax.add_patch(bola)

# membuat efek cahaya pada bola
cahaya_bola = Circle(
    (0.91, 4.51),
    radius=0.075,
    facecolor='white',
    edgecolor='none',
    alpha=0.85
)

ax.add_patch(cahaya_bola)

# membuat jejak pergerakan bola
jejak_bola, = ax.plot(
    [],
    [],
    color='#fb7185',
    linewidth=3,
    alpha=0.65
)


# ============================================================
# 5. membuat objek roda untuk rotasi
# ============================================================

# menentukan titik pusat dan ukuran roda
pusat_x = 9
pusat_y = 3.5
radius = 1.35

# membuat ban luar roda
ban = Circle(
    (pusat_x, pusat_y),
    radius,
    facecolor='#202b3b',
    edgecolor='#94a3b8',
    linewidth=9
)

ax.add_patch(ban)

# membuat lingkaran velg
velg = Circle(
    (pusat_x, pusat_y),
    1.12,
    facecolor='#64748b',
    edgecolor='#e2e8f0',
    linewidth=3
)

ax.add_patch(velg)

# membuat lingkaran bagian dalam roda
lingkaran_dalam = Circle(
    (pusat_x, pusat_y),
    0.92,
    facecolor='#253449',
    edgecolor='#cbd5e1',
    linewidth=2
)

ax.add_patch(lingkaran_dalam)

# membuat poros roda
poros = Circle(
    (pusat_x, pusat_y),
    0.22,
    facecolor='#94a3b8',
    edgecolor='white',
    linewidth=2
)

ax.add_patch(poros)

# membuat titik pusat roda
titik_pusat = Circle(
    (pusat_x, pusat_y),
    0.08,
    facecolor='#e2e8f0',
    edgecolor='white'
)

ax.add_patch(titik_pusat)


# ============================================================
# 6. membuat jeruji dan baut roda
# ============================================================

# menentukan jumlah jeruji roda
jumlah_jeruji = 8

# menentukan sudut awal setiap jeruji
sudut_awal = np.linspace(
    0,
    2 * np.pi,
    jumlah_jeruji,
    endpoint=False
)

# membuat garis jeruji roda
jeruji = []

for sudut in sudut_awal:

    garis, = ax.plot(
        [
            pusat_x + 0.18 * np.cos(sudut),
            pusat_x + 1.08 * np.cos(sudut)
        ],
        [
            pusat_y + 0.18 * np.sin(sudut),
            pusat_y + 1.08 * np.sin(sudut)
        ],
        color='#e2e8f0',
        linewidth=4,
        solid_capstyle='round'
    )

    jeruji.append(garis)


# membuat baut yang ikut berputar
jumlah_baut = 8

sudut_baut = np.linspace(
    0,
    2 * np.pi,
    jumlah_baut,
    endpoint=False
)

baut_roda = []

for sudut in sudut_baut:

    baut = Circle(
        (
            pusat_x + 0.72 * np.cos(sudut),
            pusat_y + 0.72 * np.sin(sudut)
        ),
        0.045,
        facecolor='#f8fafc',
        edgecolor='#64748b',
        linewidth=0.8
    )

    ax.add_patch(baut)
    baut_roda.append(baut)


# ============================================================
# 7. membuat informasi animasi
# ============================================================

# informasi posisi bola
info_bola = ax.text(
    3,
    3.35,
    '',
    color='#fca5a5',
    fontsize=11,
    ha='center',
    fontweight='bold'
)

# informasi sudut roda
info_roda = ax.text(
    9,
    1.65,
    '',
    color='#7dd3fc',
    fontsize=11,
    ha='center',
    fontweight='bold'
)

# keterangan gerakan bola
ax.text(
    3,
    2.85,
    'arah gerakan: dari kiri ke kanan',
    color='#94a3b8',
    fontsize=10,
    ha='center'
)

# keterangan gerakan roda
ax.text(
    9,
    1.25,
    'arah gerakan: berputar pada titik pusat',
    color='#94a3b8',
    fontsize=10,
    ha='center'
)

# keterangan rumus translasi
ax.text(
    3,
    2.35,
    'translasi: (x + dx, y)',
    color='#fca5a5',
    fontsize=10,
    ha='center'
)

# keterangan rumus rotasi
ax.text(
    9,
    0.85,
    'rotasi: sudut awal + perubahan sudut',
    color='#7dd3fc',
    fontsize=10,
    ha='center'
)


# ============================================================
# 8. membuat fungsi untuk memperbarui animasi
# ============================================================

def update(frame):

    # ----------------------------------------
    # a. proses translasi bola
    # ----------------------------------------

    # menghitung posisi horizontal bola
    progress = frame / 119

    x = 1 + progress * 4

    # memperbarui posisi badan bola
    bola.center = (x, 4.4)

    # memperbarui posisi cahaya bola
    cahaya_bola.center = (x - 0.09, 4.51)

    # memperbarui posisi bayangan bola
    bayangan.center = (x, 4.05)

    # membuat jejak pergerakan bola
    posisi_jejak = np.linspace(
        max(0.8, x - 0.9),
        x,
        20
    )

    jejak_bola.set_data(
        posisi_jejak,
        np.full_like(posisi_jejak, 4.4)
    )

    # memperbarui informasi posisi bola
    info_bola.set_text(
        f'posisi bola: x = {x:.2f}'
    )


    # ----------------------------------------
    # b. proses rotasi roda
    # ----------------------------------------

    # menghitung perubahan sudut dalam radian
    theta = np.deg2rad(frame * 5)

    # memperbarui posisi setiap jeruji
    for i, garis in enumerate(jeruji):

        sudut = sudut_awal[i] + theta

        x1 = pusat_x + 0.18 * np.cos(sudut)
        y1 = pusat_y + 0.18 * np.sin(sudut)

        x2 = pusat_x + 1.08 * np.cos(sudut)
        y2 = pusat_y + 1.08 * np.sin(sudut)

        garis.set_data(
            [x1, x2],
            [y1, y2]
        )

    # memperbarui posisi baut agar ikut berputar
    for i, baut in enumerate(baut_roda):

        sudut = sudut_baut[i] + theta

        x_baut = pusat_x + 0.72 * np.cos(sudut)
        y_baut = pusat_y + 0.72 * np.sin(sudut)

        baut.center = (x_baut, y_baut)

    # menghitung sudut rotasi dalam derajat
    sudut_derajat = (frame * 5) % 360

    # memperbarui informasi sudut roda
    info_roda.set_text(
        f'sudut rotasi: {sudut_derajat:.0f} derajat'
    )

    # mengembalikan seluruh objek yang diperbarui
    return (
        [bola, cahaya_bola, bayangan, jejak_bola,
         info_bola, info_roda]
        + jeruji
        + baut_roda
    )


# ============================================================
# 9. menjalankan animasi
# ============================================================

ani = animation.FuncAnimation(
    fig,
    update,
    frames=120,
    interval=40,
    blit=False,
    repeat=True
)


# ============================================================
# 10. menampilkan hasil animasi
# ============================================================

plt.show()

