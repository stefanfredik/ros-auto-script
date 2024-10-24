from mikrotik.api import getAnyInfo, setData
from utils.excel import read_excel, save_to_excel
import config

def main():
    # Membaca daftar IP dan New Identity dari file Excel
    ip_identity_list = read_excel(config.INPUT_FILE)

    # List untuk menyimpan hasil
    results = []

    # Loop melalui setiap perangkat dan mengambil informasi
    for entry in ip_identity_list:
        ip = entry['IP Address']
        new_identity_name = entry['New']

        # Mengambil informasi awal dari perangkat MikroTik
        mikrotik_info = getAnyInfo(ip, config.USERNAME, config.PASSWORD)

        # Jika informasi berhasil diambil, lanjutkan untuk mengubah identity name
        if mikrotik_info:
            # Simpan nama identity yang lama
            old_identity_name = mikrotik_info['Identity Name']

            # Ubah identity name sesuai dengan kolom New Identity dari file Excel
            old_name, new_name = setData(ip, config.USERNAME, config.PASSWORD, new_identity_name)

            # Tambahkan informasi nama lama dan baru ke dalam hasil
            mikrotik_info['Old Identity Name'] = old_name
            mikrotik_info['New Identity Name'] = new_name

            results.append(mikrotik_info)

    # Simpan hasil ke file Excel
    save_to_excel(results, config.OUTPUT_FILE)
    print(f"Hasil berhasil disimpan ke {config.OUTPUT_FILE}")

if __name__ == '__main__':
    main()
