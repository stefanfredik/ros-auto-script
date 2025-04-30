import routeros_api
import pandas as pd
import os
from datetime import datetime
from ftplib import FTP


# Fungsi untuk melakukan koneksi ke Mikrotik dan backup
def backup_mikrotik(ip, username, password, name):
    try:
        # Buat koneksi ke RouterOS API
        connection = routeros_api.RouterOsApiPool(ip, username=username, password=password, plaintext_login=True)
        api = connection.get_api()

        # Ambil serial number router
        serial_number = api.get_resource('/system/routerboard').get()[0]['serial-number']
        
        # Nama file backup
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{name}-{serial_number}-{timestamp}.rsc"

        # Buat file backup di Mikrotik
        api.get_resource('/').call('export', {'file': filename})
        print(f"File backup {filename} dibuat di Mikrotik.")

        # Download file backup menggunakan SFTP
        
        connection.disconnect()
        download_backup(ip, username, password, filename)

    except Exception as e:
        print(f"Error backup perangkat {name} ({ip}): {e}")


def download_backup(ip, username, password, remote_filename):
    try:
        # Pastikan direktori backup ada
        local_dir = './backups'
        if not os.path.exists(local_dir):
            os.mkdir(local_dir)

        # Koneksi ke Mikrotik via FTP
        with FTP(ip) as ftp:
            ftp.login(user=username, passwd=password)

            # Path file lokal untuk menyimpan file yang diunduh
            local_path = os.path.join(local_dir, remote_filename)
            
            # Unduh file dari Mikrotik
            with open(local_path, 'wb') as local_file:
                ftp.retrbinary(f'RETR {remote_filename}', local_file.write)
        
        print(f"File {remote_filename} berhasil diunduh ke {local_path}.")
    except Exception as e:
        print(f"Gagal mengunduh file {remote_filename} dari {ip}: {e}")

# Fungsi utama
def main():
    # Baca file Excel
    excel_file = "data.xlsx"  # Ganti dengan path file Excel Anda
    df = pd.read_excel(excel_file)

    # Iterasi tiap baris dalam file Excel
    for _, row in df.iterrows():
        ip = row['IP Address']
        name = row['Nama Perangkat']
        username = "admin"  # Ganti dengan username Anda
        password = "Hephaistos"  # Ganti dengan password Anda
        
        backup_mikrotik(ip, username, password, name)

if __name__ == "__main__":
    main()
