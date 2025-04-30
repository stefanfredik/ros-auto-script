import pandas as pd

# Fungsi utama untuk menggabungkan data
def match_suspend_ips(suspend_file, all_customers_file, output_file):
    # Baca file data pelanggan suspend
    suspend_data = pd.read_excel(suspend_file)
    
    # Baca file data seluruh pelanggan
    all_customers_data = pd.read_excel(all_customers_file)
    
    # Gabungkan berdasarkan nama pelanggan (assume kolom 'Nama Pelanggan')
    merged_data = suspend_data.merge(
        all_customers_data[['Nama Pelanggan', 'IP Address']],
        on='Nama Pelanggan',
        how='left'
    )
    
    # Simpan hasil ke file Excel baru
    merged_data.to_excel(output_file, index=False)
    print(f"File berhasil dibuat: {output_file}")

# File input dan output
suspend_file = 'datasuspend.xlsx'  # Ganti dengan path file data suspend
all_customers_file = 'datapelanggan.xlsx'  # Ganti dengan path file data seluruh pelanggan
output_file = 'datasuspendwithip.xlsx'  # Path untuk menyimpan output

# Jalankan fungsi
match_suspend_ips(suspend_file, all_customers_file, output_file)
