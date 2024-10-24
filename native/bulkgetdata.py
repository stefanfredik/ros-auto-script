from pydoc import plain
import pandas as pd
import sys
from routeros_api import RouterOsApiPool

# Fungsi untuk mengambil informasi dari perangkat MikroTik
def get_mikrotik_info(ip_address, username, password):
    # Inisialisasi dictionary hasil
    mikrotik_data = {
        'IP Address': ip_address,  # IP Address tetap ditampilkan walaupun ada error
        'Identity Name': None,
        'Wireless Mode': None,
        'Frequency': None,
        'SSID': None,
        'Routerboard Model': None
    }

    try:
        # Koneksi ke MikroTik menggunakan API
        connection = RouterOsApiPool(ip_address, username=username, password=password, plaintext_login=True)
        api = connection.get_api()

        # Mendapatkan informasi sistem identity
        try:
            system_identity = api.get_resource('/system/identity').get()[0]
            mikrotik_data['Identity Name'] = system_identity.get('name', 'Unknown')
        except (IndexError, KeyError):
            print(f"Error getting identity name from {ip_address}")

        # Mendapatkan informasi wireless
        try:
            wireless_info = api.get_resource('/interface/wireless').get()[0]
            mikrotik_data['Wireless Mode'] = wireless_info.get('mode', 'Unknown')
            mikrotik_data['Frequency'] = wireless_info.get('frequency', 'Unknown')
            mikrotik_data['SSID'] = wireless_info.get('ssid', 'Unknown')
        except (IndexError, KeyError):
            print(f"Error getting wireless info from {ip_address}")

        # Mendapatkan informasi routerboard
        try:
            routerboard_info = api.get_resource('/system/routerboard').get()[0]
            mikrotik_data['Routerboard Model'] = routerboard_info.get('model', 'Unknown')
        except (IndexError, KeyError):
            print(f"Error getting routerboard info from {ip_address}")

        # Tutup koneksi
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect or retrieve data from {ip_address}: {e}")

    return mikrotik_data  # Mengembalikan informasi IP Address bahkan jika terjadi error

# Membaca file Excel yang berisi daftar IP address
def readToExcel(file_path):
    # Membaca kolom IP dari file Excel
    try:
        data = pd.read_excel(file_path)
    except Exception as e:
        print(f"Gagal membaca file, pastikan data input excel sudah dibuat dan nama file sudah benar. {file_path} : \n {e}")
        sys.exit(1)
        
    return data['IP Address'].tolist()

# Fungsi untuk menyimpan hasil ke file Excel
def saveToExcel(data, output_file):
    # Membuat DataFrame dari hasil data
    df = pd.DataFrame(data)

    # Menambahkan kolom nomor urut
    df.insert(0, 'No', range(1, len(df) + 1))

    # Menyimpan ke file Excel
    df.to_excel(output_file, index=False)

# Fungsi utama untuk menjalankan script
def main(input_file, output_file, username, password):
    # Membaca daftar IP dari file Excel
    ip_list = readToExcel(input_file)

    # List untuk menyimpan hasil
    results = []

    # Loop melalui setiap IP address dan mengambil informasi
    for ip in ip_list:
        mikrotik_info = get_mikrotik_info(ip, username, password)
        if mikrotik_info:
            results.append(mikrotik_info)

    # Simpan hasil ke file Excel
    saveToExcel(results, output_file)
    print(f"Hasil berhasil disimpan ke {output_file}")

# Nama file input dan output
input_file = 'datainput.xlsx'  # Nama file Excel yang berisi IP address
output_file = 'dataoutput.xlsx'  # Nama file output hasil

# Username dan password untuk login ke MikroTik
username = 'admin'
password = 'Hephaistos'

# Jalankan script
if __name__ == '__main__':
    main(input_file, output_file, username, password)
