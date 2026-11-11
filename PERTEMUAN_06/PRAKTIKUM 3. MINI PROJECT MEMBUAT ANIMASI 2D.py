# ============================================================
# MINI PROJECT - ANIMASI 2D
#
# Transformasi yang dipakai (koordinat homogen 3x3):
#   SCALING   : lonceng ubur-ubur berdenyut (mengembang & mengerut)
#   ROTASI    : badan miring mengikuti gerak, rumput laut bergoyang
#   TRANSLASI : ubur-ubur melayang naik-turun, gelembung & plankton naik
#   REFLEKSI  : kembaran cermin (sumbu Y) untuk ubur-ubur & dekorasi
#
# Ubur-ubur  : M       = T @ R @ S
# Kembarannya: M_cermin = F @ T @ R @ S     (F = matriks refleksi terhadap sumbu Y)
#
# Durasi : 300 frame pada 30 FPS = 10 detik (loop mulus, memenuhi >= 150 frame)
#
# PEMETAAN KE KRITERIA PENILAIAN
#   1. Penerapan transformasi (4 jenis > min. 2) -> bagian 1 & kelas Ubur/Rumput
#   2. Kreativitas & desain : laut malam, ubur-ubur kembar cermin, cahaya, partikel
#   3. Kerapian & kebenaran kode : fungsi matriks terpisah, konstanta di atas, komentar
#   4. Kualitas hasil : 30 FPS, 10 detik, gerak periodik sehingga mengulang mulus
#
# ============================================================

import argparse
import io
import os
import shutil
import subprocess

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap, to_rgba, to_rgb
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle
from PIL import Image   # ikut terpasang bersama matplotlib

# ---------- pengaturan animasi ----------
N_FRAME = 300                 # jumlah frame (>= 150 sesuai ketentuan)
FPS = 30                      # frame per detik
DURASI = N_FRAME / FPS        # = 10 detik (ketentuan: 5-10 detik)
assert N_FRAME >= 150 and 5 <= DURASI <= 10, 'Durasi/frame tidak sesuai ketentuan'

# ---------- pengaturan penyimpanan ----------
DPI_SIMPAN = 80               # 12x8 inci x 80 dpi = 960x640 piksel
SKALA_GIF = 0.75              # GIF dikecilkan agar ukuran file lebih ringan
WARNA_GIF = 200               # jumlah warna palet GIF

# ---------- parameter transformasi ----------
DENYUT_PER_LOOP = 5           # banyak denyut lonceng dalam 1 loop  (SCALING)
AMP_SKALA_X, AMP_SKALA_Y = 0.10, 0.16   # seberapa kuat lonceng mengerut/mengembang
SUDUT_MIRING = 14             # derajat kemiringan badan             (ROTASI)
SUDUT_RUMPUT = 7              # derajat goyangan rumput laut         (ROTASI)


# ============================================================
# 1. MATRIKS TRANSFORMASI
# ============================================================

def matriks_scaling(sx, sy):
    """Matriks scaling 3x3: memperbesar/memperkecil terhadap titik asal."""
    return np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])


def matriks_rotasi(derajat):
    """Matriks rotasi 3x3: memutar berlawanan arah jarum jam terhadap titik asal."""
    r = np.deg2rad(derajat)
    return np.array([[np.cos(r), -np.sin(r), 0],
                     [np.sin(r),  np.cos(r), 0],
                     [0, 0, 1]])


def matriks_translasi(dx, dy):
    """Matriks translasi 3x3: menggeser sejauh (dx, dy)."""
    return np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])


# refleksi terhadap sumbu Y (x -> -x)
F = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]])


def terapkan(M, titik):
    """Terapkan matriks homogen M (3x3) pada array titik (N x 2) -> (N x 2)."""
    titik = np.atleast_2d(titik)
    homogen = np.column_stack([titik, np.ones(len(titik))])
    return (M @ homogen.T).T[:, :2]


# ============================================================
# 2. KANVAS & LATAR LAUT
# ============================================================

fig = plt.figure(figsize=(12, 8))
fig.patch.set_facecolor('#04162B')
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

# gradasi laut: gelap di dasar, lebih terang di permukaan
peta = LinearSegmentedColormap.from_list('laut', ['#020B18', '#06213B', '#0C4468'])
gradasi = peta(np.linspace(0, 1, 256))[::-1][:, None, :]
ax.imshow(gradasi, extent=[-6, 6, -4, 4], aspect='auto', zorder=0)
ax.set_xlim(-6, 6)
ax.set_ylim(-4, 4)
ax.set_aspect('equal')

