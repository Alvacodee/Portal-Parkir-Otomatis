# Program GateX
# Perangkat lunak sistem portal parkir otomatis oleh
# Muhammad Azikra Wira Pratama  [19624219]
# Zahran Alvan Putra Winarko    [19624236]
# Aurelia Jennifer Gunawan      [19624251]
# Nabilla Eka Putri Sunarto     [19624265]
# Fayyaz Akmal Lauda            [19624286]

# KAMUS
#kapasitas_mobil      :int         ; kapasitas total tempat parkir untuk mobil
#kapasitas_motor      :int         ; kapasitas total tempat parkir untuk motor
#mobil_terparkir      :dict        ; dictionary yang menyimpan data mobil yang sedang terparkir,
#                                   termasuk informasi nomor plat, slot parkir, dan waktu masuk
#motor_terparkir      :dict        ; dictionary yang menyimpan data motor yang sedang terparkir,
#                                   termasuk informasi nomor plat, slot parkir, dan waktu masuk
#slot_tersedia_mobil  :list(int)   ; daftar yang berisi nomor slot parkir yang masih tersedia untuk mobil
#slot_tersedia_motor  :list(int)   ; daftar yang berisi nomor slot parkir yang masih tersedia untuk motor
#plat_nomor           :str         ; nomor plat kendaraan yang akan diparkirkan atau dikeluarkan
#jenis_kendaraan      :str         ; jenis kendaraan (mobil/motor)
#pilihan              :str         ; input dari pengguna yang menentukan aksi dalam sistem (1/2/3/4)
#slot                 :int         ; nomor slot parkir yang diberikan kepada kendaraan
#waktu_masuk          :datetime    ; waktu saat kendaraan masuk ke slot parkir
#waktu_keluar         :datetime    ; waktu saat kendaraan keluar dari slot parkir
#durasi_detik         :float       ; durasi parkir dalam satuan detik
#durasi_jam           :float       ; durasi parkir dalam satuan jam
#info_mobil           :dict        ; dictionary yang menyimpan informasi mobil yang akan dikeluarkan
#info_motor           :dict        ; dictionary yang menyimpan informasi motor yang akan dikeluarkan
#biaya                :float       ; biaya parkir kendaraan berdasarkan durasi parkir dan tarif parkir
#                                   yang telah ditentukan

#ALGORITMA
from datetime import datetime, timedelta
import time

# Konfigurasi sistem parkir
kapasitas_mobil = int(input("Masukkan kapasitas tempat parkir untuk mobil: "))
kapasitas_motor = int(input("Masukkan kapasitas tempat parkir untuk motor: "))

# Variabel penyimpanan data parkir
mobil_terparkir = {}
motor_terparkir = {}
slot_tersedia_mobil = list(range(1, kapasitas_mobil + 1))
slot_tersedia_motor = list(range(1, kapasitas_motor + 1))

