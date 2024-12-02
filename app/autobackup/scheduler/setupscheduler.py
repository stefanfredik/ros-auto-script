import pandas as pd
from routeros_api import RouterOsApiPool
from datetime import datetime

# Fungsi untuk menambahkan scheduler ke perangkat Mikrotik
def add_scheduler(ip, username, password, device_name):
    try:
        # Koneksi ke RouterOS
        api_pool = RouterOsApiPool(ip, username=username, password=password, plaintext_login=True)
        api = api_pool.get_api()
        
        # Format nama file backup
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        serial_number = api.get_resource('/system/routerboard').get()[0]['serial-number']
        backup_filename = f"Backup-{device_name}-{serial_number}-{timestamp}"

    
        #memeriksa apakah script sudah ada
        script_resource = api.get_resource('/system/script') 
        existing_scripts = script_resource.get() 
        for script in existing_scripts: 
            if script['name'] == 'auto-backup': 
                script_resource.remove(id=script['id']) 

        scheduler_resource = api.get_resource('/system/scheduler') 
        existing_schedulers = scheduler_resource.get() 
        for scheduler in existing_schedulers: 
            if scheduler['name'] == 'weekly-backup': 
                scheduler_resource.remove(id=scheduler['id'])
        
        # Script untuk backup, upload, email, dan hapus file
        script_content = f"""
        :local backupFile "{backup_filename}.backup"
        :local exportFile "{backup_filename}.rsc"
        :local backupPath "/backup-config/{backup_filename}.backup"
        :local exportPath "/backup-config/{backup_filename}.rsc"

        /system backup save name=$backupFile
        /export file=$exportFile
        /tool fetch address=10.70.103.35 src-path=$exportFile user=fred password=Homenet@123 mode=ftp dst-path=$exportPath upload=yes
        /tool fetch address=10.70.103.35 src-path=$exportFile user=fred password=Homenet@123 mode=ftp dst-path=$backupPath upload=yes

        /file remove $backupFile
        /file remove $exportFile
        """
        
        # Tambahkan script ke router
        script_resource = api.get_resource('/system/script')
        script_resource.add(name="auto-backup", source=script_content)
        
        # Tambahkan scheduler ke router
        scheduler_resource = api.get_resource('/system/scheduler')
        scheduler_resource.add(
            name="weekly-backup",
            on_event="auto-backup",
            interval="1w",
            start_time="00:00:00"
        )
        
        print(f"Scheduler successfully added for device {device_name} ({ip})")
        api_pool.disconnect()
    except Exception as e:
        print(f"Failed to add scheduler for device {device_name} ({ip}): {e}")

# Baca file Excel
file_path = "data.xlsx"  # Ganti dengan path file Excel Anda
devices = pd.read_excel(file_path)

# Iterasi setiap perangkat dan tambahkan scheduler
for index, row in devices.iterrows():
    ip_address = row['IP Address']
    device_name = row['Nama Perangkat']
    username = "admin"  # Ganti dengan username perangkat
    password = "Hephaistos"  # Ganti dengan password perangkat
    
    add_scheduler(ip_address, username, password, device_name)