rng = np.random.default_rng(7)

# --- berkas cahaya dari permukaan (simetris kiri-kanan)
posisi_sinar = [0.0, 2.0, 4.0]
sinar = []
for i, x0 in enumerate(posisi_sinar):
    for cermin in ([False] if x0 == 0 else [False, True]):
        p = Polygon(np.zeros((4, 2)), facecolor='white', edgecolor='none',
                    alpha=0.06, zorder=1)
        ax.add_patch(p)
        sinar.append((p, x0, i, cermin))


def perbarui_sinar(t):
    for p, x0, i, cermin in sinar:
        geser = 0.5 * np.sin(2 * np.pi * t + i)
        lebar = 0.35 + 0.1 * i
        pts = np.array([[x0 - lebar, 4], [x0 + lebar, 4],
                        [x0 + 1.2 + geser, -3.4], [x0 - 1.2 + geser, -3.4]])
        if cermin:
            pts = terapkan(F, pts)
        p.set_xy(pts)


# --- dasar laut (setengah kanan lalu dicerminkan)
def dasar(titik, warna, z):
    kanan = np.array(titik, dtype=float)
    for pts in (kanan, terapkan(F, kanan)):
        ax.add_patch(Polygon(pts, facecolor=warna, edgecolor='none', zorder=z))


dasar([(0, -4), (0, -3.0), (1, -2.95), (2.2, -2.7), (3.5, -3.05),
       (4.8, -2.8), (6, -3.1), (6, -4)], '#0A2A3F', 3)
dasar([(0, -4), (0, -3.5), (1.5, -3.4), (3, -3.55), (4.5, -3.35),
       (6, -3.5), (6, -4)], '#061A2B', 6)


# --- rumput laut (rotasi bergoyang), kanan + kembaran cermin
class Rumput:
    """Rumput laut yang bergoyang (rotasi). cermin=True -> versi refleksi sumbu Y."""

    def __init__(self, x, tinggi, fase, cermin):
        self.x, self.tinggi, self.fase, self.cermin = x, tinggi, fase, cermin
        self.s = np.linspace(0, 1, 14)
        self.garis, = ax.plot([], [], color='#1F8A70', linewidth=6,
                              solid_capstyle='round', alpha=0.9, zorder=4)

    def perbarui(self, t):
        s = self.s
        lokal = np.column_stack([
            0.12 * s ** 2 * np.sin(2 * np.pi * 2 * t - 3 * s + self.fase),
            self.tinggi * s])
        # ROTASI di pangkal batang + TRANSLASI ke dasar laut
        M = matriks_translasi(self.x, -3.1) @ matriks_rotasi(SUDUT_RUMPUT * np.sin(2 * np.pi * 2 * t + self.fase))
        if self.cermin:
            M = F @ M
        h = terapkan(M, lokal)
        self.garis.set_data(h[:, 0], h[:, 1])


rumput = []
for x, tg, fs in [(0.9, 1.1, 0.0), (1.5, 1.6, 1.3), (2.6, 0.9, 2.4),
                  (3.8, 1.5, 0.7), (5.0, 1.2, 1.9), (5.6, 0.8, 3.1)]:
    rumput += [Rumput(x, tg, fs, False), Rumput(x, tg, fs, True)]


# ============================================================
# 3. UBUR-UBUR
# ============================================================

def bentuk_lonceng(r=0.9, h=0.7, n=36):
    th = np.linspace(0, np.pi, n)
    atas = np.column_stack([r * np.cos(th), h * np.sin(th)])
    xs = np.linspace(-r, r, 14)
    bawah = np.column_stack([xs, 0.05 * np.cos(xs * 9)])
    return np.vstack([atas, bawah])


LONCENG = bentuk_lonceng()
DALAM = LONCENG * [0.68, 0.7] + [0, 0.08]
th_halo = np.linspace(0, 2 * np.pi, 40)
HALO = np.column_stack([1.25 * np.cos(th_halo), 0.95 * np.sin(th_halo) + 0.2])
S_TENT = np.linspace(0, 1, 18)


