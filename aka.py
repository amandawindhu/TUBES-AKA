import time
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# Data untuk menyimpan nilai n dan waktu eksekusi
n_values = []
rekursif_times = []
iteratif_times = []

# Fungsi untuk menampilkan inventori
def tampilkan_inventori(inventori):
    tabel = PrettyTable()
    tabel.field_names = ["Barang", "Stok", "Harga (Rp)"]
    for barang, data in inventori.items():
        tabel.add_row([barang, data['stok'], data['harga']])
    print("\nInventori Barang:")
    print(tabel)
    print("-" * 50)

# Fungsi untuk menambah stok barang
def tambah_stok(inventori):
    print("\n=== Tambah Stok Barang ===")
    barang = input("Nama barang: ").strip()
    if not barang:
        print("Nama barang tidak boleh kosong!")
        return
    try:
        jumlah = int(input(f"Jumlah yang akan ditambahkan ke stok {barang}: "))
        harga = int(input(f"Masukkan harga untuk {barang}: "))
        if barang in inventori:
            inventori[barang]['stok'] += jumlah
        else:
            inventori[barang] = {'stok': jumlah, 'harga': harga}
        print(f"Berhasil menambahkan {jumlah} unit ke stok {barang}.")
    except ValueError:
        print("Masukkan jumlah dan harga dalam angka.")

# Fungsi untuk mengecek stok secara iteratif
def cek_stok_iteratif(inventori, barang):
    for item, data in inventori.items():
        if item == barang:
            return data['stok']
    return 0

# Fungsi untuk mengecek stok secara rekursif
def cek_stok_rekursif(inventori, barang, items=None):
    if items is None:
        items = list(inventori.items())
    if not items:
        return 0
    item, data = items[0]
    if item == barang:
        return data['stok']
    return cek_stok_rekursif(inventori, barang, items[1:])

# Fungsi untuk mengurangi stok secara iteratif
def kurangi_stok_iteratif(inventori, barang, jumlah):
    if barang in inventori and inventori[barang]['stok'] >= jumlah:
        inventori[barang]['stok'] -= jumlah
        return True
    return False

# Fungsi untuk mengurangi stok secara rekursif
def kurangi_stok_rekursif(inventori, barang, jumlah):
    if barang in inventori:
        if inventori[barang]['stok'] >= jumlah:
            inventori[barang]['stok'] -= jumlah
            return True
    return False

# Fungsi untuk mencetak struk transaksi
def cetak_struk(nama, nomor, alamat, barang, jumlah, algoritma, inventori):
    print("\n=== STRUK TRANSAKSI ===")
    print(f"Nama Pelanggan  : {nama}")
    print(f"Nomor Telepon   : {nomor}")
    print(f"Alamat          : {alamat}")
    print(f"Barang Dibeli   : {barang}")
    print(f"Jumlah Dibeli   : {jumlah}")
    print(f"Total Harga     : Rp {jumlah * inventori[barang]['harga']}")
    print(f"Algoritma       : {algoritma.capitalize()}")
    print("-" * 30)

# Fungsi untuk menampilkan grafik waktu eksekusi
def perbarui_grafik():
    plt.figure()
    plt.plot(n_values, iteratif_times, label="Iteratif", marker='o')
    plt.plot(n_values, rekursif_times, label="Rekursif", marker='s')
    plt.title("Perbandingan Waktu Eksekusi")
    plt.xlabel("Jumlah Barang (n)")
    plt.ylabel("Waktu Eksekusi (detik)")
    plt.legend()
    plt.grid()
    plt.show()

# Fungsi untuk mencetak tabel waktu eksekusi
def cetak_tabel_waktu():
    tabel = PrettyTable()
    tabel.field_names = ["Jumlah Barang (n)", "Iteratif (s)", "Rekursif (s)"]
    for i in range(len(n_values)):
        iter_time = f"{iteratif_times[i]:.4f}" if i < len(iteratif_times) else "-"
        rek_time = f"{rekursif_times[i]:.4f}" if i < len(rekursif_times) else "-"
        tabel.add_row([n_values[i], iter_time, rek_time])
    print("\n=== Tabel Waktu Eksekusi ===")
    print(tabel)
    print("-" * 50)

