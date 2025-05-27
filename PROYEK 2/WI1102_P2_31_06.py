# Projek 2 Kelas WI1102

# Program GateX
# Perangkat lunak sistem portal parkir otomatis oleh
# Muhammad Azikra Wira Pratama  [19624219]
# Zahran Alvan Putra Winarko    [19624236]
# Aurelia Jennifer Gunawan      [19624251]
# Nabilla Eka Putri Sunarto     [19624265]
# Fayyaz Akmal Lauda            [19624286]

#KAMUS
#capacity_car               :int    ;kapasitas tempat parkir untuk mobil
#capacity_motor             :int    ;kapasitas tempat parkir untuk motor
#parked_car                 :dict   ;dictionary yang menyimpan informasi kendaraan mobil yang sedang terparkir
#parked_motor               :dict   ;dictionary yang menyimpan informasi kendaraan motor yang sedang terparkir
#parking_history            :list   ;list yang menyimpan riwayat parkir kendaraan
#available_slots_car        :list   ;list nomor slot parkir yang tersedia untuk mobil
#available_slots_motor      :list   ;list nomor slot parkir yang tersedia untuk motor
#emoney_balance             :dict   ;dictionary yang menyimpan saldo e-money kendaraan berdasarkan plat nomor
#pilihan                    :str    ;pilihan menu pengguna
#plat_nomor                 :str    ;plat nomor kendaraan
#jenis_kendaraan            :str    ;jenis kendaraan (mobil atau motor)

from datetime import datetime
import re

# Konfigurasi sistem parkir
capacity_car = int(input("Masukkan kapasitas tempat parkir untuk mobil: "))
capacity_motor = int(input("Masukkan kapasitas tempat parkir untuk motor: "))

# Variabel penyimpanan data parkir
parked_car = {}
parked_motor = {}
parking_history = []
available_slots_car = list(range(1, capacity_car + 1))
available_slots_motor = list(range(1, capacity_motor + 1))
emoney_balance = {}

# Fungsi validasi plat nomor
def validasi_plat_nomor(plat):
    if len(plat) < 4:
        return False

    huruf_awal = plat[:2] if plat[1].isalpha() else plat[:1]
    if not huruf_awal.isalpha() or len(huruf_awal) > 2:
        return False

    angka_awal = plat[len(huruf_awal):len(huruf_awal)+4]
    angka = ''.join([char for char in angka_awal if char.isdigit()])
    if len(angka) < 1 or len(angka) > 4:
        return False

    huruf_akhir = plat[len(huruf_awal) + len(angka):]
    if not huruf_akhir.isalpha() or len(huruf_akhir) < 2 or len(huruf_akhir) > 3:
        return False

    return True

# Fungsi menghitung biaya parkir
def hitung_biaya(jenis_kendaraan, durasi_jam):
    if jenis_kendaraan == 'mobil':
        if durasi_jam <= 1:
            return 3000
        elif durasi_jam <= 8:
            return 3000 + (durasi_jam - 1) * 1000
        else:
            return 10000
    elif jenis_kendaraan == 'motor':
        if durasi_jam <= 1:
            return 1000
        elif durasi_jam <= 9:
            return 1000 + (durasi_jam - 1) * 500
        else:
            return 5000

# Fungsi menambahkan kendaraan ke tempat parkir
def parkir_kendaraan(plat_nomor, jenis_kendaraan):
    kendaraan_terparkir = parked_car if jenis_kendaraan == 'mobil' else parked_motor
    slot_tersedia = available_slots_car if jenis_kendaraan == 'mobil' else available_slots_motor

    if plat_nomor not in emoney_balance:
        saldo_awal = int(input(f"Masukkan saldo e-money untuk kendaraan {plat_nomor}: "))
        emoney_balance[plat_nomor] = saldo_awal

    if len(slot_tersedia) > 0:
        slot = slot_tersedia.pop(0)
        waktu_masuk = datetime.now()
        kendaraan_terparkir[plat_nomor] = {'slot': slot, 'waktu_masuk': waktu_masuk}
        print(f"{jenis_kendaraan.capitalize()} dengan plat {plat_nomor} diparkir di slot {slot} pada {waktu_masuk}.")
        print(f"Saldo e-money kendaraan: Rp{emoney_balance[plat_nomor]:.2f}")
    else:
        print(f"Maaf, tempat parkir untuk {jenis_kendaraan} penuh.")
    return