class Ubur:
    """Satu ubur-ubur. Jika cermin=True, hasil transformasi direfleksikan terhadap sumbu Y."""

    def __init__(self, warna, skala, cx, cy, amp_x, amp_y, fase, z, alpha, cermin):
        self.skala, self.cx, self.cy = skala, cx, cy
        self.amp_x, self.amp_y, self.fase = amp_x, amp_y, fase
        self.cermin = cermin
        terang = tuple(np.array(to_rgb(warna)) * 0.5 + 0.5)

        self.halo = Polygon(HALO, facecolor=to_rgba(warna, 0.07 * alpha),
                            edgecolor='none', zorder=z)
        self.lonceng = Polygon(LONCENG, facecolor=to_rgba(warna, 0.55 * alpha),
                               edgecolor=to_rgba(terang, 0.9 * alpha),
                               linewidth=1.6, joinstyle='round', zorder=z + 2)
        self.dalam = Polygon(DALAM, facecolor=to_rgba(terang, 0.45 * alpha),
                             edgecolor='none', zorder=z + 3)
        for p in (self.halo, self.lonceng, self.dalam):
            ax.add_patch(p)

        # tentakel tipis
        self.tentakel = []
        for i, x0 in enumerate(np.linspace(-0.7, 0.7, 6)):
            g, = ax.plot([], [], color=warna, linewidth=1.5, alpha=0.7 * alpha,
                         solid_capstyle='round', zorder=z + 1)
            self.tentakel.append((g, x0, 1.2 + 0.35 * ((i * 7) % 4) / 3, i))
        # lengan mulut lebih tebal
        self.lengan = []
        for i, x0 in enumerate([-0.25, 0.0, 0.25]):
            g, = ax.plot([], [], color=terang, linewidth=3.5, alpha=0.65 * alpha,
                         solid_capstyle='round', zorder=z + 1)
            self.lengan.append((g, x0, 0.75 + 0.15 * i, i))

    def perbarui(self, t):
        p = np.sin(2 * np.pi * DENYUT_PER_LOOP * t + self.fase)
        sx = self.skala * (1 - AMP_SKALA_X * p)               # SCALING
        sy = self.skala * (1 + AMP_SKALA_Y * p)
        px = self.cx + self.amp_x * np.sin(2 * np.pi * t + self.fase)        # TRANSLASI
        py = (self.cy + self.amp_y * np.sin(2 * np.pi * 2 * t + self.fase * 0.5)
              + 0.06 * self.skala * np.cos(2 * np.pi * 5 * t + self.fase))
        tilt = SUDUT_MIRING * np.cos(2 * np.pi * t + self.fase)   # ROTASI

        M = matriks_translasi(px, py) @ matriks_rotasi(tilt) @ matriks_scaling(sx, sy)
        self.keadaan = (px, py, tilt, sx, sy)                 # untuk panel info
        if self.cermin:                                       # REFLEKSI
            M = F @ M

        self.halo.set_xy(terapkan(M, HALO))
        self.lonceng.set_xy(terapkan(M, LONCENG))
        self.dalam.set_xy(terapkan(M, DALAM))

        arg = 2 * np.pi * 5 * t
        for g, x0, panjang, i in self.tentakel:
            lokal = np.column_stack([
                x0 + 0.22 * S_TENT * np.sin(arg - 4 * S_TENT + i),
                -panjang * S_TENT])
            h = terapkan(M, lokal)
            g.set_data(h[:, 0], h[:, 1])
        for g, x0, panjang, i in self.lengan:
            lokal = np.column_stack([
                x0 + 0.30 * S_TENT * np.sin(arg - 3 * S_TENT + i * 2),
                -panjang * S_TENT])
            h = terapkan(M, lokal)
            g.set_data(h[:, 0], h[:, 1])


# (warna, skala, cx, cy, amp_x, amp_y, fase, z, alpha)
PASANGAN = [
    ('#7FE9FF', 0.50, 3.9, 2.2, 0.8, 0.35, 2.0, 4, 0.75),    # kecil, jauh
    ('#B79CFF', 0.45, 1.3, -1.3, 0.45, 0.30, 4.0, 6, 0.85),   # kecil, tengah
    ('#FF7EB6', 1.00, 2.6, 0.3, 0.9, 0.55, 0.0, 8, 1.0),      # besar, dekat
]
ubur = []
for prm in PASANGAN:
    for cermin in (False, True):
        ubur.append(Ubur(*prm, cermin))


# ============================================================
# 4. GELEMBUNG & PLANKTON (translasi naik)
# ============================================================

N_GEL = 22
gel_x = rng.uniform(-5.6, 5.6, N_GEL)
gel_y = rng.uniform(0, 1, N_GEL)
gel_k = rng.integers(1, 3, N_GEL)
gel_f = rng.uniform(0, 2 * np.pi, N_GEL)
gelembung = ax.scatter([], [], s=[], facecolors='none', edgecolors='white',
                       linewidths=1.0, alpha=0.5, zorder=5)