# Fungsi utama
while True:
    print("\n=== Sistem Parkir Otomatis ===")
    print("1. Parkir kendaraan")
    print("2. Keluarkan kendaraan")
    print("3. Tampilkan status parkir")
    print("4. Keluar Sistem")
    pilihan = input("Pilih opsi (1-4): ")

    if pilihan == '1':  # Parkir kendaraan
        plat_nomor = input("Masukkan nomor plat kendaraan: ")
        jenis_kendaraan = input("Masukkan jenis kendaraan (mobil/motor): ").lower()

        if jenis_kendaraan == 'mobil':
            if len(slot_tersedia_mobil) > 0:
                slot = slot_tersedia_mobil.pop(0)
                waktu_masuk = datetime.now()
                mobil_terparkir[plat_nomor] = {'slot': slot, 'waktu_masuk': waktu_masuk}
                print(f"Mobil dengan plat {plat_nomor} diparkir di slot {slot} pada {waktu_masuk}.")
            else:
                print("Maaf, tempat parkir untuk mobil penuh.")

        elif jenis_kendaraan == 'motor':
            if len(slot_tersedia_motor) > 0:
                slot = slot_tersedia_motor.pop(0)
                waktu_masuk = datetime.now()
                motor_terparkir[plat_nomor] = {'slot': slot, 'waktu_masuk': waktu_masuk}
                print(f"Motor dengan plat {plat_nomor} diparkir di slot {slot} pada {waktu_masuk}.")
            else:
                print("Maaf, tempat parkir untuk motor penuh.")
        else:
            print("Jenis kendaraan tidak dikenal. Silakan pilih 'mobil' atau 'motor'.")

    elif pilihan == '2':  # Keluarkan kendaraan
        plat_nomor = input("Masukkan nomor plat kendaraan: ")
        jenis_kendaraan = input("Masukkan jenis kendaraan (mobil/motor): ").lower()

        if jenis_kendaraan == 'mobil' and plat_nomor in mobil_terparkir:
            info_mobil = mobil_terparkir.pop(plat_nomor)
            slot = info_mobil['slot']
            waktu_masuk = info_mobil['waktu_masuk']
            waktu_keluar = datetime.now()

            # Hitung durasi parkir
            durasi_detik = (waktu_keluar - waktu_masuk).total_seconds()
            durasi_jam = durasi_detik / 4  # 4 detik = 1 jam di sistem
            if durasi_jam>=0 and durasi_jam<=1:
                biaya = 3000
            elif durasi_jam>1 and durasi_jam<=8:
                biaya = 3000+(durasi_jam-1)*1000
            else:
                biaya = 10000

            # Kembalikan slot parkir
            slot_tersedia_mobil.append(slot)
            slot_tersedia_mobil.sort()

            print(f"Mobil dengan plat {plat_nomor} keluar dari slot {slot}.")
            print(f"Waktu masuk: {waktu_masuk}, Waktu keluar: {waktu_keluar}")
            print(f"Durasi parkir: {durasi_jam:.2f} jam")
            print(f"Biaya parkir: Rp{biaya:.2f}")

        elif jenis_kendaraan == 'motor' and plat_nomor in motor_terparkir:
            info_motor = motor_terparkir.pop(plat_nomor)
            slot = info_motor['slot']
            waktu_masuk = info_motor['waktu_masuk']
            waktu_keluar = datetime.now()

            # Hitung durasi parkir
            durasi_detik = (waktu_keluar - waktu_masuk).total_seconds()
            durasi_jam = durasi_detik / 4  # 4 detik = 1 jam di sistem
            if durasi_jam>=0 and durasi_jam<=1:
                biaya = 1000
            elif durasi_jam>1 and durasi_jam<=9:
                biaya = 1000+(durasi_jam-1)*500
            else:
                biaya = 5000

            # Kembalikan slot parkir
            slot_tersedia_motor.append(slot)
            slot_tersedia_motor.sort()

            print(f"Motor dengan plat {plat_nomor} keluar dari slot {slot}.")
            print(f"Waktu masuk: {waktu_masuk}, Waktu keluar: {waktu_keluar}")
            print(f"Durasi parkir: {durasi_jam:.2f} jam")
            print(f"Biaya parkir: Rp{biaya:.2f}")

        else:
            print("Kendaraan dengan plat tersebut tidak ditemukan atau jenis kendaraan salah.")

    elif pilihan == '3':  # Tampilkan status parkir
        print("\nStatus Tempat Parkir:")
        print("Slot mobil yang tersedia:", slot_tersedia_mobil)
        print("Slot motor yang tersedia:", slot_tersedia_motor)

        print("\nMobil yang terparkir:")
        if mobil_terparkir:
            for plat_nomor, info in mobil_terparkir.items():
                print(f"Plat {plat_nomor} di slot {info['slot']}, Waktu masuk: {info['waktu_masuk']}")
        else:
            print("Tidak ada mobil yang terparkir.")

        print("\nMotor yang terparkir:")
        if motor_terparkir:
            for plat_nomor, info in motor_terparkir.items():
                print(f"Plat {plat_nomor} di slot {info['slot']}, Waktu masuk: {info['waktu_masuk']}")
        else:
            print("Tidak ada motor yang terparkir.")
        print("\n")

    elif pilihan == '4':  # Keluar
        print("Terima kasih telah menggunakan GateX.")
        break

    else:
        print("Pilihan tidak valid. Silakan coba lagi.")