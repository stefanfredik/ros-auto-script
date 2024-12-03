import routeros_api
import pandas as pd

# Fungsi untuk mengecek status hotspot
def check_hotspot_status(router_ip, username, password, server_name):
    try:
        # Koneksi ke router Mikrotik
        connection = routeros_api.RouterOsApiPool(
            router_ip, username=username, password=password, port=8728, plaintext_login=True
        )
        api = connection.get_api()
        # Mengambil data server hotspot
        hotspot_servers = api.get_resource('/ip/hotspot').get()
        for server in hotspot_servers:
            if server.get('name') == server_name:
                connection.disconnect()
                return True  # Hotspot aktif
        connection.disconnect()
        return False  # Hotspot tidak ditemukan atau tidak aktif
    except Exception as e:
        print(f"Error connecting to {router_ip}: {e}")
        return None  # Gagal koneksi

# Membaca data dari file Excel
file_path = 'datasuspend.xlsx'  # Ganti dengan path file Excel Anda
data = pd.read_excel(file_path)

# Menambahkan kolom untuk status hotspot
data['Hotspot Status'] = None

# Parameter login Mikrotik
mikrotik_username = 'admin'  # Ganti dengan username Mikrotik Anda
mikrotik_password = 'RexusBattlefire'  # Ganti dengan password Mikrotik Anda
hotspot_name = 'hotspot-pembayaran'

# Mengecek status untuk setiap pelanggan
for index, row in data.iterrows():
    ip_address = row['IP Address']  # Ganti dengan nama kolom yang sesuai di Excel Anda
    customer_name = row['Nama Pelanggan']  # Ganti dengan nama kolom yang sesuai di Excel Anda
    print(f"Checking hotspot status for {customer_name} (IP: {ip_address})")
    status = check_hotspot_status(ip_address, mikrotik_username, mikrotik_password, hotspot_name)
    if status is None:
        result = 'Connection Failed'
    elif status:
        result = 'Suspend Ok'
    else:
        result = 'Suspend Gagal'
    
    # Simpan hasil ke data frame dan tampilkan di console
    data.at[index, 'Hotspot Status'] = result
    print(f"Result for {customer_name} (IP {ip_address}): {result}")

# Menyimpan hasil ke file baru
output_file = 'hasil_verifikasi_hotspot.xlsx'
data.to_excel(output_file, index=False)
print(f"Hasil verifikasi disimpan di {output_file}")