N_PLK = 80
plk_x = rng.uniform(-5.9, 5.9, N_PLK)
plk_y = rng.uniform(0, 1, N_PLK)
plk_f = rng.uniform(0, 2 * np.pi, N_PLK)
plk_k = rng.integers(1, 4, N_PLK)
plankton = ax.scatter(plk_x, np.zeros(N_PLK), s=6, c='white', zorder=2)


def perbarui_partikel(t):
    frac = (gel_y + gel_k * t) % 1
    x = gel_x + 0.15 * np.sin(2 * np.pi * 2 * t + gel_f)
    gelembung.set_offsets(np.column_stack([x, -3.6 + frac * 7.6]))
    gelembung.set_sizes(10 + 70 * frac)

    y = -4 + ((plk_y + t) % 1) * 8
    x = plk_x + 0.2 * np.sin(2 * np.pi * t + plk_f)
    plankton.set_offsets(np.column_stack([x, y]))
    kilau = 0.15 + 0.65 * (0.5 + 0.5 * np.sin(2 * np.pi * plk_k * t + plk_f))
    warna = np.tile(to_rgba('#BFF6FF'), (N_PLK, 1))
    warna[:, 3] = kilau
    plankton.set_facecolors(warna)



# ============================================================
# 5. PANEL INFORMASI (FPS, frame, timeline, nilai transformasi)
# ============================================================

LEBAR_BAR = 11.0
hud = []   # semua elemen panel, supaya mudah disembunyikan

hud.append(ax.add_patch(FancyBboxPatch(
    (-5.7, -4.0), 11.4, 0.88, boxstyle='round,pad=0.02,rounding_size=0.12',
    facecolor='#020B18', edgecolor='#3C7FA6', linewidth=1, alpha=0.72, zorder=19)))
hud.append(ax.add_patch(Rectangle((-5.5, -3.3), LEBAR_BAR, 0.05,       # latar timeline
                                  facecolor='#1B3F5C', edgecolor='none', zorder=20)))
bar_waktu = ax.add_patch(Rectangle((-5.5, -3.3), 0.001, 0.05,         # isi timeline
                                   facecolor='#7FE9FF', edgecolor='none', zorder=21))
hud.append(bar_waktu)


def teks_hud(y, ukuran, warna, tebal='normal'):
    t = ax.text(0, y, '', ha='center', va='center', fontsize=ukuran, color=warna,
                family='monospace', fontweight=tebal, zorder=22)
    hud.append(t)
    return t


teks_baris1 = teks_hud(-3.50, 10, '#FFFFFF', 'bold')
teks_baris2 = teks_hud(-3.72, 9, '#BFF6FF')
teks_baris3 = teks_hud(-3.92, 8.5, '#8FB9D1')

# ubur-ubur besar (non-cermin) dipakai sebagai contoh nilai transformasi
UBUR_CONTOH = next(u for u in ubur if u.skala == 1.0 and not u.cermin)


def perbarui_hud(frame):
    px, py, tilt, sx, sy = UBUR_CONTOH.keadaan
    detik = frame / FPS
    teks_baris1.set_text(f'FPS {FPS}   |   Frame {frame + 1:03d}/{N_FRAME}   |   '
                         f'Waktu {detik:4.1f}/{DURASI:.0f} dtk')
    teks_baris2.set_text(f'Translasi ({px:+.2f}, {py:+.2f})   Rotasi {tilt:+5.1f}°   '
                         f'Scaling {sx:.2f}×{sy:.2f}   Refleksi: sumbu Y')
    teks_baris3.set_text("M = T · R · S        M' = F · M  (kembaran cermin)")
    bar_waktu.set_width(max(LEBAR_BAR * (frame + 1) / N_FRAME, 0.001))


# ============================================================
# 6. UPDATE & JALANKAN
# ============================================================

def update(frame):
    t = frame / N_FRAME
    perbarui_sinar(t)
    for r in rumput:
        r.perbarui(t)
    for u in ubur:
        u.perbarui(t)
    perbarui_partikel(t)
    perbarui_hud(frame)


# ============================================================
# 7. MENYIMPAN GIF & MP4 (sekali render untuk keduanya)
# ============================================================

def folder_kode():
    """Folder tempat file ini berada (jika dijalankan di notebook: folder kerja)."""
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.getcwd()


def cari_ffmpeg():
    """Cari ffmpeg di sistem, atau dari paket imageio-ffmpeg. None jika tidak ada."""
    exe = shutil.which('ffmpeg')
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return None


