import routeros_api
import pandas as pd
from datetime import datetime

# Fungsi untuk membuat koneksi ke Mikrotik
def connect_to_router(ip, username, password):
    connection = routeros_api.RouterOsApiPool(ip, username=username, password=password, plaintext_login=True)
    return connection.get_api()

# Fungsi untuk membuat file backup di Mikrotik
def create_backup(api, device_name, serial_number):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_name = f"Backup-{device_name}-{serial_number}-{timestamp}"
    
    # Export config file
    api.get_resource('/system/script').call('run', {
        '.name': f"/export file={backup_name}-config"
    })
    
    # Backup binary
    api.get_resource('/system/backup').call('save', {
        'name': backup_name
    })
    return backup_name

# Fungsi untuk upload file backup ke FTP server
def upload_to_ftp(api, backup_name):
    ftp_server = 'smb.jinom.net'
    ftp_user = 'tsjinom'
    ftp_password = 'ts2020'
    
    api.get_resource('/tool/fetch').call('upload', {
        'address': ftp_server,
        'src-path': f"{backup_name}.backup",
        'dst-path': f"{backup_name}.backup",
        'user': ftp_user,
        'password': ftp_password,
        'port': 21
    })
    api.get_resource('/tool/fetch').call('upload', {
        'address': ftp_server,
        'src-path': f"{backup_name}-config.rsc",
        'dst-path': f"{backup_name}-config.rsc",
        'user': ftp_user,
        'password': ftp_password,
        'port': 21
    })

# Fungsi untuk mengirim file backup ke email
def send_backup_via_email(api, backup_name):
    email_to = "noc.ptpir@gmail.com"
    email_subject = "Weekly Backup"
    email_body = f"Attached is the backup file {backup_name}"
    
    api.get_resource('/tool/email').call('send', {
        'to': email_to,
        'subject': email_subject,
        'body': email_body,
        'file': f"{backup_name}.backup,{backup_name}-config.rsc"
    })

# Fungsi untuk menghapus file backup di Mikrotik
def delete_backup(api, backup_name):
    api.get_resource('/file').call('remove', {
        '.id': f"{backup_name}.backup"
    })
    api.get_resource('/file').call('remove', {
        '.id': f"{backup_name}-config.rsc"
    })

# Fungsi utama untuk memproses semua perangkat
def process_devices(file_path, username, password):
    devices = pd.read_excel(file_path)  # Baca file Excel
    for _, row in devices.iterrows():
        ip_address = row['ip_address']
        device_name = row['device_name']
        
        try:
            api = connect_to_router(ip_address, username, password)
            
            # Dapatkan serial number
            serial_number = api.get_resource('/system/routerboard').get()[0]['serial-number']
            
            # Buat file backup
            backup_name = create_backup(api, device_name, serial_number)
            
            # Upload file ke FTP server
            upload_to_ftp(api, backup_name)
            
            # Kirim file ke email
            send_backup_via_email(api, backup_name)
            
            # Hapus file backup dari Mikrotik
            delete_backup(api, backup_name)
            
            print(f"Backup and upload completed for device {device_name} ({ip_address})")
        except Exception as e:
            print(f"Failed to process device {device_name} ({ip_address}): {e}")

# Path file Excel yang berisi daftar perangkat Mikrotik
file_path = "mikrotik_devices.xlsx"

# Akun Mikrotik
username = "admin"
password = "Hephaistos"

# Jalankan proses backup untuk semua perangkat
process_devices(file_path, username, password)