def keluarkan_kendaraan(plat_nomor, jenis_kendaraan):
    kendaraan_terparkir = parked_car if jenis_kendaraan == 'mobil' else parked_motor
    slot_tersedia = available_slots_car if jenis_kendaraan == 'mobil' else available_slots_motor

    if plat_nomor in kendaraan_terparkir:
        info_kendaraan = kendaraan_terparkir[plat_nomor]  
        slot = info_kendaraan['slot']
        waktu_masuk = info_kendaraan['waktu_masuk']
        waktu_keluar = datetime.now()

        durasi_detik = (waktu_keluar - waktu_masuk).total_seconds()
        durasi_jam = durasi_detik / 4  # 4 detik = 1 jam di sistem
        biaya = hitung_biaya(jenis_kendaraan, durasi_jam)

        if emoney_balance[plat_nomor] >= biaya:
            emoney_balance[plat_nomor] -= biaya
            kendaraan_terparkir.pop(plat_nomor)  # Data dihapus setelah pembayaran sukses
            parking_history.append({
                'plat_nomor': plat_nomor,
                'jenis_kendaraan': jenis_kendaraan,
                'slot': slot,
                'waktu_masuk': waktu_masuk,
                'waktu_keluar': waktu_keluar,
                'biaya': biaya
            })
            slot_tersedia.append(slot)
            slot_tersedia.sort()

            print(f"Kendaraan dengan plat {plat_nomor} keluar dari slot {slot}.")
            print(f"Waktu masuk: {waktu_masuk}, Waktu keluar: {waktu_keluar}")
            print(f"Durasi parkir: {durasi_jam:.2f} jam")
            print(f"Biaya parkir: Rp{biaya:.2f}")
            print(f"Saldo e-money kendaraan: Rp{emoney_balance[plat_nomor]:.2f}")
        else:
            print("Saldo e-money kendaraan tidak mencukupi untuk membayar parkir.")
            print("Kendaraan tidak dapat keluar dari parkiran.")
    else:
        print("Kendaraan dengan plat tersebut tidak ditemukan.")
    return

# Fungsi isi ulang saldo e-money
def isi_ulang_saldo():
    plat_nomor = input("Masukkan nomor plat kendaraan yang ingin diisi ulang saldonya: ").upper()
    if plat_nomor in emoney_balance:
        saldo_tambah = int(input(f"Masukkan jumlah saldo yang akan ditambahkan untuk kendaraan {plat_nomor}: "))
        if saldo_tambah > 0:
            emoney_balance[plat_nomor] += saldo_tambah
            print(f"Saldo e-money kendaraan {plat_nomor} berhasil ditambahkan sebesar Rp{saldo_tambah:.2f}.")
            print(f"Saldo saat ini: Rp{emoney_balance[plat_nomor]:.2f}")
        else:
            print("Jumlah saldo yang ditambahkan harus lebih dari 0.")
    else:
        print("Kendaraan dengan plat tersebut tidak ditemukan dalam sistem.")
    return

# Fungsi menampilkan status tempat parkir
def tampilkan_status_parkir():
    print("\nStatus Tempat Parkir:")
    print("Slot mobil yang tersedia:", available_slots_car)
    print("Slot motor yang tersedia:", available_slots_motor)

    print("\nMobil yang terparkir:")
    if parked_car:
        for plat_nomor, info in parked_car.items():
            print(f"Plat {plat_nomor} di slot {info['slot']}, Waktu masuk: {info['waktu_masuk']}")
    else:
        print("Tidak ada mobil yang terparkir.")

    print("\nMotor yang terparkir:")
    if parked_motor:
        for plat_nomor, info in parked_motor.items():
            print(f"Plat {plat_nomor} di slot {info['slot']}, Waktu masuk: {info['waktu_masuk']}")
    else:
        print("Tidak ada motor yang terparkir.")
    return

# Fungsi menampilkan riwayat parkir
def tampilkan_riwayat_parkir():
    print("\nRiwayat Parkir:")
    total_pendapatan = 0 
    
    if parking_history:
        for riwayat in parking_history:
            print(f"Plat {riwayat['plat_nomor']} ({riwayat['jenis_kendaraan']}) di slot {riwayat['slot']}")
            print(f"Waktu masuk: {riwayat['waktu_masuk']}, Waktu keluar: {riwayat['waktu_keluar']}")
            print(f"Biaya parkir: Rp{riwayat['biaya']:.2f}\n")
            total_pendapatan += riwayat['biaya'] 

        print(f"Total Pendapatan Hari Ini: Rp{total_pendapatan:.2f}")
    else:
        print("Tidak ada riwayat parkir.")
    return

# Fungsi utama
while True:
    print("\n=== Sistem Parkir Otomatis ===")
    print("1. Parkir kendaraan")
    print("2. Keluarkan kendaraan")
    print("3. Isi ulang saldo")
    print("4. Tampilkan status parkir")
    print("5. Lihat riwayat parkir")
    print("6. Keluar Sistem")
    pilihan = input("Pilih opsi (1-6): ")

    if pilihan == '1':
        plat_nomor = input("Masukkan nomor plat kendaraan: ").upper()
        if not validasi_plat_nomor(plat_nomor):
            print("Nomor plat tidak valid. Format harus sesuai (contoh: B1234XYZ).")
            continue
        jenis_kendaraan = input("Masukkan jenis kendaraan (mobil/motor): ").lower()
        parkir_kendaraan(plat_nomor, jenis_kendaraan)
    elif pilihan == '2':
        plat_nomor = input("Masukkan nomor plat kendaraan: ").upper()
        jenis_kendaraan = input("Masukkan jenis kendaraan (mobil/motor): ").lower()
        keluarkan_kendaraan(plat_nomor, jenis_kendaraan)
    elif pilihan == '3':
        isi_ulang_saldo()
    elif pilihan == '4':
        tampilkan_status_parkir()
    elif pilihan == '5':
        tampilkan_riwayat_parkir()
    elif pilihan == '6':
        print("Terima kasih telah menggunakan sistem portal parkir otomatis: 'GateX' （*＾-＾*）.")
        break
    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
