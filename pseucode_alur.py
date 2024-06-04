import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Fungsi untuk menambahkan panah ke plot
def add_arrow(ax, x_start, y_start, x_end, y_end, text):
    ax.annotate(text, xy=(x_end, y_end), xytext=(x_start, y_start),
                arrowprops=dict(facecolor='black', shrink=0.05))

# Inisialisasi plot
fig, ax = plt.subplots(figsize=(12, 6))

# Menggambar panah untuk setiap langkah dalam alur kerja
arrows = [
    (0.1, 0.5, 0.25, 0.5, 'User memasukkan parameter input'),
    (0.25, 0.5, 0.4, 0.5, 'Memulai inisialisasi titik api'),
    (0.4, 0.5, 0.6, 0.5, 'Simulasi Berjalan, Penyebaran Api Bergerak'),
    (0.6, 0.5, 0.75, 0.5, 'Api berhenti menyebar, simulasi dihentikan'),
    (0.75, 0.5, 0.9, 0.5, 'Hasil Simulasi')
]

# Menambahkan panah ke plot
for arrow in arrows:
    add_arrow(ax, *arrow)

# Menambahkan teks dengan frame kotak
for i in range(1, len(arrows)):
    x_start, y_start, x_end, y_end, text = arrows[i]
    prev_x_start, _, prev_x_end, _, prev_text = arrows[i-1]
    text_x = (prev_x_end + x_start) / 2
    text_y = (y_start + y_end) / 2
    ax.text(text_x, text_y, text, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

# Mengatur batas sumbu
plt.xlim(0, 1)
plt.ylim(0, 1)

# Menghilangkan sumbu
plt.axis('off')

# Menampilkan plot
plt.title('Alur Kerja Simulasi Penyebaran Kebakaran Hutan')
plt.show()
