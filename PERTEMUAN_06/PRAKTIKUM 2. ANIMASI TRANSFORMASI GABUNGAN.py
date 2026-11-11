# ============================================================
# GRAFIKA KOMPUTER - PERTEMUAN 6
# PRAKTIKUM 2: ANIMASI TRANSFORMASI GEOMETRI GABUNGAN
# KONSEP: RUMAH (versi minimalis)
#
# 1. SCALING   : 1.0 -> 0.8
# 2. ROTASI    : 30 derajat
# 3. TRANSLASI : (+3, +1)
#
# URUTAN MATRIKS: M = T @ R @ S   ->   P' = M @ P
#
# python rumah_impian.py                    # tampilkan
# python rumah_impian.py --simpan rumah.gif # simpan GIF
# ============================================================

import argparse

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import to_rgb
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle, FancyBboxPatch


# ============================================================
# 1. KONFIGURASI
# ============================================================

WARNA = {
    'langit': '#B9DDF2', 'biru_tua': '#18324B', 'putih': '#FFFDF7',
    'krem': '#F6DDA8', 'atap': '#B94E43', 'hijau': '#628B69',
    'hijau_tua': '#345C49', 'rumput': '#A5BE83', 'cokelat': '#81543C',
    'kuning': '#F4C95D', 'kaca': '#8FC8D9', 'bayangan': '#29443B',
}

SKALA_AKHIR = 0.8
SUDUT_AKHIR = 30.0
GESER_AKHIR = (3.0, 1.0)

JADWAL = [('tahan', 12), ('scaling', 34), ('tahan', 8),
          ('rotasi', 34), ('tahan', 8),
          ('translasi', 34), ('tahan', 30)]
TOTAL_FRAME = sum(d for _, d in JADWAL)


# ============================================================
# 2. MATRIKS TRANSFORMASI
# ============================================================

def matriks_scaling(sx, sy):
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])


def matriks_rotasi(derajat):
    r = np.deg2rad(derajat)
    return np.array([[np.cos(r), -np.sin(r), 0],
                     [np.sin(r),  np.cos(r), 0],
                     [0, 0, 1]])


def matriks_translasi(dx, dy):
    return np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])


def matriks_gabungan(s, sudut, dx, dy):
    return matriks_translasi(dx, dy) @ matriks_rotasi(sudut) @ matriks_scaling(s, s)


def terapkan(M, titik):
    titik = np.atleast_2d(titik)
    homogen = np.column_stack([titik, np.ones(len(titik))])
    return (M @ homogen.T).T[:, :2]


def ease(t):
    return t * t * (3 - 2 * t)


def campur(a, b, t):
    a, b = np.array(to_rgb(a)), np.array(to_rgb(b))
    return tuple(a + (b - a) * t)


def hitung_keadaan(frame):
    """Mengembalikan (skala, sudut, dx, dy, tahap, progres_tahap)."""
    s, sudut, dx, dy = 1.0, 0.0, 0.0, 0.0
    tahap, p, mulai = None, 0.0, 0
    for nama, durasi in JADWAL:
        akhir = mulai + durasi
        e = 1.0 if frame >= akhir else (ease((frame - mulai) / durasi) if frame >= mulai else 0.0)
        if nama == 'scaling':
            s = 1 + (SKALA_AKHIR - 1) * e
        elif nama == 'rotasi':
            sudut = SUDUT_AKHIR * e
        elif nama == 'translasi':
            dx, dy = GESER_AKHIR[0] * e, GESER_AKHIR[1] * e
        if nama != 'tahan' and frame >= mulai:
            tahap, p = nama, e
        mulai = akhir
    return s, sudut, dx, dy, tahap, p


# ============================================================
# 3. KANVAS (penuh, tanpa margin)
# ============================================================

fig = plt.figure(figsize=(12, 8))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(-6, 6)
ax.set_ylim(-3.5, 4.5)
ax.set_aspect('equal')
ax.axis('off')

ax.add_patch(Rectangle((-6, -3.5), 12, 8, facecolor=WARNA['langit'], edgecolor='none', zorder=0))


def latar(titik, warna, z):
    ax.add_patch(Polygon(titik, facecolor=warna, edgecolor='none', zorder=z))


latar([(-6, -0.7), (-4.8, 0.15), (-3.5, -0.65), (-1.5, 0.25), (0, -0.55), (2, 0.2),
       (3.5, -0.55), (5, 0.1), (6, -0.6), (6, -3.5), (-6, -3.5)], '#91B99C', 1)
latar([(-6, -1.35), (-4.2, -0.8), (-2.5, -1.35), (-0.5, -0.85), (1.5, -1.35),
       (3.5, -0.9), (6, -1.4), (6, -3.5), (-6, -3.5)], WARNA['rumput'], 2)
