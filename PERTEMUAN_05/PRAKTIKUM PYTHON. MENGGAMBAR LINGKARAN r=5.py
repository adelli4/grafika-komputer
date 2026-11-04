
import matplotlib.pyplot as plt

# fungsi untuk menggambar lingkaran menggunakan algoritma midpoint circle
# xc dan yc merupakan koordinat titik pusat lingkaran
# r merupakan jari-jari lingkaran
def midpoint_circle(xc, yc, r):

    # menentukan titik awal lingkaran
    # x dimulai dari 0 dan y dimulai dari nilai jari-jari
    x, y = 0, r

    # menentukan nilai keputusan awal untuk mencari titik berikutnya
    d = 1 - r

    # menyiapkan list kosong untuk menyimpan koordinat titik lingkaran
    points = []

    # melakukan perulangan selama nilai x tidak melebihi nilai y
    while x <= y:

        # menentukan delapan titik yang memiliki posisi simetris
        # terhadap titik pusat lingkaran
        for px, py in [(x, y), (y, x), (-x, y), (-y, x),
                       (x, -y), (y, -x), (-x, -y), (-y, -x)]:

            # menambahkan koordinat titik simetris ke titik pusat
            # kemudian menyimpan hasilnya ke dalam list points
            points.append((xc + px, yc + py))

        # memeriksa nilai keputusan untuk menentukan titik berikutnya
        if d < 0:

            # jika nilai d kurang dari 0, titik bergerak ke arah kanan
            d = d + 2 * x + 3

        else:

            # jika nilai d lebih dari atau sama dengan 0,
            # titik bergerak ke arah kanan bawah
            d = d + 2 * (x - y) + 5

            # mengurangi nilai y sebanyak satu
            y -= 1

        # menambah nilai x sebanyak satu pada setiap perulangan
        x += 1

    # mengembalikan seluruh koordinat titik yang telah dihitung
    return points


# memanggil fungsi untuk menggambar lingkaran
# titik pusat berada di koordinat (0, 0) dengan jari-jari 5
pts = midpoint_circle(0, 0, 5)

# memisahkan koordinat titik menjadi kumpulan nilai x dan y
x, y = zip(*pts)

# membuat area gambar dengan ukuran 5 x 5 inci
plt.figure(figsize=(5, 5))

# menampilkan titik-titik hasil perhitungan dengan warna merah
# s=60 digunakan untuk mengatur ukuran titik
plt.scatter(x, y, s=60, c='red')

# menyamakan skala sumbu x dan y agar lingkaran tidak terlihat lonjong
plt.axis('equal')

# menampilkan garis bantu pada grafik
plt.grid(True)

# memberikan judul pada gambar
plt.title('Lingkaran (r = 5) - Midpoint Algorithm')

# memberikan nama pada sumbu horizontal dan vertikal
plt.xlabel('X')
plt.ylabel('Y')

# menampilkan hasil gambar lingkaran
plt.show()