def transaksi(inventori, algoritma):
    start_time = time.time()  # Mulai timer

    tampilkan_inventori(inventori)
    nama = input("Nama pelanggan: ").strip()
    nomor = input("Nomor telepon pelanggan: ").strip()
    alamat = input("Alamat pelanggan: ").strip()
    barang = input("Masukkan nama barang yang dibeli: ").strip()

    if barang not in inventori:
        print("Barang tidak tersedia.")
        return

    try:
        jumlah = int(input(f"Masukkan jumlah {barang} yang dibeli: "))
    except ValueError:
        print("Masukkan jumlah dalam angka.")
        return

    harga_satuan = inventori[barang]['harga']

    if algoritma == 'iteratif':
        stok = cek_stok_iteratif(inventori, barang)
        if stok >= jumlah:
            if kurangi_stok_iteratif(inventori, barang, jumlah):
                total = harga_satuan * jumlah
                print(f"Total harga: Rp {total}")
                cetak_struk(nama, nomor, alamat, barang, jumlah, algoritma, inventori)
            else:
                print(f"Gagal mengurangi stok {barang}.")
        else:
            print(f"Stok tidak mencukupi! Stok tersedia: {stok}")
    elif algoritma == 'rekursif':
        stok = cek_stok_rekursif(inventori, barang)
        if stok >= jumlah:
            if kurangi_stok_rekursif(inventori, barang, jumlah):
                total = harga_satuan * jumlah
                print(f"Total harga: Rp {total}")
                cetak_struk(nama, nomor, alamat, barang, jumlah, algoritma, inventori)
            else:
                print(f"Gagal mengurangi stok {barang}.")
        else:
            print(f"Stok tidak mencukupi! Stok tersedia: {stok}")
    else:
        print("Algoritma tidak dikenal. Pilih 'iteratif' atau 'rekursif'.")

    end_time = time.time()  # Akhiri timer
    execution_time = end_time - start_time

    # Mencatat waktu eksekusi
    n_values.append(jumlah)  # Menambahkan jumlah barang yang dibeli
    if algoritma == 'iteratif':
        iteratif_times.append(execution_time)
        rekursif_times.append(0)  # Tambahkan nilai default untuk rekursif
    else:
        rekursif_times.append(execution_time)
        iteratif_times.append(0)  # Tambahkan nilai default untuk iteratif

    print(f"Waktu eksekusi transaksi menggunakan algoritma {algoritma.capitalize()}: {execution_time:.4f} detik")


# Fungsi utama program
def main():
    print(" Hai, Teman Gaming! Selamat Datang!")
    # Gunakan inventori default
    inventori = {
        "PS5 Controller": {'stok': 10, 'harga': 500000},
        "PS4 Game": {'stok': 15, 'harga': 350000},
        "Headset Gaming": {'stok': 5, 'harga': 250000}
    }

    while True:
        print(" ==================================================")
        print(" |                 Galaxy Playstation             |")
        print(" |          Teman Setia dalam Transaksi Anda!     |")
        print(" ==================================================")
        print(" |                    M E N U                     |")
        print(" ==================================================")
        print(" |                 1. Lihat Inventori             |")
        print(" |                 2. Transaksi Iteratif          |")
        print(" |                 3. Transaksi Rekursif          |")
        print(" |                 4. Tambah Stok Barang          |")
        print(" |                 5. Tampilkan Grafik            |")
        print(" |                 6. Tampilkan Tabel Waktu       |")
        print(" |                 7. Keluar                      |")
        print(" ==================================================")
        opsi = input("Pilih opsi: ").strip()

        if opsi == '1':
            tampilkan_inventori(inventori)
        elif opsi == '2':
            transaksi(inventori, 'iteratif')
        elif opsi == '3':
            transaksi(inventori, 'rekursif')
        elif opsi == '4':
            tambah_stok(inventori)
        elif opsi == '5':
            perbarui_grafik()
        elif opsi == '6':
            cetak_tabel_waktu()
        elif opsi == '7':
            print("Terima kasih telah memilih Galaxy PlayStation. Have fun and play on!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()