latar([(-6, -2.0), (-3, -1.8), (0, -2.0), (3, -1.75), (6, -2.0),
       (6, -3.5), (-6, -3.5)], WARNA['hijau'], 3)

# matahari + sinar
PUSAT_MATAHARI = np.array([4.8, 3.3])
ax.add_patch(Circle(PUSAT_MATAHARI, 0.45, facecolor=WARNA['kuning'],
                    edgecolor='#E6A943', linewidth=2, zorder=1))
sudut_sinar = np.linspace(0, 2 * np.pi, 12, endpoint=False)
garis_sinar = [ax.plot([], [], color='#E6A943', linewidth=2, zorder=1)[0] for _ in sudut_sinar]


def perbarui_sinar(frame):
    putar, denyut = frame * 0.02, 0.04 * np.sin(frame * 0.2)
    for sd, g in zip(sudut_sinar, garis_sinar):
        a = sd + putar
        arah = np.array([np.cos(a), np.sin(a)])
        p1, p2 = PUSAT_MATAHARI + 0.57 * arah, PUSAT_MATAHARI + (0.70 + denyut) * arah
        g.set_data([p1[0], p2[0]], [p1[1], p2[1]])


# awan melayang
BAGIAN_AWAN = [(0, 0, 0.22), (0.28, 0.12, 0.30), (0.58, 0.03, 0.24), (0.32, -0.07, 0.25)]
awan_list = []


def buat_awan(x, y, skala, kecepatan):
    patches = []
    for ox, oy, r in BAGIAN_AWAN:
        c = Circle((0, 0), r * skala, facecolor=WARNA['putih'], edgecolor='none', zorder=2)
        ax.add_patch(c)
        patches.append((c, ox * skala, oy * skala))
    awan_list.append((patches, x, y, kecepatan))


buat_awan(-5.0, 2.7, 0.9, 0.012)
buat_awan(0.5, 2.9, 0.8, 0.008)
buat_awan(-2.2, 1.6, 0.6, 0.010)


def perbarui_awan(frame):
    for patches, x0, y, v in awan_list:
        x = (x0 + 7 + v * frame * 3) % 15 - 7
        for c, ox, oy in patches:
            c.center = (x + ox, y + oy)


def buat_pohon(x, y, s):
    ax.add_patch(Polygon([(x - .09 * s, y - .75 * s), (x + .09 * s, y - .75 * s),
                          (x + .09 * s, y + .05 * s), (x - .09 * s, y + .05 * s)],
                         facecolor=WARNA['cokelat'], edgecolor='none', zorder=4))
    for ox, oy, r in [(0, .15, .38), (-.25, -.05, .28), (.25, -.05, .28)]:
        ax.add_patch(Circle((x + ox * s, y + oy * s), r * s, facecolor=WARNA['hijau_tua'],
                            edgecolor='#456E50', linewidth=1, zorder=5))


buat_pohon(-4.7, -0.8, 1.1)
buat_pohon(5.0, -0.9, 0.95)
buat_pohon(-3.5, -1.25, 0.65)


# ============================================================
# 4. OBJEK RUMAH
# ============================================================

def persegi(x1, y1, x2, y2):
    return np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]])


BAGIAN = [
    ('cerobong',  persegi(0.48, 0.92, 0.78, 1.55),    WARNA['cokelat']),
    ('badan',     persegi(-1.0, -1.0, 1.0, 0.5),      WARNA['krem']),
    ('papan',     persegi(-1.08, -1.02, 1.08, -0.91), WARNA['cokelat']),
    ('atap',      np.array([[-1.25, .5], [0, 1.55], [1.25, .5]]), WARNA['atap']),
    ('pintu',     persegi(-0.28, -1.0, 0.28, -0.12),  WARNA['cokelat']),
    ('jendela_k', persegi(-0.83, -0.05, -0.43, 0.34), WARNA['kaca']),
    ('jendela_n', persegi(0.43, -0.05, 0.83, 0.34),   WARNA['kaca']),
]
GARIS_DETAIL = [
    np.array([[-1.0, 0.55], [0.0, 1.39], [1.0, 0.55]]),
    np.array([[-0.63, -0.05], [-0.63, 0.34]]), np.array([[-0.83, 0.145], [-0.43, 0.145]]),
    np.array([[0.63, -0.05], [0.63, 0.34]]),   np.array([[0.43, 0.145], [0.83, 0.145]]),
]
GAGANG = np.array([[0.18, -0.57]])
TITIK_BAYANGAN = np.array([[0.0, -1.18]])
CEROBONG_ATAS = np.array([[0.63, 1.58]])

bayangan = Ellipse((0, -1.18), 2.8, 0.24, facecolor=WARNA['bayangan'],
                   edgecolor='none', alpha=0.4, zorder=6)
