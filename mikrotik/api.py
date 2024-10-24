import ipaddress
from routeros_api import RouterOsApiPool


def getAnyInfo(ip_address, username, password):
    # Inisialisasi dictionary hasil
    mikrotik_data = {
        'IP Address': ip_address,
        'Identity Name': None,
        'Wireless Mode': None,
        'Frequency': None,
        'SSID': None,
        'Routerboard Model': None,
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

    return mikrotik_data

def getIdentity(ip_address, username, password):
    # Inisialisasi dictionary hasil
    mikrotik_data = {
        'IP Address': ip_address,
        'Identity Name': None,
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

        # Tutup koneksi
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect or retrieve data from {ip_address}: {e}")

    return mikrotik_data


def changeIdentity(ip_address, username, password, new_identity_name):
    old_identity_name = None
    new_identity_name_result = None

    try:
        # Koneksi ke MikroTik menggunakan API
        connection = RouterOsApiPool(ip_address, username=username, password=password, plaintext_login=True)
        api = connection.get_api()

        # Mendapatkan nama identity yang lama
        try:
            system_identity = api.get_resource('/system/identity').get()[0]
            old_identity_name = system_identity.get('name', 'Unknown')
        except (IndexError, KeyError):
            print(f"Error getting current identity name from {ip_address}")
            old_identity_name = 'Unknown'

        # Mengubah identity name
        try:
            api.get_resource('/system/identity').set(name=new_identity_name)
            new_identity_name_result = new_identity_name
            print(f"Identity name for {ip_address} changed from '{old_identity_name}' to '{new_identity_name_result}'")
        except Exception as e:
            print(f"Failed to change identity name for {ip_address}: {e}")
            new_identity_name_result = old_identity_name  # Jika gagal, nama baru tetap sama seperti yang lama

        # Tutup koneksi
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect to {ip_address}: {e}")

    # Mengembalikan nama identity lama dan baru
    return old_identity_name, new_identity_name_result

def changeIpAddress(ip_address, username, password, new_ip_address,prefix="/27"):
    oldIpAddress = ip_address
    newIpAddress = new_ip_address

    try:
        connection = RouterOsApiPool(ip_address, username=username, password=password, plaintext_login=True)
        api = connection.get_api()

        # Mendapatkan interface utama yang digunakan untuk mengubah IP address
        try:
            data = api.get_resource('/ip/address')
            result = data.get(address=f"{ip_address}{prefix}")
            
            # print(f"Result : {result}")
            idResult = result[0]["id"]
            interface = result[0]["interface"]

            # Mengubah IP Address
            api.get_resource('/ip/address').set(id=idResult,address=new_ip_address, interface=interface)


            print(f"IP Address for {ip_address} changed from '{ip_address}' to '{new_ip_address}'")

        except (IndexError, KeyError):
            print(f"Error changing IP address on {ip_address}")

        # Tutup koneksi
        connection.disconnect()

    except Exception as e:
        print(f"Failed to connect {ip_address}: {e}")

    # Mengembalikan IP address lama dan baru
    return oldIpAddress, newIpAddress