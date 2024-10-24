from mikrotik.api import getAnyInfo, getIdentity
from utils.excel import readExcelColumn, save_to_excel
import config

def main():
    # Membaca daftar IP dari file Excel
    column = ["IP Address"]

    ip_list = readExcelColumn(config.INPUT_FILE,column)

    # return print(ip_list)

    # List untuk menyimpan hasil
    results = []

    # Loop melalui setiap IP address dan mengambil informasi
    for index in ip_list:
        ip = index["IP Address"]

        mikrotik_info = getAnyInfo(ip, config.USERNAME, config.PASSWORD)
        if mikrotik_info:
            results.append(mikrotik_info)

    # Simpan hasil ke file Excel
    save_to_excel(results, config.OUTPUT_FILE)
    print(f"Hasil berhasil disimpan ke {config.OUTPUT_FILE}")

if __name__ == '__main__':
    main()