ax.add_patch(bayangan)

JUMLAH_ASAP = 5
asap = []
for _ in range(JUMLAH_ASAP):
    c = Circle((0, 0), 0.05, facecolor='#F2F2F2', edgecolor='none', zorder=6)
    ax.add_patch(c)
    asap.append(c)

objek_bagian = {}
for nama, titik, warna in BAGIAN:
    p = Polygon(titik, closed=True, facecolor=warna, edgecolor=WARNA['putih'],
                linewidth=2, joinstyle='round', zorder=7)
    ax.add_patch(p)
    objek_bagian[nama] = p

objek_garis = [ax.plot(g[:, 0], g[:, 1], color=WARNA['putih'], linewidth=2,
                       solid_capstyle='round', zorder=9)[0] for g in GARIS_DETAIL]
objek_gagang = Circle(tuple(GAGANG[0]), 0.045, facecolor=WARNA['kuning'], edgecolor='none', zorder=10)
ax.add_patch(objek_gagang)

# frame saat translasi selesai (lampu tetap menyala)
_t = 0
for _n, _d in JADWAL:
    _t += _d
    if _n == 'translasi':
        FRAME_TIBA = _t
        break


# ============================================================
# 5. KETERANGAN MINIMAL: satu baris + bilah progres
# ============================================================

teks_info = ax.text(0, -2.85, '', ha='center', va='center', fontsize=14,
                    fontweight='bold', color=WARNA['putih'], zorder=12)
ax.add_patch(FancyBboxPatch((-1.8, -3.25), 3.6, 0.1, boxstyle='round,pad=0,rounding_size=0.05',
                            facecolor='#2C4A66', edgecolor='none', zorder=11))
bilah = FancyBboxPatch((-1.8, -3.25), 0.001, 0.1, boxstyle='round,pad=0,rounding_size=0.05',
                       facecolor=WARNA['kuning'], edgecolor='none', zorder=12)
ax.add_patch(bilah)


def keterangan(tahap, s, sudut, dx, dy):
    if tahap == 'scaling':
        return f'SCALING   {s:.2f}×'
    if tahap == 'rotasi':
        return f'ROTASI   {sudut:.0f}°'
    if tahap == 'translasi':
        return f'TRANSLASI   ({dx:.1f}, {dy:.1f})'
    return ''


# ============================================================
# 6. UPDATE
# ============================================================

def update(frame):
    s, sudut, dx, dy, tahap, p = hitung_keadaan(frame)
    M = matriks_gabungan(s, sudut, dx, dy)

    for nama, titik, _ in BAGIAN:
        objek_bagian[nama].set_xy(terapkan(M, titik))
    for garis, g in zip(objek_garis, GARIS_DETAIL):
        h = terapkan(M, g)
        garis.set_data(h[:, 0], h[:, 1])

    objek_gagang.center = tuple(terapkan(M, GAGANG)[0])
    objek_gagang.radius = 0.045 * s
    bayangan.center = tuple(terapkan(M, TITIK_BAYANGAN)[0])
    bayangan.width, bayangan.height = 2.8 * s, 0.24 * s

    # jendela menyala saat rumah tiba
    nyala = ease(p) if tahap == 'translasi' and frame < FRAME_TIBA else (1.0 if frame >= FRAME_TIBA else 0.0)
    w = campur(WARNA['kaca'], WARNA['kuning'], nyala)
    objek_bagian['jendela_k'].set_facecolor(w)
    objek_bagian['jendela_n'].set_facecolor(w)

    # asap
    for i, c in enumerate(asap):
        fase = (frame * 0.025 + i / JUMLAH_ASAP) % 1
        lokal = CEROBONG_ATAS + [0.12 * np.sin(fase * 6 + i), 0.7 * fase]
        c.center = tuple(terapkan(M, lokal)[0])
        c.radius = (0.06 + 0.14 * fase) * s
        c.set_alpha(0.75 * (1 - fase))

    perbarui_sinar(frame)
    perbarui_awan(frame)

    teks_info.set_text(keterangan(tahap, s, sudut, dx, dy))
    bilah.set_width(max(3.6 * frame / (TOTAL_FRAME - 1), 0.001))


# ============================================================
# 7. JALANKAN / SIMPAN
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Animasi Transformasi Gabungan')
    parser.add_argument('--simpan', metavar='FILE.gif', help='simpan animasi sebagai GIF')
    args = parser.parse_args()

    ani = animation.FuncAnimation(fig, update, frames=TOTAL_FRAME, interval=40,
                                  blit=False, repeat=True)
    if args.simpan:
        ani.save(args.simpan, writer=animation.PillowWriter(fps=25), dpi=80)
        print(f'Tersimpan: {args.simpan}')
    else:
        plt.show()