def simpan_animasi(nama, folder):
    """
    Render tiap frame SATU kali, lalu dipakai untuk:
      - MP4 : dikirim langsung ke ffmpeg (H.264, 30 FPS, tepat 10 detik)
      - GIF : palet warna dibuat sekali agar tidak berkedip, ukuran file kecil
    """
    lebar = int(round(fig.get_figwidth() * DPI_SIMPAN))
    tinggi = int(round(fig.get_figheight() * DPI_SIMPAN))
    jalur_gif = os.path.join(folder, nama + '.gif')
    jalur_mp4 = os.path.join(folder, nama + '.mp4')

    # --- siapkan ffmpeg untuk MP4
    ffmpeg = cari_ffmpeg()
    proses = None
    if ffmpeg:
        proses = subprocess.Popen(
            [ffmpeg, '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba',
             '-s', f'{lebar}x{tinggi}', '-r', str(FPS), '-i', '-',
             '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20',
             '-movflags', '+faststart', jalur_mp4],
            stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    else:
        print('! MP4 dilewati: ffmpeg belum ada. Jalankan  pip install imageio-ffmpeg  lalu ulangi.')

    # --- render semua frame satu kali
    ukuran_gif = (int(lebar * SKALA_GIF), int(tinggi * SKALA_GIF))

    def ambil_frame(frame):
        """Render 1 frame -> (bytes RGBA mentah, gambar RGB berukuran GIF)."""
        update(frame)
        buf = io.BytesIO()
        fig.savefig(buf, format='rgba', dpi=DPI_SIMPAN)
        mentah = buf.getvalue()
        rgb = Image.frombytes('RGBA', (lebar, tinggi), mentah).convert('RGB')
        return mentah, rgb.resize(ukuran_gif, Image.LANCZOS)

    # palet GIF dibuat sekali dari beberapa frame contoh (agar warna lengkap & tidak berkedip)
    contoh = [ambil_frame(f)[1] for f in range(0, N_FRAME, N_FRAME // 5)]
    mosaik = Image.new('RGB', (ukuran_gif[0], ukuran_gif[1] * len(contoh)))
    for i, g in enumerate(contoh):
        mosaik.paste(g, (0, i * ukuran_gif[1]))
    palet = mosaik.quantize(colors=WARNA_GIF)

    print(f'Merender {N_FRAME} frame ({DURASI:.0f} detik @ {FPS} FPS)...')
    frame_gif = []
    for frame in range(N_FRAME):
        mentah, rgb = ambil_frame(frame)
        if proses:                                        # -> MP4
            proses.stdin.write(mentah)
        frame_gif.append(rgb.quantize(palette=palet, dither=0))   # -> GIF
        if (frame + 1) % 50 == 0:
            print(f'  {frame + 1}/{N_FRAME} frame')

    # --- selesaikan MP4
    if proses:
        proses.stdin.close()
        if proses.wait() == 0:
            print('MP4 tersimpan :', jalur_mp4)
        else:
            print('! MP4 gagal dibuat (ffmpeg error).')

    # --- tulis GIF. GIF hanya mengenal kelipatan 10 ms, jadi pola 30-30-40 ms
    #     menghasilkan rata-rata 33,3 ms/frame -> total tepat 10 detik.
    jeda = [40 if i % 3 == 2 else 30 for i in range(N_FRAME)]
    frame_gif[0].save(jalur_gif, save_all=True, append_images=frame_gif[1:],
                      duration=jeda, loop=0, optimize=True, disposal=1)
    print('GIF tersimpan :', jalur_gif)


# ============================================================
# 8. JALANKAN
# ============================================================

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Animasi Ubur-Ubur Kembar Cermin')
    parser.add_argument('--nama', default='hasil_animasi', help='nama file hasil (tanpa ekstensi)')
    parser.add_argument('--tanpa-simpan', action='store_true', help='jangan simpan GIF/MP4')
    parser.add_argument('--tanpa-tampil', action='store_true', help='jangan buka jendela animasi')
    parser.add_argument('--tanpa-info', action='store_true',
                        help='sembunyikan panel info (FPS, frame, timeline)')
    args = parser.parse_args()

    if args.tanpa_info:
        for elemen in hud:
            elemen.set_visible(False)

    if not args.tanpa_simpan:
        simpan_animasi(args.nama, folder_kode())

    if not args.tanpa_tampil:
        ani = animation.FuncAnimation(fig, update, frames=N_FRAME,
                                      interval=1000 / FPS, blit=False, repeat=True)
        plt.show()