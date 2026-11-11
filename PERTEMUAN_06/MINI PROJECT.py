#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mini Project Pertemuan 6 - Grafika Komputer
BLOOM: From a Tiny Seed to a Magical Garden

Nama  : ................
NIM   : ................
Kelas : ................

Animasi 2D dengan Python + Matplotlib (450 frame, 30 FPS = 15 detik).
Transformasi geometri memakai matriks homogen 3x3 pada [x, y, 1]:
  Translasi T(tx,ty), Rotasi R(a), Scaling S(sx,sy), gabungan M = T @ R @ S

Cara pakai: atur MODE di bawah, lalu Run (F5) di Thonny.
Paket: numpy, matplotlib, pillow
"""
import types
import numpy as np

# =============== PENGATURAN (ubah di sini, lalu tekan Run di Thonny) ===============
MODE = "save"        # "save"    -> simpan video/GIF ke folder yang sama dengan file ini
                     # "show"    -> tampilkan animasi di jendela (bisa agak berat/lambat)
                     # "preview" -> simpan beberapa gambar PNG saja untuk cek cepat
FORCE_GIF = False    # True -> selalu simpan GIF (kalau ffmpeg tidak ada, otomatis GIF)
OUT_NAME = "bloom"   # nama file keluaran (tanpa ekstensi)
DPI = None           # None = otomatis (100 untuk mp4, 60 untuk gif)
PREVIEW_FRAMES = [20, 50, 100, 160, 240, 330, 440]
# ====================================================================================

import os
try:                                                      # simpan hasil di folder file ini
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
except NameError:                                         # file belum disimpan di Thonny
    pass                                                  # -> hasil disimpan di folder kerja Thonny

ARGS = types.SimpleNamespace(
    show=(MODE == "show"), gif=FORCE_GIF, out=OUT_NAME, dpi=DPI,
    preview=PREVIEW_FRAMES if MODE == "preview" else None)

import matplotlib
if not ARGS.show:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib import font_manager as fm
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb, to_rgba
from matplotlib.patches import Rectangle

# ---------- 1. MATRIKS TRANSFORMASI HOMOGEN 2D ----------
def T(tx, ty):
    return np.array([[1.0, 0.0, tx], [0.0, 1.0, ty], [0.0, 0.0, 1.0]])


def R(deg):
    a = np.radians(deg)
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def S(sx, sy=None):
    sy = sx if sy is None else sy
    return np.array([[sx, 0.0, 0.0], [0.0, sy, 0.0], [0.0, 0.0, 1.0]])


def apply(M, pts):
    """Kalikan matriks 3x3 dengan sekumpulan titik (N,2) -> (N,2), lewat [x, y, 1]."""
    pts = np.asarray(pts, float)
    P = np.hstack([pts, np.ones((len(pts), 1))])
    return (P @ M.T)[:, :2]


# ---------- 2. UTILITAS: easing, warna, timeline ----------
FPS, TOTAL = 30, 450
SC = [0, 60, 120, 185, 275, 345, 450]          # batas frame tiap scene
G, XC = 2.4, 8.0                                # tinggi permukaan tanah, posisi x tanaman utama


def clamp01(x):
    return float(np.clip(x, 0.0, 1.0))


def prog(f, a, b):
    return clamp01((f - a) / float(b - a))


def smooth(t):
    t = clamp01(t)
    return t * t * (3 - 2 * t)


def ease_out(t):
    return 1 - (1 - clamp01(t)) ** 3


def ease_in(t):
    return clamp01(t) ** 2


def ease_out_back(t, k=1.70158):
    t = clamp01(t)
    return 1 + (k + 1) * (t - 1) ** 3 + k * (t - 1) ** 2


def lerp(a, b, t):
    return a + (b - a) * t


def hexmix(a, b, t):
    return tuple(np.array(to_rgb(a)) * (1 - t) + np.array(to_rgb(b)) * t)


def scene_of(f):
    for i in range(6):
        if SC[i] <= f < SC[i + 1]:
            return i
    return 5


# ---------- 3. PALET WARNA (soft pastel, dreamy) ----------
C = dict(
    soil="#CFA48A", crust="#E3C3A9", soil_dark="#B98D73", pebble="#EBDACB",
    leaf="#86D6A0", leaf_edge="#55B380", leaf_hi="#A9E8BC", leaf_vein="#5DBB86",
    stem="#74CB93", stem_edge="#58B07C", stem_hi="#A4E5BC", sepal="#8FD6A4",
    seed="#C99A76", seed_edge="#9E7156",
    plum="#6E4F8F",
)
GRASS_COLS = ["#9ADBA8", "#8FD3A1", "#B3E6B0", "#7CCB9A", "#A6E3C0", "#93D9AE"]
SPARK_COLS = ["#FFFFFF", "#FFF2A8", "#FFC8E0", "#E2D2FF", "#FFD9B8"]


def light(c, t=0.55):
    return hexmix(c, "#FFFFFF", t)


# ---------- 4. LIBRARY BENTUK (koordinat lokal) ----------
def circle_pts(r=1.0, n=24):
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return np.c_[r * np.cos(th), r * np.sin(th)]


CIRCLE, CIRCLE12 = circle_pts(1, 24), circle_pts(1, 12)


def chaikin(pts, it=3):
    P = np.asarray(pts, float)
    for _ in range(it):
        Q = 0.75 * P + 0.25 * np.roll(P, -1, axis=0)
        Rr = 0.25 * P + 0.75 * np.roll(P, -1, axis=0)
        P = np.empty((2 * len(P), 2))
        P[0::2], P[1::2] = Q, Rr
    return P


def ribbon(c, w0, w1=None):
    """Ubah garis tengah (N,2) menjadi poligon pita dengan lebar w0 -> w1 (satuan dunia)."""
    w1 = w0 if w1 is None else w1
    d = np.gradient(c, axis=0)
    n = np.c_[-d[:, 1], d[:, 0]]
    n = n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)
    w = (np.linspace(w0, w1, len(c)) / 2.0)[:, None]
    return np.vstack([c + n * w, (c - n * w)[::-1]])


def _petal():
    u = np.linspace(0, 1, 15)
    w = 0.5 * np.clip(np.sin(np.pi * u ** 1.35), 0, None) ** 0.75
    x = np.r_[w, -w[::-1][1:-1]]
    y = np.r_[u, u[::-1][1:-1]]
    return np.c_[x + 0.06 * y ** 2, y]          # sedikit melengkung agar organik


PETAL = _petal()
_vu = np.linspace(0.08, 0.75, 6)
PVEIN = np.c_[0.06 * _vu ** 2, _vu]


def _leaf():
    u = np.linspace(0, 1, 14)
    w = 0.21 * np.sin(np.pi * u ** 0.85)
    b = 0.07 * u ** 2
    top = np.c_[u, b + w]
    bot = np.c_[u[::-1], (b - w)[::-1]]
    mid = np.c_[u[::-1], b[::-1]]
    return np.vstack([top, bot[1:-1]]), np.vstack([top, mid[1:-1]]), np.c_[u, b]


LEAF, LEAF_HALF, LEAF_VEIN = _leaf()
_s = np.linspace(0, 1, 26)
STEM_C = np.c_[0.22 * np.sin(2 * np.pi * _s), _s]            # garis tengah batang (S-curve halus)
BLADE = np.array([[-0.07, 0], [-0.045, 0.5], [0.05, 1.0], [0.035, 0.5], [0.07, 0]])


def _star(n=4, r2=0.28):
    th = np.linspace(0, 2 * np.pi, 2 * n, endpoint=False) + np.pi / 2
    r = np.where(np.arange(2 * n) % 2 == 0, 1.0, r2)
    return np.c_[r * np.cos(th), r * np.sin(th)]


STAR = _star()
UWING = chaikin([(0, 0.02), (-0.10, 0.30), (-0.40, 0.50), (-0.62, 0.34), (-0.48, 0.06)])
LWING = chaikin([(0, 0.0), (-0.34, 0.02), (-0.46, -0.20), (-0.26, -0.40), (-0.06, -0.18)])
BODY = circle_pts(1, 14) * np.array([0.05, 0.22])
STEM_M = np.array([[-0.09, 0], [0.09, 0], [0.065, 0.34], [-0.065, 0.34]])
_th = np.linspace(0, np.pi, 22)
CAP = np.c_[0.42 * np.cos(_th), 0.32 * np.sin(_th)]
CLOUD_C = [(-0.95, -0.05, 0.50), (-0.45, 0.30, 0.65), (0.25, 0.35, 0.78), (0.95, 0.05, 0.55), (0.10, -0.02, 0.70)]

# ---------- 5. LAYER POLIGON (satu PolyCollection per layer -> cepat; urutan tambah = urutan gambar) ----------
class Layer:
    def __init__(self, ax, z):
        self.coll = PolyCollection([], closed=True)
        self.coll.set_zorder(z)
        ax.add_collection(self.coll, autolim=False)
        self.clear()

    def clear(self):
        self.v, self.fc, self.ec = [], [], []

    def add(self, pts, color, alpha=1.0, edge=None):
        if len(pts) < 3 or alpha <= 0.002:
            return
        self.v.append(pts)
        self.fc.append(to_rgba(color, alpha))
        self.ec.append(to_rgba(edge, alpha) if edge is not None else (0, 0, 0, 0))

    def flush(self):
        if not self.v:
            self.coll.set_visible(False)
            return
        self.coll.set_visible(True)
        self.coll.set_verts(self.v)
        self.coll.set_facecolor(self.fc)
        self.coll.set_edgecolor(self.ec)
        self.coll.set_linewidth(0.7)


def disc(L, c, r, col, a=1.0, edge=None):
    L.add(apply(T(c[0], c[1]) @ S(r), CIRCLE if r > 0.12 else CIRCLE12), col, a, edge)


def star(L, c, r, rot, col, a):
    L.add(apply(T(c[0], c[1]) @ R(rot) @ S(r), STAR), col, a)


# ---------- 6. KONFIGURASI BUNGA ----------
def ring(n, Ln, W, off, c, d0, l0, w0, vein=False):
    return dict(n=n, L=Ln, W=W, off=off, c=c, ci=light(c), d0=d0, l0=l0, w0=w0, vein=vein)


MAIN_RINGS = [
    ring(10, 1.05, 0.62, 0, "#C9B0F2", 0.00, 0.85, 0.80, True),
    ring(10, 0.95, 0.66, 18, "#F8A6C6", 0.10, 0.85, 0.80, True),
    ring(8, 0.72, 0.64, 9, "#FFC3A0", 0.35, 0.0, 0.0),
    ring(6, 0.46, 0.58, 30, "#FFE08A", 0.55, 0.0, 0.0),
]


def small_rings(c1, c2):
    return [ring(7, 1.0, 0.72, 0, c1, 0.0, 0.85, 0.8), ring(5, 0.62, 0.70, 36, c2, 0.5, 0.0, 0.0)]


SMALL = [  # x, tinggi batang, ukuran kepala, (warna1, warna2, pusat)
    dict(x=8.0 - 3.4, H=2.4, hs=0.55, pal=("#C9B0F2", "#F8B8D8", "#FFD36E")),
    dict(x=8.0 + 3.0, H=1.7, hs=0.46, pal=("#FFC3A0", "#FFE08A", "#B388EB")),
    dict(x=8.0 - 1.9, H=1.5, hs=0.42, pal=("#FFE08A", "#FFC3A0", "#F4A261")),
    dict(x=8.0 + 4.4, H=2.5, hs=0.58, pal=("#F8A6C6", "#D9C2F7", "#FFE08A")),
    dict(x=8.0 - 5.6, H=1.8, hs=0.50, pal=("#F8A6C6", "#FFD1A6", "#FFE08A")),
    dict(x=8.0 + 1.9, H=1.4, hs=0.40, pal=("#D9C2F7", "#FFC3A0", "#FFD36E")),
    dict(x=8.0 - 7.0, H=1.3, hs=0.40, pal=("#FFC3A0", "#F8A6C6", "#FFE08A")),
    dict(x=8.0 + 6.9, H=1.5, hs=0.44, pal=("#C9B0F2", "#FFE08A", "#F4A261")),
]
for _i, _sp in enumerate(sorted(SMALL, key=lambda d: abs(d["x"] - XC))):
    _sp["t0"] = 280 + 5 * _i                    # tumbuh dari dekat bunga utama ke tepi
    _sp["rings"] = small_rings(_sp["pal"][0], _sp["pal"][1])

MAIN_LEAVES = [
    dict(a=0.90, side="R", t0=88, dur=40, ang=32, size=0.95, ph=0.0),
    dict(a=1.35, side="L", t0=128, dur=40, ang=30, size=1.00, ph=1.0),
    dict(a=1.90, side="R", t0=140, dur=40, ang=26, size=1.05, ph=2.0),
    dict(a=2.35, side="L", t0=152, dur=40, ang=34, size=0.90, ph=3.0),
    dict(a=2.75, side="R", t0=165, dur=36, ang=40, size=0.75, ph=4.0),
]

_rng = np.random.default_rng(11)
SPARK = [dict(a=_rng.uniform(0, 2 * np.pi), r=_rng.uniform(0.9, 2.7), per=int(_rng.integers(50, 95)),
              life=int(_rng.integers(34, 56)), ph=int(_rng.integers(0, 95)), sz=_rng.uniform(0.06, 0.15),
              col=SPARK_COLS[i % 5], rot=_rng.uniform(0, 90)) for i in range(58)]
BURST = [dict(a=2 * np.pi * i / 28 + _rng.uniform(-0.1, 0.1), v=_rng.uniform(1.5, 3.2),
              col=SPARK_COLS[i % 5]) for i in range(28)]
POLLEN = [dict(x=_rng.uniform(0.5, 15.5), y=_rng.uniform(G + 0.6, 8.2), ax=_rng.uniform(0.2, 0.7),
               ay=_rng.uniform(0.15, 0.5), px=_rng.uniform(0, 6.28), py=_rng.uniform(0, 6.28),
               sz=_rng.uniform(0.035, 0.07), col=["#FFF2A8", "#FFFFFF", "#FFD1E6", "#E2D2FF"][i % 4])
          for i in range(26)]
CRUMBS = [(-0.9, 1.7), (-0.55, 2.0), (-0.25, 2.2), (0.2, 2.1), (0.5, 1.9), (0.85, 1.6), (0.1, 1.4), (-0.4, 1.3)]
BLADES = []
for _ in range(130):
    early = _rng.random() < 0.15
    BLADES.append(dict(x=_rng.uniform(-1, 17), h=_rng.uniform(0.25, 0.75) * (1.0 + 0.5 * (_rng.random() < 0.12)),
                       lean=_rng.uniform(-12, 12), ph=_rng.uniform(0, 6.28),
                       t0=(128 + _rng.uniform(0, 40)) if early else (282 + _rng.uniform(0, 50)),
                       col=GRASS_COLS[int(_rng.integers(0, len(GRASS_COLS)))]))
BLADES.sort(key=lambda b: b["h"])
CLOUDS = [(2.0, 7.2, 0.65, 0.010), (10.0, 8.2, 0.8, 0.007), (15.0, 6.8, 0.55, 0.012), (5.5, 8.6, 0.6, 0.009)]
BFLY = [
    dict(A=2.7, B=1.5, w=0.041, ph=0.0, start=(-1.8, 6.8), fb=292, size=0.95,
         col=("#F6A8D0", "#C8A8F0", "#B9739F", "#FFFFFF")),
    dict(A=3.6, B=1.9, w=-0.033, ph=2.1, start=(17.8, 7.6), fb=306, size=0.85,
         col=("#FFC09A", "#FFE28A", "#D98F6A", "#B388EB")),
    dict(A=1.9, B=1.1, w=0.055, ph=4.0, start=(3.0, -0.8), fb=320, size=0.75,
         col=("#B9A5F2", "#F8B8D8", "#8E78CC", "#FFFFFF")),
]
CY = G + 3.6                                    # pusat orbit kupu-kupu

# ---------- 7. KAMERA ----------
CAM = [(0, 1.30, 7.9, 4.7), (185, 1.22, 8.0, 4.9), (275, 1.18, 8.0, 5.2), (345, 1.0, 8.0, 5.0), (450, 1.0, 8.0, 5.0)]


def camera(f):
    for (f0, z0, x0, y0), (f1, z1, x1, y1) in zip(CAM[:-1], CAM[1:]):
        if f <= f1:
            t = smooth(prog(f, f0, f1))
            return lerp(z0, z1, t), lerp(x0, x1, t), lerp(y0, y1, t)
    return CAM[-1][1:]


# ---------- 8. FUNGSI MENGGAMBAR OBJEK ----------
def draw_plant(L, base, h, sway, leaves, f, w0=0.17, w1=0.10):
    """Batang (scaling sumbu-y) + daun (translasi + rotasi + scaling). Mengembalikan frame ujung batang."""
    P0 = T(base[0], base[1]) @ R(sway)                    # frame tanaman: translasi + rotasi (goyang)
    if h > 0.04:
        cl = apply(P0 @ S(1, h), STEM_C)                  # SCALING: tinggi batang = h
        L.add(ribbon(cl, w0, w1), C["stem"], edge=C["stem_edge"])
        L.add(ribbon(cl + np.array([-0.012, 0]), w0 * 0.3, w1 * 0.3), C["stem_hi"], 0.8)
    vis = None
    for lf in leaves:
        p = ease_out_back(prog(f, lf["t0"], lf["t0"] + lf["dur"]), 1.3)
        if p <= 0.02 or h < 0.5 * lf["a"]:
            continue
        fr = min(lf["a"] / h, 0.97)
        ap = np.array([0.22 * np.sin(2 * np.pi * fr), fr * h])
        sg = 1 if lf["side"] == "R" else -1
        pc = min(p, 1.2)
        ang = lerp(86, lf["ang"], pc) + 3.0 * np.sin(0.09 * f + lf["ph"]) * min(p, 1)   # ROTASI membuka
        sz = lf["size"] * lerp(0.15, 1.0, pc)                                          # SCALING membesar
        M = P0 @ T(ap[0], ap[1]) @ R(sg * ang) @ S(sg * sz, sz)
        L.add(apply(M, LEAF), C["leaf"], edge=C["leaf_edge"])
        L.add(apply(M, LEAF_HALF), C["leaf_hi"], 0.85)
        L.add(ribbon(apply(M, LEAF_VEIN), 0.03 * sz), C["leaf_vein"], 0.9)
        vis = (apply(P0, ap[None, :])[0], ang, sz)
    return P0 @ T(0, h), vis


def draw_head(L, Mh, hs, bloom, rings, ccol, dots, f, hud=None, tilt=0.66, spin=0.0):
    """Kepala bunga berlapis. Tiap kelopak: M = Head @ R(phi) @ S(lebar, panjang)."""
    sq = lerp(1.0, tilt, smooth(bloom))
    Mu = Mh @ S(hs)
    Mb = Mh @ S(hs, hs * sq)
    sb = smooth(bloom)
    L.add(apply(Mu @ T(0, -0.06) @ S(0.24), CIRCLE), C["sepal"], edge=C["leaf_edge"])
    for j in range(5):                                      # sepal hijau ikut berotasi membuka
        k = j - 2
        M = Mu @ R(lerp(k * 13, k * 54, sb)) @ S(0.26, 0.62 * lerp(1, 0.8, sb))
        L.add(apply(M, PETAL), C["sepal"], edge=C["leaf_edge"])
    idle = smooth((bloom - 0.9) / 0.1)
    for ri, rg in enumerate(rings):
        items = []
        for j in range(rg["n"]):
            delay = rg["d0"] * 0.55 + 0.25 * (j / rg["n"])     # kelopak muncul satu per satu (spiral)
            p = ease_out_back(clamp01((bloom - delay) / 0.42), 1.2)
            wob = idle * 5.0 * np.sin(0.03 * f + ri * 1.7)
            po = (rg["off"] + 360.0 * j / rg["n"] + wob + 180) % 360 - 180
            items.append((np.cos(np.radians(po)), j, po, p))
        items.sort(key=lambda t: -t[0])                        # belakang dulu, depan terakhir
        for _, j, po, p in items:
            ls, ws = lerp(rg["l0"], 1.0, p), lerp(rg["w0"], 1.0, p)   # SCALING kelopak
            if ls < 0.05:
                continue
            phi = po * lerp(0.12, 1.0, min(p, 1.15))                  # ROTASI tertutup -> terbuka
            M = Mb @ R(phi) @ S(rg["W"] * ws, rg["L"] * ls)
            L.add(apply(M, PETAL), rg["c"], edge=hexmix(rg["c"], "#9C6B9E", 0.28))
            L.add(apply(M @ T(0, 0.10) @ S(0.56, 0.80), PETAL), rg["ci"], 0.85)
            if rg["vein"]:
                L.add(ribbon(apply(M, PVEIN), 0.02 * hs * ls), hexmix(rg["c"], "#B05A8A", 0.4), 0.5)
            if hud is not None and ri == 1 and j == 0:
                hud["petal"] = dict(obj="Kelopak pink #1", T=(Mh[0, 2], Mh[1, 2]), R=phi,
                                    S=(rg["W"] * ws * hs, rg["L"] * ls * hs))
    cs = ease_out_back(prog(bloom, 0.62, 0.95), 1.4)
    if cs > 0.03:
        L.add(apply(Mb @ S(0.31 * cs), CIRCLE), ccol, edge="#F2A65A")
        L.add(apply(Mb @ T(-0.07, 0.08) @ S(0.15 * cs, 0.10 * cs), CIRCLE12), "#FFF1BF", 0.8)
        for k in range(dots):
            r = 0.25 * np.sqrt((k + 0.5) / dots) * cs
            a = k * 2.39996 + spin
            pt = apply(Mb, [[r * np.cos(a), r * np.sin(a)]])[0]
            disc(L, pt, 0.03 * hs * cs, "#F4A261" if k % 2 == 0 else "#B388EB")


def draw_small_plants(L, f):
    for i, sp in enumerate(SMALL):
        t0 = sp["t0"]
        g = ease_out(prog(f, t0, t0 + 30))
        if g <= 0.01:
            continue
        H = sp["H"]
        leaves = [dict(a=H * 0.45, side="R", t0=t0 + 14, dur=26, ang=34, size=0.55, ph=i),
                  dict(a=H * 0.30, side="L", t0=t0 + 20, dur=26, ang=30, size=0.50, ph=i + 1)]
        top, _ = draw_plant(L, (sp["x"], G), H * g, 2.5 * np.sin(0.07 * f + i * 1.3) * g, leaves, f, 0.07, 0.05)
        bud = ease_out_back(prog(f, t0 + 22, t0 + 36), 1.0)
        bloom = prog(f, t0 + 30, t0 + 66)
        hs = sp["hs"] * (0.35 + 0.65 * smooth(bloom)) * bud
        if hs > 0.02:
            draw_head(L, top, hs, bloom, sp["rings"], sp["pal"][2], 0, f, tilt=0.72)


def draw_mushroom(L, x, f, t0, s):
    g = ease_out_back(prog(f, t0, t0 + 26), 1.8)
    if g < 0.03:
        return
    M = T(x, G - 0.02) @ S(s * g)
    L.add(apply(M, STEM_M), "#FFF2E3", edge="#E9CDB5")
    Mc = M @ T(0, 0.30)
    L.add(apply(Mc, CAP), "#F7A3BC", edge="#D9809F")
    for dx, dy, r in ((-0.18, 0.2, 0.07), (0.10, 0.28, 0.06), (0.24, 0.14, 0.05)):
        disc(L, apply(Mc, [[dx, dy]])[0], r * s * g, "#FFFFFF", 0.9)


def draw_grass(L, f):
    for b in BLADES:
        g = ease_out_back(prog(f, b["t0"], b["t0"] + 32), 1.2)
        if g <= 0.02:
            continue
        sway = 4.0 * np.sin(0.06 * f + b["ph"] + b["x"] * 0.5)
        M = T(b["x"], G - 0.02) @ R(b["lean"] + sway) @ S(1, b["h"] * g)
        L.add(apply(M, BLADE), b["col"])


def draw_seed(L, f, hud):
    A, B = 0.30, 0.40
    y0 = 8.7
    if f < 36:                                              # TRANSLASI jatuh (gerak dipercepat)
        t = f / 36.0
        y = lerp(y0, G - 0.12 + B, ease_in(t))
        x = XC + 0.28 * np.sin(t * np.pi * 3) * (1 - t)
        rot = 28 * np.sin(t * 2 * np.pi) * (1 - 0.3 * t)
        sx = sy = 1.0
    else:                                                   # getaran + squash (SCALING) saat menyentuh tanah
        tau = (f - 36) / 30.0
        d, o = np.exp(-4.5 * tau), np.cos(15 * tau)
        sy, sx = 1 - 0.30 * d * o, 1 + 0.22 * d * o
        x = XC + 0.07 * np.exp(-6 * tau) * np.sin(50 * tau)
        rot = 8 * np.sin(0.7 * (f - 72)) * prog(f, 72, 100) * (1 - prog(f, 100, 112))
        y = None
    sh = 1 - 0.85 * ease_out(prog(f, 72, 112))              # benih mengecil saat tunas keluar
    al = 1 - smooth(prog(f, 96, 118))
    if al <= 0.01:
        return
    yc = y if y is not None else G - 0.12 + B * sy * sh
    M = T(x, yc) @ R(rot) @ S(A * sx * sh, B * sy * sh)
    L.add(apply(M, CIRCLE), C["seed"], al, edge=C["seed_edge"])
    L.add(apply(M @ T(-0.35, 0.5) @ R(20) @ S(0.15, 0.09), CIRCLE12), "#F0CFB3", 0.8 * al)
    if sh > 0.45:                                           # wajah kawaii
        for sg in (-1, 1):
            disc(L, apply(M, [[sg * 0.32, 0.12]])[0], 0.04 * sh, "#5B3A29", al)
            disc(L, apply(M, [[sg * 0.60, -0.12]])[0], 0.05 * sh, "#FF9DB5", 0.7 * al)
        xs = np.linspace(-0.25, 0.25, 7)
        L.add(ribbon(apply(M, np.c_[xs, -0.04 - 0.14 * (1 - (xs / 0.25) ** 2)]), 0.018 * sh), "#6B4533", al)
    hud["seed"] = dict(obj="Benih", T=(x - XC, yc - y0), R=rot, S=(sx * sh, sy * sh))


def draw_dust(L, f):
    tau = prog(f, 36, 60)
    if tau <= 0 or tau >= 1:
        return
    for k in range(10):
        side = -1 if k % 2 else 1
        dist = (0.25 + 0.12 * (k // 2)) * 2.2 * ease_out(tau)
        y = G + 0.05 + 0.35 * np.sin(np.pi * tau) * (0.4 + 0.15 * (k // 2))
        disc(L, (XC + side * dist, y), 0.07 + 0.07 * tau, "#EBD5C3", 0.7 * (1 - tau))


def draw_mound(L, f):
    g = ease_out_back(prog(f, 60, 92), 1.2)
    if g <= 0.02:
        return
    th = np.linspace(0, np.pi, 24)
    semi = np.c_[np.cos(th), np.sin(th)]
    L.add(apply(T(XC, G - 0.03) @ S(1.0, 0.34 * g), semi), "#D9B39A")
    L.add(apply(T(XC, G - 0.03) @ S(0.7, 0.22 * g), semi), "#E3C3A9", 0.8)


def draw_crumbs(L, f):
    t = (f - 72) / 30.0
    if t <= 0 or t > 1.4:
        return
    for vx, vy in CRUMBS:
        x, y = XC + vx * t, G + 0.1 + vy * t - 3.6 * t * t
        if y >= G:
            disc(L, (x, y), 0.05, C["soil_dark"], 0.9)


def draw_cloud(L, x, y, s, a):
    for cx, cy, r in CLOUD_C:
        L.add(apply(T(x, y - 0.1 * s) @ S(s) @ T(cx, cy) @ S(r), CIRCLE), "#DCD0F0", 0.8 * a)
    for cx, cy, r in CLOUD_C:
        L.add(apply(T(x, y) @ S(s) @ T(cx, cy) @ S(r), CIRCLE), "#FFFFFF", a)


def draw_clouds(L, f):
    a = lerp(0.55, 0.95, smooth(prog(f, 0, 260)))
    for x0, y, s, sp in CLOUDS:
        x = ((x0 + sp * f * 30 / 3.0 + 3) % 22) - 3        # TRANSLASI horizontal (wrap-around)
        draw_cloud(L, x, y, s, a)


def draw_sun(L, f):
    xs = 13.0
    ys = 10.4 - 1.0 * smooth(prog(f, 60, 120)) - 1.7 * ease_out(prog(f, 280, 335))
    ig = smooth(prog(f, 62, 100))
    for r, a in ((3.8, 0.07), (2.9, 0.08), (2.1, 0.10), (1.5, 0.12)):
        L.add(apply(T(xs, ys) @ S(r * (1 + 0.03 * np.sin(0.08 * f))), CIRCLE), "#FFF0B0", a * ig)
    s = ease_out_back(prog(f, 280, 325))
    if s > 0.03:
        for j in range(12):                                 # sinar berputar (rotasi dekoratif)
            Mr = T(xs, ys) @ R(30 * j + 0.35 * f) @ S(0.75 * s)
            L.add(apply(Mr, np.array([[-0.16, 1.05], [0.16, 1.05], [0, 1.65]])), "#FFD98A", 0.95)
        Ms = T(xs, ys) @ S(0.75 * s)
        L.add(apply(Ms, CIRCLE), "#FFE48A", edge="#FFCB6B")
        L.add(apply(Ms @ S(0.82), CIRCLE), "#FFF1B0", 0.9)
        for sg in (-1, 1):
            disc(L, apply(Ms, [[sg * 0.30, 0.12]])[0], 0.045 * s, "#8B5E3C")
            disc(L, apply(Ms, [[sg * 0.50, -0.12]])[0], 0.07 * s, "#FFB3A7", 0.85)
        xx = np.linspace(-0.25, 0.25, 8)
        L.add(ribbon(apply(Ms, np.c_[xx, -0.10 - 0.16 * (1 - (xx / 0.25) ** 2)]), 0.025 * s), "#8B5E3C")
    return xs, ys


def draw_beams(L, f, xs, ys):
    ig = smooth(prog(f, 66, 105))
    if ig <= 0.01:
        return
    for k, (dx, wd) in enumerate(((4.8, 0.7), (7.2, 0.9), (9.6, 0.8), (12.0, 1.0))):
        puls = 0.6 + 0.4 * np.sin(0.045 * f + k * 1.7)
        xg = xs - dx
        L.add(np.array([[xs - 0.25, ys], [xs + 0.25, ys], [xg + wd, G], [xg - wd, G]]),
              "#FFF7C8", 0.085 * ig * puls)


def draw_sparkles(L, f, c):
    ig = smooth(prog(f, 205, 240))
    if ig > 0:
        for s in SPARK:
            tau = ((f - s["ph"]) % s["per"]) / float(s["life"])
            if tau >= 1:
                continue
            al = np.sin(np.pi * tau) * ig
            pos = np.array([c[0] + s["r"] * np.cos(s["a"]), c[1] + s["r"] * 0.8 * np.sin(s["a"]) + 0.4 * tau])
            star(L, pos, s["sz"] * (0.5 + al), s["rot"] + 90 * tau, s["col"], al)
    tau = prog(f, 236, 272)                                 # ledakan partikel saat mekar
    if 0 < tau < 1:
        for b in BURST:
            d = b["v"] * ease_out(tau)
            disc(L, (c[0] + d * np.cos(b["a"]), c[1] + d * 0.85 * np.sin(b["a"])), 0.07 * (1 - tau) + 0.015,
                 b["col"], 1 - tau)


def draw_pollen(L, f):
    ig = smooth(prog(f, 300, 340))
    if ig <= 0:
        return
    for p in POLLEN:
        pos = (p["x"] + p["ax"] * np.sin(0.025 * f + p["px"]), p["y"] + p["ay"] * np.sin(0.037 * f + p["py"]))
        tw = (0.55 + 0.45 * np.sin(0.12 * f + p["px"] * 3)) * ig
        disc(L, pos, p["sz"] * 3.2, p["col"], 0.13 * tw)
        disc(L, pos, p["sz"], p["col"], 0.9 * tw)


def bfly_pos(b, f):
    th = b["w"] * f + b["ph"]
    orb = np.array([XC + b["A"] * np.cos(th), CY + b["B"] * np.sin(th) + 0.45 * np.sin(2.3 * th + 1.0)
                    + 0.12 * np.sin(0.5 * f + b["ph"])])
    k = smooth(prog(f, b["fb"], b["fb"] + 60))
    return lerp(np.array(b["start"], float), orb, k)       # TRANSLASI: masuk dari luar layar lalu mengorbit


def draw_butterflies(L, f, hud):
    for i, b in enumerate(BFLY):
        if f < b["fb"]:
            continue
        pos = bfly_pos(b, f)
        d = bfly_pos(b, f + 1) - bfly_pos(b, f - 1)
        heading = np.degrees(np.arctan2(d[1], d[0]))        # ROTASI mengikuti arah gerak
        size = b["size"] * (0.4 + 0.6 * smooth(prog(f, b["fb"], b["fb"] + 30)))
        flap = 0.6 * f + i * 1.3
        fl = 0.22 + 0.78 * abs(np.cos(flap))                # SCALING sayap saat mengepak
        Mb = T(pos[0], pos[1]) @ R(heading - 90) @ S(size)
        Mw = Mb @ S(fl, 1)
        for sg in (1, -1):
            Mx = Mw @ S(sg, 1)
            L.add(apply(Mx, LWING), b["col"][1], edge=b["col"][2])
            L.add(apply(Mx, UWING), b["col"][0], edge=b["col"][2])
            L.add(apply(Mx @ T(-0.38, 0.27) @ S(0.08), CIRCLE12), b["col"][3], 0.85)
            L.add(apply(Mx @ T(-0.25, -0.17) @ S(0.06), CIRCLE12), b["col"][3], 0.85)
        L.add(apply(Mb, BODY), "#7A5C98")
        L.add(apply(Mb @ T(0, 0.25) @ S(0.065), CIRCLE12), "#7A5C98")
        for sg in (-1, 1):
            an = np.c_[np.linspace(0, sg * 0.14, 5), 0.28 + np.linspace(0, 0.24, 5) ** 1.0]
            L.add(ribbon(apply(Mb, an), 0.015 * size), "#7A5C98")
        if i == 0:
            hud["bfly"] = dict(obj="Kupu-kupu", T=tuple(pos), R=heading, S=(fl, 1.0))


# ---------- 9. SETUP FIGURE & LATAR STATIS ----------
_AV = {f.name for f in fm.fontManager.ttflist}


def pick(*names):
    for n in names:
        if n in _AV:
            return n
    return "DejaVu Sans"


FONT_T = pick("Berlin Sans FB Demi", "Baloo 2", "Fredoka", "Comic Sans MS", "Trebuchet MS", "Verdana")
FONT_S = pick("Segoe Script", "Lucida Handwriting", "Brush Script MT", "Georgia")

fig = plt.figure(figsize=(12.8, 7.2))
ax = fig.add_axes([0, 0, 1, 1])
ax.axis("off")
ax.set_autoscale_on(False)

_ys = np.linspace(-1, 10.5, 256)
_stops = [(-1, "#FFE3D0"), (3.5, "#FFE9D8"), (5.8, "#FBD8EA"), (8.0, "#DAD3F7"), (10.5, "#BBD8FF")]
_sy = [s[0] for s in _stops]
_sky = np.stack([np.interp(_ys, _sy, [to_rgb(s[1])[k] for s in _stops]) for k in range(3)], axis=1)
ax.imshow(_sky[:, None, :], extent=(-2, 18, -1, 10.5), origin="lower", aspect="auto", zorder=0,
          interpolation="bilinear")


def hill(base, amp, ph, f1=0.5, f2=1.3):
    x = np.linspace(-2, 18, 160)
    y = G + base + amp * np.sin(f1 * x + ph) + 0.4 * amp * np.sin(f2 * x + 2 * ph)
    return x, y


hills_v, hills_c = [], []
for base, amp, ph, col in ((1.5, 0.6, 0.5, "#D8CDF3"), (0.8, 0.4, 2.0, "#CBEBDD"), (0.3, 0.2, 4.0, "#BDE8C8")):
    hx, hy = hill(base, amp, ph)
    hills_v.append(np.vstack([np.c_[hx, hy], [[18, -1], [-2, -1]]]))
    hills_c.append(col)
for tx_, tc in ((1.0, "#C4B4EE"), (4.0, "#CFC0F2"), (11.5, "#C4B4EE"), (14.5, "#CFC0F2")):   # pohon lollipop
    hx, hy = hill(1.5, 0.6, 0.5)
    ty_ = float(np.interp(tx_, hx, hy))
    hills_v.append(np.array([[tx_ - 0.06, ty_ - 0.1], [tx_ + 0.06, ty_ - 0.1], [tx_ + 0.06, ty_ + 0.6], [tx_ - 0.06, ty_ + 0.6]]))
    hills_c.append("#B9A6D8")
    hills_v.append(apply(T(tx_, ty_ + 0.9) @ S(0.45, 0.5), CIRCLE))
    hills_c.append(tc)
ax.add_collection(PolyCollection(hills_v, facecolors=[to_rgba(c) for c in hills_c], edgecolors="none", zorder=3),
                  autolim=False)

_r = np.random.default_rng(3)
gv, gc = [np.array([[-2, -1], [18, -1], [18, G], [-2, G]])], [C["soil"]]
gv.append(np.array([[-2, G - 0.14], [18, G - 0.14], [18, G], [-2, G]]))
gc.append(C["crust"])
for _ in range(34):                                        # bercak tanah gelap
    cx, cy = _r.uniform(-1.5, 17.5), _r.uniform(-0.6, G - 0.35)
    gv.append(apply(T(cx, cy) @ R(_r.uniform(0, 180)) @ S(_r.uniform(0.2, 0.6), _r.uniform(0.07, 0.16)), CIRCLE))
    gc.append(C["soil_dark"])
for _ in range(20):                                        # kerikil
    cx, cy = _r.uniform(-1.5, 17.5), _r.uniform(0.0, G - 0.25)
    s_ = _r.uniform(0.07, 0.17)
    gv.append(apply(T(cx, cy - 0.03) @ S(s_ * 1.2, s_ * 0.8), CIRCLE))
    gc.append("#BE9980")
    gv.append(apply(T(cx, cy) @ S(s_ * 1.2, s_ * 0.8), CIRCLE))
    gc.append(C["pebble"])
for _ in range(60):                                        # butiran kecil
    cx, cy = _r.uniform(-1.5, 17.5), _r.uniform(-0.8, G - 0.2)
    gv.append(apply(T(cx, cy) @ S(0.03), CIRCLE12))
    gc.append("#E8CDB6")
ax.add_collection(PolyCollection(gv, facecolors=[to_rgba(c) for c in gc], edgecolors="none", zorder=4),
                  autolim=False)

back = Layer(ax, 2)       # matahari & awan (di belakang bukit)
front = Layer(ax, 5)      # tanaman, kupu-kupu, partikel
mist = Rectangle((-2, -1), 20, 11.5, fc="#8E7BB8", ec="none", zorder=6)
ax.add_patch(mist)

axv = fig.add_axes([0, 0, 1, 1])
axv.axis("off")
axv.set_xlim(0, 1)
axv.set_ylim(0, 1)
axv.set_zorder(10)
_yy, _xx = np.mgrid[0:1:180j, 0:1:320j]
_rr = np.sqrt(((_xx - 0.5) / 0.5) ** 2 + ((_yy - 0.5) / 0.5) ** 2) / np.sqrt(2)
_vig = np.zeros(_rr.shape + (4,))
_vig[..., :3] = to_rgb("#6B4C8C")
_vig[..., 3] = 0.22 * np.clip((_rr - 0.55) / 0.45, 0, 1) ** 1.5
axv.imshow(_vig, extent=(0, 1, 0, 1), aspect="auto", origin="lower", interpolation="bilinear", zorder=0)

SCENES = ["A LITTLE SEED", "THE FIRST SPROUT", "GROWING STRONGER", "THE BLOOMING MOMENT",
          "A MAGICAL GARDEN", "THE FINAL BLOOM"]
_halo = [pe.Stroke(linewidth=4, foreground="white"), pe.Normal()]
cap1 = axv.text(0.035, 0.945, "", fontsize=12, color="#8C6FB0", fontweight="bold", family=FONT_T,
                path_effects=_halo, va="center")
cap2 = axv.text(0.035, 0.905, "", fontsize=22, color=C["plum"], fontweight="bold", family=FONT_T,
                path_effects=_halo, va="center")
hud_txt = axv.text(0.015, 0.03, "", fontsize=9, family="DejaVu Sans Mono", color="#5A4478", va="bottom",
                   ha="left", bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="#CDB8E8", alpha=0.72))
LCOLS = ["#F58DB4", "#FFA777", "#F7C24E", "#A98BEA", "#F58DB4"]
_tfx = [pe.Stroke(linewidth=10, foreground="#B79AD6"), pe.Stroke(linewidth=6, foreground="white"), pe.Normal()]
title_txt = [axv.text(0.5 + (i - 2) * 0.092, 0.862, ch, ha="center", va="center", fontsize=1, color=LCOLS[i],
                      fontweight="bold", family=FONT_T, alpha=0, path_effects=_tfx)
             for i, ch in enumerate("BLOOM")]
sub_txt = axv.text(0.5, 0.775, "Every little thing takes time to grow", ha="center", va="center", fontsize=21,
                   style="italic", color="#7A5C98", family=FONT_S, alpha=0,
                   path_effects=[pe.Stroke(linewidth=5, foreground="white"), pe.Normal()])


def hud_text(sc, hud):
    if sc == 5:
        return "M = T . R . S      titik homogen [x, y, 1]^T\ntranslasi + rotasi + scaling"
    d = {0: hud.get("seed"), 1: hud.get("stem") or hud.get("seed"), 2: hud.get("stem"),
         3: hud.get("petal"), 4: hud.get("bfly")}[sc]
    if not d:
        return ""
    return (f"{d['obj']}\n"
            f"T(tx,ty) = ({d['T'][0]:+6.2f}, {d['T'][1]:+6.2f})\n"
            f"R(theta) = {d['R']:+7.2f} deg\n"
            f"S(sx,sy) = ({d['S'][0]:5.2f}, {d['S'][1]:5.2f})")


# ---------- 10. FRAME UPDATE ----------
def update(f):
    sc = scene_of(f)
    hud = {}
    back.clear()
    front.clear()

    z, cx, cy = camera(f)
    ax.set_xlim(cx - 8 / z, cx + 8 / z)
    ax.set_ylim(cy - 4.5 / z, cy + 4.5 / z)

    xs, ys = draw_sun(back, f)
    draw_clouds(back, f)

    # ---- parameter tanaman utama --------------------------------------------------
    h = 1.5 * ease_out(prog(f, 70, 120)) + 1.8 * smooth(prog(f, 120, 185))      # SCALING tinggi batang
    sway = (1.6 + 1.6 * smooth(prog(f, 120, 260))) * np.sin(0.06 * f)
    head_c = np.array([XC - h * np.sin(np.radians(sway)), G + h * np.cos(np.radians(sway))])
    bloom = prog(f, 200, 278)

    # cahaya lembut di belakang bunga utama
    if bloom > 0:
        for r, a in ((2.7, 0.10), (2.0, 0.12), (1.4, 0.14)):
            gp = apply(T(head_c[0], head_c[1]) @ S(r * (0.5 + smooth(bloom)) * (1 + 0.04 * np.sin(0.1 * f))), CIRCLE)
            gp[:, 1] = np.maximum(gp[:, 1], G)          # potong di permukaan tanah
            front.add(gp, "#FFE6F2", a)

    draw_small_plants(front, f)

    w0 = 0.12 + 0.05 * smooth(prog(f, 70, 185))
    top, vis = draw_plant(front, (XC, G), h, sway, MAIN_LEAVES, f, w0, w0 * 0.62)
    if vis is not None:
        hud["stem"] = dict(obj="Batang (S) + Daun (R)", T=tuple(vis[0]), R=vis[1], S=(1.0, h))
    elif h > 0.04:
        hud["stem"] = dict(obj="Batang (S)", T=(XC, G), R=sway, S=(1.0, h))

    if f >= 148:                                              # kuncup muncul & membesar, lalu mekar
        hs = 0.44 * ease_out_back(prog(f, 148, 192), 0.9) + (1.12 - 0.44) * smooth(prog(f, 205, 275))
        shake = 3.5 * np.sin(np.pi * prog(f, 188, 200)) * np.sin(2.2 * (f - 188)) if 188 <= f <= 200 else 0.0
        hr = 3.0 * np.sin(0.025 * f) * smooth(prog(f, 270, 300))   # rotasi dekoratif pelan
        if hs > 0.01:
            draw_head(front, top @ R(shake + hr), hs, bloom, MAIN_RINGS, "#FFD36E", 28, f, hud=hud, spin=0.02 * f)

    draw_seed(front, f, hud)
    draw_mushroom(front, 5.85, f, 300, 1.0)
    draw_mushroom(front, 10.3, f, 308, 0.8)
    draw_grass(front, f)
    draw_mound(front, f)
    draw_dust(front, f)
    draw_crumbs(front, f)

    mist.set_alpha(0.22 * (1 - smooth(prog(f, 0, 260))))

    draw_sparkles(front, f, head_c)
    draw_beams(front, f, xs, ys)
    draw_pollen(front, f)
    draw_butterflies(front, f, hud)

    back.flush()
    front.flush()

    # ---- teks / HUD ---------------------------------------------------------------
    a1 = SC[sc + 1] if sc < 5 else 372
    ca = clamp01(min((f - SC[sc]) / 10.0, (a1 - f) / 10.0, 1.0))
    cap1.set_text(f"SCENE {sc + 1}")
    cap2.set_text(SCENES[sc])
    cap1.set_alpha(ca)
    cap2.set_alpha(ca)
    t = hud_text(sc, hud)
    hud_txt.set_text(t)
    hud_txt.set_visible(bool(t))
    for i, tt in enumerate(title_txt):
        s_ = ease_out_back(prog(f, 352 + 6 * i, 376 + 6 * i), 2.0)
        tt.set_fontsize(max(1.0, 84 * s_))
        tt.set_alpha(clamp01(s_ * 1.5))
    sub_txt.set_alpha(smooth(prog(f, 396, 420)))
    return []


# ---------- 11. JALANKAN ----------
if __name__ == "__main__":
    if ARGS.preview:
        for n in ARGS.preview:
            update(n)
            fig.savefig(f"{ARGS.out}_frame{n:03d}.png", dpi=ARGS.dpi or 100)
            print("saved", f"{ARGS.out}_frame{n:03d}.png")
    else:
        anim = FuncAnimation(fig, update, frames=TOTAL, interval=1000 / FPS, blit=False, repeat=False)
        if ARGS.show:
            plt.show()
        else:
            use_gif = ARGS.gif or not FFMpegWriter.isAvailable()
            if use_gif:
                fn = ARGS.out + ".gif"
                anim.save(fn, writer=PillowWriter(fps=FPS), dpi=ARGS.dpi or 60)
            else:
                fn = ARGS.out + ".mp4"
                anim.save(fn, writer=FFMpegWriter(fps=FPS, bitrate=6000, codec="libx264",
                                                  extra_args=["-pix_fmt", "yuv420p"]), dpi=ARGS.dpi or 100)
            print("Selesai ->", fn)